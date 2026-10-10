"""Analytics, forecast and AI-provider integration; keep business logic outside views."""
import os
import requests
import pandas as pd
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta
from .models import Product, Sale


def dashboard_metrics():
    today = timezone.localdate()
    month_start = today.replace(day=1)
    revenue_expr = ExpressionWrapper(F("quantity") * F("unit_price"), output_field=DecimalField(max_digits=14, decimal_places=2))
    month_sales = Sale.objects.filter(date__gte=month_start, date__lte=today)
    revenue = month_sales.aggregate(total=Sum(revenue_expr))["total"] or 0
    units = month_sales.aggregate(total=Sum("quantity"))["total"] or 0
    low_stock = Product.objects.filter(stock_on_hand__lte=F("reorder_level")).count()
    product_count = Product.objects.count()
    recent = list(Sale.objects.select_related("product").order_by("-date")[:8])
    daily = list(Sale.objects.filter(date__gte=today-timedelta(days=29), date__lte=today).values("date").annotate(units=Sum("quantity")).order_by("date"))
    chart = {"labels": [str(x["date"]) for x in daily], "units": [x["units"] for x in daily]}
    category_rows = list(Sale.objects.filter(date__gte=month_start, date__lte=today).values("product__category").annotate(units=Sum("quantity")).order_by("-units")[:6])
    return {"revenue": revenue, "units": units, "low_stock": low_stock, "product_count": product_count, "recent_sales": recent, "chart": chart, "category_rows": category_rows}


def forecast_product(product, horizon=7):
    """Small-data baseline forecast. Uses lag features only when enough history exists.

    Forecast is a planning estimate, not a guarantee. Chronological split is used for
    evaluation to avoid random train/test leakage.
    """
    rows = list(Sale.objects.filter(product=product).values("date", "quantity").order_by("date"))
    if not rows:
        return {"product": product.name, "sku": product.sku, "method": "No history", "daily_forecast": [0] * horizon,
                "total_forecast": 0, "mae": None, "recommendation": max(0, product.reorder_level-product.stock_on_hand),
                "note": "No sales history is available. Add sales data before relying on a forecast."}
    frame = pd.DataFrame(rows)
    frame["date"] = pd.to_datetime(frame["date"])
    daily = frame.groupby("date")["quantity"].sum().asfreq("D", fill_value=0).astype(float)
    if len(daily) >= 35 and daily.sum() > 0:
        supervised = pd.DataFrame({"y": daily})
        for lag in (1, 7, 14, 28):
            supervised[f"lag_{lag}"] = supervised["y"].shift(lag)
        supervised["dow"] = supervised.index.dayofweek
        supervised = supervised.dropna()
        split = max(1, int(len(supervised) * 0.8))
        train, test = supervised.iloc[:split], supervised.iloc[split:]
        if len(train) >= 10 and len(test) > 0:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_absolute_error
            feature_cols = [c for c in supervised.columns if c != "y"]
            eval_model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=2)
            eval_model.fit(train[feature_cols], train["y"])
            mae = round(float(mean_absolute_error(test["y"], eval_model.predict(test[feature_cols]))), 3)
            model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=2)
            model.fit(supervised[feature_cols], supervised["y"])
            history = list(daily.astype(float))
            predictions = []
            for _ in range(horizon):
                idx = daily.index[-1] + pd.Timedelta(days=len(predictions)+1)
                row = {f"lag_{lag}": history[-lag] if len(history) >= lag else float(daily.mean()) for lag in (1,7,14,28)}
                row["dow"] = idx.dayofweek
                pred = max(0, float(model.predict(pd.DataFrame([row]))[0]))
                predictions.append(round(pred, 2)); history.append(pred)
            method = "Random Forest (lag features)"
        else:
            predictions, mae, method = _baseline(daily, horizon), None, "7-day moving-average baseline"
    else:
        predictions, mae, method = _baseline(daily, horizon), None, "7-day moving-average baseline"
    total = round(sum(predictions))
    target_stock = total + max(0, product.reorder_level)
    recommendation = max(0, int(round(target_stock - product.stock_on_hand)))
    return {"product": product.name, "sku": product.sku, "method": method, "daily_forecast": predictions,
            "total_forecast": total, "mae": mae, "recommendation": recommendation,
            "note": "Forecast is an estimate. Validate against your own historical data and business constraints."}


def _baseline(daily, horizon):
    avg = float(daily.tail(7).mean()) if len(daily) else 0.0
    return [round(max(0, avg), 2) for _ in range(horizon)]


def build_business_context():
    """Return aggregate facts only; never pass raw customer-sensitive records to an LLM."""
    from django.db.models import Sum, F
    products = Product.objects.count()
    low = list(Product.objects.filter(stock_on_hand__lte=F("reorder_level")).values("sku", "name", "stock_on_hand", "reorder_level")[:20])
    recent_units = Sale.objects.filter(date__gte=timezone.localdate()-timedelta(days=30)).aggregate(total=Sum("quantity"))["total"] or 0
    return {"product_count": products, "low_stock_products": low, "units_sold_last_30_days": int(recent_units)}


def answer_business_question(question):
    """Optional Groq-powered narrative; safe deterministic fallback when key unavailable."""
    context = build_business_context()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        low_names = ", ".join(f"{p['name']} ({p['stock_on_hand']}/{p['reorder_level']})" for p in context["low_stock_products"][:5]) or "none currently flagged"
        return {"answer": f"I can answer basic inventory questions from the current database. Products tracked: {context['product_count']}. Units sold in the last 30 days: {context['units_sold_last_30_days']}. Low-stock items: {low_names}. For a generative AI explanation, configure GROQ_API_KEY in your environment.", "mode": "rule-based fallback"}
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    prompt = ("You are IntelliStock, an inventory analytics assistant. Use only the supplied JSON facts. "
              "Clearly state when the data does not answer a question. Do not invent numbers or claim to execute actions. "
              "Keep recommendations cautious and concise. Facts: " + str(context))
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", timeout=20,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "temperature": 0.2, "messages": [{"role":"system","content":prompt},{"role":"user","content":question[:1000]}]})
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"].strip()
        return {"answer": answer, "mode": "Groq API"}
    except (requests.RequestException, KeyError, ValueError):
        return {"answer": "The AI service is temporarily unavailable. Please try again later. Your inventory data has not been changed.", "mode": "fallback"}

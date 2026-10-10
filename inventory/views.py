import csv
import io
import json
from decimal import Decimal, InvalidOperation
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from .models import Product, Sale
from .services import dashboard_metrics, forecast_product, answer_business_question


def dashboard(request):
    return render(request, "inventory/dashboard.html", dashboard_metrics())


def products(request):
    q = request.GET.get("q", "").strip()[:100]
    qs = Product.objects.all()
    if q:
        from django.db.models import Q
        qs = qs.filter(Q(sku__icontains=q) | Q(name__icontains=q) | Q(category__icontains=q))
    return render(request, "inventory/products.html", {"products": qs, "q": q})

@require_POST
@csrf_protect
def add_product(request):
    try:
        sku = request.POST.get("sku", "").strip().upper()[:40]
        name = request.POST.get("name", "").strip()[:160]
        category = request.POST.get("category", "Uncategorized").strip()[:100] or "Uncategorized"
        stock = int(request.POST.get("stock_on_hand", "0"))
        reorder = int(request.POST.get("reorder_level", "10"))
        lead = int(request.POST.get("lead_time_days", "7"))
        cost = Decimal(request.POST.get("unit_cost", "0"))
        if not sku or not name or min(stock, reorder, lead) < 0 or cost < 0:
            raise ValueError("Please enter valid, non-negative values.")
        Product.objects.create(sku=sku, name=name, category=category, stock_on_hand=stock, reorder_level=reorder, lead_time_days=lead, unit_cost=cost)
        messages.success(request, "Product added successfully.")
    except (ValueError, InvalidOperation, IntegrityError):
        messages.error(request, "Product could not be added. Check fields and ensure SKU is unique.")
    return redirect("products")

@require_POST
@csrf_protect
def upload_sales(request):
    uploaded = request.FILES.get("file")
    if not uploaded or uploaded.size > 5 * 1024 * 1024:
        messages.error(request, "Choose a CSV file smaller than 5 MB.")
        return redirect("dashboard")
    try:
        text = uploaded.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        required = {"date", "sku", "product_name", "quantity", "unit_price"}
        if not reader.fieldnames or not required.issubset({h.strip() for h in reader.fieldnames}):
            raise ValueError("CSV must contain date, sku, product_name, quantity, unit_price columns.")
        count = 0
        with transaction.atomic():
            for line, row in enumerate(reader, start=2):
                row = {str(k).strip(): (v or "").strip() for k, v in row.items() if k}
                sale_date = date.fromisoformat(row["date"])
                sku = row["sku"].upper()[:40]
                name = row["product_name"][:160]
                quantity = int(row["quantity"])
                price = Decimal(row["unit_price"])
                if not sku or not name or quantity <= 0 or price < 0:
                    raise ValueError(f"Invalid values on CSV row {line}.")
                product, _ = Product.objects.get_or_create(sku=sku, defaults={"name": name})
                Sale.objects.create(product=product, date=sale_date, quantity=quantity, unit_price=price)
                count += 1
        messages.success(request, f"Imported {count} sales rows. Existing stock values were not changed automatically.")
    except (UnicodeDecodeError, csv.Error, KeyError, ValueError, InvalidOperation, IntegrityError) as exc:
        messages.error(request, f"CSV import failed; no rows were saved. Check the file format and values. ({str(exc)[:160]})")
    return redirect("dashboard")


def forecast_page(request):
    products = Product.objects.all()
    selected = products.first()
    result = forecast_product(selected) if selected else None
    return render(request, "inventory/forecast.html", {"products": products, "selected": selected, "result_json": json.dumps(result) if result else "null"})

@require_GET
def forecast_api(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        horizon = int(request.GET.get("days", "7"))
        if horizon < 1 or horizon > 30:
            raise ValueError
    except ValueError:
        return JsonResponse({"error": "days must be between 1 and 30"}, status=400)
    return JsonResponse(forecast_product(product, horizon))


def assistant_page(request):
    return render(request, "inventory/assistant.html")

@require_POST
@csrf_protect
def assistant_api(request):
    if not request.content_type or "application/json" not in request.content_type:
        return HttpResponseBadRequest("Expected application/json")
    try:
        payload = json.loads(request.body or b"{}")
        question = str(payload.get("question", "")).strip()
        if not question or len(question) > 1000:
            return JsonResponse({"error": "Enter a question of up to 1000 characters."}, status=400)
        return JsonResponse(answer_business_question(question))
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "intellistock"})

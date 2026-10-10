import csv
import io
import json
from datetime import date, timedelta
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Product, Sale
from .services import forecast_product

class IntelliStockTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(sku="TEST-1", name="Test Widget", stock_on_hand=4, reorder_level=8, lead_time_days=3, unit_cost=Decimal("12.50"))

    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inventory overview")

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_add_product_post(self):
        response = self.client.post(reverse("add_product"), {"sku":"TEST-2", "name":"Another", "category":"Tools", "stock_on_hand":"12", "reorder_level":"4", "lead_time_days":"5", "unit_cost":"2.50"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(sku="TEST-2").exists())

    def test_forecast_without_history_is_safe(self):
        result = forecast_product(self.product, 7)
        self.assertEqual(result["total_forecast"], 0)
        self.assertEqual(len(result["daily_forecast"]), 7)
        self.assertEqual(result["recommendation"], 4)

    def test_forecast_api_validates_horizon(self):
        response = self.client.get(reverse("forecast_api", args=[self.product.id]) + "?days=90")
        self.assertEqual(response.status_code, 400)

    def test_assistant_requires_json(self):
        response = self.client.post(reverse("assistant_api"), data="hello", content_type="text/plain")
        self.assertEqual(response.status_code, 400)

    def test_assistant_uses_fallback_without_key(self):
        from unittest.mock import patch
        with patch.dict("os.environ", {"GROQ_API_KEY": ""}):
            response = self.client.post(reverse("assistant_api"), data=json.dumps({"question":"What is low stock?"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", response.json())

    def test_csv_upload(self):
        content = b"date,sku,product_name,quantity,unit_price\n2026-09-01,CSV-1,CSV Product,2,10.00\n"
        from django.core.files.uploadedfile import SimpleUploadedFile
        upload = SimpleUploadedFile("sales.csv", content, content_type="text/csv")
        response = self.client.post(reverse("upload_sales"), {"file": upload})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Sale.objects.filter(product__sku="CSV-1").exists())

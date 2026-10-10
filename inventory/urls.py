from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),
    path("sales/upload/", views.upload_sales, name="upload_sales"),
    path("forecast/", views.forecast_page, name="forecast"),
    path("api/forecast/<int:product_id>/", views.forecast_api, name="forecast_api"),
    path("assistant/", views.assistant_page, name="assistant"),
    path("api/assistant/", views.assistant_api, name="assistant_api"),
    path("health/", views.health, name="health"),
]

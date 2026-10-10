from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=100, blank=True, default="Uncategorized")
    stock_on_hand = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    lead_time_days = models.PositiveIntegerField(default=7)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return f"{self.sku} — {self.name}"

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    date = models.DateField(db_index=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["product", "date"])]
    @property
    def revenue(self):
        return self.quantity * self.unit_price
    def __str__(self):
        return f"{self.product.sku} / {self.date} / {self.quantity}"

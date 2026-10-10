from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=160)),
                ('category', models.CharField(blank=True, default='Uncategorized', max_length=100)),
                ('stock_on_hand', models.PositiveIntegerField(default=0)),
                ('reorder_level', models.PositiveIntegerField(default=10)),
                ('lead_time_days', models.PositiveIntegerField(default=7)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True)),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='inventory.product')),
            ],
            options={'ordering': ['-date']},
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(
                fields=['product', 'date'],
                name='sale_product_date_idx',
            ),
        ),
    ]

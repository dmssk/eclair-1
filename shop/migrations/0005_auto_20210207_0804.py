# Generated by Django 3.1.6 on 2021-02-07 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_product_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price_discounted",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Цена после скидки",
            ),
        ),
    ]
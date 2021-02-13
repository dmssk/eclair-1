# Generated by Django 3.1.6 on 2021-02-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_product_recommendations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="recommendations",
            field=models.ManyToManyField(
                blank=True, related_name="_product_recommendations_+", to="shop.Product"
            ),
        ),
    ]

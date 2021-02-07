# Generated by Django 3.1.6 on 2021-02-07 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_auto_20210207_0804"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price_discounted",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Цена после скидки",
            ),
        ),
    ]

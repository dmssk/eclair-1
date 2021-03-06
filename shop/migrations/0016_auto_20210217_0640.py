# Generated by Django 3.1.6 on 2021-02-17 06:40

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0015_auto_20210215_1849"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="coordinates",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                validators=[shop.validators.is_coordinates],
                verbose_name="Координаты",
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="name",
            field=models.CharField(
                default="Точка", max_length=255, verbose_name="Название точки"
            ),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1.6 on 2021-02-09 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_auto_20210209_0620"),
    ]

    operations = [
        migrations.AddField(
            model_name="promotedproductsmanual",
            name="promoted",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.promotedproductssettings",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="promotedproductssettings",
            name="title",
            field=models.CharField(max_length=100, verbose_name="Заголовок промо"),
        ),
    ]

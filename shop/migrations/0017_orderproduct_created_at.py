# Generated by Django 3.1.6 on 2021-02-19 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0016_auto_20210217_0640"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderproduct",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата покупки",
            ),
            preserve_default=False,
        ),
    ]

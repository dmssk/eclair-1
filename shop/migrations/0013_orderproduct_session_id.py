# Generated by Django 3.1.6 on 2021-02-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0012_auto_20210215_0549"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderproduct",
            name="session_id",
            field=models.CharField(max_length=100, null=True, verbose_name="Сессия"),
        ),
    ]
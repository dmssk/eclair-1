# Generated by Django 3.1.6 on 2021-02-15 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0014_auto_20210215_1848"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderproduct",
            name="session_id",
        ),
        migrations.AddField(
            model_name="order",
            name="session_id",
            field=models.CharField(
                default="xer8z99g7zpgu8qdm8lc5ods7822z047",
                max_length=100,
                verbose_name="Сессия",
            ),
            preserve_default=False,
        ),
    ]

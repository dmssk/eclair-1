# Generated by Django 3.1.6 on 2021-02-09 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_auto_20210209_0521"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Cart",
            new_name="CartProduct",
        ),
    ]
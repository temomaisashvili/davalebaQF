# Generated by Django 5.1.2 on 2024-10-31 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventManager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="first_name",
            field=models.CharField(default="", max_length=100, verbose_name="სახელი"),
        ),
        migrations.AlterField(
            model_name="customer",
            name="username",
            field=models.CharField(max_length=100, verbose_name="იუზერნეიმი"),
        ),
    ]
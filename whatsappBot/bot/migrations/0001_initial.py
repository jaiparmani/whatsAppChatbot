# Generated by Django 4.1 on 2023-12-20 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Expenses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(max_length=50)),
                ("amount", models.IntegerField(verbose_name="Amount")),
                ("category", models.CharField(max_length=50, verbose_name="Category")),
                ("desc", models.CharField(max_length=500, verbose_name="Description")),
                (
                    "timestamp",
                    models.DateTimeField(auto_now=True, verbose_name="Timestamp"),
                ),
            ],
        ),
    ]

# Generated by Django 4.1 on 2023-12-20 08:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0002_alter_expenses_amount_alter_expenses_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expenses",
            name="timestamp",
            field=models.DateField(),
        ),
    ]

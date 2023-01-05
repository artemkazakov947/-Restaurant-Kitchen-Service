# Generated by Django 4.1.3 on 2022-12-02 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("kitchen_service", "0005_alter_dish_options_remove_dish_ingredients_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="recipe",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dish",
                to="kitchen_service.recipe",
            ),
        ),
    ]

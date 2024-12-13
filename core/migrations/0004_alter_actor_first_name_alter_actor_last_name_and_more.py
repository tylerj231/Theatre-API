# Generated by Django 5.1.4 on 2024-12-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_ticket_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actor",
            name="first_name",
            field=models.CharField(max_length=75, unique=True),
        ),
        migrations.AlterField(
            model_name="actor",
            name="last_name",
            field=models.CharField(max_length=75, unique=True),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

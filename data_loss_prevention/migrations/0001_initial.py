# Generated by Django 5.0.4 on 2024-04-15 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pattern",
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
                ("name", models.CharField(max_length=120)),
                ("regex", models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name="CaughtMessage",
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
                ("text", models.TextField(blank=True)),
                ("caught_at", models.DateTimeField(auto_now_add=True)),
                ("sent_at", models.DateTimeField()),
                (
                    "pattern",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="data_loss_prevention.pattern",
                    ),
                ),
            ],
        ),
    ]

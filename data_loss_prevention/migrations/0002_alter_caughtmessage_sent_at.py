# Generated by Django 5.0.4 on 2024-04-21 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_loss_prevention", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="caughtmessage",
            name="sent_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servings", "0003_log_current_time_alter_log_time_of_serving"),
    ]

    operations = [
        migrations.AddField(
            model_name="log",
            name="alert_sent",
            field=models.BooleanField(default=False),
        ),
    ]

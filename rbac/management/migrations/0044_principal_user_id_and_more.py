# Generated by Django 4.2.10 on 2024-02-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0043_auditlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="principal",
            name="user_id",
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddConstraint(
            model_name="principal",
            constraint=models.UniqueConstraint(
                fields=("user_id", "tenant"), name="unique principal user_id per tenant"
            ),
        ),
    ]

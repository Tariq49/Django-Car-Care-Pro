# Generated by Django 5.0.7 on 2024-08-21 11:45

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Mechanic", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("address", models.TextField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                (
                    "contact_number",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Contact number should be 9 digits.",
                                regex="^\\d{9}$",
                            )
                        ],
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_images/"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Customer",
                "db_table": "customer",
            },
        ),
        migrations.CreateModel(
            name="ServiceRequest",
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
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Two_wheeler_with_gear", "Two_wheeler_with_gear"),
                            ("Two_wheeler_without_gear", "Two_wheeler_without_gear"),
                            ("Four_wheeler", "Four Wheeler"),
                            ("Three_wheeler", "Three_wheeler"),
                        ],
                        max_length=50,
                    ),
                ),
                ("vehicle_no", models.CharField(max_length=20)),
                ("vehicle_name", models.CharField(max_length=50)),
                ("vehicle_model", models.CharField(max_length=50)),
                ("vehicle_brand", models.CharField(max_length=50)),
                ("problem_description", models.TextField()),
                (
                    "date_of_request",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "service_name",
                    models.CharField(
                        choices=[
                            ("Engine Repair", "Engine Repair"),
                            ("Oil Change", "Oil Change"),
                            ("Tire Replacement", "Tire Replacement"),
                            ("Brake Service", "Brake Service"),
                            ("General Maintenance", "General Maintenance"),
                            ("Transmission Repair", "Transmission Repair"),
                            ("Battery Replacement", "Battery Replacement"),
                            ("AC Repair", "AC Repair"),
                            ("Wheel Alignment", "Wheel Alignment"),
                            ("Suspension Repair", "Suspension Repair"),
                            ("Electrical System Repair", "Electrical System Repair"),
                            ("Exhaust System Repair", "Exhaust System Repair"),
                            ("Radiator Repair", "Radiator Repair"),
                            ("Fuel System Repair", "Fuel System Repair"),
                            ("Clutch Repair", "Clutch Repair"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Customer.customer",
                    ),
                ),
                (
                    "mechanic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Mechanic.mechanic",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="customer",
            index=models.Index(fields=["user"], name="customer_user_id_3aba83_idx"),
        ),
        migrations.AddConstraint(
            model_name="customer",
            constraint=models.UniqueConstraint(
                fields=("contact_number",), name="unique_contact_number"
            ),
        ),
        migrations.AddConstraint(
            model_name="servicerequest",
            constraint=models.UniqueConstraint(
                fields=(
                    "customer",
                    "vehicle_no",
                    "problem_description",
                    "service_name",
                ),
                name="unique_service_request",
            ),
        ),
    ]

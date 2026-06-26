from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0010_restore_lane_type_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckingcompany",
            name="company_address",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="truckingcompany",
            name="primary_port_of_entry",
            field=models.CharField(
                blank=True,
                choices=[
                    ("LAREDO", "Laredo"),
                    ("EL_PASO", "El Paso"),
                    ("TIJUANA", "Tijuana"),
                ],
                max_length=20,
                verbose_name="Primary border crossing",
            ),
        ),
        migrations.AddField(
            model_name="truckingcompany",
            name="popular_destinations",
            field=models.TextField(
                blank=True,
                help_text="Corridors or cities you run often, e.g. Houston, Dallas, Laredo",
            ),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="equipment_type",
            field=models.CharField(
                choices=[
                    ("VAN", "Van"),
                    ("REEFER", "Reefer"),
                    ("FLATBED", "Flatbed"),
                    ("STEP_DECK", "Step deck"),
                    ("POWER_ONLY", "Power only"),
                    ("OTHER", "Other"),
                ],
                default="VAN",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="trailer_length_ft",
            field=models.PositiveSmallIntegerField(default=53),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="load_type",
            field=models.CharField(
                choices=[("FULL", "Full"), ("PARTIAL", "Partial")],
                default="FULL",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="weight_lbs",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="min_rate_per_mile",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=6,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
            ),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="reference_id",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="post_status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Open"),
                    ("BOOKED", "Booked"),
                    ("EXPIRED", "Expired"),
                ],
                default="OPEN",
                max_length=20,
            ),
        ),
    ]

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0015_post_compliance_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="BrokerLoad",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "lane_type",
                    models.CharField(
                        choices=[
                            ("LANE", "Lane"),
                            ("POTENTIAL_LANE", "Potential Lane"),
                            ("SPOT_LANE", "Spot Lane"),
                        ],
                        default="LANE",
                        max_length=20,
                    ),
                ),
                (
                    "port_of_entry",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("LAREDO", "Laredo"),
                            ("EL_PASO", "El Paso"),
                            ("TIJUANA", "Tijuana"),
                        ],
                        max_length=20,
                    ),
                ),
                ("location_address", models.CharField(blank=True, max_length=255)),
                ("current_city", models.CharField(max_length=120)),
                (
                    "equipment_type",
                    models.CharField(
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
                ("trailer_length_ft", models.PositiveSmallIntegerField(default=53)),
                (
                    "load_type",
                    models.CharField(
                        choices=[("FULL", "Full"), ("PARTIAL", "Partial")],
                        default="FULL",
                        max_length=20,
                    ),
                ),
                ("weight_lbs", models.PositiveIntegerField(blank=True, null=True)),
                ("reference_id", models.CharField(blank=True, max_length=64)),
                ("mexico_corridor", models.TextField(blank=True)),
                ("us_corridor", models.TextField(blank=True)),
                ("ctpat_required", models.BooleanField(default=False)),
                ("b1_drivers_required", models.BooleanField(default=False)),
                ("load_notes", models.CharField(blank=True, max_length=255)),
                (
                    "post_status",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("BOOKED", "Booked"),
                            ("EXPIRED", "Expired"),
                        ],
                        default="OPEN",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "profile",
                    models.ForeignKey(
                        limit_choices_to={"role": "broker"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="loads",
                        to="register.userprofile",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "broker loads",
                "ordering": ["-created_at"],
            },
        ),
    ]

from django.db import migrations, models


def lane_to_thor(apps, schema_editor):
    TruckAvailability = apps.get_model("register", "TruckAvailability")
    TruckAvailability.objects.filter(lane_type="LANE").update(lane_type="THOR")


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0007_remove_lane_field"),
    ]

    operations = [
        migrations.RunPython(lane_to_thor, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="truckavailability",
            name="lane_type",
            field=models.CharField(
                choices=[
                    ("THOR", "Thor"),
                    ("POTENTIAL_LANE", "Potential lane"),
                    ("SPOT_LANE", "Spot lane"),
                ],
                default="THOR",
                max_length=20,
            ),
        ),
    ]

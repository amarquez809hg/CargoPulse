from django.db import migrations, models


def remove_thor_lane_type(apps, schema_editor):
    TruckAvailability = apps.get_model("register", "TruckAvailability")
    TruckAvailability.objects.filter(lane_type__in=("THOR", "LANE")).update(
        lane_type="SPOT_LANE"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0008_rename_lane_to_thor"),
    ]

    operations = [
        migrations.RunPython(remove_thor_lane_type, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="truckavailability",
            name="lane_type",
            field=models.CharField(
                choices=[
                    ("SPOT_LANE", "Spot lane"),
                    ("POTENTIAL_LANE", "Potential lane"),
                ],
                default="SPOT_LANE",
                max_length=20,
            ),
        ),
    ]

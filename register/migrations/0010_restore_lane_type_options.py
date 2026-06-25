from django.db import migrations, models


def restore_lane_type(apps, schema_editor):
    TruckAvailability = apps.get_model("register", "TruckAvailability")
    TruckAvailability.objects.filter(lane_type="THOR").update(lane_type="LANE")


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0009_spot_and_potential_lane_only"),
    ]

    operations = [
        migrations.RunPython(restore_lane_type, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="truckavailability",
            name="lane_type",
            field=models.CharField(
                choices=[
                    ("LANE", "Lane"),
                    ("POTENTIAL_LANE", "Potential Lane"),
                    ("SPOT_LANE", "Spot Lane"),
                ],
                default="LANE",
                max_length=20,
            ),
        ),
    ]

from django.db import migrations, models


def migrate_lane_fields(apps, schema_editor):
    TruckAvailability = apps.get_model("register", "TruckAvailability")
    for post in TruckAvailability.objects.all():
        if post.spot_lane:
            post.lane_type = "SPOT_LANE"
            post.lane = post.spot_lane
        elif post.potential_lane:
            post.lane_type = "POTENTIAL_LANE"
            post.lane = post.potential_lane
        elif not post.lane:
            post.lane_type = "LANE"
        else:
            post.lane_type = "LANE"
        post.save(update_fields=["lane_type", "lane"])


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0005_remove_availability_dates"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckavailability",
            name="lane_type",
            field=models.CharField(
                choices=[
                    ("LANE", "Lane"),
                    ("POTENTIAL_LANE", "Potential lane"),
                    ("SPOT_LANE", "Spot lane"),
                ],
                default="LANE",
                max_length=20,
            ),
        ),
        migrations.RunPython(migrate_lane_fields, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="truckavailability",
            name="potential_lane",
        ),
        migrations.RemoveField(
            model_name="truckavailability",
            name="spot_lane",
        ),
    ]

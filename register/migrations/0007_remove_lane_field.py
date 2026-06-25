from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0006_consolidate_lane_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="truckavailability",
            name="lane",
        ),
    ]

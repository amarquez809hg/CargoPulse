from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0004_lane_and_port_of_entry"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="truckavailability",
            name="available_from",
        ),
        migrations.RemoveField(
            model_name="truckavailability",
            name="available_to",
        ),
    ]

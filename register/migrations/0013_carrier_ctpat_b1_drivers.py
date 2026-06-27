from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0012_post_location_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckingcompany",
            name="ctpat_certified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="truckingcompany",
            name="b1_drivers",
            field=models.BooleanField(default=False),
        ),
    ]

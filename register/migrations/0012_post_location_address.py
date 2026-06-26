from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0011_company_profile_and_post_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckavailability",
            name="location_address",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

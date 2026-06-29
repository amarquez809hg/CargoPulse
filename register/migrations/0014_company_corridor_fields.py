from django.db import migrations, models


def copy_popular_destinations_to_us_corridor(apps, schema_editor):
    TruckingCompany = apps.get_model("register", "TruckingCompany")
    for company in TruckingCompany.objects.exclude(popular_destinations=""):
        if not company.us_corridor:
            company.us_corridor = company.popular_destinations
            company.save(update_fields=["us_corridor"])


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0013_carrier_ctpat_b1_drivers"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckingcompany",
            name="mexico_corridor",
            field=models.TextField(
                blank=True,
                help_text="Cities or regions in Mexico before the border crossing.",
            ),
        ),
        migrations.AddField(
            model_name="truckingcompany",
            name="us_corridor",
            field=models.TextField(
                blank=True,
                help_text="US cities or regions after the border crossing.",
            ),
        ),
        migrations.RunPython(
            copy_popular_destinations_to_us_corridor,
            migrations.RunPython.noop,
        ),
    ]

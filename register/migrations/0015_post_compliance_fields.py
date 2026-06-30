from django.db import migrations, models


def copy_company_compliance_to_posts(apps, schema_editor):
    TruckAvailability = apps.get_model("register", "TruckAvailability")
    for post in TruckAvailability.objects.select_related("company").iterator():
        company = post.company
        if company.ctpat_certified or company.b1_drivers:
            post.ctpat_certified = company.ctpat_certified
            post.b1_drivers = company.b1_drivers
            post.save(update_fields=["ctpat_certified", "b1_drivers"])


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0014_company_corridor_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="truckavailability",
            name="b1_drivers",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="truckavailability",
            name="ctpat_certified",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(copy_company_compliance_to_posts, migrations.RunPython.noop),
    ]

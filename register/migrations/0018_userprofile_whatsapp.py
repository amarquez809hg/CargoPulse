from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0017_broker_load_commodity"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

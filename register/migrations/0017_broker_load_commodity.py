from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0016_broker_load"),
    ]

    operations = [
        migrations.AddField(
            model_name="brokerload",
            name="commodity",
            field=models.CharField(default="General freight", max_length=120),
            preserve_default=False,
        ),
    ]

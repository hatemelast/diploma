from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0003_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='pin',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0004_alter_buyer_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='phone',
            field=models.CharField(default='', max_length=11),
        ),
    ]

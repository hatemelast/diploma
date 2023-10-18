from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0005_buyer_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buyer',
            old_name='emails',
            new_name='email',
        ),
    ]

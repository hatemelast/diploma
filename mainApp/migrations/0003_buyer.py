from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0002_alter_brand_id_alter_maincategory_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('emails', models.EmailField(max_length=30)),
                ('address', models.TextField(blank=True, default='', null=True)),
                ('pin', models.IntegerField(blank=True, default='', null=True)),
                ('city', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('pic', models.ImageField(blank=True, default='', null=True, upload_to='uploads/users')),
            ],
        ),
    ]

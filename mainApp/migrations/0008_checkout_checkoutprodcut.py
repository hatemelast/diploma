from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0007_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('orderstatus', models.IntegerField(choices=[(0, 'order is Place'), (1, 'order is Packed'), (2, 'order is Dispatched'), (3, 'Dispatched'), (4, 'out for Delivery'), (5, 'Delivered')], default=0)),
                ('paymentstatus', models.IntegerField(choices=[(0, 'Pending'), (1, 'Done')], default=0)),
                ('paymentmode', models.IntegerField(choices=[(0, 'COD'), (1, 'NetBanking')], default=0)),
                ('subtotal', models.IntegerField()),
                ('shipping', models.IntegerField()),
                ('total', models.IntegerField()),
                ('rppid', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutProdcut',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('total', models.ImageField(upload_to='')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.checkout')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.product')),
            ],
        ),
    ]

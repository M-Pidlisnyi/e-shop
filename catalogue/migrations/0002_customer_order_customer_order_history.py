# Generated by Django 5.0.3 on 2024-04-04 16:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('discount_card_number', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shop Customer',
                'verbose_name_plural': 'Shop Customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('price_with_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.customer')),
                ('product', models.ForeignKey(default='deleted product', on_delete=django.db.models.deletion.SET_DEFAULT, to='catalogue.product')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='order_history',
            field=models.ManyToManyField(through='catalogue.Order', to='catalogue.product'),
        ),
    ]

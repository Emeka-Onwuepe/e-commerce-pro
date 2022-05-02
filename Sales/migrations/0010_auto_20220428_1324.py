# Generated by Django 3.1.5 on 2022-04-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0009_auto_20220406_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='destination',
            field=models.CharField(default='not set', max_length=256, verbose_name='destination'),
        ),
        migrations.AddField(
            model_name='sales',
            name='logistics',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='logistics'),
        ),
    ]

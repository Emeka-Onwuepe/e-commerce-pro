# Generated by Django 3.1.5 on 2022-04-20 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0013_auto_20220409_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]
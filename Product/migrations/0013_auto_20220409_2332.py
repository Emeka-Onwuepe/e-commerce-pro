# Generated by Django 3.1.5 on 2022-04-09 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=150, verbose_name='description'),
        ),
    ]

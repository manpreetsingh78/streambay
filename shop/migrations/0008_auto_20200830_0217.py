# Generated by Django 3.1 on 2020-08-29 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_replacement_reset'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='oid',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orderupdate',
            name='oid',
            field=models.CharField(default='', max_length=100),
        ),
    ]
# Generated by Django 2.2.9 on 2020-02-02 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_auto_20200201_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='pending', max_length=500),
        ),
    ]

# Generated by Django 2.2.9 on 2020-02-03 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plate',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='special',
            field=models.TextField(default='None', max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='volume',
            field=models.CharField(default='None', max_length=30),
        ),
    ]
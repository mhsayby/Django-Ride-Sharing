# Generated by Django 2.2.9 on 2020-02-03 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_mysharer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(default='owner', max_length=50),
        ),
    ]

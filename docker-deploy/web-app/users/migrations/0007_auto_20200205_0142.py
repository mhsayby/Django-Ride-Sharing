# Generated by Django 2.2.9 on 2020-02-05 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('rides', '0005_auto_20200203_1508'),
        ('users', '0006_auto_20200203_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='special',
        ),
        migrations.DeleteModel(
            name='mySharer',
        ),
    ]
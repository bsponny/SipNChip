# Generated by Django 3.2.9 on 2021-12-05 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SipNChipApp', '0021_merge_20211117_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecard',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]

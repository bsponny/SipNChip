# Generated by Django 3.2.9 on 2021-12-05 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SipNChipApp', '0022_scorecard_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='triedToOrder',
            field=models.BooleanField(default=False),
        ),
    ]

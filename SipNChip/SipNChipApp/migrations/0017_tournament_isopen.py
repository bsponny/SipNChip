# Generated by Django 3.1.5 on 2021-11-11 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SipNChipApp', '0016_auto_20211110_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='isOpen',
            field=models.BooleanField(default=False),
        ),
    ]

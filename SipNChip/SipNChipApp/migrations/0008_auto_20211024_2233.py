# Generated by Django 3.2.8 on 2021-10-25 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SipNChipApp', '0007_auto_20211021_0303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsorrequest',
            name='tournament',
        ),
        migrations.AddField(
            model_name='sponsorrequest',
            name='dayOfTournament',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='sponsorrequest',
            name='sponsor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

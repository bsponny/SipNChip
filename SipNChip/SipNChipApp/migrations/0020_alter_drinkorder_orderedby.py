# Generated by Django 3.2.7 on 2021-11-13 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SipNChipApp', '0019_alter_drinkorder_totalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkorder',
            name='orderedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

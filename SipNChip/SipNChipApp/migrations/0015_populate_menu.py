from django.db import migrations, models
from SipNChipApp.forms import User

def populate_menu(apps, schema_editor):
    Drink = apps.get_model('SipNChipApp', 'Drink')

    drink1 = Drink(
        name = 'Purple Rain',
        description = 'A delicious cocktail named for its stunning color. Made with vodka, blue curacao, grenadine, and lemonade.',
        price = 9.99
    )
    drink1.save()

    drink2 = Drink(
        name = 'Mai Tai',
        description = 'A traditional tiki cocktail made with rum, orange juice, triple sec, and sweetener.',
        price = 11.99
    )
    drink2.save()

    drink3 = Drink(
        name = 'Irish Mule',
        description = 'A spin on the classic moscow mule made with Irish whiskey, lime juice, and ginger beer.',
        price = 11.99
    )
    drink3.save()

    drink4 = Drink(
        name = 'Mango Margarita',
        description = 'A delicious frozen margarita made with lime juice, tequila, frozen mango, and sweetener.',
        price = 9.99
    )
    drink4.save()

def populate_user(apps, schema_editor):
    Account = apps.get_model('SipNChipApp', 'Account')

    admin = User.objects.create_user(username='admin', password='SipNChip')
#    user.save()

#    account = Account(user=user, userType=5, id=1)
#    account.save()

class Migration(migrations.Migration):

    dependencies = [
        ('SipNChipApp', '0014_auto_20211109_1849'),
    ]

    operations = [
        migrations.RunPython(populate_menu),
        migrations.RunPython(populate_user),
    ]
    

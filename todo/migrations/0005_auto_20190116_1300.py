# Generated by Django 2.1.4 on 2019-01-16 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_profile_active_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='time_password',
            new_name='idsession',
        ),
        migrations.AlterField(
            model_name='companyname',
            name='name',
            field=models.CharField(help_text='RGD, Aeroflot, Rosneft, Gazprom or empty', max_length=50),
        ),
    ]

# Generated by Django 2.1.4 on 2019-01-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_auto_20190116_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desks',
            name='language',
        ),
        migrations.RemoveField(
            model_name='desks',
            name='linenos',
        ),
        migrations.RemoveField(
            model_name='desks',
            name='style',
        ),
        migrations.RemoveField(
            model_name='desks',
            name='title',
        ),
    ]
# Generated by Django 2.2.28 on 2023-03-21 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamerateapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='publisher',
            field=models.BooleanField(default=False, verbose_name=False),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2.4 on 2019-08-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_discord_connector', '0002_auto_20190823_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='discordclient',
            name='invite_link',
            field=models.URLField(default='Test'),
            preserve_default=False,
        ),
    ]

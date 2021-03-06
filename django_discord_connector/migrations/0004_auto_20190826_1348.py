# Generated by Django 2.2.4 on 2019-08-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_discord_connector', '0003_discordclient_invite_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordchannel',
            name='external_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='discordgroup',
            name='external_id',
            field=models.BigIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discorduser',
            name='external_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]

# Generated by Django 2.2.13 on 2020-09-29 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_discord_connector', '0008_auto_20200107_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discordtoken',
            name='discord_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discord_token', to='django_discord_connector.DiscordUser'),
        ),
    ]

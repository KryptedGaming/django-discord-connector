from django.contrib import admin
from django_discord_connector.models import DiscordClient, DiscordToken, DiscordGroup, DiscordChannel, DiscordUser

# Register your models here.
admin.site.register(DiscordClient)
admin.site.register(DiscordToken)
admin.site.register(DiscordGroup)
admin.site.register(DiscordChannel)
admin.site.register(DiscordUser)
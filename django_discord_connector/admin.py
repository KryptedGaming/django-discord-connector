from django.contrib import admin
from django_discord_connector.models import DiscordClient, DiscordToken, DiscordGroup, DiscordChannel, DiscordUser
from django_discord_connector.tasks import sync_discord_groups
from django.apps import apps

def update_discord_groups(modeladmin, request, queryset):
    sync_discord_groups()
update_discord_groups.short_description="Update Discord groups from Discord Server"

# Register your models here.
admin.site.register(DiscordGroup)
admin.site.register(DiscordChannel)
admin.site.register(DiscordUser)

if apps.is_installed('django_singleton_admin'):
    # Highly Recommended: https://github.com/porowns/django-singleton-admin
    from django_singleton_admin.admin import DjangoSingletonModelAdmin
    @admin.register(DiscordClient)
    class DiscordClientAdmin(DjangoSingletonModelAdmin):
        fieldsets = (
            ('General Settings', {
                'fields': ('callback_url', 'server_id', 'client_id', 'client_secret', 'bot_token', 'invite_link' )
            }),
            ('Advanced Settings', {
                'classes': ('collapse', 'open'),
                'fields': ('api_endpoint', 'base_uri', 'token_uri', 'token_revoke_uri')
            }),
        )
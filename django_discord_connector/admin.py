from django.contrib import admin
from django_discord_connector.models import DiscordClient, DiscordToken, DiscordGroup, DiscordChannel, DiscordUser
from django_discord_connector.tasks import sync_discord_groups

def update_discord_groups(modeladmin, request, queryset):
    sync_discord_groups()
update_discord_groups.short_description="Update Discord groups from Discord Server"

# Register your models here.
admin.site.register(DiscordGroup)
admin.site.register(DiscordChannel)
admin.site.register(DiscordUser)

class DiscordClientAdmin(admin.ModelAdmin):
    list_display = ['server_id', 'callback_url', 'invite_link']
    ordering = ['server_id']
    search_fields = ('name', 'external_id')
    actions = [update_discord_groups]


admin.site.register(DiscordClient, DiscordClientAdmin)
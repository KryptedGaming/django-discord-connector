from django.apps import AppConfig
from django.db.models.signals import m2m_changed


class DjangoDiscordConnectorConfig(AppConfig):
    name = 'django_discord_connector'
    verbose_name = 'discord'

    def ready(self):
        from .signals import user_group_change_sync_discord_groups
        from django.contrib.auth.models import User
        m2m_changed.connect(
            user_group_change_sync_discord_groups, sender=User.groups.through)

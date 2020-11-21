from django.apps import AppConfig
from django.db.models.signals import m2m_changed
from django.apps import apps

class DjangoDiscordConnectorConfig(AppConfig):
    name = 'django_discord_connector'
    package_name = __import__(name).__package_name__
    version = __import__(name).__version__
    verbose_name = 'discord'
    url_slug = 'discord'

    def ready(self):
        from .signals import user_group_change_sync_discord_groups
        from django.contrib.auth.models import User
        m2m_changed.connect(
            user_group_change_sync_discord_groups, sender=User.groups.through)

        if apps.is_installed('packagebinder'):
            from .bindings import create_bindings
            create_bindings()
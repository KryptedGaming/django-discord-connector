from django.apps import AppConfig
from django.db.models.signals import m2m_changed, pre_delete
from django.apps import apps

class DjangoDiscordConnectorConfig(AppConfig):
    name = 'django_discord_connector'
    package_name = __import__(name).__package_name__
    version = __import__(name).__version__
    verbose_name = 'discord'
    url_slug = 'discord'

    def ready(self):
        from .signals import user_group_change_sync_discord_groups, user_delete
        from django.contrib.auth.models import User
        m2m_changed.connect(
            user_group_change_sync_discord_groups, sender=User.groups.through)

        pre_delete.connect(
            user_delete,
            sender=User
        )
        if apps.is_installed('packagebinder'):
            from .bindings import create_bindings
            create_bindings()
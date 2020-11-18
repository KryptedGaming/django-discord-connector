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
            from packagebinder.exceptions import BindException
            try:
                bind = apps.get_app_config('packagebinder').get_bind_object(
                    self.package_name, self.version)
                # Required Task Bindings
                bind.add_required_task(
                    name="Discord: Sync User Groups",
                    task="django_discord_connector.tasks.verify_all_discord_users_groups",
                    interval=5,
                    interval_period="minutes",
                )
                bind.add_required_task(
                    name="Discord: Update User Information",
                    task="django_discord_connector.tasks.sync_all_discord_users_accounts",
                    interval=1,
                    interval_period="days",
                )
                bind.add_optional_task(
                    name="Discord: Hard Sync Users",
                    task="django_discord_connector.tasks.remote_sync_all_discord_users_groups",
                    interval=7,
                    interval_period="days",
                )
                bind.save()
            except BindException as e:
                print(e)
                return
            except Exception as e:
                print(e)
                return

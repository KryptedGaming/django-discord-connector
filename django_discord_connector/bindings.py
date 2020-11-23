from django.apps import apps 
from django.urls import reverse
from django.conf import settings
from .models import DiscordClient
from .forms import DiscordClientForm
from packagebinder.bind import PackageBinding, SettingsBinding, TaskBinding, SidebarBinding
import logging 

logger = logging.getLogger(__name__)

app_config = apps.get_app_config('django_discord_connector')

package_binding = PackageBinding(
    package_name=app_config.name, 
    version=app_config.version, 
    url_slug='discord', 
)

settings_binding = SettingsBinding(
    package_name=app_config.name, 
    settings_class=DiscordClient,
    settings_form=DiscordClientForm,
)

task_binding = TaskBinding(
    package_name=app_config.name, 
    required_tasks = [
        {
            "name": "Discord: Sync User Groups",
            "task_name": "django_discord_connector.tasks.verify_all_discord_users_groups",
            "interval": 5,
            "interval_period": "minutes",
        },
        {
            "name": "Discord: Update User Information",
            "task_name": "django_discord_connector.tasks.sync_all_discord_users_accounts",
            "interval": 1,
            "interval_period": "days",
        },
    ],
    optional_tasks = [
        {
            "name": "Discord: Hard Sync Users",
            "task_name": "django_discord_connector.tasks.remote_sync_all_discord_users_groups",
            "interval": 7,
            "interval_period": "days",
        },
    ]
)

def create_bindings():
    try:
        package_binding.save()
        settings_binding.save()
        task_binding.save()
    except Exception as e:
        if settings.DEBUG:
            raise(e)
        else:
            logger.error(f"Failed package binding step for {app_config.name}: {e}")

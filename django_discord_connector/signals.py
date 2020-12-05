from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_delete
from django.contrib.auth.models import User
from .models import DiscordUser, DiscordGroup
from .tasks import verify_discord_user_groups, remove_discord_user

import logging
logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=User.groups.through)
def user_group_change_sync_discord_groups(sender, **kwargs):
    django_user = kwargs.get('instance')
    action = str(kwargs.get('action'))

    # Check if Django user exists
    try:
        discord_user = DiscordUser.objects.get(discord_token__user=django_user)
    except DiscordUser.DoesNotExist:
        logger.info(
            "DiscordUser not found for %s, skipping group sync" % django_user)
        return

    if "post" in kwargs.get('action'):
        verify_discord_user_groups.apply_async(args=[discord_user.external_id], countdown=30)

@receiver(pre_delete, sender=User)
def user_delete(sender, **kwargs):
    django_user = kwargs.get('instance')

    if DiscordUser.objects.filter(discord_token__user=django_user).exists():
        discord_user = DiscordUser.objects.get(discord_token__user=django_user)
    else:
        return 

    remove_discord_user.apply_async(args=[discord_user.external_id])
    
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User
from .models import DiscordUser, DiscordGroup
from .tasks import add_discord_group_to_discord_user, remove_discord_group_from_discord_user


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

    group_ids = [pk for pk in kwargs.get('pk_set')]

    if action == "post_remove":
        for group_id in group_ids:
            try:
                discord_group = DiscordGroup.objects.get(group_id=group_id)
                remove_discord_group_from_discord_user.apply_async(
                    args=[discord_group.external_id, discord_user.external_id])
            except DiscordGroup.DoesNotExist:
                logger.info(
                    "DiscordGroup not found for %s, skipping group sync" % group_id)
    elif action == "post_add":
        for group_id in group_ids:
            try:
                discord_group = DiscordGroup.objects.get(group_id=group_id)
                add_discord_group_to_discord_user.apply_async(
                    args=[discord_group.external_id, discord_user.external_id])
            except DiscordGroup.DoesNotExist:
                logger.info(
                    "DiscordGroup not found for %s, skipping group sync" % group_id)

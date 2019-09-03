from celery import shared_task
from django_discord_connector.models import DiscordUser, DiscordGroup, DiscordClient, DiscordChannel
from django_discord_connector.request import DiscordRequest
from django.conf import settings
from http.client import responses
import logging


logger = logging.getLogger(__name__)
discord_client = DiscordClient.get_instance()
discord_request = DiscordRequest(settings=discord_client.serialize())

"""
Cron Tasks
These are tasks to be set up on a crontab schedule
"""
@shared_task
def sync_discord_users():
    for discord_user in DiscordUser.objects.all():
        update_discord_user.apply_async(args=[discord_user.external_id])
        sync_discord_user_discord_groups.apply_async(
            args=[discord_user.external_id])


@shared_task
def sync_discord_groups():
    # convert role list into dict of IDs
    discord_guild_roles = {
        role['id']: role for role in discord_request.get_guild_roles().json()}
    discord_local_roles = list(DiscordGroup.objects.all().values_list(
        'external_id', flat=True))  # get list of local roles we know about from database

    # build role change lists
    discord_roles_to_remove = set(
        discord_local_roles) - set(discord_guild_roles.keys())
    discord_roles_to_add = set(
        discord_guild_roles.keys()) - set(discord_local_roles)

    for role_id in discord_roles_to_remove:
        DiscordGroup.objects.get(external_id=role_id).delete()

    for role_id in discord_roles_to_add:
        if not discord_guild_roles[role_id]['hoist']:
            continue
        DiscordGroup.objects.create(
            name=discord_guild_roles[role_id]['name'], external_id=role_id)


@shared_task
def sync_discord_channels():
    discord_guild_channels = {
        channel['id']: channel for channel in discord_request.get_guild_channels().json()}
    discord_local_channels = list(DiscordChannel.objects.all().values_list(
        'external_id', flat=True))

    # build channel change lists
    discord_channels_to_remove = set(
        discord_local_channels) - set(discord_guild_channels.keys())
    discord_channels_to_add = set(
        discord_guild_channels.keys()) - set(discord_local_channels)

    for channel_id in discord_channels_to_remove:
        DiscordChannel.objects.get(external_id=channel_id).delete()

    for channel_id in discord_channels_to_add:
        if discord_guild_channels[channel_id]['type'] == 0:
            DiscordChannel.objects.create(
                external_id=channel_id, name="#%s" % discord_guild_channels[channel_id]['name'])


"""
Discord User tasks
Tasks related to keeping DiscordUser objects up to date.
"""
@shared_task
def update_discord_user(discord_user_id):
    discord_user = DiscordUser.objects.get(external_id=discord_user_id)
    response = discord_request.get_discord_user(discord_user_id)
    if responses[response.status_code] == 'OK':
        response = response.json()
        discord_user.nickname = response['nick'] + \
            "#" + response['user']['discriminator']
        discord_user.username = response['user']['username'] + \
            "#" + response['user']['discriminator']
        discord_user.save()
    else:
        raise Exception(
            "[%s Response] Failed to update discord user" % response.status_code)


@shared_task
def sync_discord_user_discord_groups(discord_user_id):
    discord_user = DiscordUser.objects.get(external_id=discord_user_id)
    response = discord_request.get_discord_user(discord_user_id)
    discord_user_remote_role_ids = set([int(role_id) for role_id in response.json()['roles']])
    discord_user_local_role_ids = set(discord_user.groups.all().values_list('external_id', flat=True))

    logger.debug("remote: %s" % discord_user_remote_role_ids)
    logger.debug("local: %s" % discord_user_local_role_ids)
    # Test value DJANGO_DISCORD_REMOTE_PRIORITY in settings, but make it optional
    try:
        if settings.DJANGO_DISCORD_REMOTE_PRIORITY:
            remote_priority = True
        else:
            remote_priority = False
    except AttributeError:
        remote_priority = False

    if responses[response.status_code] == 'OK':
        if remote_priority:
            logger.info(
                "Setting DJANGO_DISCORD_REMOTE_PRIORITY set. Adding groups to local DiscordUser store.")
            discord_groups_to_add = discord_user_remote_role_ids - discord_user_local_role_ids
            discord_groups_to_remove = discord_user_local_role_ids - discord_user_remote_role_ids
            logger.info("Discord groups to add: %s" % discord_groups_to_add)
            logger.info("Discord groups to remove: %s" %
                         discord_groups_to_remove)
            for discord_group_id in discord_groups_to_add:
                discord_group = DiscordGroup.objects.get(
                    external_id=discord_group_id)
                discord_user.groups.add(discord_group)
                if discord_group.group:
                    discord_user.discord_token.user.groups.add(
                        discord_group.group)

            for discord_group_id in discord_groups_to_remove:
                discord_group = DiscordGroup.objects.get(
                    external_id=discord_group_id)
                discord_user.groups.remove(discord_group)
                if discord_group.group:
                    discord_user.discord_token.user.groups.remove(
                        discord_group.group)
        else:
            logger.info(
                "Setting DJANGO_DISCORD_REMOTE_PRIORITY unset. Removing groups from remote DiscordUser.")
            discord_groups_to_remove = discord_user_remote_role_ids - discord_user_local_role_ids
            discord_groups_to_add = discord_user_local_role_ids - discord_user_remote_role_ids
            logger.info("Discord groups to add: %s" % discord_groups_to_add)
            logger.info("Discord groups to remove: %s" %
                         discord_groups_to_remove)
            for discord_group_id in discord_groups_to_remove:
                remove_discord_group_from_discord_user.apply_async(
                    args=[discord_group_id, discord_user_id])
                logger.info("Removing group %s from user %s due to mismatched local groups" % (
                    discord_group_id, discord_user_id))

            for discord_group_id in discord_groups_to_add:
                add_discord_group_to_discord_user.apply_async(
                    args=[discord_group_id, discord_user_id])
                logger.info("Adding group %s to user %s due to mismatched local groups" % (
                    discord_group_id, discord_user_id))

    else:
        raise Exception("[%s Response] Failed to sync discord groups for user %s" % (
            response.status_code, discord_user_id))


@shared_task(rate_limit="1/s")
def add_discord_group_to_discord_user(discord_group_id, discord_user_id):
    response = discord_request.add_role_to_user(
        discord_group_id, discord_user_id)
    if responses[response.status_code] == "No Content":
        discord_user = DiscordUser.objects.get(external_id=discord_user_id)
        logger.info("Succesfully added Discord role %s to Discord user %s" % (
            discord_group_id, discord_user_id))
    elif responses[response.status_code] == "Too Many Requests":
        logger.warning("[RATELIMIT] adding Discord group %s to Discord User %s" % (
            discord_group_id, discord_user_id))
        add_discord_group_to_discord_user.apply_async(
            args=[discord_group_id, discord_user_id], countdown=600)
    else:
        raise Exception("[%s Response] Failed to add discord group %s to discord user %s: %s" % (
            response.status_code, discord_group_id, discord_user_id, response.json()))


@shared_task(rate_limit="1/s")
def remove_discord_group_from_discord_user(discord_group_id, discord_user_id):
    response = discord_request.remove_role_from_user(
        discord_group_id, discord_user_id)
    if responses[response.status_code] == "No Content":
        discord_user = DiscordUser.objects.get(external_id=discord_user_id)
        logger.info("Succesfully removed Discord role %s from Discord user %s" % (
            discord_group_id, discord_user_id))
        discord_user.groups.remove(
            DiscordGroup.objects.get(external_id=discord_group_id))
    elif responses[response.status_code] == "Too Many Requests":
        logger.warning("[RATELIMIT] removing Discord group %s from Discord User %s" % (
            discord_group_id, discord_user_id))
        remove_discord_group_from_discord_user.apply_async(
            args=[discord_group_id, discord_user_id], countdown=600)
    else:
        raise Exception("[%s Response] Failed to remove discord group %s from discord user %s : %s" % (
            response.status_code, discord_group_id, discord_user_id, response.json()))

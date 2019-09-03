from celery import shared_task
from django_discord_connector.models import DiscordUser, DiscordGroup, DiscordClient, DiscordChannel
from django_discord_connector.request import DiscordRequest

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
        if discord_guild_roles[role_id]['hoist']:
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
    pass


@shared_task
def sync_discord_user_discord_groups(discord_user_id):
    pass


@shared_task
def add_discord_group_to_discord_user(discord_group_id, discord_user_id):
    pass


@shared_task
def remove_discord_group_from_discord_user(discord_group_id, discord_user_id):
    pass

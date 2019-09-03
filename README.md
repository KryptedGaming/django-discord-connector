# django-discord-connector
Discord connector for Django.

# Django Settings
The Django Discord Connector adds several settings, changing the behavior of the celery tasks and other functionality.

|   Setting    |    Values   |    Description   |
|  ---  |  ---  |  ---  |
|   `DJANGO_DISCORD_REMOTE_PRIORITY`    |    True / False   |   `sync_discord_user_discord_groups` will update the DiscordUser according to the remote Discord groups, instead of the local groups.   |
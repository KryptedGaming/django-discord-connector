# Django Discord Connector
Django Discord Connector is a saimple Django application that adds models, urls, and Celery tasks to help manage Discord entities. 

There are several behaviors that the application will add:
1. Automatically adding discord roles when adding attached DjangoGroup objects to a User
2. Periodically syncing Discord entities with information from the Discord server

## Installation
1. Add django_discord_connector to your INSTALLED_APPS
2. Include the django_discord_connector URLs in your urls.py
3. Run `python3 manage.py migrate` to create the django_discord_connector tables
4. Create a DiscordClient in the administration panel
5. Load the default periodic tasks `python3 manage.py loaddata discord_default_schedule.json`

## Settings
The Django Discord Connector adds settings which change the behavior of the celery tasks and other functionality.

|   Setting    |    Values   |    Description   |
|  ---  |  ---  |  ---  |
|   `DJANGO_DISCORD_REMOTE_PRIORITY`    |    True / False   |   `sync_discord_user_discord_groups` will update the DiscordUser according to the remote Discord groups, instead of the local groups.   |

## Provided URLs
|    URL Name   |   Description    |
|  ---  |  ---  |
|   django-discord-connector-sso-callback    |   The callback url for SSO tokens (`sso/callback`)    |
|   django-discord-connector-sso-token-add    |   Redirects users to the SSO login for Discord    |
|   django-discord-connector-sso-token-remove    |  Removes an SSO token (expects kwarg pk)     |

## Provided Celery Tasks
|   Task Name    |   Action    |
|  ---  |  ---  |
|   sync_discord_users    |   Updates all information and groups for a DiscordUser    |
|   sync_discord_groups    |  Updates all DiscordGroup objects with groups from Discord server     |
|   sync_discord_channels   | Updates all DiscordChannel objects with channels from Discord server      |


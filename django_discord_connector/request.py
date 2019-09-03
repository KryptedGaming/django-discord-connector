import json
import requests
from discord.ext import commands


class DiscordRequest():
    def __init__(self, api_endpoint=None, server_id=None, client_id=None, secret=None, bot_token=None, settings=None):
        if settings:
            self.api_endpoint = str(settings['api_endpoint'])
            self.server_id = int(settings['server_id'])
            self.client_id = int(settings['client_id'])
            self.secret = str(settings['secret'])
            self.bot_token = str(settings['bot_token'])
        else:
            self.api_endpoint = api_endpoint
            self.server_id = server_id
            self.client_id = client_id
            self.secret = secret
            self.bot_token = bot_token

    @staticmethod
    def get_instance():
        from django_discord_connector.models import DiscordClient
        return DiscordRequest(settings=DiscordClient.get_instance().serialize())

    def activate(self):
        prefix = "?"
        bot = commands.Bot(command_prefix=prefix)
        bot.run(self.bot_token)

    def get_discord_user(self, user_id):
        url = self.api_endpoint + "/guilds/" + \
            str(self.server_id) + "/members/" + str(user_id)
        response = requests.get(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + self.bot_token
        })
        return response

    def get_discord_users(self):
        url = self.api_endpoint + "/guilds/" + self.server_id + "/members/"
        response = requests.get(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + self.bot_token
        })
        return response

    def add_role_to_user(self, role_id, user_id):
        url = self.api_endpoint + "/guilds/" + str(self.server_id) + \
            "/members/" + str(user_id) + "/roles/" + str(role_id)
        response = requests.put(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + self.bot_token
        })
        return response

    def remove_role_from_user(self, role_id, user_id):
        url = self.api_endpoint + "/guilds/" + str(self.server_id) + \
            "/members/" + str(user_id) + "/roles/" + str(role_id)
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + self.bot_token
        })
        return response

    def add_role_to_server(self, role_name):
        url = self.api_endpoint + "/guilds/" + str(self.server_id) + "/roles"
        data = json.dumps({'name': role_name})
        response = requests.post(url,
                                 data=data,
                                 headers={
                                     'Content-Type': 'application/x-www-form-urlencoded',
                                     'Authorization': 'Bot ' + self.bot_token
                                 }
                                 )
        return response

    def remove_role_from_server(self, role_id):
        url = self.api_endpoint + "/guilds/" + \
            str(self.server_id) + "/roles/" + str(role_id)
        response = requests.delete(url, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bot ' + self.bot_token
        })
        return response

    def send_channel_message(self, channel_id, message):
        url = self.api_endpoint + "/channels/" + str(channel_id) + "/messages"
        data = json.dumps({'content': message})
        response = requests.post(url,
                                 data=data,
                                 headers={
                                     'Content-Type': 'application/x-www-form-urlencoded',
                                     'Authorization': 'Bot ' + self.bot_token
                                 }
                                 )
        return response

    def get_guild_roles(self):
        url = self.api_endpoint + "/guilds/" + str(self.server_id) + "/roles"
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bot ' + self.bot_token
            }
        )
        return response

    def get_guild_channels(self):
        url = self.api_endpoint + "/guilds/" + \
            str(self.server_id) + "/channels"
        response = requests.get(
            url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Bot ' + self.bot_token
            }
        )
        return response

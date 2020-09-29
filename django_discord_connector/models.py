from django.db import models
from django.contrib.auth.models import User, Group
from django_discord_connector.request import DiscordRequest


class DiscordClient(models.Model):
    api_endpoint = models.URLField(default="https://discordapp.com/api/v6")
    base_uri = models.URLField(
        default="https://discordapp.com/api/oauth2/authorize")
    token_uri = models.URLField(
        default="https://discordapp.com/api/oauth2/token")
    token_revoke_uri = models.URLField(
        default="https://discordapp.com/api/oauth2/token/revoke")

    callback_url = models.URLField()
    server_id = models.TextField()
    client_id = models.TextField()
    client_secret = models.CharField(max_length=255)
    bot_token = models.CharField(max_length=255)
    invite_link = models.URLField()

    def save(self, *args, **kwargs):
        if "discord.gg/" in self.invite_link:
            self.invite_link = self.invite_link.replace('discord.gg/', 'discordapp.com/api/invites/')
        super(DiscordClient, self).save(*args, **kwargs)

    @staticmethod
    def get_instance():
        if DiscordClient.objects.all().exists():
            return DiscordClient.objects.all()[0]
        raise Exception(
            "DiscordClient must be created before using Discord Connector features.")

    def serialize(self):
        return {
            "api_endpoint": self.api_endpoint,
            "server_id": int(self.server_id),
            "client_id": int(self.client_id),
            "client_secret": self.client_secret,
            "bot_token": self.bot_token,
        }

    def __str__(self):
        return self.callback_url


class DiscordToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    discord_user = models.OneToOneField(
        "DiscordUser", null=True, on_delete=models.CASCADE, related_name="discord_token")
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="discord_token")

    def __str__(self):
        if self.discord_user.nickname:
            return "<%s:%s>" % (self.user.username, self.discord_user.nickname)
        return "<%s:%s>" % (self.user.username, self.discord_user.username)


class DiscordUser(models.Model):
    username = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    external_id = models.BigIntegerField(unique=True)
    groups = models.ManyToManyField("DiscordGroup", blank=True)

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username 
        super(DiscordUser, self).save(*args, **kwargs)

    def __str__(self):
        if self.nickname:
            return self.nickname
        return self.username


class DiscordGroup(models.Model):
    name = models.CharField(max_length=255)
    external_id = models.BigIntegerField(unique=True)
    group = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.SET_NULL, related_name="discord_group")

    def __str__(self):
        if self.group:
            return "<%s:%s>" % (self.name, self.group.name)
        return "<%s>" % self.name


class DiscordChannel(models.Model):
    name = models.CharField(max_length=255)
    external_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name

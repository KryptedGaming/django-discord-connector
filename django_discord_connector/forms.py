from django import forms
from django.forms import ModelForm
from .models import DiscordClient

class DiscordClientForm(ModelForm):
    callback_url = forms.URLField(label="Discord Callback URL")
    server_id = forms.CharField(max_length=255, label="Discord Server ID")
    client_id = forms.CharField(max_length=255, label="Discord Client ID")
    client_secret = forms.CharField(max_length=255, label="Discord Secret ID")
    bot_token = forms.CharField(max_length=255, label="Discord Bot Token")
    invite_link = forms.CharField(max_length=255, label="Discord Invite Link")

    class Meta:
        model = DiscordClient
        fields = ['callback_url', 'server_id', 'client_id', 'client_secret', 'bot_token', 'invite_link']

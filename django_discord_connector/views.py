from django.shortcuts import render, redirect
from django_discord_connector.models import DiscordClient, DiscordToken, DiscordUser
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib import messages
from django.apps import apps
from requests_oauthlib import OAuth2Session
import logging
import base64
import requests


def sso_callback(request):
    try:
        discord_client = DiscordClient.get_instance()
    except:
        messages.warning(
            request, "The site administrator has not added the Discord Client to the admin panel.")
        return redirect('dashboard')
    data = {
        "client_id": discord_client.client_id,
        "client_secret": discord_client.client_secret,
        "grant_type": "authorization_code",
        "code": request.GET['code'],
        "redirect_uri": discord_client.callback_url,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post('%s/oauth2/token' %
                      discord_client.api_endpoint, data, headers)
    r.raise_for_status()

    json = r.json()
    token = json['access_token']
    me = requests.get('https://discordapp.com/api/users/@me',
                      headers={'Authorization': "Bearer " + token}).json()
    join = requests.post(discord_client.invite_link, headers={
                         'Authorization': "Bearer " + token}).json()
    # Catch errors
    if not me['email']:
        messages.add_message(
            request, messages.ERROR, 'Could not find an email on your Discord profile. Please make sure your not signed in as a Guest Discord user.')
        return redirect('dashboard')
    if me['email'] != request.user.email:
        messages.add_message(
            request, messages.WARNING, 'You linked a Discord account with a mismatched email, please verify you linked the correct Discord account.'
        )
    # Delete old token if exists
    if DiscordToken.objects.filter(user=request.user).exists():
        discord_token = request.user.discord_token
        discord_token.delete()

    # Get or Create Discord User
    discord_user = DiscordUser.objects.get_or_create(external_id=me['id'])[0]
    discord_user.username = me['username'] + "#" + me['discriminator']
    if 'nick' in me:
        discord_user.nickname = me['nick'] + "#" + me['discriminator']

    discord_user.save()

    # Attach DiscordToken to user
    token = DiscordToken(
        access_token=json['access_token'],
        refresh_token=json['refresh_token'],
        discord_user=discord_user,
        user=request.user
    )
    token.save()

    return redirect('/')


def add_sso_token(request):
    scope = (['email', 'guilds.join', 'identify'])
    try:
        discord_client = DiscordClient.get_instance()
    except:
        messages.warning(
            request, "The site administrator has not added the Discord Client to the admin panel.")
        return redirect('dashboard')
    oauth = OAuth2Session(discord_client.client_id,
                          redirect_uri=discord_client.callback_url, scope=scope, token=None, state=None)
    url, state = oauth.authorization_url(discord_client.base_uri)
    return HttpResponseRedirect(url)


def remove_sso_token(request, pk):
    discord_token = DiscordToken.objects.get(pk=pk)
    if request.user == discord_token.user:
        discord_token.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Discord token has been deleted.")
        return redirect('/')
    else:
        messages.add_message(request, messages.ERROR,
                             "That Discord token does not belong to you.")
        return redirect('/')

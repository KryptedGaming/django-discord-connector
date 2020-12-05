from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User, Group 
from django_discord_connector.models import DiscordUser, DiscordGroup, DiscordToken
import django_discord_connector
import logging 
logger = logging.getLogger('django_discord_connector')

def mock_discord_task(args, countdown=None):
    logger.info(f"args={args},countdown={countdown}")

class TestDiscordSignalSuite(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name="Group"
        )

        self.user = User.objects.create(
            username="test"
        )

        self.discord_user = DiscordUser.objects.create(
            username="test",
            nickname="test",
            external_id=1,
        )

        self.discord_token = DiscordToken.objects.create(
            access_token="null",
            refresh_token="null",
            discord_user=self.discord_user,
            user=self.user
        )

        self.discord_group = DiscordGroup.objects.create(
            name="DiscordGroup",
            external_id=1,
            group=self.group
        )

    def tearDown(self):
        try:
            self.user.delete()
            self.group.delete()
            self.discord_token.delete()
            self.discord_user.delete()
            self.discord_group.delete()
        except Exception as e:
            pass

    @patch.object(django_discord_connector.signals.verify_discord_user_groups, 'apply_async', mock_discord_task)
    def test_user_group_change(self):
        with self.assertLogs('django_discord_connector', level='INFO') as cm:
            self.user.groups.add(self.group)
            message = cm.output[0]
            self.assertTrue("args=[1]" in message)
            self.assertTrue("countdown=30" in message)

    
    @patch.object(django_discord_connector.signals.remove_discord_user, 'apply_async', mock_discord_task)
    def test_user_delete(self):
        with self.assertLogs('django_discord_connector', level='INFO') as cm:
            self.user.delete()
            message = cm.output[0]
            self.assertTrue("args=[1]" in message)
        


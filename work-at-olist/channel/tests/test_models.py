from django.test import TestCase
from django.db import IntegrityError

from channel.models import Channel


class ChannelTest(TestCase):
    def test_create_channel(self):
        channel = Channel.objects.create(name='Lojas Americanas')

        self.assertEqual(channel.name, 'Lojas Americanas')
        self.assertEqual(channel.slug, 'lojas-americanas')

    def test_name(self):
        channel = Channel.objects.create(name='Lojas Americanas')

        self.assertEqual(channel.name, 'Lojas Americanas')

    def test_required_name(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create()

    def test_auto_generated_slug(self):
        channel = Channel.objects.create(name='Lojas Americanas')

        self.assertEqual(channel.slug, 'lojas-americanas')

    def test_duplicated_slugs(self):
        Channel.objects.create(name='Lojas Americanas')
        channel = Channel.objects.create(name='Lojas Americanas')

        self.assertEqual(Channel.objects.count(), 2)
        self.assertEqual(channel.slug, 'lojas-americanas-2')

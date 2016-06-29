from django.test import TestCase
from django.db import IntegrityError

from channel.models import Channel
from category.models import Category


class CategoryTest(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(name='Lojas Americanas')

    def test_create_category(self):
        category = Category.objects.create(
            name='National Literature',
            channel=self.channel)

        self.assertEqual(category.name, 'National Literature')
        self.assertEqual(category.slug, 'national-literature')
        self.assertEqual(category.channel, self.channel)
        self.assertQuerysetEqual(
            self.channel.categories.all(),
            ['<Category: National Literature>'])

    def test_name(self):
        category = Category.objects.create(
            name='National Literature',
            channel=self.channel)

        self.assertEqual(category.name, 'National Literature')

    def test_required_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create()

    def test_auto_generated_slug(self):
        category = Category.objects.create(
            name='National Literature',
            channel=self.channel)

        self.assertEqual(category.slug, 'national-literature')

    def test_duplicated_slugs(self):
        Category.objects.create(
            name='National Literature', channel=self.channel)
        category = Category.objects.create(
            name='National Literature',
            channel=self.channel)

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(category.slug, 'national-literature-2')

    def test_channel(self):
        category = Category.objects.create(
            name='National Literature',
            channel=self.channel)

        self.assertEqual(category.channel, self.channel)
        self.assertQuerysetEqual(
            self.channel.categories.all(),
            ['<Category: National Literature>'])

    def test_required_channel(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='National Literature')

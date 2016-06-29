from django.core.management import call_command, CommandError
from django.test import TestCase

from channel.models import Channel
from category.models import Category


class ImportCategoriesCommandTest(TestCase):
    def test_channel_argument_required(self):
        with self.assertRaises(CommandError):
            call_command(
                name='importcategories',
                categories_file='category/fixtures/empty.csv')
        self.assertEqual(Channel.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)

    def test_categories_file_argument_required(self):
        with self.assertRaises(CommandError):
            call_command(
                name='importcategories',
                channel='Lojas Americanas')
        self.assertEqual(Channel.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)

    def test_non_existent_file(self):
        with self.assertRaises(CommandError):
            call_command(
                name='importcategories',
                channel='Lojas Americanas',
                categories_file='category/fixtures/non-existent.csv')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 0)

    def test_channel(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/empty.csv')

        self.assertQuerysetEqual(
            Channel.objects.all(),
            ['<Channel: Lojas Americanas>'])

    def test_empty_file(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/empty.csv')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 0)

    def test_one_level_file(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/one_level.csv')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 3)
        self.assertQuerysetEqual(
            Category.objects.all(),
            ['<Category: Books>',
             '<Category: Games>',
             '<Category: Computers>'],
            ordered=False)

    def test_duplicated_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/duplicated_categories.csv')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 2)
        self.assertQuerysetEqual(
            Category.objects.all(),
            ['<Category: Books>',
             '<Category: Games>'],
            ordered=False)

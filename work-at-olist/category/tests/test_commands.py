from django.core.management import call_command, CommandError
from django.test import TestCase

from channel.models import Channel
from category.models import Category


class ImportCategoriesCommandTest(TestCase):
    def test_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/categories.csv')

        books = Category.objects.get(slug='books')
        games = Category.objects.get(slug='games')
        games2 = Category.objects.get(slug='games-2')
        xbox_360 = Category.objects.get(slug='xbox-360')
        games3 = Category.objects.get(slug='games-3')
        xbox_one = Category.objects.get(slug='xbox-one')
        computers = Category.objects.get(slug='computers')
        computers2 = Category.objects.get(slug='computers-2')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 23)
        self.assertQuerysetEqual(
            Category.objects.all(),
            ['<Category: Books>',
             '<Category: National Literature>',
             '<Category: Science Fiction>',
             '<Category: Fiction Fantastic>',
             '<Category: Foreign Literature>',
             '<Category: Computers>',
             '<Category: Applications>',
             '<Category: Database>',
             '<Category: Programming>',
             '<Category: Games>',
             '<Category: XBOX 360>',
             '<Category: Console>',
             '<Category: Games>',
             '<Category: Accessories>',
             '<Category: XBOX One>',
             '<Category: Console>',
             '<Category: Games>',
             '<Category: Accessories>',
             '<Category: Playstation 4>',
             '<Category: Computers>',
             '<Category: Notebooks>',
             '<Category: Tablets>',
             '<Category: Desktop>'],
            ordered=False)

        self.assertQuerysetEqual(
            books.subcategories.all(),
            ['<Category: National Literature>',
             '<Category: Foreign Literature>',
             '<Category: Computers>'],
            ordered=False)

        self.assertQuerysetEqual(
            games.subcategories.all(),
            ['<Category: XBOX 360>',
             '<Category: XBOX One>',
             '<Category: Playstation 4>'],
            ordered=False)
        self.assertEqual(games2.parent, xbox_360)
        self.assertEqual(games3.parent, xbox_one)

        self.assertEqual(computers.parent, books)
        self.assertQuerysetEqual(
            computers.subcategories.all(),
            ['<Category: Applications>',
             '<Category: Database>',
             '<Category: Programming>'],
            ordered=False)

        self.assertEqual(computers2.parent, None)
        self.assertQuerysetEqual(
            computers2.subcategories.all(),
            ['<Category: Notebooks>',
             '<Category: Tablets>',
             '<Category: Desktop>'],
            ordered=False)

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

    def test_two_levels_file(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/two_levels.csv')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 3)
        self.assertQuerysetEqual(
            Category.objects.all(),
            ['<Category: Books>',
             '<Category: National Literature>',
             '<Category: Science Fiction>'],
            ordered=False)

        books = Category.objects.get(slug='books')
        self.assertQuerysetEqual(
            books.subcategories.all(),
            ['<Category: National Literature>'])

        national_literature = Category.objects.get(slug='national-literature')
        self.assertQuerysetEqual(
            national_literature.subcategories.all(),
            ['<Category: Science Fiction>'])

    def test_duplicated_categories_with_diferent_levels(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file=(
                'category/fixtures/'
                'duplicated_categories_with_diferent_levels.csv'))

        games = Category.objects.get(slug='games')
        games2 = Category.objects.get(slug='games-2')
        xbox_360 = Category.objects.get(slug='xbox-360')
        games3 = Category.objects.get(slug='games-3')
        xbox_one = Category.objects.get(slug='xbox-one')

        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 10)
        self.assertQuerysetEqual(
            Category.objects.all(),
            ['<Category: Games>',
             '<Category: XBOX 360>',
             '<Category: Console>',
             '<Category: Games>',
             '<Category: Accessories>',
             '<Category: XBOX One>',
             '<Category: Console>',
             '<Category: Games>',
             '<Category: Accessories>',
             '<Category: Playstation 4>'],
            ordered=False)

        self.assertQuerysetEqual(
            games.subcategories.all(),
            ['<Category: XBOX 360>',
             '<Category: XBOX One>',
             '<Category: Playstation 4>'],
            ordered=False)
        self.assertEqual(games2.parent, xbox_360)
        self.assertEqual(games3.parent, xbox_one)

import csv

from django.core.management.base import BaseCommand, CommandError

from channel.models import Channel
from category.models import Category


class Command(BaseCommand):
    help = 'A helper command to import categories from a csv file.'

    def add_arguments(self, parser):
        parser.add_argument('--channel', help='The Channel`s name.')
        parser.add_argument(
            '--categories_file', help='Path to the categories csv file.')

    def handle(self, *args, **kwargs):
        self.channel = kwargs.get('channel')
        self.categories_file = kwargs.get('categories_file')

        if not self.channel:
            raise CommandError('The Channel is required.')

        if not self.categories_file:
            raise CommandError('The path of a Categories file is required.')

        self.import_categories()

    def import_categories(self):
        self.channel = self.get_or_create_channel(self.channel)

        try:
            with open(self.categories_file, 'r') as csv_file:
                csv_object = csv.reader(csv_file)
                for row in csv_object:
                    if csv_object.line_num == 1:
                        continue
                    self.create_category_from_row(row[0])
        except OSError as e:
            raise CommandError(e)

    def get_or_create_channel(self, name):
        channel, created = Channel.objects.get_or_create(name=name)
        return channel

    def get_or_create_category(self, name, parent=None):
        category, created = Category.objects.get_or_create(
            name=name,
            channel=self.channel)
        if parent:
            category.parents.add(parent)
        return category

    def create_category_from_row(self, row):
        categories = row.split(' / ')
        parent = None
        for category in categories:
            parent = self.get_or_create_category(
                name=category,
                parent=parent
            )

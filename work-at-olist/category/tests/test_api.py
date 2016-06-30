from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase


class ChannelTest(APITestCase):
    def test_detail_with_three_category(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/one_level.csv')

        url = reverse('category:detail', kwargs={
            'slug': 'books',
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': 'Books',
            'slug': 'books',
            'url': 'http://testserver/categories/books/',
            'channel': 'http://testserver/lojas-americanas/',
            'parent': None,
            'subcategories': [],
        })

    def test_detail_with_nested_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/two_levels.csv')

        url = reverse('category:detail', kwargs={
            'slug': 'national-literature',
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': 'National Literature',
            'slug': 'national-literature',
            'url': 'http://testserver/categories/national-literature/',
            'channel': 'http://testserver/lojas-americanas/',
            'parent': 'http://testserver/categories/books/',
            'subcategories': [{
                'name': 'Science Fiction',
                'slug': 'science-fiction',
                'url': 'http://testserver/categories/science-fiction/',
                'channel': 'http://testserver/lojas-americanas/',
                'parent': 'http://testserver/categories/national-literature/',
                'subcategories': [],
            }],
        })

from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase


class ChannelTest(APITestCase):
    def tst_empty_list(self):
        url = reverse('channel:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_without_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/empty.csv')

        url = reverse('channel:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'categories': []
        }])

    def test_list_with_three_category(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/one_level.csv')

        url = reverse('channel:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'categories': [{
                'id': 1,
                'name': 'Books',
                'slug': 'books',
                'channel': 1,
                'parents': [],
                'subcategories': [],
            }, {
                'id': 2,
                'name': 'Games',
                'slug': 'games',
                'channel': 1,
                'parents': [],
                'subcategories': [],
            }, {
                'id': 3,
                'name': 'Computers',
                'slug': 'computers',
                'channel': 1,
                'parents': [],
                'subcategories': [],
            }]
        }])

    def test_list_with_nested_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/two_levels.csv')

        url = reverse('channel:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'categories': [{
                'id': 1,
                'parents': [],
                'subcategories': [2],
                'name': 'Books',
                'slug': 'books',
                'channel': 1
            }, {
                'id': 2,
                'parents': [1],
                'subcategories': [3],
                'name': 'National Literature',
                'slug': 'national-literature',
                'channel': 1
            }, {
                'id': 3,
                'parents': [2],
                'subcategories': [],
                'name': 'Science Fiction',
                'slug': 'science-fiction',
                'channel': 1
            }]
        }])

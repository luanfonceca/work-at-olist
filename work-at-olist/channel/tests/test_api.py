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

    def test_list(self):
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
            'url': 'http://testserver/channels/lojas-americanas/'
        }])

    def test_detail_without_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/empty.csv')

        url = reverse('channel:detail', kwargs={'slug': 'lojas-americanas'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/channels/lojas-americanas/',
            'categories': []
        })

    def test_detail_with_three_category(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/one_level.csv')

        url = reverse('channel:detail', kwargs={'slug': 'lojas-americanas'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/channels/lojas-americanas/',
            'categories': [{
                'id': 1,
                'name': 'Books',
                'slug': 'books',
                'url': 'http://testserver/categories/books/',
                'channel': 'http://testserver/channels/lojas-americanas/',
                'parents': [],
                'subcategories': [],
            }, {
                'id': 2,
                'name': 'Games',
                'slug': 'games',
                'url': 'http://testserver/categories/games/',
                'channel': 'http://testserver/channels/lojas-americanas/',
                'parents': [],
                'subcategories': [],
            }, {
                'id': 3,
                'name': 'Computers',
                'slug': 'computers',
                'url': 'http://testserver/categories/computers/',
                'channel': 'http://testserver/channels/lojas-americanas/',
                'parents': [],
                'subcategories': [],
            }]
        })

    def test_detail_with_nested_categories(self):
        call_command(
            name='importcategories',
            channel='Lojas Americanas',
            categories_file='category/fixtures/two_levels.csv')

        url = reverse('channel:detail', kwargs={'slug': 'lojas-americanas'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': 1,
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/channels/lojas-americanas/',
            'categories': [{
                'id': 1,
                'parents': [],
                'subcategories': [
                    'http://testserver/categories/national-literature/'
                ],
                'name': 'Books',
                'slug': 'books',
                'url': 'http://testserver/categories/books/',
                'channel': 'http://testserver/channels/lojas-americanas/'
            }, {
                'id': 2,
                'parents': [
                    'http://testserver/categories/books/'
                ],
                'subcategories': [
                    'http://testserver/categories/science-fiction/'
                ],
                'name': 'National Literature',
                'slug': 'national-literature',
                'url': 'http://testserver/categories/national-literature/',
                'channel': 'http://testserver/channels/lojas-americanas/'
            }, {
                'id': 3,
                'parents': [
                    'http://testserver/categories/national-literature/'
                ],
                'subcategories': [],
                'name': 'Science Fiction',
                'slug': 'science-fiction',
                'url': 'http://testserver/categories/science-fiction/',
                'channel': 'http://testserver/channels/lojas-americanas/'
            }]
        })

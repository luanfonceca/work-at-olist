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
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/lojas-americanas/'
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
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/lojas-americanas/',
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
            'url': 'http://testserver/lojas-americanas/',
            'slug': 'lojas-americanas',
            'name': 'Lojas Americanas',
            'categories': [{
                'name': 'Books',
                'slug': 'books',
                'url': 'http://testserver/categories/books/',
            }, {
                'name': 'Games',
                'slug': 'games',
                'url': 'http://testserver/categories/games/',
            }, {
                'name': 'Computers',
                'slug': 'computers',
                'url': 'http://testserver/categories/computers/',
            }],
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
            'name': 'Lojas Americanas',
            'slug': 'lojas-americanas',
            'url': 'http://testserver/lojas-americanas/',
            'categories': [{
                'name': 'Books',
                'slug': 'books',
                'url': 'http://testserver/categories/books/',
            }]
        })

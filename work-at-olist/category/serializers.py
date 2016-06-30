from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from category.models import Category


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='category:detail',
        lookup_field='slug',
        read_only=True,
    )

    class Meta:
        model = Category
        fields = ('name', 'slug', 'url')


class CategorySerializer(CategoryListSerializer):
    subcategories = RecursiveField(many=True, allow_null=True)

    class Meta:
        model = Category
        extra_kwargs = {
            'channel': {
                'view_name': 'channel:detail',
                'lookup_field': 'slug',
            },
            'parent': {
                'view_name': 'category:detail',
                'lookup_field': 'slug',
            }
        }

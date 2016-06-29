from rest_framework import generics

from category.models import Category
from category import serializers


class CategoryMixin(object):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetail(CategoryMixin, generics.RetrieveAPIView):
    lookup_field = 'slug'

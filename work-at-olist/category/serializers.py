from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    channel = serializers.HyperlinkedRelatedField(
        view_name='channel:detail',
        lookup_field='slug',
        read_only=True,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='category:detail',
        lookup_field='slug'
    )
    parents = serializers.HyperlinkedRelatedField(
        view_name='category:detail',
        lookup_field='slug',
        many=True,
        read_only=True,
    )
    subcategories = serializers.HyperlinkedRelatedField(
        view_name='category:detail',
        lookup_field='slug',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Category

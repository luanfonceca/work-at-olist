from rest_framework import serializers

from channel.models import Channel
from category.serializers import CategoryListSerializer


class ChannelListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='channel:detail',
        lookup_field='slug'
    )

    class Meta:
        model = Channel


class ChannelSerializer(ChannelListSerializer):
    categories = CategoryListSerializer(
        source='get_first_level_categories',
        many=True,
    )

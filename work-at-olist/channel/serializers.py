from rest_framework import serializers

from channel.models import Channel
from category.serializers import CategorySerializer


class ChannelListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='channel:detail',
        lookup_field='slug'
    )

    class Meta:
        model = Channel


class ChannelSerializer(ChannelListSerializer):
    categories = CategorySerializer(many=True)

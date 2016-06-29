from rest_framework import serializers

from channel.models import Channel
from category.serializers import CategorySerializer


class ChannelSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Channel

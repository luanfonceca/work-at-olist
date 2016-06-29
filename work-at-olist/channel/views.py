from rest_framework import generics

from channel.models import Channel
from channel import serializers


class ChannelMixin(object):
    queryset = Channel.objects.all()
    serializer_class = serializers.ChannelSerializer


class ChannelList(ChannelMixin, generics.ListAPIView):
    serializer_class = serializers.ChannelListSerializer


class ChannelDetail(ChannelMixin, generics.RetrieveAPIView):
    lookup_field = 'slug'

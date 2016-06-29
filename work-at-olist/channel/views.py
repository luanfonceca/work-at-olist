from rest_framework import generics

from channel.models import Channel
from channel import serializers


class ChannelMixin(object):
    queryset = Channel.objects.all()
    serializer_class = serializers.ChannelSerializer


class ChannelList(ChannelMixin, generics.ListAPIView):
    pass

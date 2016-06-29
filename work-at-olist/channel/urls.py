from django.conf.urls import url

from channel import views

urlpatterns = [
    url(regex=r'^$',
        view=views.ChannelList.as_view(),
        name='list'),
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.ChannelDetail.as_view(),
        name='detail'),
]

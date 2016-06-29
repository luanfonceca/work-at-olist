from django.conf.urls import url

from channel import views

urlpatterns = [
    url(regex=r'^$',
        view=views.ChannelList.as_view(),
        name='list'),
]

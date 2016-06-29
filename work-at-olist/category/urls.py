from django.conf.urls import url

from category import views

urlpatterns = [
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=views.CategoryDetail.as_view(),
        name='detail'),
]

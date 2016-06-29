from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Local apps
    url(r'^channels/', include('channel.urls', namespace='channel')),
    url(r'^categories/', include('category.urls', namespace='category')),
]

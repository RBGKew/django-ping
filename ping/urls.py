from django.conf.urls import include, url
from ping.views import status

urlpatterns = [
    url(r'^$', status, name='status'),
]

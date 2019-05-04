from frontend.views import index
from django.conf.urls import url, include

app_name = 'frontend'

urlpatterns = [
    url(r'^$', index, name='index'),
]

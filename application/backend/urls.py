from django.conf.urls import url, include
from backend.views.example import example_view

app_name = 'backend'

urlpatterns = [
    url(r'example', example_view, name='example'),
]

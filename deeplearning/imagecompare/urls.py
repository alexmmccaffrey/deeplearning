from .views import ImageView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ImageView.upload, name='upload'),
]
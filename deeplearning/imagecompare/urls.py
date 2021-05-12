from django.urls import include, path
from rest_framework import routers
from .views import NameView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', NameView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
from django.urls import path

from Home.views import Dashboard

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
]

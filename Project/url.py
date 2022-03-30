from django.urls import path
from .views import CreateProject

urlpatterns = [
    path('create_project/', CreateProject.as_view(), name='create_project'),
]

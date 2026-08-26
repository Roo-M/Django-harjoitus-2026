from django.urls import path
from . import views

urlpatterns = [
    path('robotit/', views.robotit, name='robotit'),
]
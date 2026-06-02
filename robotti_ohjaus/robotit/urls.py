from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('robotit/', views.robotit, name='robotit'),
    path('robotit/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
]
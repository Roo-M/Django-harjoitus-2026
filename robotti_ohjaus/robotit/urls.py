from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'robotit', views.RobottiViewSet)

urlpatterns = [
    #path('robotit/', views.robotit, name='robotit'),
    path('', include(router.urls)), 
]

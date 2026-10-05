from tempfile import template

from django.http import HttpResponse
from django.template import loader

from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from .models import Robotti
from .serializers import RobottiSerializer


def robotit(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

def robotit_list(request):
   template = loader.get_template('robotit_list.html')
   robotit = Robotti.objects.all()
   return HttpResponse(template.render({'robotit': robotit}))

class RobottiViewSet(viewsets.ModelViewSet):
    queryset = Robotti.objects.all()
    serializer_class = RobottiSerializer

# class TaskListAPI(generics.ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
 
#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff or user.is_superuser:
#             return Task.objects.all()
#         return Task.objects.filter(user=user)
 
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
 
# class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
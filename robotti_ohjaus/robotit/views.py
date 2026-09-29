from tempfile import template

from django.http import HttpResponse
from django.template import loader

from rest_framework import viewsets
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
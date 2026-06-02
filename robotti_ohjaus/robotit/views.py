from django.http import HttpResponse
from django.template import loader
from .models import Robotti

def robotit(request):
  myrobotit = Robotti.objects.all().values()
  template = loader.get_template('all_robotit.html')
  context = {
    'myrobotit': myrobotit,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  myrobotit = Robotti.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'myrobotit': myrobotit,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'marjoja': ['Mansikka', 'Mustikka', 'Tyrni'],   
  }
  return HttpResponse(template.render(context, request))
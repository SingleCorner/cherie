from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def test(request):
  return HttpResponse("hello world")



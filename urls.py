"""cherie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^$', views.test),
]

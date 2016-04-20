"""cherie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""
from django.conf.urls import url
from common import views

urlpatterns = [
    url(r'^$', views.user_dashboard),
    url(r'^signin$', views.user_signin),
    url(r'^signout$', views.user_signout),
    url(r'^signup$', views.user_signup),
    url(r'^user/(?P<module>.*)/(?P<sid>.*)$', views.user_module),
    url(r'^admin/(?P<module>.*)/(?P<sid>.*)$', views.admin_module),
    url(r'^exec$', views.data_execute),
    url(r'^api$', views.rpc_api),
    url(r'^apitest$', views.rpc_api_test),
    url(r'^hmc_demo',views.hmc_demo),
]

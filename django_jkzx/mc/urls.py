# _*_coding: utf-8_*_
__author__ = 'Xu dr'

from django.conf.urls import url
from django.contrib import admin
import views
urlpatterns = [
    url(r'^dashboard/$', views.dashboard),
    url(r'^schedule/overview/$', views.overview, name='overview'),
    url(r'^schedule/overview/(\d+)/$', views.detail, name='detail'),
    url(r'^schedule/test/$', views.test, name='test'),
    url(r'^report/$', views.sch_report, name='sch_report'),
    url(r'^report_test/$', views.report_test, name='report_test'),
    # url(r'^business/(?P<appName>\w+)/$', views.business, name='business'),
    # url(r'^schedule/overview/schedule_list/$', views.schedule_list),
    #url(r'^customers/$', views.customers),
]
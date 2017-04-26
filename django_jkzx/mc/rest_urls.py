# _*_coding: utf-8_*_
__author__ = 'Xu dr'


from django.conf.urls import url, include
from rest_framework import routers
from mc import rest_views

router = routers.DefaultRouter()
router.register(r'users', rest_views.UserViewSet)
router.register(r'groups', rest_views.GroupViewSet)
router.register(r'schedule', rest_views.ScheduleViewSet)
router.register(r'idc', rest_views.IDCViewSet)
router.register(r'nic', rest_views.NICViewSet)
router.register(r'ram', rest_views.RAMViewSet)
router.register(r'personInfo', rest_views.PersonalInfoViewSet)
router.register(r'tag', rest_views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'sch_list/$', rest_views.scheduleList),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
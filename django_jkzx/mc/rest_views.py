# _*_coding: utf-8_*_
__author__ = 'Xu dr'

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, permissions
from mc.serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request

from mc import models



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = ScheduleSerializer

class IDCViewSet(viewsets.ModelViewSet):
    queryset = models.IDC.objects.all()
    serializer_class = IDCSerializer

class NICViewSet(viewsets.ModelViewSet):
    queryset = models.NIC.objects.all()
    serializer_class = NICSerializer

class RAMViewSet(viewsets.ModelViewSet):
    queryset = models.RAM.objects.all()
    serializer_class = RAMSerializer

class PersonalInfoViewSet(viewsets.ModelViewSet):
    queryset = models.PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['GET', 'POST'])
def scheduleList(request):
    serializer_context = {
        'request': Request(request),
    }
    if request.method == 'GET':
        sch_list = models.Schedule.objects.all()
        serializer = ScheduleSerializer(instance=sch_list, context=serializer_context, many=True)
        return Response(serializer.data)
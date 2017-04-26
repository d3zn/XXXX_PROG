# _*_coding: utf-8_*_
__author__ = 'Xu dr'

from django.contrib.auth.models import User, Group
from mc import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    # name = serializers.ReadOnlyField(source='idc.name')

    class Meta:
        model = models.Schedule
        # depth = 1
        fields = ('url','hostname', 'relaynum', 'mem_size', 'dns', 'idc', 'status', 'admin')


class IDCSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.IDC
        fields = ('idc_name', 'address', 'contact')


class NICSerializer(serializers.HyperlinkedModelSerializer):
    # queryset = models.NIC.objects.all()
    hostname = serializers.StringRelatedField()
    class Meta:
        model = models.NIC
        # depth = 0
        fields = ('url', 'hostname', 'nic_name', 'macaddr', 'ipaddr', 'netmask', 'memo', 'update_date')


class RAMSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.RAM
        fields = ('hostname', 'type', 'slot', 'capacity', 'manufacturer', 'update_date')


class PersonalInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PersonalInfo
        fields = ('name', 'department', 'tel', 'qq', 'email')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name', 'creater')
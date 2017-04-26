# _*_coding: utf-8_*_
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Schedule(models.Model):
    hostname = models.CharField(u"主机名", unique=True, max_length=64,)
    relaynum = models.CharField(u"中继号", max_length=64, null=True, blank=True)

    mem_size = models.CharField(u"内存大小(MB)", max_length=64, blank=True, null=True)

    dns = models.CharField(u"DNS", max_length=64, blank=True)

    os_type = models.CharField(u"系统类型", max_length=64)
    os_version = models.CharField(u"系统版本", max_length=64)
    os_release = models.CharField(u"系统内核", max_length=64)

    status_choices = (
        (0, u"在线"),
        (1, u"下线"),
        (2, u"未知"),
        (3, u"故障"),
        (4, u"备用"),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    idc = models.ForeignKey('IDC', verbose_name=u"IDC机房", null=True, blank=True)
    admin = models.ForeignKey('PersonalInfo', verbose_name=u"负责人", null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    memo = models.CharField(u"备注", max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return self.hostname

    class Meta:
        verbose_name = u"拨号器"
        verbose_name_plural = u"拨号器"

# class Operator(models.Model):
#     name =

class IDC(models.Model):
    idc_name = models.CharField(u"机房名称", max_length=64, unique=True)
    address = models.CharField(u"地址", max_length=128, unique=True)
    contact = models.CharField(u"联系方式", max_length=64, blank=True, null=True)
    memo = models.CharField(u"备注", max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.idc_name

    class Meta:
        verbose_name = u"机房"
        verbose_name_plural = u"机房"


class NIC(models.Model):
    hostname = models.ForeignKey('Schedule', verbose_name=u"主机")
    nic_name = models.CharField(u"网卡名", max_length=64, blank=True, null=True)
    macaddr = models.CharField(u"MAC地址", max_length=128, unique=True)
    ipaddr = models.GenericIPAddressField(u"IP地址", blank=True, null=True, unique=True)
    netmask = models.GenericIPAddressField(u"子网掩码", blank=True, null=True)
    memo = models.CharField(u"备注", max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return "<%s, %s>" %(self.hostname , self.nic_name)
    class Meta:
        verbose_name = u"网卡"
        verbose_name_plural = u"网卡"
        unique_together = ('hostname', 'nic_name')


class CPU(models.Model):
    hostname = models.OneToOneField('Schedule', verbose_name=u"主机")
    cpu_model = models.CharField(u"CPU型号", max_length=128)
    cpu_count = models.SmallIntegerField(u"物理CPU个数")
    cpu_core = models.SmallIntegerField(u"CPU核数")
    memo = models.TextField(u"备注", null=True, blank=True)
    create_data = models.DateTimeField(blank=True,auto_now_add=True)
    update_data = models.DateTimeField(blank=True,auto_now=True)

    def __unicode__(self):
        return "<%s>" % self.hostname


    class Meta:
        verbose_name = u"CPU部件"
        verbose_name_plural = u"CPU部件"


class RAM(models.Model):
    hostname = models.ForeignKey('Schedule', verbose_name=u"主机")
    type = models.CharField(u"内存型号", max_length=128)
    slot = models.CharField(u"插槽", max_length=64)
    capacity = models.IntegerField(u"内存大小（MB）")
    manufacturer = models.CharField(u"生产厂商", max_length=64, blank=True, null=True)
    memo = models.CharField(u"备注", max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    def __unicode__(self):
        return "<%s, %s, %s>" %(self.hostname, self.slot, self.capacity)
    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAM'
        unique_together = ('hostname', 'slot')


class PersonalInfo(models.Model):
    name = models.CharField(u"姓名",max_length=32)
    department = models.CharField(u"部门", max_length=32)
    tel = models.BigIntegerField(u"联系方式")
    qq = models.BigIntegerField(u"QQ号")
    email = models.EmailField(u"邮箱地址")

    def __unicode__(self):
        return '<%s %s>' %(self.name, self.department)

    class Meta:
        verbose_name = u"人员信息"
        verbose_name_plural = u"人员信息"


class Tag(models.Model):
    name = models.CharField('Tag name',max_length=32,unique=True )
    creater = models.ForeignKey('PersonalInfo')
    create_date = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"标签"
        verbose_name_plural = u"标签"


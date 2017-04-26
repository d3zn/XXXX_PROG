#!/usr/bin/env python
# _*_coding: utf-8_*_
__author__ = 'Xu dr'

import json
from mc import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class SchHandler(object):
    def __init__(self,request):
        self.request = request
        self.base_fields = ['hostname','isNew']
        self.clean_data = None
        self.sch_obj = None

        self.response = {
            'error': [],
            'info': [],
            'warning': []
        }


    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def data_is_valid(self):
        data = self.request.POST.get("sch_data")

        if data:
            try:
                data = json.loads(data)
                self.base_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error','ScheduleDataInvalid', str(e))
                return False

    def base_check(self, data):
        for field in self.base_fields:
            if field not in data:
                self.response_msg('error', 'MandatoryCheckFailed',
                                  "The field [%s] is mandatory and not provided in your reporting data" % field)
            else:
                if self.response['error']: return False


    def data_inject(self):
        if self.__is_new_asset():
            # create sch_info
            self._create_sch()

        else:
            # update sch_info
            self._update_sch()

    def __is_new_asset(self):
        # isNew = self.clean_data['isNew']

        try:
            self.sch_obj = models.Schedule.objects.get(hostname=self.clean_data['hostname'])

        except ObjectDoesNotExist as e:
            self.response_msg('warning', 'ScheduleDataInvalid',
                              "Cannot find Schedule object in DB by using hostname [%s], the object will be created!" % self.clean_data['hostname'])

        if not hasattr(self.sch_obj, 'hostname'):
            return True
        else:
            return False

    def _create_sch(self):

        self.__create_sch_info()
        self.__create_cpu_info()
        self.__create_ram_info()
        self.__create_nic_info()
        print('create')

    def _update_sch(self):
        self.__update_sch_info()
        self.__update_cpu_info()
        self.__update_ram_info()
        self.__update_nic_info()
        print('update')

    def __create_sch_info(self,):
        try:
            if not len(self.response['error']):
                data_set = {
                    'hostname': self.clean_data.get('hostname'),
                    'os_version': self.clean_data.get('os')[0].get('os_version'),
                    'os_type': self.clean_data.get('os')[0].get('os_type'),
                    'os_release': self.clean_data.get('os')[0].get('os_release'),
                    'mem_size': self.clean_data.get('mem_size'),
                }
                obj = models.Schedule(**data_set)
                obj.save()
                self.sch_obj = models.Schedule.objects.get(hostname=self.clean_data.get('hostname'))
        except Exception as e:
            self.response_msg('error', 'ObjectCreationException', 'Object [sch] %s' % str(e))

    def __create_cpu_info(self):
        try:
            if not len(self.response['error']):
                data_set = {
                    'hostname': self.sch_obj,
                    'cpu_model': self.clean_data.get('cpu')[0].get('cpu_model'),
                    'cpu_count': int(self.clean_data.get('cpu')[0].get('cpu_count')),
                    'cpu_core': int(self.clean_data.get('cpu')[0].get('cpu_core'))
                }
                obj = models.CPU(**data_set)
                obj.save()
                return obj
        except Exception as e:
            self.response_msg('error', 'ObjectCreationException', 'Object [cpu] %s' % str(e))

    def __create_ram_info(self):
        mem_info = self.clean_data.get('mem')
        for mem_item in mem_info:
            try:
                if not len(self.response['error']):
                    data_set = {
                        'hostname': self.sch_obj,
                        'type': mem_item.get('type'),
                        'slot': mem_item.get('slot'),
                        'capacity': mem_item.get('capacity'),
                        'manufacturer': mem_item.get('manufacturer')
                    }
                    obj = models.RAM(**data_set)
                    obj.save()
            except Exception as e:
                self.response_msg('error', 'ObjectCreationException', 'Object [ram] %s' % str(e))

    def __create_nic_info(self):
        nic_info = self.clean_data.get('nic')
        for nic_item in nic_info:
            try:
                if not len(self.response['error']):
                    data_set = {
                        'hostname': self.sch_obj,
                        'macaddr': nic_item.get('macaddress'),
                        'nic_name': nic_item.get('name'),
                        'netmask': nic_item.get('netmask'),
                        'ipaddr': nic_item.get('ipaddress')
                    }
                    obj = models.NIC(**data_set)
                    obj.save()
            except Exception as e:
                self.response_msg('error', 'ObjectCreationException', 'Object [nic] %s' % str(e))

    def __update_sch_info(self):
        try:
            if not len(self.response['error']):
                data_set = {
                    'hostname': self.sch_obj.hostname,
                    'os_version': self.clean_data.get('os')[0].get('os_version'),
                    'os_type': self.clean_data.get('os')[0].get('os_type'),
                    'os_release': self.clean_data.get('os')[0].get('os_release'),
                    'mem_size': self.clean_data.get('mem_size'),
                    'update_date': timezone.now()
                }
                models.Schedule.objects.filter(id=self.sch_obj.id).update(**data_set)


        except Exception as e:
            self.response_msg('error', 'ObjectUpdateException', 'Object [sch] %s' % str(e))

    def __update_cpu_info(self):
        try:
            if not len(self.response['error']):
                data_set = {
                    'hostname': self.sch_obj,
                    'cpu_model': self.clean_data.get('cpu')[0].get('cpu_model'),
                    'cpu_count': int(self.clean_data.get('cpu')[0].get('cpu_count')),
                    'cpu_core': int(self.clean_data.get('cpu')[0].get('cpu_core'))
                }
                print(data_set)
                models.CPU.objects.filter(hostname=self.sch_obj.id).update(**data_set)


        except Exception as e:
            self.response_msg('error', 'ObjectUpdateException', 'Object [sch] %s' % str(e))

    def __update_ram_info(self):
        data_source = self.clean_data.get('mem')
        # print(data_source)
        ram_obj = models.RAM.objects.filter(hostname=self.sch_obj.id)

        slot_list = []
        """find reporting data but not in db, create.
           find reporting data in db, update.
        """
        for ram_data in data_source:
            slot_list.append(ram_data.get('slot'))
            get_slot = ram_data.get('slot')

            data_set = {
                'hostname': self.sch_obj,
                'type': ram_data.get('type'),
                'capacity': ram_data.get('capacity'),
                'manufacturer': ram_data.get('manufacturer')
            }
            # print(data_set)
            try:
                if ram_obj.filter(slot=get_slot):
                    data_set['update_date'] = timezone.now()
                    models.RAM.objects.filter(hostname=self.sch_obj.id, slot=get_slot).update(**data_set)
                else:
                    data_set['slot'] = ram_data.get('slot')
                    print(data_set)
                    obj = models.RAM(**data_set)
                    obj.save()
            except Exception as e:
                self.response_msg('error', 'ObjectUpdateException', 'Object [ram] %s' % str(e))

        """find value of ram in db but not in reporting data, delete."""
        for ram_instance in ram_obj:
            print(ram_instance)
            val_from_db = getattr(ram_instance,'slot')
            if val_from_db not in slot_list:
                ram_instance.delete()

    def __update_nic_info(self):
        data_source = self.clean_data.get('nic')

        nic_obj = models.NIC.objects.filter(hostname=self.sch_obj.id)

        nic_mac_list = []
        """find reporting data but not in db, create.
           find reporting data in db, update.
        """
        for nic_data in data_source:
            nic_mac_list.append(nic_data.get('macaddress'))
            get_macaddr = nic_data.get('macaddress')

            data_set = {
                'hostname': self.sch_obj,
                'nic_name': nic_data.get('name'),
                'netmask': nic_data.get('netmask'),
                'ipaddr': nic_data.get('ipaddress')
            }
            # print(data_set)
            try:
                if nic_obj.filter(macaddr=get_macaddr):
                    data_set['update_date'] = timezone.now()
                    models.NIC.objects.filter(hostname=self.sch_obj.id, macaddr=get_macaddr).update(**data_set)
                else:
                    data_set['macaddr'] = nic_data.get('macaddress')
                    print(data_set)
                    obj = models.NIC(**data_set)
                    obj.save()
            except Exception as e:
                self.response_msg('error', 'ObjectUpdateException', 'Object [nic] %s' % str(e))

        """find value of ram in db but not in reporting data, delete."""
        for nic_instance in nic_obj:
            print(nic_instance)
            val_from_db = getattr(nic_instance,'macaddr')
            if val_from_db not in nic_mac_list:
                ram_instance.delete()




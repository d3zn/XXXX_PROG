# _*_coding: utf-8_*_
__author__ = 'Xu dr'


from celery import shared_task
from django_jkzx.celeryapp import app
from subprocess import Popen, PIPE

@shared_task()
def upWav(upWavName):
    res_obj = Popen('python /root/test.py %s' % upWavName, shell=True, stdout=PIPE)
    res = res_obj.stdout.read()
    print(res)
    msg = upWavName

    return msg
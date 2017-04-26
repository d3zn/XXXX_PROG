# coding: utf-8
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, Http404
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from mc import models
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import mc.tasks as schTasks
import json
from mc import handler
# Create your views here.




def index(request):

    return HttpResponseRedirect('mc/dashboard/')



def dashboard(request):

    return render(request, 'mc/dashboard.html')



def overview(request):
    bhq_obj = models.Schedule.objects.all()
    titie = u"拨号器概要"
    return render(request, 'mc/schedule/schedule_overview.html', {'bhq_obj': bhq_obj, 'title': titie, })

def detail(request,bhq_id):
    if request.method == 'GET':
        try:
            schedule_obj = models.Schedule.objects.get(id=bhq_id)

        except ObjectDoesNotExist as e:
            return render(request, 'mc/schedule/schedule_detail.html', {'error': e})

        print(schedule_obj.id, schedule_obj)
        return render(request, 'mc/schedule/schedule_detail.html', {'schedule_obj': schedule_obj})

@csrf_exempt
def test(request):
    msg = 'ok'
    if request.is_ajax() and request.method == 'POST':
        reqList = request.POST.keys()
        if len(reqList) == 1:
            req = reqList[0]
            print(req)
            if req == 'upWavName':
                wavlist = request.POST[req].split('\r\n')

                for wav in wavlist:
                    if wav.strip() != '':
                        schTasks.upWav.delay(wav)
                return HttpResponse(wavlist)
            elif req == 'downWavName':
                arg = request.POST[req].split('\r\n')
                return HttpResponse(arg)
        else:
            return HttpResponse('error')

    return render(request, 'mc/schedule/schdeule_ops.html')

@csrf_exempt
def sch_report(request):
    if request.method == 'POST':
        sch_handler = handler.SchHandler(request)
        if sch_handler.data_is_valid():
            sch_handler.data_inject()

            return HttpResponse(json.dumps(sch_handler.response))
            #return HttpResponse(request.POST.get('sch_data'))
        else:
            return HttpResponse(json.dumps(sch_handler.response))
    else:
        raise Http404



def report_test(request):
    return render(request, 'mc/report_test.html')





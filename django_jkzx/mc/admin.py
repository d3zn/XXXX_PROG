from django.contrib import admin
from mc import models
# Register your models here.

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('hostname',
                    'relaynum',
                    'mem_size',
                    'os_type',
                    'os_version',
                    'os_release',
                    'dns',
                    'status'
    )


admin.site.register(models.Schedule,ScheduleAdmin)
admin.site.register(models.NIC)
admin.site.register(models.IDC)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.PersonalInfo)
admin.site.register(models.Tag)



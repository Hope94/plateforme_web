from django.contrib import admin
from main.models import Apk,Extract,Feature,Dataset,PermissionAPI,SuspiciousAPI
# Register your models here.

admin.site.register(Apk)
admin.site.register(Extract)
admin.site.register(Feature)
admin.site.register(Dataset)
admin.site.register(PermissionAPI)
admin.site.register(SuspiciousAPI)


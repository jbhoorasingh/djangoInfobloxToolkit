from django.contrib import admin
from .models import Datacenter, DatacenterNetworkBlock, Network

class DatacenterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class NetworkAdmin(admin.ModelAdmin):
    list_display = ['application', 'application_environment', 'datacenter_name','network', 'created_by']
    list_filter = ('application_environment', 'datacenter_name', 'created_by')


admin.site.register(Datacenter, DatacenterAdmin)
admin.site.register(DatacenterNetworkBlock)
admin.site.register(Network, NetworkAdmin)
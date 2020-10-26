from django.conf.urls import url
from . import views

urlpatterns = [
    #main index /components
    url(r'^index/(?P<ws_name>\w+)/(?P<release>\w+)/$', views.index, name='index'),

    url(r'^addcomponent/$', views.addcomponent, name='addcomponent'),
    
    #url(r'^addcomponent/allcomponents/$', views.addallcomponent, name='addallcomponent'),

    url(r'^modify/(?P<componentId>[0-9]+)/$', views.modify, name='modify'),

    url(r'^delete/(?P<componentId>\d+)/$', views.delete, name='delete'),

    url(r'^hookdisc/(?P<componentId>[0-9]+)/$', views.discoveryHookList, name='discoveryHookList'),

    url(r'^hookdisc/(?P<discoveryHookId>[0-9]+)$', views.discoveryHookEdit, name='discoveryHookEdit'),

    url(r'^hookdisc/$', views.discoveryHookEdit, name='discoveryHookEdit'),

    url(r'^hookdisc/(?P<componentId>[0-9]+)/(?P<discoveryHookId>[0-9]+)/delete$', views.discoveryHookDelete, name='discoveryHookDelete'),

    url(r'^hookupdt/(?P<componentId>[0-9]+)/$', views.updateHookList, name='updateHookList'),

    url(r'^hookupdt/(?P<componentId>[0-9]+)/(?P<updateHookId>[0-9]+)$', views.updateHookEdit, name='updateHookEdit'),

    url(r'^hookupdt/(?P<componentId>[0-9]+)/(?P<updateHookId>[0-9]+)/delete$', views.updateHookDelete, name='updateHookDelete'),

    url(r'^popdb/$', views.popdb, name='popdb'),

    url(r'^listplatform/$', views.listplatform, name='listplatform'),

    url(r'^listplatform/add/$', views.platformadd, name='platformadd'),

    url(r'^listplatform/delete/$', views.platformDelete, name='platformDelete'),

    url(r'^listplatform/edit/', views.platformEdit, name='platformEdit'),

    url(r'^listrelease/$', views.listrelease, name='listrelease'),

    url(r'^listrelease/add/$', views.releaseadd, name='releaseadd'),

    url(r'^listrelease/delete/$', views.releaseDelete, name='releaseDelete'),

    url(r'^listrelease/edit/', views.releaseEdit, name='releaseEdit'),

    url(r'^toollist/$', views.toollist, name='toollist'),

    url(r'^listtool/delete/(?P<toolid>[0-9]+)$', views.toolDelete, name='toolDelete'),

    url(r'^listtool/edit/(?P<toolid>[0-9]+)$', views.toolEdit, name='toolEdit'),

    url(r'^addtool/$', views.addtool, name='addtool'),

    url(r'^addtool/(?P<vendorsel>\w+.*)$', views.addtool, name='addtool'),
    
    url(r'^addtool/(?P<tool_id>[0-9]+)$', views.addtool, name='addtool'),

    url(r'^firmwarelist/$', views.firmwarelist, name='firmwarelist'),

    url(r'^listfirmware/delete/(?P<firmwareid>[0-9]+)$', views.firmwareDelete, name='firmwareDelete'),

    url(r'^listfirmware/edit/(?P<firmwareid>[0-9]+)$', views.firmwareEdit, name='firmwareEdit'),

    url(r'^addfirmware/$', views.addfirmware, name='addfirmware'),
    
    url(r'^addfirmware/(?P<firmware_id>[0-9]+)$', views.addfirmware, name='addfirmware'),
    
    url(r'^hooks/$', views.hooks, name='hooks'),

    url(r'^psuindex/$', views.psuindex, name='psuindex'),
    
    url(r'^addpsu/$', views.addpsu, name='addpsu'),

    url(r'^cpuindex/$', views.cpuindex, name='cpuindex'),

    url(r'^adddrive/$', views.adddrive, name='adddrive'),

    url(r'^addcpu/$', views.addcpu, name='addcpu'),

    url(r'^memoryindex/$', views.memoryindex, name='memoryindex'),

    url(r'^addmemory/$', views.addmemory, name='addmemory'),

    url(r'^addcomponent/addpolicy$', views.addpolicy, name='addpolicy'),

    url(r'^modifypsu/(?P<psuId>[0-9]+)/$', views.modifypsu, name='modifypsu'),

    url(r'^deletepsu/(?P<psuId>\d+)/$', views.deletepsu, name='deletepsu'),

    url(r'^modifycpu/(?P<cpuId>[0-9]+)/$', views.modifycpu, name='modifycpu'),

    url(r'^deletecpu/(?P<cpuId>\d+)/$', views.deletecpu, name='deletecpu'),

    url(r'^modifymemory/(?P<memoryId>[0-9]+)/$', views.modifymemory, name='modifymemory'),

    url(r'^deletememory/(?P<memoryId>\d+)/$', views.deletememory, name='deletememory'),

    url(r'^storageindex/$', views.storageindex, name='storageindex'),

    url(r'^addstorage/$', views.addstorage, name='addstorage'),

    url(r'^modifystorage/(?P<storageId>[0-9]+)/$', views.modifystorage, name='modifystorage'),

    url(r'^deletestorage/(?P<storageId>\d+)/$', views.deletestorage, name='deletestorage'),

    url(r'^addstorage_pcie_slots/$', views.addstorage_pcie_slots, name='addstorage_pcie_slots'),

    url(r'^nvmeindex/$', views.nvmeindex, name='nvmeindex'),

    url(r'^addnvme/$', views.addnvme, name='addnvme'),

    url(r'^addswitch_info/$', views.addswitch_info, name='addswitch_info'),

    url(r'^addcontroler_info/$', views.addcontroler_info, name='addcontroler_info'),

    url(r'^deletenvme/(?P<nvmeId>\d+)/$', views.deletenvme, name='deletenvme'),

    url(r'^modifynvme/(?P<nvmeId>\d+)/$', views.modifynvme, name='modifynvme'),

    url(r'^hddindex/$', views.hddindex, name='hddindex'),

    url(r'^addhdd/$', views.addHDD, name='addhdd'),

    url(r'^deletehdd/(?P<hddId>\d+)/$', views.deletehdd, name='deletehdd'),

    url(r'^modifyhdd/(?P<hddId>\d+)/$', views.modifyhdd, name='modifyhdd'),

    url(r'^serverindex/$', views.serverindex, name='server'),

    url(r'^addserver/$', views.addserver, name='addserver'),

    url(r'^deleteserver/(?P<serverId>\d+)/$', views.deleteserver, name='deleteserver'),

    url(r'^modifyserver/(?P<serverId>\d+)/$', views.modifyserver, name='modifyserver'),

    url(r'^expanderindex/$', views.expanderindex, name='expanderindex'),

    url(r'^addexpander/$', views.addexpander, name='addexpander'),

    url(r'^deleteexpander/(?P<expanderId>\d+)/$', views.deleteexpander, name='deleteexpander'),

    url(r'^modifyexpander/(?P<expanderId>\d+)/$', views.modifyexpander, name='modifyexpander'),

    url(r'^mswitchindex/$', views.mswitchindex, name='mswitchindex'),

    url(r'^addmswitch/$', views.addmswitch, name='addmswitch'),

    url(r'^deletemswitch/(?P<mswitchId>\d+)/$', views.deletemswitch, name='deletemswitch'),

    url(r'^modifymswitch/(?P<mswitchId>\d+)/$', views.modifymswitch, name='modifymswitch'),


    #url(r'^download/$',views.downloadjson, name='downloadjson'),
    
    #url(r'^addpolicy/$', views.addpolicy, name='addpolicy'),

    # url(r'^policytable/$', views.policytable, name='policytable'),

]

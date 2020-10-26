# coding=utf-8
"""
"""
# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from .models import Component, DiscoveryHook, UpdateHook, Platform, Tool, Firmware, Release, ToolAssociation, \
    FirmwareAssociation, MiscComponent, PSU, Policy, PolicyAssociation, CPU, Memory, Storage_pcie_slots, Storage, \
    StorageAssociation, Nvme, NvmeSwitch, NvmeSwitchPort, NvmeCtrlInfo
from django.shortcuts import render, redirect
from components.forms import EditComponent, AddComponent, AddCPU, AddMemory, AddPSU, EditPSU, EditMemory, EditCPU, \
    AddStorage, AddNvme, EditNvme, AddHDD , EditHDD, AddExpander, EditExpander, AddServer, EditServer, AddMswitch, EditMswitch
from components.forms import DiscoveryEdit, UpdateEdit
import fileinput
import shutil
import json
import os
import sys
from website import settings
from django.db import DatabaseError
import models
from django.utils import timezone
import pprint
import copy
import re

# os.path.join(request.session['ws_path'],'deltas/post-build/rootfs/root/CBL')
updatehookdir = 'C:/Users/sausuvar/Documents/files/updateHooks/'  # path to where the update hooks will be saved

discoveryhookdir = 'C:/Users/sausuvar/Documents/files/discoveryHooks/'  # path to where the discovery hooks will be saved

toolbasedir = 'C:/Users/sausuvar/Documents/files/Tools'  # path to where the tools will be stored

firmwarebasedir = 'C:/Users/sausuvar/Documents/files/Firmware'  # path to where the tools will be stored

basedir = 'C:/Users/sausuvar/Desktop/'  # base directory where projet environment is set up

# def policytable(request):
#     allComponents = Component.objects.all()
#     allPlatforms = Platform.objects.all()
#
#     print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)
#     try:
#         tool_component = models.ToolAssociation.objects.all()
#     except:
#         DatabaseError
#     from itertools import chain
#     result_list = list(chain(tool_component, allComponents))
#     return render(request, 'components/policytable.html',{'allComponents': allComponents, 'allPlatforms': allPlatforms, 'result_list': result_list})

gpolicy_table = []
g_pcie_slots = []
g_switch_table = []
g_ctrl_info_table = []



def index(request, ws_name, release):
    uname = request.session['users']
    ws_path = request.session['ws_path']
    settings.DATABASE_APPS_MAPPING = {'components': uname + "_" + ws_name, }
    database_id = uname + "_" + ws_name  # just something unique
    newDatabase = {}
    newDatabase["id"] = database_id
    newDatabase['ENGINE'] = 'django.db.backends.sqlite3'
    newDatabase['NAME'] = ws_path + '/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3'
    # newDatabase['NAME'] = ws_path + '/db.sqlite3'
    newDatabase['USER'] = ''
    newDatabase['PASSWORD'] = ''
    newDatabase['HOST'] = ''
    newDatabase['PORT'] = ''
    settings.DATABASES[database_id] = newDatabase

   # allComponents = Component.objects.filter(~Q(uniqueName = 'HDD'))
    allComponents = Component.objects.filter(device_type='PCIE')
    allMisccomponents = MiscComponent.objects.filter(device_type='PCIE')
    allPlatforms = Platform.objects.all()

    # load standard pci.sid file %
    pciIds= os.path.join(settings.BASE_DIR, 'pci.ids')
    with open(pciIds) as file:
        for line in file:
            if not line.startswith('\t') and not line.startswith('#'):
                if len(line) != 0:
                    pcilist = line.encode('utf-8').strip().split('  ', 1)
                    #print(pcilist)
                    if len(pcilist) > 1:
                        settings.pci_sig_lst.append(pcilist[0].encode('utf-8') +'_'+ pcilist[1].encode('utf-8'))
                        settings.pci_sig_dict[pcilist[0].encode('utf-8')] = [pcilist[1].encode('utf-8')]
            #if line.startswith('\t') and not line.startswith('#') and not line.startswith('\t\t'):

    #print(settings.pci_sig_lst[0],settings.pci_sig_lst[1])
    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)
    try:
        tool_component = models.ToolAssociation.objects.all()
    except:
        DatabaseError
    from itertools import chain
    result_list = list(chain(tool_component, allComponents))
    return render(request, 'components/index.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents, 'allPlatforms': allPlatforms,
                   'result_list': result_list})


def psuindex(request):
    allPSU = PSU.objects.all()
    allComponents = Component.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    allPlatforms = Platform.objects.all()

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/psuindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents, 'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allPSU': allPSU})


def storageindex(request):
    response = {}

    allPlatforms = Platform.objects.all()
    allStorage = Storage.objects.all()
    allStorage_pcie_slots = Storage_pcie_slots.objects.all()
    storageassociation = StorageAssociation.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allStorage"] = allStorage
    response["allStorage_pcie_slots"] = allStorage_pcie_slots
    response["storageassociation"] = storageassociation

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)
    print(response["storageassociation"])

    return render(request, 'components/storageindex.html', response)

def nvmeindex(request):
    response = {}

    allPlatforms = Platform.objects.all()
    allNvme=Nvme.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allNvme"] = allNvme


    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)


    return render(request, 'components/nvmeindex.html', response)

def mswitchindex(request):
    response = {}

    allComponents = Component.objects.filter(device_type__iexact='M-SWITCH')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='M-SWITCH')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/mswitchindex.html', response)

def expanderindex(request):
    response = {}

    allComponents = Component.objects.filter(device_type__iexact='EXPANDER')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='EXPANDER')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/expanderindex.html', response)

def serverindex(request):
    response = {}

    allComponents = Component.objects.filter(device_type__iexact='SERVER')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='SERVER')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/serverindex.html', response)

def hddindex(request):
    response = {}

    allComponents = Component.objects.filter(device_type='Drive')
    allMisccomponents = MiscComponent.objects.filter(device_type='Drive')
    allPlatforms = Platform.objects.all()


    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents



    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)


    return render(request, 'components/hddindex.html', response)

def cpuindex(request):
    allCPU = CPU.objects.all()
    allComponents = Component.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    allPlatforms = Platform.objects.all()

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/cpuindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents, 'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allCPU': allCPU})


def memoryindex(request):
    allMemory = Memory.objects.all()
    allComponents = Component.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    allPlatforms = Platform.objects.all()

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    return render(request, 'components/memoryindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents, 'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allMemory': allMemory})


def base(request):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allComponents = Component.objects.all()
    return render(request, 'components/base.html', {'allComponents': allComponents})


# def addport_info(request):
#     my_response_data = {}
#
#     if request.method == 'POST' and request.is_ajax():
#         global gaddport_table
#         gpolicy_table = json.loads(request.POST.get('policy_table'))
#         print(gpolicy_table)
#         # gpolicytable = copy._deepcopy_list()
#         print("i got the right json")
#
#         msg = "Policy table updated successfully"
#         my_response_data['msg'] = msg
#         return HttpResponse(json.dumps(my_response_data), content_type="application/json")


def addswitch_info(request):
    my_response_data = {}

    if request.method == 'POST' and request.is_ajax():
        global g_switch_table
        print ("*****************************************************")
        unformatted_data = json.loads(request.POST.get('switch_info'))

        #g_switch_table =  unformatted_data

        #last_row = request.POST.get('lastrow').encode('UTF-8')
        #print("last_row =",last_row)
        count = 0;
        print (unformatted_data)

        for data_dict in unformatted_data:
            print(data_dict["_RowCount"])
            for count in range(0,data_dict["_RowCount"]):
                #for count in range(0,int(last_row)+1):
                #print("length of dictionary is : =",(len(data_dict)-3)/5)

                print data_dict["drive_name_" + str(count)]
                print data_dict["nvme_index_" + str(count)]
                print data_dict["usp_pcie_fn_num_" + str(count)]
                print data_dict["dsp_pcie_fn_num_" + str(count)]
                print data_dict["usp_port_num_" + str(count)]
                print data_dict["dsp_port_num_" + str(count)]

                # count = count + 1
                #
                # print data_dict["drive_name_" + str(count)]
                # print data_dict["nvme_index_" + str(count)]
                # print data_dict["usp_pcie_fn_num_" + str(count)]
                # print data_dict["usp_port_num_" + str(count)]
                # print data_dict["dsp_port_num_" + str(count)]
                #for data in data_dict:




        #print(request.POST.get('switch_info'))
        print ("*****************************************************")
        g_switch_table = json.loads(request.POST.get('switch_info'))
        print(g_switch_table)

        for switch in g_switch_table:
            print "switch =",switch

        # gpolicytable = copy._deepcopy_list()
        print("i got the right json")

        msg = "Policy table updated successfully"
        my_response_data['msg'] = msg
        return HttpResponse(json.dumps(my_response_data), content_type="application/json")

def addcontroler_info(request):
    my_response_data = {}

    if request.method == 'POST' and request.is_ajax():
        global g_ctrl_info_table
        g_ctrl_info_table = json.loads(request.POST.get('ctrl_info'))
        print(g_ctrl_info_table)
        # gpolicytable = copy._deepcopy_list()
        print("i got the right json")

        msg = "Policy table updated successfully"
        my_response_data['msg'] = msg
        return HttpResponse(json.dumps(my_response_data), content_type="application/json")


def addpolicy(request):
    my_response_data = {}

    if request.method == 'POST' and request.is_ajax():
        global gpolicy_table
        gpolicy_table = json.loads(request.POST.get('policy_table'))
        print(gpolicy_table)
        # gpolicytable = copy._deepcopy_list()
        print("i got the right json")

        msg = "Policy table updated successfully"
        my_response_data['msg'] = msg
        return HttpResponse(json.dumps(my_response_data), content_type="application/json")


# def addpolicy(request):
#     response_data = {}
#     #response_data['firmwareid'] = firmwareid
#
#     call=Component.objects.all()
#     rall=Release.objects.all()
#     pall=Platform.objects.all()
#
#     ctrlOptionsComp=[]
#     for c in call:
#         ctrlOptionsComp.append(c.description)
#
#     ctrlOptionsRel=[]
#     for r in rall:
#         ctrlOptionsRel.append(r.releaseName)
#
#     ctrlOptionsPlat = []
#     for p in pall:
#         ctrlOptionsPlat.append(p.platformName)
#
#     response_data['ctrlOptionsComp']= json.dumps(ctrlOptionsComp)
#
#     response_data['ctrlOptionsRel']=json.dumps(ctrlOptionsRel)
#
#     response_data['ctrlOptionsPlat']=json.dumps(ctrlOptionsPlat)
#
#     #t=Firmware.objects.get(id=firmwareid)
#     #firmwarea=FirmwareAssociation.objects.filter(firmware=t)
#     initm = []
#     #for taq in firmwarea:
#     #    initm.append({'release':'', 'component': taq.component.description,'platform' : taq.platform.platformName,'firmware' : taq.firmware.firmwareName })
#     response_data['initm'] = json.dumps(initm)
#
#     if request.method == 'POST' and request.is_ajax():
#         firmwares_association = json.loads(request.POST.get('firmwares_association'))
#         try:
#             firmwarea.delete()
#         except:
#             msg="objects not deleted from table firmware association"
#         for firmware in firmwares_association:
#             try:
#                 rel = Release.objects.get(releaseName=firmware['release'])
#                 plat = Platform.objects.get(platformName=firmware['platform'])
#                 comp = Component.objects.get(description=firmware['component'])
#                 firmwareassociation = FirmwareAssociation(firmware=t, release=rel, component=comp, platform=plat)
#                 firmwareassociation.save()
#                 msg = "Firmware " + firmware.firmwareName + " associated with " + plat.platformName + " " + comp.description + "."
#             except:
#                 msg = "Firmware association failed."
#         msg="Firmware associated successfully"
#         response_data['msg'] = msg
#         return HttpResponse(json.dumps(response_data), content_type="application/json")
#     return render(request, 'components/addpolicy.html', response_data)

def addmemory(request):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddMemory(request.POST)
        print 'here i have to deal with server'

        # check whether it's valid:
        if form.is_valid():
            vendor = form.cleaned_data['vendor']
            model = form.cleaned_data['model']
            revision = form.cleaned_data['revision']
            name = form.cleaned_data['name']
            pid = form.cleaned_data['pid']
            vid = form.cleaned_data['vid']
            part_number = form.cleaned_data.get('part_number')
            sku_id = form.cleaned_data.get('sku_id')
            oem = form.cleaned_data.get('oem')
            oem_part_number = form.cleaned_data.get('oem_part_number')
            platform = request.POST.getlist('platform')

            print("cleaned data got is =", form.cleaned_data)

            # verifyApi = form.cleaned_data.get('verifyApi')  # check with velu

            a = Memory.objects.create(vendor=vendor, model=model, revision=revision, name=name, pid=pid, vid=vid,
                                      part_number=part_number, sku_id=sku_id, oem=oem,
                                      oem_part_number=oem_part_number)  # , verifyApi=verifyApi)
            a.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()
            # msg = "Success"
            # return HttpResponse(msg)
            allMemory = Memory.objects.all()
            return render(request, 'components/memoryindex.html',
                          {'allComponents': allComponents,
                           'allPlatforms': allPlatforms,
                           'result_list': allComponents, 'allMemory': allMemory})
            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form

            # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})
        # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents})
    else:
        form = AddMemory()
    return render(request, 'components/addmemory.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})


def addstorage_pcie_slots(request):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    my_response_data = {}
    global g_pcie_slots
    if request.method == 'POST' and request.is_ajax():
        g_pcie_slots = json.loads(request.POST.get('pcie_slots'))

        msg = "g_pcie_slots table updated successfully"
        my_response_data['msg'] = msg
        return HttpResponse(json.dumps(my_response_data), content_type="application/json")


def addstorage(request):
    allStorage = Storage.objects.all()
    allStorage_pcie_slots = Storage_pcie_slots.objects.all()
    storageassociation = StorageAssociation.objects.all()
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name

    call = Component.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()

    response = {}

    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)

    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)

    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    initm = []

    response['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)
    response['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)
    response['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response['initm'] = json.dumps(initm)

    response["allPlatforms"] = allPlatforms
    response["allStorage"] = allStorage
    response["allStorage_pcie_slots"] = allStorage_pcie_slots
    response["storageassociation"] = storageassociation

    if request.method == 'POST':
        form = AddStorage(request.POST)
        if form.is_valid():
            match = form.cleaned_data['match']
            init = form.cleaned_data['init']
            max_drives = form.cleaned_data['max_drives']
            slot_map_strategy = form.cleaned_data['slot_map_strategy']
            platform = request.POST.getlist('platform')

            a = Storage.objects.create(match=match, init=init, max_drives=max_drives,
                                       slot_map_strategy=slot_map_strategy)
            a.save()

            for pcie_slot in g_pcie_slots:
                pci_slot_name = pcie_slot['pci_slot_name'].encode('UTF-8')
                i2c_dev_address = pcie_slot['i2c_dev_address'].encode('UTF-8')
                i2c_channel = pcie_slot['i2c_channel'].encode('UTF-8')
                unique_id = pcie_slot['unique_id'].encode('UTF-8')
                chassis_pos = pcie_slot['chassis_pos'].encode('UTF-8')
                vendor = pcie_slot['vendor'].encode('UTF-8')

                b = Storage_pcie_slots.objects.create(pci_slot_name=pci_slot_name, i2c_dev_address=i2c_dev_address,
                                                      i2c_channel=i2c_channel, unique_id=unique_id,
                                                      chassis_pos=chassis_pos,
                                                      vendor=vendor)
                b.save()

                c = StorageAssociation.objects.create(storage=a, storage_pcie_slots=b)
                c.save()
                print("a =", a, "b=", b, "c=", c)
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()

            return render(request, 'components/storageindex.html', response)

    else:
        print("GET reguest received in addstorage is empty sending responce")
        #form = EditStorage()
    return render(request, 'components/addstorage.html', response)

def addnvme(request):
    allNvme = Nvme.objects.all()
    allNvmeSwitch = NvmeSwitch.objects.all()
    allSwitchPort = NvmeSwitchPort.objects.all()
    allNVmeCtrl = NvmeCtrlInfo.objects.all()

    global g_switch_table
    global g_ctrl_info_table

    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name

    nall = Nvme.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()

    response = {}

    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    initm = []


    response['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response['initm'] = json.dumps(initm)

    response["allPlatforms"] = allPlatforms


    if request.method == 'POST':
        form = AddNvme(request.POST)
        if form.is_valid():
            match = form.cleaned_data['match']
            init = form.cleaned_data['init']
            max_drives = form.cleaned_data['max_drives']
            slot_map_strategy = form.cleaned_data['slot_map_strategy']
            platform = request.POST.getlist('platform')

            a = Nvme.objects.create(match=match, init=init, max_drives=max_drives,
                                       slot_map_strategy=slot_map_strategy)
            a.save()

            for data_dict in g_switch_table:

                pci_slot_name = data_dict["pci_slot_name"]
                switch_i2c_channel = data_dict["switch_i2c_channel"]
                switch_i2c_dev_address =  data_dict["switch_i2c_dev_address"]

                b = NvmeSwitch.objects.create(pci_slot_name = pci_slot_name, switch_i2c_channel=switch_i2c_channel, switch_i2c_dev_address=switch_i2c_dev_address, nvme=a)
                b.save()

                for count in range(0, data_dict["_RowCount"]):

                    drive_name = data_dict["drive_name_" + str(count)]
                    nvme_index = data_dict["nvme_index_" + str(count)]
                    usp_pcie_fn_num = data_dict["usp_pcie_fn_num_" + str(count)]
                    dsp_pcie_fn_num = data_dict["dsp_pcie_fn_num_" + str(count)]
                    usp_port_num = data_dict["usp_port_num_" + str(count)]
                    dsp_port_num = data_dict["dsp_port_num_" + str(count)]

                    print drive_name
                    print nvme_index
                    print usp_pcie_fn_num
                    print dsp_pcie_fn_num
                    print usp_port_num
                    print dsp_port_num

                    c = NvmeSwitchPort.objects.create(drive_name=drive_name, nvme_index=nvme_index, usp_pcie_fn_num=usp_pcie_fn_num, dsp_pcie_fn_num=dsp_pcie_fn_num, usp_port_num=usp_port_num, dsp_port_num=dsp_port_num, nvmeswitch=b )
                    c.save()

            for data_dict in g_ctrl_info_table:

                pci_slot_name = data_dict["pci_slot_name"]
                i2c_channel = data_dict["i2c_channel"]
                i2c_dev_address = data_dict["i2c_dev_address"]
                info_id = data_dict["id"]
                vendor = data_dict["vendor"]
                nvme_type = data_dict["nvme_type"]
                nvme_parent_type = data_dict["nvme_parent_type"]

                d = NvmeCtrlInfo.objects.create(pci_slot_name=pci_slot_name, i2c_channel=i2c_channel, i2c_dev_address=i2c_dev_address, info_id=info_id, vendor=vendor, nvme_type=nvme_type, nvme_parent_type=nvme_parent_type, nvme=a)
                d.save()


            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()

            allNvme = Nvme.objects.all()
            allNvmeSwitch = NvmeSwitch.objects.all()
            allSwitchPort = NvmeSwitchPort.objects.all()
            allNVmeCtrl = NvmeCtrlInfo.objects.all()

            response['allNvme'] = allNvme
            response['allNvmeSwitch'] = allNvmeSwitch
            response['allSwitchPort'] = allSwitchPort
            response['allNVmeCtrl'] = allNVmeCtrl
            return render(request, 'components/nvmeindex.html', response)

    else:
        print("GET reguest received in addstorage is empty sending responce")
        #form = EditStorage()
    return render(request, 'components/addnvme.html', response)

def addcpu(request):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddCPU(request.POST)
        print 'here i have to deal with server'

        # check whether it's valid:
        if form.is_valid():
            vendor = form.cleaned_data['vendor']
            model = form.cleaned_data['model']
            revision = form.cleaned_data['revision']
            name = form.cleaned_data['name']
            pid = form.cleaned_data['pid']
            vid = form.cleaned_data['vid']
            part_number = form.cleaned_data.get('part_number')
            oem_part_number = form.cleaned_data.get('oem_part_number')
            sku_id = form.cleaned_data.get('sku_id')
            oem_name = form.cleaned_data.get('oem_name')
            print("received data = oem", oem_name, "cleaned data =", form.cleaned_data)
            platform = request.POST.getlist('platform')

            # verifyApi = form.cleaned_data.get('verifyApi')  # check with velu

            a = CPU.objects.create(vendor=vendor, model=model, revision=revision, name=name, pid=pid, vid=vid,
                                   part_number=part_number, sku_id=sku_id, oem=oem_name, oem_part_number=oem_part_number)  # , verifyApi=verifyApi)
            a.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()
            # msg = "Success"
            # return HttpResponse(msg)
            allCPU = CPU.objects.all()
            return render(request, 'components/cpuindex.html',
                          {'allComponents': allComponents,
                           'allPlatforms': allPlatforms,
                           'result_list': allComponents, 'allCPU': allCPU})

            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form

            # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})
        # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents})
    else:
        form = AddCPU()
    return render(request, 'components/addcpu.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})


def adddrive(request):
    allComponents = Component.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    allPlatforms = Platform.objects.all()
    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    # if request.method == 'POST':

    return render(request, 'components/adddrive.html', {'allPlatforms': allPlatforms})


def addpsu(request):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')

    allMisccomponents = MiscComponent.objects.all()

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)

    print __name__ + ".py :", sys._getframe().f_code.co_name
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddPSU(request.POST)
        print 'here i have to deal with server'

        # check whether it's valid:
        if form.is_valid():
            psu_model_type = form.cleaned_data['psu_model_type']
            psu_description = form.cleaned_data['psu_description']
            psu_vendor_name = form.cleaned_data['psu_vendor_name']
            psu_part_number = form.cleaned_data['psu_part_number']
            max_power_wattage = form.cleaned_data['max_power_wattage']
            min_correction_time = form.cleaned_data['min_correction_time']

            platform = request.POST.getlist('platform')

            a = PSU.objects.create(psu_model_type=psu_model_type, psu_description=psu_description,
                                   psu_vendor_name=psu_vendor_name, psu_part_number=psu_part_number,
                                   max_power_wattage=max_power_wattage,
                                   min_correction_time=min_correction_time)  # , verifyApi=verifyApi)
            a.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("a.platform =", a.platform, "type(a.platform)", type(a.platform), "type(a)", type(a))
                a.platform.add(p)
                a.save()
            # msg = "Success"
            # return HttpResponse(msg)
            # {'allmisccomponents': allMisccomponents, 'allComponents': allComponents, 'allPlatforms': allPlatforms,
            # 'result_list': allComponents, 'allPSU': allPSU})
            allPSU = PSU.objects.all()

            return render(request, 'components/psuindex.html',
                          {'allmisccomponents': allMisccomponents, 'allComponents': allComponents,
                           'allPlatforms': allPlatforms,
                           'result_list': allComponents, 'allPSU': allPSU})
            # return HttpResponseRedirect('components/psuindex')
            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form

            # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})
        # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents})
    else:
        form = AddPSU()
    return render(request, 'components/addpsu.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})


def addcomponent(request):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    pci_attribute = ''

    # prepare responce data dictionary for the table to be displayed in JSON dynamically in javascript
    global gpolicy_table
    response_data = {}
    fanpolicy_options = {"1": "LOW_POWER_POLICY",
                         "2": "HIGH_POWER_POLICY",
                         "3": "BALANCED_POWER_POLICY",
                         "4": "MAX_POWER_POLICY",
                         }
    # response_data['firmwareid'] = firmwareid

    call = Component.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()

    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)

    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)

    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    initm = []

    response_data['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)
    response_data['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)
    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response_data['initm'] = json.dumps(initm)

    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddComponent(request.POST)
        # print 'here i have to deal with server'

        # check whether it's valid:
        if form.is_valid():
            vendorId = form.cleaned_data['vendorId']
            deviceId = form.cleaned_data['deviceId']
            subVendorId = form.cleaned_data['subVendorId']
            subDeviceId = form.cleaned_data['subDeviceId']
            uniqueName = form.cleaned_data['uniqueName']
            description = form.cleaned_data['description']
            packageVersion = form.cleaned_data.get('packageVersion')
            device_type = "PCIE"
            # platform = request.POST.get('platform')  # getlist

            # for p in platform: words = text.split(",")
            #     print("p = ",p)

            vendorString = form.cleaned_data.get('vendorString')

            pmin = form.cleaned_data.get('pmin')
            pmax = form.cleaned_data.get('pmax')
            pid = form.cleaned_data.get('pid')
            vid = form.cleaned_data.get('vid')
            sku = form.cleaned_data.get('sku')
            peripheral_type = form.cleaned_data.get('peripheral_type')
            no_of_temp_sensor = form.cleaned_data.get('no_of_temp_sensor')
            temp_sensor_i2cslaveaddr = form.cleaned_data.get('temp_sensor_i2cslaveaddr')
            # fanpolicy = form.cleaned_data.get('fanpolicy')
            secure_firmware_support = form.cleaned_data.get('secure_firmware_support')
            secure_firmware_update_i2cslaveaddr = form.cleaned_data.get('secure_firmware_update_i2cslaveaddr')
            command = form.cleaned_data.get('command')
            lock_payload = form.cleaned_data.get('lock_payload')
            unlock_payload = form.cleaned_data.get('unlock_payload')
            oem_part_number = form.cleaned_data.get('oem_part_number')
            part_number = form.cleaned_data.get('part_number')
            lff = form.cleaned_data.get('lff')
            # card_threshold_offset = form.cleaned_data.get('card_threshold_offset')
            fru_major_type = form.cleaned_data.get('fru_major_type')
            fru_minor_type = form.cleaned_data.get('fru_minor_type')
            pci_attrlist = request.POST.getlist('pci_attribute')
            mctp_supported = form.cleaned_data.get('mctp_supported')
            mctp_interfaces_supported = form.cleaned_data.get('mctp_interfaces_supported')
            oem_name = form.cleaned_data.get('oem_name')
            model = form.cleaned_data.get('model')
            print("** oem_name =",oem_name,"model =",model)

            count = 0
            for p in pci_attrlist:
                if (count == 0):
                    count = count + 1
                    pci_attribute = pci_attribute + p
                else:
                    pci_attribute = pci_attribute + ',' + p

            print("pci_attribute =", pci_attribute, "pci_attribute_list=", pci_attrlist)
            # pci_attribute = form.cleaned_data.get('pci_attribute')
            a = MiscComponent.objects.create(vendorId=vendorId, deviceId=deviceId, subVendorId=subVendorId,
                                             subDeviceId=subDeviceId, uniqueName=uniqueName, description=description,
                                             packageVersion=packageVersion, vendorString=vendorString,
                                             pmin=pmin, pmax=pmax, pid=pid, vid=vid, sku=sku,
                                             oem_part_number=oem_part_number, part_number=part_number, lff=lff, peripheral_type=peripheral_type,
                                             no_of_temp_sensor=no_of_temp_sensor,
                                             temp_sensor_i2cslaveaddr=temp_sensor_i2cslaveaddr,
                                             secure_firmware_support=secure_firmware_support,
                                             secure_firmware_update_i2cslaveaddr=secure_firmware_update_i2cslaveaddr,
                                             command=command, lock_payload=lock_payload, unlock_payload=unlock_payload,
                                             fru_major_type=fru_major_type, fru_minor_type=fru_minor_type,
                                             pci_attribute=pci_attribute, mctp_supported=mctp_supported,
                                             mctp_interfaces_supported=mctp_interfaces_supported, oem_name=oem_name, model=model,device_type=device_type)
            a.save()

            # get platform fanpolicy and cardthresholdoffset from global data and fill it to policy table
            for policy1 in gpolicy_table:
                p = Platform.objects.get(platformName=policy1['platform'].encode('UTF-8'))
                a.platform.add(p)
                a.save()
                fanpolicy = policy1['fanpolicy'].encode('UTF-8')
                #card_threshold_offset = policy1['cardthresholdoffset'].encode('UTF-8')
                card_threshold_offset = ""


                po = Policy.objects.filter(fanpolicy=fanpolicy_options[fanpolicy],
                                           card_threshold_offset=card_threshold_offset)

                if (len(po) == 0):
                    print ("not exists : policy creating")
                    b = Policy.objects.create(fanpolicy=fanpolicy_options[fanpolicy],
                                              card_threshold_offset=card_threshold_offset)
                    b.save()
                else:
                    print("policy already exists")
                    b = po[0]
                # a is component b is policy and p is platform

                policy = Policy.objects.get(id=b.id)
                print("Policy is , type is ", policy, type(policy))
                comp = Component.objects.get(id=a.component_ptr_id)
                print ("Component is , type is ", comp, type(comp))
                policyassociation = PolicyAssociation.objects.create(component=comp, policy=policy, platform=p)
                # policyassociation=PolicyAssociation(component=comp, policy=policy, platform=p)
                policyassociation.save()

            # msg = "Success"
            # return HttpResponse(msg)
            return HttpResponseRedirect(
                '/components/index/' + request.session['ws_name'] + "/" + request.session['release'])
            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form

            # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})
        # return render(request, 'components/addallcomponent.html', {'allComponents': allComponents})
    else:
        form = AddComponent()
    return render(request, 'components/addcomponent.html', response_data)

def addmswitch(request):
    allComponents = Component.objects.filter(device_type__iexact='M-SWITCH')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name

    response_data = {}
    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddMswitch(request.POST)

        # check whether it's valid:
        if form.is_valid():
            vendorId = form.cleaned_data['vendorId']
            deviceId = form.cleaned_data['deviceId']

            uniqueName = form.cleaned_data['uniqueName']
            description = form.cleaned_data['description']

            packageVersion = form.cleaned_data.get('packageVersion')
            device_type = 'M-SWITCH'

            platform = request.POST.getlist('platform')
            a = MiscComponent.objects.create(vendorId=vendorId, deviceId=deviceId, subVendorId="",
                                             subDeviceId="", uniqueName=uniqueName, description=description,
                                             packageVersion=packageVersion, vendorString="",
                                             pmin="", pmax="", pid="", vid="", sku="",
                                             oem_part_number="", part_number="", lff="", peripheral_type="",
                                             no_of_temp_sensor="",
                                             temp_sensor_i2cslaveaddr="",
                                             secure_firmware_support="",
                                             secure_firmware_update_i2cslaveaddr="",
                                             command="", lock_payload="", unlock_payload="",
                                             fru_major_type="", fru_minor_type="",
                                             pci_attribute='', mctp_supported="",
                                             mctp_interfaces_supported="",model="", oem_name="",device_type=device_type)
            a.save()

            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()

            # Code for populating response back
            response = {}
            allComponents = Component.objects.filter(device_type__iexact='M-SWITCH')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='M-SWITCH')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents

            return render(request, 'components/mswitchindex.html', response)
    else:
        form = AddMswitch()
    return render(request, 'components/addmswitch.html', response_data)

def addexpander(request):
    allComponents = Component.objects.filter(device_type__iexact='EXPANDER')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name

    response_data = {}
    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddExpander(request.POST)

        # check whether it's valid:
        if form.is_valid():
            uniqueName = form.cleaned_data['uniqueName']
            description = form.cleaned_data['description']

            packageVersion = form.cleaned_data.get('packageVersion')
            device_type = 'EXPANDER'

            platform = request.POST.getlist('platform')
            a = MiscComponent.objects.create(vendorId="", deviceId="", subVendorId="",
                                             subDeviceId="", uniqueName=uniqueName, description=description,
                                             packageVersion=packageVersion, vendorString="",
                                             pmin="", pmax="", pid="", vid="", sku="",
                                             oem_part_number="", part_number="", lff="", peripheral_type="",
                                             no_of_temp_sensor="",
                                             temp_sensor_i2cslaveaddr="",
                                             secure_firmware_support="",
                                             secure_firmware_update_i2cslaveaddr="",
                                             command="", lock_payload="", unlock_payload="",
                                             fru_major_type="", fru_minor_type="",
                                             pci_attribute='', mctp_supported="",
                                             mctp_interfaces_supported="",model="", oem_name="",device_type=device_type)
            a.save()

            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()

            # Code for populating response back
            response = {}
            allComponents = Component.objects.filter(device_type__iexact='EXPANDER')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='EXPANDER')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents

            return render(request, 'components/expanderindex.html', response)
    else:
        form = AddExpander()
    return render(request, 'components/addexpander.html', response_data)

def addserver(request):
    allComponents = Component.objects.filter(device_type__iexact='SERVER')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name

    response_data = {}
    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddServer(request.POST)

        # check whether it's valid:
        if form.is_valid():
            uniqueName = form.cleaned_data['uniqueName']
            description = form.cleaned_data['description']

            packageVersion = form.cleaned_data.get('packageVersion')
            device_type = "SERVER"

            platform = request.POST.getlist('platform')
            a = MiscComponent.objects.create(vendorId="", deviceId="", subVendorId="",
                                             subDeviceId="", uniqueName=uniqueName, description=description,
                                             packageVersion=packageVersion, vendorString="",
                                             pmin="", pmax="", pid="", vid="", sku="",
                                             oem_part_number="", part_number="", lff="", peripheral_type="",
                                             no_of_temp_sensor="",
                                             temp_sensor_i2cslaveaddr="",
                                             secure_firmware_support="",
                                             secure_firmware_update_i2cslaveaddr="",
                                             command="", lock_payload="", unlock_payload="",
                                             fru_major_type="", fru_minor_type="",
                                             pci_attribute='', mctp_supported="",
                                             mctp_interfaces_supported="", model="", oem_name="",
                                             device_type=device_type)
            a.save()

            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()

            # Code for populating response back
            response = {}
            allComponents = Component.objects.filter(device_type__iexact='SERVER')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='SERVER')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents

            return render(request, 'components/serverindex.html', response)
    else:
        form = AddServer()
    return render(request, 'components/addserver.html', response_data)

def addHDD(request):
    allComponents = Component.objects.filter(device_type='Drive')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__ + ".py :", sys._getframe().f_code.co_name
    pci_attribute = ''

    # prepare responce data dictionary for the table to be displayed in JSON dynamically in javascript
    global gpolicy_table
    response_data = {}

    # response_data['firmwareid'] = firmwareid

    call = Component.objects.filter(device_type='Drive')
    rall = Release.objects.all()
    pall = Platform.objects.all()

    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)

    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)

    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    initm = []

    response_data['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)
    response_data['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)
    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response_data['initm'] = json.dumps(initm)

    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddHDD(request.POST)
        # print 'here i have to deal with server'

        # check whether it's valid:
        if form.is_valid():
            uniqueName = 'HDD'
            description = form.cleaned_data['description']

            packageVersion = form.cleaned_data.get('packageVersion')
            device_type = 'Drive'
            # platform = request.POST.get('platform')  # getlist

            # for p in platform: words = text.split(",")
            #     print("p = ",p)

            vendorString = form.cleaned_data.get('vendorString')
            model = form.cleaned_data.get('model')
            part_number = form.cleaned_data.get('part_number')
            pid = form.cleaned_data.get('pid')
            vid = form.cleaned_data.get('vid')
            print("** Vid =", vid)
            sku = form.cleaned_data.get('sku')
            oem_part_number = form.cleaned_data.get('oem_part_number')
            oem_name = form.cleaned_data.get('oem_name')
            lff = form.cleaned_data.get('lff')


            pmin = form.cleaned_data.get('pmin')
            pmax = form.cleaned_data.get('pmax')

            platform = request.POST.getlist('platform')
            # pci_attribute = form.cleaned_data.get('pci_attribute')
            a = MiscComponent.objects.create(vendorId="", deviceId="", subVendorId="",
                                             subDeviceId="", uniqueName=uniqueName, description=description,
                                             packageVersion=packageVersion, vendorString=vendorString,
                                             pmin=pmin, pmax=pmax, pid=pid, vid=vid, sku=sku,
                                             oem_part_number=oem_part_number, part_number=part_number, lff=lff, peripheral_type="",
                                             no_of_temp_sensor="",
                                             temp_sensor_i2cslaveaddr="",
                                             secure_firmware_support="",
                                             secure_firmware_update_i2cslaveaddr="",
                                             command="", lock_payload="", unlock_payload="",
                                             fru_major_type="", fru_minor_type="",
                                             pci_attribute=pci_attribute, mctp_supported="",
                                             mctp_interfaces_supported="",model=model, oem_name=oem_name,device_type=device_type)
            a.save()

            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()
            # get platform fanpolicy and cardthresholdoffset from global data and fill it to policy table

            response = {}
            allComponents = Component.objects.filter(device_type='Drive')
            allMisccomponents = MiscComponent.objects.filter(device_type='Drive')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents
            # msg = "Success"
            # return HttpResponse(msg)
            #return HttpResponseRedirect('/components/hddindex/')
            return render(request, 'components/hddindex.html', response)
    else:
        form = AddHDD()
    return render(request, 'components/addhdd.html', response_data)

'''
def addcomponent(request):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    print __name__+".py :",sys._getframe().f_code.co_name
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddComponent(request.POST)
        # check whether it's valid:
        if form.is_valid():
            vendorId = form.cleaned_data['vendorId']
            deviceId = form.cleaned_data['deviceId']
            subVendorId = form.cleaned_data['subVendorId']
            subDeviceId = form.cleaned_data['subDeviceId']
            uniqueName = form.cleaned_data['uniqueName']
            description = form.cleaned_data['description']
            exists = form.cleaned_data.get('exists')
            packageVersion = form.cleaned_data.get('packageVersion')
            platform = request.POST.getlist('platform')

            vendorString = form.cleaned_data.get('vendorString')
            #verifyApi = form.cleaned_data.get('verifyApi')  # check with velu
            a = Component.objects.create(vendorId=vendorId, deviceId=deviceId, subVendorId=subVendorId, subDeviceId=subDeviceId, uniqueName=uniqueName, description=description, exists=exists, packageVersion=packageVersion, vendorString=vendorString)#, verifyApi=verifyApi)
            a.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                a.platform.add(p)
                a.save()
            #msg = "Success"
            #return HttpResponse(msg)
            return HttpResponseRedirect('/components/index/'+request.session['ws_name']+"/"+request.session['release'])
            #return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form
    else:
        form = AddComponent()
    return render(request, 'components/addcomponent.html', {'allComponents': allComponents, 'allPlatforms': allPlatforms})
'''


def modifymemory(request, memoryId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')
    allMemory = Memory.objects.all()
    memory = Memory.objects.get(pk=memoryId)

    response_data = {}
    response_data['allMemory'] = allMemory
    response_data['allPlatforms'] = allPlatforms
    response_data['memory'] = memory
    if request.method == 'POST':
        form = EditMemory(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            memory.vendor = form.cleaned_data['vendor']
            memory.model = form.cleaned_data['model']
            memory.revision = form.cleaned_data['revision']
            memory.name = form.cleaned_data['name']
            memory.pid = form.cleaned_data['pid']
            memory.vid = form.cleaned_data['vid']
            memory.part_number = form.cleaned_data.get('part_number')
            memory.sku_id = form.cleaned_data.get('sku_id')
            memory.oem = form.cleaned_data.get('oem')
            memory.oem_part_number = form.cleaned_data.get('oem_part_number')
            platform = request.POST.getlist('platform')
            memory.platform.clear()
            memory.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print(
                    "memory.platform =", memory.platform, "type(memory.platform)", type(memory.platform),
                    "type(memory)",
                    type(memory))
                memory.platform.add(p)
                memory.save()

            allMemory = Memory.objects.all()
            response_data['allMemory'] = allMemory
            return render(request, 'components/memoryindex.html', response_data)

    else:
        form = EditMemory()
    return render(request, 'components/modifymemory.html', response_data)


def deletememory(request, memoryId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    Memory.objects.filter(pk=memoryId).delete()
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    allMemory = Memory.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    return render(request, 'components/memoryindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents,
                   'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allMemory': allMemory})


def modifycpu(request, cpuId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')
    allCPU = CPU.objects.all()
    cpu = CPU.objects.get(pk=cpuId)

    response_data = {}
    response_data['allCPU'] = allCPU
    response_data['allPlatforms'] = allPlatforms
    response_data['cpu'] = cpu
    if request.method == 'POST':
        form = EditCPU(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            print("received cleaned data =", form.cleaned_data)
            cpu.vendor = form.cleaned_data['vendor']
            cpu.model = form.cleaned_data['model']
            cpu.revision = form.cleaned_data['revision']
            cpu.name = form.cleaned_data['name']
            cpu.pid = form.cleaned_data['pid']
            cpu.vid = form.cleaned_data['vid']
            cpu.part_number = form.cleaned_data.get('part_number')
            cpu.oem_part_number = form.cleaned_data.get('oem_part_number')
            cpu.sku_id = form.cleaned_data.get('sku_id')
            cpu.oem = form.cleaned_data.get('oem_name')

            platform = request.POST.getlist('platform')
            cpu.platform.clear()
            cpu.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("cpu.platform =", cpu.platform, "type(cpu.platform)", type(cpu.platform), "type(cpu)", type(cpu))
                cpu.platform.add(p)
                cpu.save()

            allCPU = CPU.objects.all()
            response_data['allCPU'] = allCPU
            return render(request, 'components/cpuindex.html', response_data)

    else:
        form = EditCPU()
    return render(request, 'components/modifycpu.html', response_data)


def deletecpu(request, cpuId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    CPU.objects.filter(pk=cpuId).delete()
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    allCPU = CPU.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    return render(request, 'components/cpuindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents,
                   'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allCPU': allCPU})


def modifynvme(request, nvmeId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')
    allNvme = Nvme.objects.all()
    nvme = Nvme.objects.get(pk=nvmeId)

    global g_switch_table
    global g_ctrl_info_table

    response_data = {}
    response_data['allNvme'] = allNvme
    response_data['allPlatforms'] = allPlatforms
    response_data['nvme'] = nvme

    nvmeswitch = NvmeSwitch.objects.filter(nvme=nvmeId)

    initm = []
    for switch in nvmeswitch:
        SubGridData = []
        switchport = NvmeSwitchPort.objects.filter(nvmeswitch=switch)
        for port in switchport:
            drive_name=port.drive_name
            usp_port_num=port.usp_port_num
            dsp_port_num=port.dsp_port_num
            usp_pcie_fn_num=port.usp_pcie_fn_num
            dsp_pcie_fn_num = port.dsp_pcie_fn_num
            nvme_index=port.nvme_index
            SubGridData.append({'drive_name': drive_name, 'usp_port_num': usp_port_num, 'dsp_port_num': dsp_port_num, 'usp_pcie_fn_num': usp_pcie_fn_num, 'dsp_pcie_fn_num': dsp_pcie_fn_num , 'nvme_index': nvme_index})

        initm.append({'pci_slot_name': switch.pci_slot_name, 'switch_i2c_channel': switch.switch_i2c_channel, 'switch_i2c_dev_address': switch.switch_i2c_dev_address, 'SubGridData': SubGridData})

    response_data['initm'] = json.dumps(initm)
    print(response_data['initm'])

    initc = []
    ctrlinfo = NvmeCtrlInfo.objects.filter(nvme=nvmeId)
    for ctrl in ctrlinfo:
        pci_slot_name = ctrl.pci_slot_name
        i2c_channel = ctrl.i2c_channel
        i2c_dev_address = ctrl.i2c_dev_address
        id = ctrl.info_id
        vendor = ctrl.vendor
        nvme_type = ctrl.nvme_type
        nvme_parent_type = ctrl.nvme_parent_type

        initc.append({'pci_slot_name': pci_slot_name, 'i2c_channel': i2c_channel, 'i2c_dev_address': i2c_dev_address, 'id': id, 'vendor': vendor, 'nvme_type': nvme_type, 'nvme_parent_type':nvme_parent_type })

    response_data['initc'] = json.dumps(initc)
    print(response_data['initc'])

    if request.method == 'POST':
        form = EditNvme(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            nvme.match = form.cleaned_data['match']
            nvme.init = form.cleaned_data['init']
            nvme.max_drives = form.cleaned_data['max_drives']
            nvme.slot_map_strategy = form.cleaned_data['slot_map_strategy']

            nvmeswitch = NvmeSwitch.objects.filter(nvme=nvmeId)
            data_dict_iterator = iter(g_switch_table)
            for switch in nvmeswitch:
                try:
                    data_dict = next(data_dict_iterator)
                except StopIteration:
                    break
                switch.pci_slot_name = data_dict["pci_slot_name"]
                switch.switch_i2c_channel = data_dict["switch_i2c_channel"]
                switch.switch_i2c_dev_address =  data_dict["switch_i2c_dev_address"]

                switchport = NvmeSwitchPort.objects.filter(nvmeswitch=switch)
                port_iterator = iter(switchport)

                for count in range(0, data_dict["_RowCount"]):
                    try:
                        port = next(port_iterator)
                    except StopIteration:
                        break
                    port.drive_name = data_dict["drive_name_" + str(count)]
                    port.nvme_index = data_dict["nvme_index_" + str(count)]
                    port.usp_pcie_fn_num = data_dict["usp_pcie_fn_num_" + str(count)]
                    port.dsp_pcie_fn_num = data_dict["dsp_pcie_fn_num_" + str(count)]
                    port.usp_port_num = data_dict["usp_port_num_" + str(count)]
                    port.dsp_port_num = data_dict["dsp_port_num_" + str(count)]
                    port.save()

                switch.save()


            nvmectrl = NvmeCtrlInfo.objects.filter(nvme=nvmeId)
            ctrl_dict_iterator = iter(g_ctrl_info_table)
            for ctrl in nvmectrl:
                try:
                    ctrl_dict = next(ctrl_dict_iterator)
                except StopIteration:
                    break
                ctrl.pci_slot_name = ctrl_dict["pci_slot_name"]
                ctrl.i2c_channel = ctrl_dict["i2c_channel"]
                ctrl.i2c_dev_address = ctrl_dict["i2c_dev_address"]
                ctrl.info_id = ctrl_dict["id"]
                ctrl.vendor = ctrl_dict["vendor"]
                ctrl.nvme_type = ctrl_dict["nvme_type"]
                ctrl.nvme_parent_type = ctrl_dict["nvme_parent_type"]
                ctrl.save()




            platform = request.POST.getlist('platform')
            nvme.platform.clear()
            nvme.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("psu.platform =", nvme.platform, "type(psu.platform)", type(nvme.platform), "type(a)", type(nvme))
                nvme.platform.add(p)
                nvme.save()

            allNvme = Nvme.objects.all()
            allNvmeSwitch = NvmeSwitch.objects.all()
            allSwitchPort = NvmeSwitchPort.objects.all()
            allNVmeCtrl = NvmeCtrlInfo.objects.all()
            allPlatforms = Platform.objects.order_by('platformName')

            response = {}
            response['allNvme'] = allNvme
            response['allNvmeSwitch'] = allNvmeSwitch
            response['allSwitchPort'] = allSwitchPort
            response['allNVmeCtrl'] = allNVmeCtrl
            response['allPlatforms'] = allPlatforms

            return render(request, 'components/nvmeindex.html', response)

    else:
        form = EditNvme()
    return render(request, 'components/modifynvme.html', response_data)

def modifymswitch(request, mswitchId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')

    try:
        mswitch = MiscComponent.objects.get(component_ptr_id=mswitchId)
        allComponent = MiscComponent.objects.filter(device_type__iexact='M-Switch')
        legacy = '0'
    except:
        print("Found a legacy Coomponent ")
        legacy = '1'
        allComponent = Component.objects.filter(device_type__iexact='M-Switch')
        mswitch = Component.objects.get(pk=mswitchId)

    response_data = {}
    response_data['allComponents'] = allComponent
    response_data['allPlatforms'] = allPlatforms
    response_data['component'] = mswitch
    response_data['legacy'] = legacy
    print("** test **")
    print("", type(mswitch))
    if request.method == 'POST':
        form = EditMswitch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            print("received cleaned data =", form.cleaned_data)
            mswitch.vendorId = form.cleaned_data['vendorId']
            mswitch.deviceId = form.cleaned_data['deviceId']
            mswitch.description = form.cleaned_data['description']
            mswitch.packageVersion = form.cleaned_data['packageVersion']
            mswitch.uniqueName = form.cleaned_data['uniqueName']
            mswitch.device_type = "M-SWITCH"
            if legacy == '1':
                a = MiscComponent.objects.create(component_ptr_id=mswitch.pk, pmin="", pmax="", pid="", vid="",
                                                 sku="", oem_part_number="", lff="",
                                                 part_number="",
                                                 peripheral_type="", no_of_temp_sensor="",
                                                 temp_sensor_i2cslaveaddr="",
                                                 secure_firmware_support="",
                                                 secure_firmware_update_i2cslaveaddr="",
                                                 command="", lock_payload="",
                                                 unlock_payload="", fru_major_type="",
                                                 fru_minor_type="", pci_attribute="",
                                                 mctp_supported="", oem_name="", model="",
                                                 mctp_interfaces_supported="")
                a.save()
            platform = request.POST.getlist('platform')
            mswitch.platform.clear()
            mswitch.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print(
                "mswitch.platform =", mswitch.platform, "type(mswitch.platform)", type(mswitch.platform), "type(mswitch)",
                type(mswitch))
                mswitch.platform.add(p)
                mswitch.save()

            response = {}
            allComponents = Component.objects.filter(device_type__iexact='M-SWITCH')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='M-SWITCH')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents

            return render(request, 'components/mswitchindex.html', response)

    else:
        form = EditMswitch()
    return render(request, 'components/modifymswitch.html', response_data)

def modifyexpander(request, expanderId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')

    try:
        expander = MiscComponent.objects.get(component_ptr_id=expanderId)
        allComponent = MiscComponent.objects.filter(device_type__iexact='EXPANDER')
        legacy = '0'
    except:
        print("Found a legacy Coomponent ")
        legacy = '1'
        allComponent = Component.objects.filter(device_type__iexact='EXPANDER')
        expander = Component.objects.get(pk=expanderId)

    response_data = {}
    response_data['allComponents'] = allComponent
    response_data['allPlatforms'] = allPlatforms
    response_data['component'] = expander
    response_data['legacy'] = legacy
    print("** test **")
    print("", type(expander))
    if request.method == 'POST':
        form = EditExpander(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            print("received cleaned data =", form.cleaned_data)
            expander.description = form.cleaned_data['description']
            expander.packageVersion = form.cleaned_data['packageVersion']
            expander.uniqueName = form.cleaned_data['uniqueName']
            expander.device_type = "EXPANDER"
            if legacy == '1':
                a = MiscComponent.objects.create(component_ptr_id=expander.pk, pmin="", pmax="", pid="", vid="",
                                                 sku="", oem_part_number="", lff="",
                                                 part_number="",
                                                 peripheral_type="", no_of_temp_sensor="",
                                                 temp_sensor_i2cslaveaddr="",
                                                 secure_firmware_support="",
                                                 secure_firmware_update_i2cslaveaddr="",
                                                 command="", lock_payload="",
                                                 unlock_payload="", fru_major_type="",
                                                 fru_minor_type="", pci_attribute="",
                                                 mctp_supported="", oem_name="", model="",
                                                 mctp_interfaces_supported="")
                a.save()
            platform = request.POST.getlist('platform')
            expander.platform.clear()
            expander.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print(
                "expander.platform =", expander.platform, "type(expander.platform)", type(expander.platform), "type(expander)",
                type(expander))
                expander.platform.add(p)
                expander.save()

            response = {}
            allComponents = Component.objects.filter(device_type__iexact='EXPANDER')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='EXPANDER')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents

            return render(request, 'components/expanderindex.html', response)

    else:
        form = EditExpander()
    return render(request, 'components/modifyexpander.html', response_data)

def modifyserver(request, serverId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')

    print("serverId i am getting as = ",serverId)

   # component = Component.objects.get(pk=hddId)
    try:
        server = MiscComponent.objects.get(component_ptr_id=serverId)
        allComponent = MiscComponent.objects.filter(device_type__iexact='SERVER')
        legacy = '0'
    except:
        print("Found a legacy Coomponent ")
        legacy = '1'
        allComponent = Component.objects.filter(device_type__iexact='SERVER')
        server = Component.objects.get(pk=serverId)


    response_data = {}
    response_data['allComponents'] = allComponent
    response_data['allPlatforms'] = allPlatforms
    response_data['component'] = server
    response_data['legacy'] = legacy
    print("** test **")
    print("",type(server))
    if request.method == 'POST':
        form = EditServer(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            print("received cleaned data =", form.cleaned_data)
            server.description = form.cleaned_data['description']
            server.packageVersion = form.cleaned_data['packageVersion']
            server.uniqueName = form.cleaned_data['uniqueName']
            server.device_type = "SERVER"
            if legacy == '1':
                a = MiscComponent.objects.create(component_ptr_id=server.pk, pmin="", pmax="", pid="", vid="",
                                                 sku="", oem_part_number="", lff="",
                                                 part_number="",
                                                 peripheral_type="", no_of_temp_sensor="",
                                                 temp_sensor_i2cslaveaddr="",
                                                 secure_firmware_support="",
                                                 secure_firmware_update_i2cslaveaddr="",
                                                 command="", lock_payload="",
                                                 unlock_payload="", fru_major_type="",
                                                 fru_minor_type="", pci_attribute="",
                                                 mctp_supported="", oem_name="", model="",
                                                 mctp_interfaces_supported = "")
                a.save()
            platform = request.POST.getlist('platform')
            server.platform.clear()
            server.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("server.platform =", server.platform, "type(server.platform)", type(server.platform), "type(server)", type(server))
                server.platform.add(p)
                server.save()

            response = {}
            allComponents = Component.objects.filter(device_type__iexact='SERVER')
            allMisccomponents = MiscComponent.objects.filter(device_type__iexact='SERVER')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents
            # msg = "Success"
            # return HttpResponse(msg)
            # return HttpResponseRedirect('/components/hddindex/')
            return render(request, 'components/serverindex.html', response)

    else:
        form = EditServer()
    return render(request, 'components/modifyserver.html', response_data)

def modifyhdd(request, hddId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')


    #allComponent = MiscComponent.objects.all()
    #allComponent = MiscComponent.objects.filter(device_type='Drive')

    print("hdd id i am getting as = ",hddId)

   # component = Component.objects.get(pk=hddId)
    try:
        hdd = MiscComponent.objects.get(component_ptr_id=hddId)
        allComponent = MiscComponent.objects.filter(device_type='Drive')
        legacy = '0'
    except:
        print("Found a legacy Coomponent ")
        legacy = '1'
        allComponent = Component.objects.filter(device_type='Drive')
        hdd = Component.objects.get(pk=hddId)
        misccomponent = ''
        #response_data['selected_pci_attr'] = ''

    #hdd = MiscComponent.objects.get(component_ptr_id=hddId)
    #component = hdd

    response_data = {}
    response_data['allComponents'] = allComponent
    response_data['allPlatforms'] = allPlatforms
    response_data['component'] = hdd
    response_data['legacy'] = legacy
    print("** test **")
    print("",type(hdd))
    if request.method == 'POST':
        form = EditHDD(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            print("received cleaned data =", form.cleaned_data)
            hdd.description = form.cleaned_data['description']
            hdd.packageVersion = form.cleaned_data['packageVersion']
            hdd.vendorString = form.cleaned_data['vendorString']
            hdd.model = form.cleaned_data['model']
            hdd.device_type = "Drive"
            if legacy == '0':
                hdd.part_number = form.cleaned_data['part_number']
                hdd.pid = form.cleaned_data.get('pid')
                hdd.vid = form.cleaned_data.get('vid')
                hdd.sku = form.cleaned_data.get('sku')
                hdd.oem_part_number = form.cleaned_data.get('oem_part_number')
                hdd.oem_name = form.cleaned_data.get('oem_name')
                hdd.pmax = form.cleaned_data.get('pmax')
                hdd.pmin = form.cleaned_data.get('pmin')
                hdd.lff = form.cleaned_data.get('lff')
                print("form is valid lff =", hdd.lff)
            else:
                part_number = form.cleaned_data['part_number']
                pid = form.cleaned_data.get('pid')
                vid = form.cleaned_data.get('vid')
                sku = form.cleaned_data.get('sku')
                oem_part_number = form.cleaned_data.get('oem_part_number')
                oem_name = form.cleaned_data.get('oem_name')
                pmax = form.cleaned_data.get('pmax')
                pmin = form.cleaned_data.get('pmin')
                lff = form.cleaned_data.get('lff')
                print("lff =",lff)

                a = MiscComponent.objects.create(component_ptr_id=hdd.pk, pmin=pmin, pmax=pmax, pid=pid, vid=vid,
                                                 sku=sku, oem_part_number=oem_part_number, lff=lff,
                                                 part_number=part_number,
                                                 peripheral_type="", no_of_temp_sensor="",
                                                 temp_sensor_i2cslaveaddr="",
                                                 secure_firmware_support="",
                                                 secure_firmware_update_i2cslaveaddr="",
                                                 command="", lock_payload="",
                                                 unlock_payload="", fru_major_type="",
                                                 fru_minor_type="", pci_attribute="",
                                                 mctp_supported="", oem_name=oem_name, model="",
                                                 mctp_interfaces_supported = "")
                a.save()
            platform = request.POST.getlist('platform')
            hdd.platform.clear()
            hdd.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("hdd.platform =", hdd.platform, "type(hdd.platform)", type(hdd.platform), "type(hdd)", type(hdd))
                hdd.platform.add(p)
                hdd.save()

            response = {}
            allComponents = Component.objects.filter(device_type='Drive')
            allMisccomponents = MiscComponent.objects.filter(device_type='Drive')
            allPlatforms = Platform.objects.all()

            response["allPlatforms"] = allPlatforms
            response["allComponents"] = allComponents
            response["allmisccomponents"] = allMisccomponents
            # msg = "Success"
            # return HttpResponse(msg)
            # return HttpResponseRedirect('/components/hddindex/')
            return render(request, 'components/hddindex.html', response)

    else:
        form = EditHDD()
    return render(request, 'components/modifyhdd.html', response_data)

def deletemswitch(request, mswitchId):
    print __name__ + ".py :", sys._getframe().f_code.co_name

    MiscComponent.objects.filter(component_ptr_id=mswitchId).delete()
    response = {}
    allComponents = Component.objects.filter(device_type__iexact='M-SWITCH')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='M-SWITCH')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    return render(request, 'components/mswitchindex.html', response)

def deleteexpander(request, expanderId):
    print __name__ + ".py :", sys._getframe().f_code.co_name

    MiscComponent.objects.filter(component_ptr_id=expanderId).delete()
    response = {}
    allComponents = Component.objects.filter(device_type__iexact='EXPANDER')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='EXPANDER')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    return render(request, 'components/expanderindex.html', response)

def deleteserver(request, serverId):
    print __name__ + ".py :", sys._getframe().f_code.co_name

    MiscComponent.objects.filter(component_ptr_id=serverId).delete()
    response = {}
    allComponents = Component.objects.filter(device_type__iexact='SERVER')
    allMisccomponents = MiscComponent.objects.filter(device_type__iexact='SERVER')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    return render(request, 'components/serverindex.html', response)

def deletehdd(request, hddId):
    print __name__ + ".py :", sys._getframe().f_code.co_name

    MiscComponent.objects.filter(component_ptr_id=hddId).delete()
    response = {}
    allComponents = Component.objects.filter(device_type='Drive')
    allMisccomponents = MiscComponent.objects.filter(device_type='Drive')
    allPlatforms = Platform.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allComponents"] = allComponents
    response["allmisccomponents"] = allMisccomponents

    return render(request, 'components/hddindex.html', response)


def deletenvme(request, nvmeId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    nvmeswitch = NvmeSwitch.objects.filter(nvme=nvmeId)

    for switch in nvmeswitch:
        NvmeSwitchPort.objects.filter(nvmeswitch=switch).delete()


    NvmeSwitch.objects.filter(nvme=nvmeId).delete()
    NvmeCtrlInfo.objects.filter(nvme=nvmeId).delete()
    Nvme.objects.filter(pk=nvmeId).delete()

    allNvme = Nvme.objects.all()
    allNvmeSwitch = NvmeSwitch.objects.all()
    allSwitchPort = NvmeSwitchPort.objects.all()
    allNVmeCtrl = NvmeCtrlInfo.objects.all()
    allPlatforms = Platform.objects.order_by('platformName')

    response = {}
    response['allNvme'] = allNvme
    response['allNvmeSwitch'] = allNvmeSwitch
    response['allSwitchPort'] = allSwitchPort
    response['allNVmeCtrl'] = allNVmeCtrl
    response['allPlatforms'] = allPlatforms


    return render(request, 'components/nvmeindex.html', response)



def modifypsu(request, psuId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')
    allPSU = PSU.objects.all()
    psu = PSU.objects.get(pk=psuId)

    response_data = {}
    response_data['allPSU'] = allPSU
    response_data['allPlatforms'] = allPlatforms
    response_data['psu'] = psu
    if request.method == 'POST':
        form = EditPSU(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print("The form is valid")
            psu.psu_model_type = form.cleaned_data['psu_model_type']
            psu.psu_description = form.cleaned_data['psu_description']
            psu.psu_vendor_name = form.cleaned_data['psu_vendor_name']
            psu.psu_part_number = form.cleaned_data['psu_part_number']
            psu.max_power_wattage = form.cleaned_data['max_power_wattage']
            psu.min_correction_time = form.cleaned_data['min_correction_time']

            platform = request.POST.getlist('platform')
            psu.platform.clear()
            psu.save()
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                print("psu.platform =", psu.platform, "type(psu.platform)", type(psu.platform), "type(a)", type(psu))
                psu.platform.add(p)
                psu.save()

            allPSU = PSU.objects.all()
            response_data['allPSU'] = allPSU
            return render(request, 'components/psuindex.html', response_data)

    else:
        form = EditPSU()
    return render(request, 'components/modifypsu.html', response_data)


def deletepsu(request, psuId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    PSU.objects.filter(pk=psuId).delete()
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    allPSU = PSU.objects.all()
    allMisccomponents = MiscComponent.objects.all()
    return render(request, 'components/psuindex.html',
                  {'allmisccomponents': allMisccomponents, 'allComponents': allComponents,
                   'allPlatforms': allPlatforms,
                   'result_list': allComponents, 'allPSU': allPSU})


def modifystorage(request, storageId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    allPlatforms = Platform.objects.order_by('platformName')
    allStorage = Storage.objects.all()
    allStorage_pcie_slots = Storage_pcie_slots.objects.all()

    storageassociation = StorageAssociation.objects.filter(storage=storageId)

    storage = Storage.objects.get(pk=storageId)

    ctrlOptionsPlat = []
    pall = Platform.objects.all()
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    initm = []
    for taq in storageassociation:
        # initm.append({'release':'', 'component': taq.component.description,'platform' : taq.platform.platformName,'firmware' : taq.firmware.firmwareName })
        print("sending pci_slot_name =", taq.storage_pcie_slots.pci_slot_name)
        print("sending i2c_dev_address =", taq.storage_pcie_slots.i2c_dev_address)
        print("sending i2c_channel =", taq.storage_pcie_slots.i2c_channel)
        print("sending unique_id =", taq.storage_pcie_slots.unique_id)
        print("sending chassis_pos =", taq.storage_pcie_slots.chassis_pos)
        print("sending vendor =", taq.storage_pcie_slots.vendor)

        initm.append({'pci_slot_name': taq.storage_pcie_slots.pci_slot_name, 'i2c_dev_address': taq.storage_pcie_slots.i2c_dev_address,
                      'i2c_channel': taq.storage_pcie_slots.i2c_channel, 'unique_id': taq.storage_pcie_slots.unique_id,
                      'chassis_pos': taq.storage_pcie_slots.chassis_pos, 'vendor': taq.storage_pcie_slots.vendor})



    response_data = {}
    response_data['allStorage'] = allStorage
    response_data['allPlatforms'] = allPlatforms
    response_data["allStorage"] = allStorage
    response_data['storage'] = storage
    response_data['allStorage_pcie_slots'] = allStorage_pcie_slots

    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response_data['initm'] = json.dumps(initm)
    response_data["storageassociation"] = storageassociation

    if request.method == 'POST':
        form = AddStorage(request.POST)
        if form.is_valid():
            storage.match = form.cleaned_data['match']
            storage.init = form.cleaned_data['init']
            storage.max_drives = form.cleaned_data['max_drives']
            storage.slot_map_strategy = form.cleaned_data['slot_map_strategy']
            platform = request.POST.getlist('platform')
            storage.platform.clear()

            sa_obj = StorageAssociation.objects.filter(storage=storageId)

            print("sa_obj = ", sa_obj)
            for sa in sa_obj:
                print("sa = ", sa, "sa.storage_pcie_slots = ", sa.storage_pcie_slots)
                sa.storage_pcie_slots.delete()

            sa_obj.delete()

            storage.save()

            for pcie_slot in g_pcie_slots:
                pci_slot_name = pcie_slot['pci_slot_name'].encode('UTF-8')
                i2c_dev_address = pcie_slot['i2c_dev_address'].encode('UTF-8')
                i2c_channel = pcie_slot['i2c_channel'].encode('UTF-8')
                unique_id = pcie_slot['unique_id'].encode('UTF-8')
                chassis_pos = pcie_slot['chassis_pos'].encode('UTF-8')
                vendor = pcie_slot['vendor'].encode('UTF-8')

                b = Storage_pcie_slots.objects.create(pci_slot_name=pci_slot_name, i2c_dev_address=i2c_dev_address,
                                                      i2c_channel=i2c_channel, unique_id=unique_id,
                                                      chassis_pos=chassis_pos,
                                                      vendor=vendor)
                b.save()

                c = StorageAssociation.objects.create(storage=storage, storage_pcie_slots=b)
                c.save()
                print("a =", storage, "b=", b, "c=", c)
            for plat in platform:
                p = Platform.objects.get(platformName=plat)
                storage.platform.add(p)
                storage.save()

            return render(request, 'components/storageindex.html', response_data)

    else:
        print("GET reguest received in addstorage is empty sending responce")
        #form = EditStorage()
    return render(request, 'components/modifystorage.html', response_data)


def deletestorage(request, storageId):
    print __name__ + ".py :", sys._getframe().f_code.co_name

    sa_obj = StorageAssociation.objects.filter(storage=storageId)

    print("sa_obj = ", sa_obj)
    for sa in sa_obj:
        print("sa = ", sa, "sa.storage_pcie_slots = ", sa.storage_pcie_slots)
        sa.storage_pcie_slots.delete()

    sa_obj.delete()

    Storage.objects.filter(pk=storageId).delete()

    response = {}

    allPlatforms = Platform.objects.all()
    allStorage = Storage.objects.all()
    allStorage_pcie_slots = Storage_pcie_slots.objects.all()
    storageassociation = StorageAssociation.objects.all()

    response["allPlatforms"] = allPlatforms
    response["allStorage"] = allStorage
    response["allStorage_pcie_slots"] = allStorage_pcie_slots
    response["storageassociation"] = storageassociation

    print(__name__ + ".py :", "= " + sys._getframe().f_code.co_name)
    print(response["storageassociation"])

    return render(request, 'components/storageindex.html', response)


def delete(request, componentId):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    MiscComponent.objects.filter(component_ptr_id=componentId).delete()
    return HttpResponseRedirect('/components/index/' + request.session['ws_name'] + "/" + request.session['release'])


def modify(request, componentId):
    allComponents = Component.objects.order_by('description')
    allPlatforms = Platform.objects.order_by('platformName')
    policyarea = PolicyAssociation.objects.filter(component=componentId)
    print __name__ + ".py :", sys._getframe().f_code.co_name

    legacy = 0
    # prepare responce data dictionary for the table to be displayed in JSON dynamically in javascript
    global gpolicy_table
    response_data = {}
    fanpolicy_options = {"1": "LOW_POWER_POLICY",
                         "2": "HIGH_POWER_POLICY",
                         "3": "BALANCED_POWER_POLICY",
                         "4": "MAX_POWER_POLICY",
                         }
    pci_attribute_options = [
        "ADAPTER_ATTRIBUTE_NIL",
        "OPROM_MUST_BE_EXECUTED",
        "OPROM_MUTUAL_EXCLUSIVE",
        "OPROM_FORCE_DISABLE_UEFI",
        "OPROM_FORCE_DISABLE_LEGACY",
        "OPROM_FORCE_ENABLE_UEFI",
        "OPROM_FORCE_ENABLE_LEGACY",
        "FORCE_DISABLE_ACS",
        "ALLOCATE_MMIO_ABOVE_4GB",
        "ADAPTER_SKIP_BIOS_ENUMERATION",
    ]

    # response_data['firmwareid'] = firmwareid

    call = Component.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()

    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)

    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)

    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    component = Component.objects.get(pk=componentId)

    try:
        misccomponent = MiscComponent.objects.get(component_ptr_id=componentId)
        pciattr = misccomponent.pci_attribute.encode('UTF-8')
        selected_pci_attr = pciattr.split(',')
        response_data['selected_pci_attr'] = selected_pci_attr
    except:
        print("Found a legacy Coomponent ")
        legacy = 1
        misccomponent = ''
        response_data['selected_pci_attr'] = ''

    initm = []
    if legacy == 1:
        for plat in allPlatforms:
            if plat in component.platform.all():
                print("sending platform =", plat)
                print ("sending fanpolicy =", "Null")
                print ("sending cardthresholdoffset ", "Null")
                initm.append({'platform': plat.platformName, 'fanpolicy': '',
                              'cardthresholdoffset': ''})

    for taq in policyarea:
        # initm.append({'release':'', 'component': taq.component.description,'platform' : taq.platform.platformName,'firmware' : taq.firmware.firmwareName })
        print("sending fanpolicy =", taq.policy.fanpolicy)
        print("sending card_threshold_offfset =", taq.policy.card_threshold_offset)
        initm.append({'platform': taq.platform.platformName, 'fanpolicy': taq.policy.fanpolicy,
                      'cardthresholdoffset': taq.policy.card_threshold_offset})

    response_data['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)
    response_data['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)
    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    response_data['initm'] = json.dumps(initm)

    response_data['allComponents'] = allComponents
    response_data['allPlatforms'] = allPlatforms
    response_data['component'] = component
    response_data['misccomponent'] = misccomponent
    response_data['pci_attribute_options'] = pci_attribute_options
    response_data['legacy'] = legacy

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditComponent(request.POST)
        # check whether it's valid:
        if form.is_valid():

            if (misccomponent == ''):
                # add a new misc component
                print("This is legacy component just modify the past value and add new value to component , data=",form.cleaned_data)
                component.vendorId = form.cleaned_data['vendorId']
                component.deviceId = form.cleaned_data['deviceId']
                component.subVendorId = form.cleaned_data['subVendorId']
                component.subDeviceId = form.cleaned_data['subDeviceId']
                component.device_type = "PCIE"


                component.uniqueName = form.cleaned_data['uniqueName']
                component.description = form.cleaned_data['description']


                component.packageVersion = form.cleaned_data.get('packageVersion')
                component.vendorString = form.cleaned_data.get('vendorString')
                component.save()

                component.platform.clear()

                pmin = form.cleaned_data.get('pmin')
                pmax = form.cleaned_data.get('pmax')
                pid = form.cleaned_data.get('pid')
                vid = form.cleaned_data.get('vid')
                sku = form.cleaned_data.get('sku')
                peripheral_type = form.cleaned_data.get('peripheral_type')
                no_of_temp_sensor = form.cleaned_data.get('no_of_temp_sensor')
                temp_sensor_i2cslaveaddr = form.cleaned_data.get('temp_sensor_i2cslaveaddr')
                # fanpolicy = form.cleaned_data.get('fanpolicy')
                secure_firmware_support = form.cleaned_data.get('secure_firmware_support')
                secure_firmware_update_i2cslaveaddr = form.cleaned_data.get('secure_firmware_update_i2cslaveaddr')
                command = form.cleaned_data.get('command')
                lock_payload = form.cleaned_data.get('lock_payload')
                unlock_payload = form.cleaned_data.get('unlock_payload')
                oem_part_number = form.cleaned_data.get('oem_part_number')
                # card_threshold_offset = form.cleaned_data.get('card_threshold_offset')
                part_number = form.cleaned_data.get('part_number')
                lff = form.cleaned_data.get('lff')
                fru_major_type = form.cleaned_data.get('fru_major_type')
                fru_minor_type = form.cleaned_data.get('fru_minor_type')
                pci_attrlist = request.POST.getlist('pci_attribute')
                mctp_supported = form.cleaned_data.get('mctp_supported')
                mctp_interfaces_supported = form.cleaned_data.get('mctp_interfaces_supported')
                oem_name = form.cleaned_data.get('oem_name')
                model = form.cleaned_data.get('model')
                pci_attribute = ''

                count = 0
                for p in pci_attrlist:
                    if (count == 0):
                        count = count + 1
                        pci_attribute = pci_attribute + p
                    else:
                        pci_attribute = pci_attribute + ',' + p

                print("pci_attribute =", pci_attribute, "pci_attribute_list=", pci_attrlist)
                # pci_attribute = form.cleaned_data.get('pci_attribute')
                #component.save()

                component = Component.objects.get(id=componentId)
                a = MiscComponent.objects.create(component_ptr_id=component.pk, pmin=pmin,vendorId=component.vendorId,
                                                 deviceId=component.deviceId, subVendorId=component.subVendorId ,
                                                 subDeviceId=component.subDeviceId ,
                                                 device_type=component.device_type , uniqueName=component.uniqueName,
                                                 description=component.description,
                                                 packageVersion=component.packageVersion, vendorString=component.vendorString,
                                                 pmax=pmax, pid=pid, vid=vid,
                                                 sku=sku, oem_part_number=oem_part_number, lff=lff, part_number=part_number,
                                                 peripheral_type=peripheral_type, no_of_temp_sensor=no_of_temp_sensor,
                                                 temp_sensor_i2cslaveaddr=temp_sensor_i2cslaveaddr,
                                                 secure_firmware_support=secure_firmware_support,
                                                 secure_firmware_update_i2cslaveaddr=secure_firmware_update_i2cslaveaddr,
                                                 command=command, lock_payload=lock_payload,
                                                 unlock_payload=unlock_payload, fru_major_type=fru_major_type,
                                                 fru_minor_type=fru_minor_type, pci_attribute=pci_attribute,
                                                 mctp_supported=mctp_supported, oem_name=oem_name, model=model,
                                                 mctp_interfaces_supported=mctp_interfaces_supported)
                a.save()



                print("****** MODIFY ****")
                print("Misccomoonent object created ")
                #print("****Misccomponent *** =",MiscComponent.objects.get(component_ptr_id=componentId))
                # get platform fanpolicy and cardthresholdoffset from global data and fill it to policy table
                for policy1 in gpolicy_table:
                    p = Platform.objects.get(platformName=policy1['platform'].encode('UTF-8'))
                    a.platform.add(p)
                    a.save()
                    fanpolicy = policy1['fanpolicy'].encode('UTF-8')
                    #card_threshold_offset = policy1['cardthresholdoffset'].encode('UTF-8')
                    card_threshold_offset = ""

                    po = Policy.objects.filter(fanpolicy=fanpolicy,
                                               card_threshold_offset=card_threshold_offset)

                    if (len(po) == 0):
                        print ("not exists : policy creating")
                        b = Policy.objects.create(fanpolicy=fanpolicy,
                                                  card_threshold_offset=card_threshold_offset)
                        b.save()
                    else:
                        print("policy already exists")
                        b = po[0]
                    # a is component b is policy and p is platform

                    policy = Policy.objects.get(id=b.id)
                    print("Policy is , type is ", policy, type(policy))
                    comp = Component.objects.get(id=a.component_ptr_id)
                    #print ("Component is , type is ", comp, type(comp))
                    policyassociation = PolicyAssociation.objects.create(component=comp, policy=policy, platform=p)
                    # policyassociation=PolicyAssociation(component=comp, policy=policy, platform=p)
                    policyassociation.save()


            else:
                misccomponent.vendorId = form.cleaned_data['vendorId']
                misccomponent.deviceId = form.cleaned_data['deviceId']
                misccomponent.subVendorId = form.cleaned_data['subVendorId']
                misccomponent.subDeviceId = form.cleaned_data['subDeviceId']
                misccomponent.uniqueName = form.cleaned_data['uniqueName']
                misccomponent.description = form.cleaned_data['description']

                misccomponent.packageVersion = form.cleaned_data.get('packageVersion')
                misccomponent.vendorString = form.cleaned_data.get('vendorString')
                misccomponent.device_type = "PCIE"
                misccomponent.save()

                misccomponent.pmin = form.cleaned_data.get('pmin')
                misccomponent.pmax = form.cleaned_data.get('pmax')
                misccomponent.pid = form.cleaned_data.get('pid')
                misccomponent.save()
                print("************************ saved misccomponent.pid =", misccomponent.pid, "**********pmax= ",
                      misccomponent.pmax)
                print("direct try with form in pid = ", form.cleaned_data.get('pid'), " for pmax =",
                      form.cleaned_data.get('pmax'))
                print("checking cleaned data =", form.cleaned_data)
                misccomponent.vid = form.cleaned_data.get('vid')
                misccomponent.sku = form.cleaned_data.get('sku')
                misccomponent.peripheral_type = form.cleaned_data.get('peripheral_type')
                misccomponent.no_of_temp_sensor = form.cleaned_data.get('no_of_temp_sensor')
                misccomponent.temp_sensor_i2cslaveaddr = form.cleaned_data.get('temp_sensor_i2cslaveaddr')
                # fanpolicy = form.cleaned_data.get('fanpolicy')
                misccomponent.secure_firmware_support = form.cleaned_data.get('secure_firmware_support')
                misccomponent.secure_firmware_update_i2cslaveaddr = form.cleaned_data.get(
                    'secure_firmware_update_i2cslaveaddr')
                misccomponent.command = form.cleaned_data.get('command')
                misccomponent.lock_payload = form.cleaned_data.get('lock_payload')
                misccomponent.unlock_payload = form.cleaned_data.get('unlock_payload')
                misccomponent.oem_part_number = form.cleaned_data.get('oem_part_number')
                misccomponent.part_number = form.cleaned_data.get('part_number')
                misccomponent.lff = form.cleaned_data.get('lff')
                # card_threshold_offset = form.cleaned_data.get('card_threshold_offset')
                misccomponent.fru_major_type = form.cleaned_data.get('fru_major_type')
                misccomponent.fru_minor_type = form.cleaned_data.get('fru_minor_type')

                misccomponent.mctp_supported = form.cleaned_data.get('mctp_supported')
                misccomponent.mctp_interfaces_supported = form.cleaned_data.get('mctp_interfaces_supported')
                misccomponent.model = form.cleaned_data.get('model')
                misccomponent.oem_name = form.cleaned_data.get('oem_name')

                misccomponent.save()
                # print("intentionally error"+misccomponent.fru_minor_type)

                pci_attrlist = request.POST.getlist('pci_attribute')

                count = 0
                pci_attribute = ''
                for p in pci_attrlist:
                    if (count == 0):
                        count = count + 1
                        pci_attribute = pci_attribute + p
                    else:
                        pci_attribute = pci_attribute + ',' + p

                # misccomponent.pci_attribute.clear()
                misccomponent.pci_attribute = pci_attribute
                misccomponent.save()
                # do here for updation work
                misccomponent.platform.clear()
                policyassociations = PolicyAssociation.objects.filter(component=component)
                policyassociations.delete()

                for policy1 in gpolicy_table:
                    p = Platform.objects.get(platformName=policy1['platform'].encode('UTF-8'))
                    misccomponent.platform.add(p)
                    misccomponent.save()

                    fanpolicy = policy1['fanpolicy'].encode('UTF-8')
                    #card_threshold_offset = policy1['cardthresholdoffset'].encode('UTF-8')
                    card_threshold_offset = ""

                    po = Policy.objects.filter(fanpolicy=fanpolicy,
                                               card_threshold_offset=card_threshold_offset)

                    if (len(po) == 0):
                        print ("not exists : policy creating")
                        b = Policy.objects.create(fanpolicy=fanpolicy,
                                                  card_threshold_offset=card_threshold_offset)
                        b.save()
                    else:
                        print("policy already exists")
                        b = po[0]
                    # a is component b is policy and p is platform

                    policy = Policy.objects.get(id=b.id)
                    print("Policy is , type is ", policy, type(policy))
                    comp = Component.objects.get(id=misccomponent.component_ptr_id)
                    print ("Component is , type is ", comp, type(comp))

                    policyassociation = PolicyAssociation.objects.create(component=comp, policy=policy, platform=p)
                    # policyassociation=PolicyAssociation(component=comp, policy=policy, platform=p)
                    policyassociation.save()

            return HttpResponseRedirect(
                '/components/index/' + request.session['ws_name'] + "/" + request.session['release'])
        # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = EditComponent()
    return render(request, 'components/modify.html', response_data)


def discoveryHookEdit(request, componentId='', discoveryHookId=''):
    print __name__ + ".py :", sys._getframe().f_code.co_name
    response_data = {}
    discoveryhookdir = os.path.join(request.session['ws_path'], 'deltas/post-build/rootfs/root/CBL/Hooks/')
    fname = ''

    print("in discoveryHookEdit passed with arg componentid", componentId, " discoveryHookID =", discoveryHookId,
          "discoveryhookdir=", discoveryhookdir)

    if request.method == 'POST':
        print ">>>>>>", request.POST.get('dhookName')
        components = request.POST.getlist('components')
        dhookName = request.POST.get('dhookName')
        dplatform = request.POST.get('dplatform')
        fname = os.path.join(discoveryhookdir, dhookName + '.py')
        with open(fname, "w+") as f:
            f.write(request.POST.get('dpreHook'))
        try:
            dhook = DiscoveryHook.objects.filter(dhookName=dhookName).delete()
        except:
            DatabaseError
        #         for comp in components:
        #             component = Component.objects.get(uniqueName=comp)
        # #                 for plat in dplatform:
        #             DiscoveryHook.objects.create(dcomp=component, dcomponentId=component.id, id=discoveryHookId,
        #                                                  dhookName=dhookName)
        try:
            for comp in components:
                component = Component.objects.get(uniqueName=comp)
                #                 for plat in dplatform:
                DiscoveryHook.objects.create(dcomp=component, dcomponentId=component.id, id=discoveryHookId,
                                             dhookName=dhookName)
        except:
            DatabaseError

        return HttpResponseRedirect('/components/hooks/')

    form = DiscoveryEdit()
    try:
        dhook = DiscoveryHook.objects.get(id=discoveryHookId)
        component = Component.objects.get(id=dhook.dcomp.id)
        print("dhookname type=", type(dhook))
    # print("dhookname =",dhook.dhookName.encode('UTF-8'),"dhook type=",type(dhook),"component=",component)
    # dhook=
    except:
        dhook = ''
        component = ''
    if fname == '':
        # fname = os.path.join(settings.BASE_DIR,'hook.py')
        print discoveryhookdir.encode('UTF-8')
        print dhook.dhookName.encode('UTF-8')
        fname = os.path.join(discoveryhookdir.encode('UTF-8'), dhook.dhookName.encode('UTF-8') + '.py')
        print ("fname =", fname)
    with open(fname) as f:
        hook = f.read()
        # hook=''
        print("filename =", fname, "hook=", hook, "settings.ws_path", settings.ws_path)
    try:
        all_component = Component.objects.all()
    except:
        all_component = ''
    try:
        all_platforms = Platform.objects.all()
    except:
        all_platforms = ''
    try:
        component = Component.objects.get(id=dhook.dcomp.id)
    except:
        component = ''
    try:
        sel_comp = DiscoveryHook.objects.filter(dhookName=dhook.dhookName)
        sel_components = []
        for comp in sel_comp:
            print "&&&&", comp.dcomp.uniqueName
            if comp.dcomp.uniqueName not in sel_components:
                sel_components.append(comp.dcomp.uniqueName)
        sel_platforms = []
        for comp in sel_comp:
            print "****", comp.dcomp.uniqueName
            if comp.dcomp.uniqueName not in sel_platforms:
                sel_platforms.append(comp.dcomp.uniqueName)
    except:
        DatabaseError
        sel_components = ''
        sel_platforms = ''
    print ">>>>>>>>>...........", component.platform
    response_data['hook'] = hook
    response_data['dhook'] = dhook
    response_data['all_component'] = all_component
    response_data['component'] = component
    response_data['componentId'] = componentId
    response_data['discoveryHookId'] = discoveryHookId
    response_data['all_platforms'] = all_platforms
    response_data['sel_components'] = sel_components

    return render(request, 'components/discoveryhookmodify.html', response_data)


# def discoveryHookEdit(request, componentId, discoveryHookId):
#     response_data = {}
#     discoveryhookdir = os.path.join(request.session['ws_path'],'deltas/post-build/rootfs/root/CBL/') 
#     fname = ''
#     component = Component.objects.get(id=componentId)
# #     try:
# #         dhook = DiscoveryHook.objects.get(dcomp=component, dcomponentId=componentId, id=discoveryHookId)
# #         
# #     except DiscoveryHook.DoesNotExist:
# #         dhook = ''
#     fname = os.path.join(discoveryhookdir,dhook.dhookName+'.py')
#     if request.method == 'POST':
# #         if dhook!='':
#         components = request.POST.get('components')
#         dhookName = request.POST.get('dhookName')   
# #             dhook.dhookName = request.POST.get('dhookName')
# #             dhook.dpreHook = request.POST.get('dpreHook')
# #             dhook.dplatform = request.POST.get('dplatform')
# #             dhook.save()
# #             hook = dhook.dpreHook
#             fname = os.path.join(discoveryhookdir,dhookName+'.py')
#             with open(fname,"w+") as f:
#                     f.write(request.POST.get('dpreHook'))
#             return HttpResponseRedirect('/components/hookdisc/'+componentId)
# #         else:
# #             dhookName =  request.POST.get('dhookName')
# #             dpreHook = request.POST.get('dpreHook')
# #             dplatform = request.POST.get('dplatform')
# #             d = DiscoveryHook.objects.create(dcomp=component, dcomponentId=componentId, id=discoveryHookId,
# #                                                  dhookName=dhookName, dpreHook=dpreHook, dplatform=dplatform)
# #             d.save()
# #             hook = dpreHook
# #             fname = os.path.join(discoveryhookdir,dhookName+'.py')
# #             with open(fname,"w+") as f:
# #                 f.write(request.POST.get('dpreHook'))
# #             
# #             return HttpResponseRedirect('/components/hookdisc/' + componentId)
#     
#     form = DiscoveryEdit()
#     if fname == '':
#         fname = os.path.join(settings.BASE_DIR,'hook.py')
#     with open(fname) as f:
#         hook=f.read()
#     try:
#         all_component = Component.objects.all()
#     except:
#         all_component = ''
#     try:
#         all_platforms = Platform.objects.all()
#     except:
#         all_platforms = ''
#     
#     response_data['hook'] = hook
#     response_data['dhook'] = dhook
#     response_data['all_component'] = all_component
#     response_data['component'] = component
#     response_data['componentId'] = componentId
#     response_data['discoveryHookId'] = discoveryHookId
#     response_data['all_platforms'] = all_platforms
#     
#     return render(request, 'components/discoveryhookmodify.html', response_data)


def discoveryHookDelete(request, componentId, discoveryHookId):
    discoveryhookdir = os.path.join(request.session['ws_path'], 'deltas/post-build/rootfs/root/CBL/Hooks/')
    dhook = DiscoveryHook.objects.get(id=discoveryHookId)
    os.remove(discoveryhookdir + dhook.dhookName + '.py')
    DiscoveryHook.objects.filter(id=discoveryHookId).delete()
    return HttpResponseRedirect('/components/hookdisc/' + componentId)


def discoveryHookList(request, componentId):
    component = Component.objects.get(id=componentId)
    dhookn = DiscoveryHook.objects.create(dcomp=component)
    dhooknew = dhookn.id
    DiscoveryHook.objects.filter(id=dhooknew).delete()
    discoveryHooks = DiscoveryHook.objects.filter(dcomp=component)
    return render(request, 'components/discoveryhooklist.html',
                  {'discoveryHooks': discoveryHooks, 'component': component, 'dhooknew': dhooknew})


def updateHookEdit(request, componentId, updateHookId):
    component = Component.objects.get(id=componentId)
    # os.path.isfile(request.POST.get('hookName'))

    try:
        hook = UpdateHook.objects.get(comp=component, componentId=componentId, id=updateHookId)
    except UpdateHook.DoesNotExist:
        hook = ''
    if request.method == 'POST':
        if hook != '':
            # create a form instance and populate it with data from the request:
            hook.hookName = 'update_' + request.POST.get('hookName')
            hook.preHook = request.POST.get('preHook')
            hook.inHook = request.POST.get('inHook')
            hook.postHook = request.POST.get('postHook')
            hook.platform = request.POST.get('platform')
            hook.save()
            shutil.copy2(basedir + 'update.py', updatehookdir + hook.hookName + '.py')
            for line in fileinput.input(updatehookdir + hook.hookName + '.py', inplace=1):
                print line,
                if line.startswith('/*insert prehook here*/'):
                    print '\n' + hook.preHook + '\n'
                if line.startswith('/*insert inhook here*/'):
                    print '\n' + hook.inHook + '\n'
                if line.startswith('/*insert posthook here*/'):
                    print'\n' + hook.postHook + '\n'

            return HttpResponseRedirect('/components/hookupdt/' + componentId)
        else:
            hookName = 'update_' + request.POST.get('hookName')
            preHook = request.POST.get('preHook')
            inHook = request.POST.get('inHook')
            postHook = request.POST.get('postHook')
            platform = request.POST.get('platform')
            h = UpdateHook.objects.create(comp=component, componentId=componentId, id=updateHookId,
                                          hookName=hookName, preHook=preHook, inHook=inHook,
                                          postHook=postHook, platform=platform)
            h.save()
            shutil.copy2(basedir + 'update.py',
                         updatehookdir + h.hookName + '.py')
            for line in fileinput.input(updatehookdir + h.hookName + '.py', inplace=1):
                print line,
                if line.startswith('/*insert prehook here*/'):
                    print '\n' + h.preHook + '\n'
                if line.startswith('/*insert inhook here*/'):
                    print '\n' + h.inHook + '\n'
                if line.startswith('/*insert posthook here*/'):
                    print'\n' + h.postHook + '\n'

            return HttpResponseRedirect('/components/hookupdt/' + componentId)
            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

            # if a GET (or any other method) we'll create a blank form
    else:
        form = UpdateEdit()
    return render(request, 'components/updatehookmodify.html',
                  {'hook': hook, 'component': component, 'componentId': componentId, 'updateHookId': updateHookId})


def updateHookDelete(request, componentId, updateHookId):
    uhook = UpdateHook.objects.get(id=updateHookId)
    os.remove(updatehookdir + uhook.hookName + '.py')
    UpdateHook.objects.filter(id=updateHookId).delete()

    return HttpResponseRedirect('/components/hookupdt/' + componentId)


def updateHookList(request, componentId):
    component = Component.objects.get(id=componentId)
    hookn = UpdateHook.objects.create(comp=component)
    hooknew = hookn.id
    UpdateHook.objects.filter(id=hooknew).delete()
    updateHooks = UpdateHook.objects.filter(comp=component)
    return render(request, 'components/updatehooklist.html',
                  {'updateHooks': updateHooks, 'component': component, 'hooknew': hooknew})


def popdb(request):
    allComponents = Component.objects.all()
    for a in fileinput.input(basedir + 'db.txt', inplace=1):
        vendorId = ''
        deviceId = ''
        subVendorId = ''
        subDeviceId = ''
        uniqueName = ''
        description = ''
        dsc_scr = ''
        upd_scr = ''
        #exists = ''
        packageVersion = ''
        platform = ''
        vendorString = ''
        tools = ''
        firmware = ''
        verifyApi = ''
        d = [vendorId, deviceId, subVendorId, subDeviceId, uniqueName, description, dsc_scr, upd_scr,
             packageVersion, platform, vendorString,
             tools, firmware, verifyApi]
        b = a.split(",")
        for i in range(0, 15):
            c = b[i].split('"')
            if c[0] == 'false':
                d[i] = False
            elif c[0] == 'NULL':
                d[i] = c[0]
            elif c[0] == 'true':
                d[i] = True
            else:
                d[i] = c[1]

        component = Component.objects.create(vendorId=d[0], deviceId=d[1], subVendorId=d[2], subDeviceId=d[3],
                                             uniqueName=d[4], description=d[5], packageVersion=d[11],
                                             vendorString=d[14])
        component.save()
        e = d[12].split("-")
        for plat in e:
            platfor, creat = Platform.objects.get_or_create(platformName=plat)
            platfor.save()
            platfor.component_set.add(component)
            platfor.save()

    return render(request, 'components/index.html', {'allComponents': allComponents})


def addtool(request, tool_id='',vendorsel=''):
    response_data = {}
    categories = ['Storage', 'Category2', 'Category3', 'Category4']
    tool = ''
    # allComponents = Adaptor.objects.order_by('comp')
    # allPlatforms = Platform.objects.order_by('platformName')
    allComponents = Component.objects.order_by('description')

    if request.method == 'POST' and request.is_ajax():
        vendorId = request.POST.get('vendorId')
        print('I am in addtool post and got vendorId as ',vendorId)
        deviceId = 'Jatin'
        data = {'data':deviceId}
        return HttpResponse(json.dumps(data), content_type="application/json")

    '''
        if bool(vendorsel):
            print(vendorsel)
            pciIds = os.path.join(settings.BASE_DIR, 'pci.ids')
            with open(pciIds) as file:
                for line in file:
                    if not line.startswith('\t') and not line.startswith('#'):
                        if len(line) != 0:
                            pcilist = line.encode('utf-8').strip().split('  ', 1)
                            # print(pcilist)
                            if len(pcilist) > 1:
                                settings.pci_sig_lst.append(pcilist[0].encode('utf-8') + '_' + pcilist[1].encode('utf-8'))
                                settings.pci_sig_dict[pcilist[0].encode('utf-8')] = [pcilist[1].encode('utf-8')]'''

    if request.method == 'POST':
        #         category = request.POST['category']
        document = request.FILES['document']

        toolName = request.POST['toolName']  # + extension
        version = request.POST['version']
        vendorstr = request.POST['vendorId']
        devicestr = request.POST['deviceId']
        subVendorstr = request.POST['subVendorId']
        subDevicestr = request.POST['subDeviceId']

        #get vendor id by vendor name
        vendorId = vendorstr.split()


        pattern = re.compile(vendorId, re.IGNORECASE)
        with open('pci.ids', encoding='utf-8') as file:
            for linenum, line in enumerate(file):
                if pattern.search(line) != None:
                    if not line.startswith('\t'):
                        print(linenum, line.rstrip('\n'))
                        vendorName = line.rstrip('\n').split()[1]






        filepath = os.path.join(request.session['ws_path'], 'third_party/tools_rhel', upload_path.strip('/'),
                                toolName.strip('/'))  # .replace("\\","/")
        u_path = os.path.join(request.session['ws_path'], 'third_party/tools_rhel', upload_path.strip('/'))
        if not os.path.exists(u_path):
            os.makedirs(u_path)
        location = filepath, u_path
        print ">>>>>>>>>>", filepath

        if tool_id == '':
            print("Creating New Tool")
            newtool = Tool.objects.create(toolName=toolName, location=upload_path, softLocation=destination)
            newtool.save()
        else:
            print("using existing tool toolid=%s",str(tool_id))
            oldtool = Tool.objects.get(id=tool_id)
            oldtool.toolName = toolName
            oldtool.location = upload_path
            oldtool.softLocation =  destination
            oldtool.uploaded_at = timezone.now()
            oldtool.save()

        '''for plat in platform:
            p = Platform.objects.get(id=plat)
            newtool.platform.add(p)
            newtool.save()'''
        with open(filepath, 'wb+') as dest:
            for chunk in document.chunks():
                print(chunk)
                dest.write(chunk)
        # msg = "Success"
        # return HttpResponse(msg)
        return HttpResponseRedirect('/components/toollist/')
    # return render(request, 'components/addcomponent.html', {'allComponents': allComponents})

    # if a GET (or any other method) we'll create a blank form
    if tool_id:
        try:
            tool = Tool.objects.get(id=tool_id)
        except:
            tool = ''
    response_data['tool'] = tool
    response_data['categories'] = categories
    response_data['allComponents'] = allComponents
    response_data['allVendors'] =  settings.pci_sig_lst
    return render(request, 'components/addtool.html', response_data)


def platformDelete(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        platformid = request.POST.get('platformid')
        try:
            plat = Platform.objects.get(id=platformid)
            platn = plat.platformName
        except:
            msg = "Platform couldn't be found"
        plat.delete()
        msg = "Platform " + platn + " deleted."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listplatform.html', response_data)


def platformEdit(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        platformid = request.POST.get('platformid')
        platformName = request.POST.get('platformName')
        try:
            plat = Platform.objects.get(id=platformid)
            platn = plat.platformName
        except:
            msg = "Platform couldn't be found"
        plat.platformName = platformName
        msg = "Platform " + platn + " Edited to " + plat.platformName + "."
        plat.save()
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listplatform.html', response_data)


def listplatform(request):
    allPlatforms = Platform.objects.order_by('platformName')
    return render(request, 'components/listplatform.html', {'allPlatforms': allPlatforms})


def platformadd(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        platformName = request.POST.get('platformName')
        try:
            plat = Platform.objects.create(platformName=platformName)
        except:
            msg = "Platform couldn't be created"
        msg = "Platform " + plat.platformName + " Added."
        plat.save()
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listplatform.html', response_data)


def releaseDelete(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        releaseid = request.POST.get('releaseid')
        try:
            rel = Release.objects.get(id=releaseid)
            reln = rel.releaseName
        except:
            msg = "Release couldn't be found"
        rel.delete()
        msg = "Release " + reln + " deleted."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listrelease.html', response_data)


def releaseEdit(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        releaseid = request.POST.get('releaseid')
        releaseName = request.POST.get('releaseName')
        platform = json.loads(request.POST.get('platform'))
        try:
            rel = Release.objects.get(id=releaseid)
            reln = rel.releaseName
        except:
            msg = "Release couldn't be found"

        rel.platforms.clear()
        for plat in platform:
            p = Platform.objects.get(platformName=plat)
            rel.platforms.add(p)
            rel.save()
        rel.releaseName = releaseName
        msg = "Release " + reln + " Edited to " + rel.releaseName + "."
        rel.save()
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listrelease.html', response_data)


def listrelease(request):
    allReleases = Release.objects.all()
    allPlatforms = Platform.objects.order_by('platformName')
    return render(request, 'components/listrelease.html', {'allReleases': allReleases, 'allPlatforms': allPlatforms})


def releaseadd(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        releaseName = request.POST.get('releaseName')
        platform = json.loads(request.POST.get('platform'))
        try:
            rel = Release.objects.create(releaseName=releaseName)
        except:
            msg = "release couldn't be created"
        rel.save()
        for plat in platform:
            p = Platform.objects.get(platformName=str(plat))
            rel.platforms.add(p)
            rel.save()
        msg = "release " + rel.releaseName + " Added."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/listrelease.html', response_data)


def toolDelete(request, toolid):
    Tool.objects.filter(id=toolid).delete()
    return HttpResponseRedirect('/components/toollist/')


def toolEdit(request, toolid):
    tool = Tool.objects.get(id=toolid)
    response_data = {}
    response_data['toolid'] = toolid
    call = Component.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()
    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)
    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)
    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    response_data['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)

    response_data['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)

    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    t = Tool.objects.get(id=toolid)
    toola = ToolAssociation.objects.filter(tool=t)
    initm = []
    init = {}
    i = 0
    for taq in toola:
        initm.append({'release': '', 'component': taq.component.description, 'platform': taq.platform.platformName,
                      'tool': taq.tool.toolName})
    response_data['initm'] = json.dumps(initm)

    if request.method == 'POST' and request.is_ajax():
        tools_association = json.loads(request.POST.get('tools_association'))
        try:
            toola.delete()
        except:
            msg = "objects not deleted from table tool association"
        for tool_a in tools_association:
            rel = Release.objects.get(releaseName=tool_a['release'])
            plat = Platform.objects.get(platformName=tool_a['platform'])
            comp = Component.objects.get(description=tool_a['component'])
            toolassociation = ToolAssociation(tool=t, release=rel, component=comp, platform=plat)
            toolassociation.save()
        msg = "tool " + tool.toolName + " associated with " + rel.releaseName + " " + plat.platformName + " " + comp.description + "."

        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/tooledit.html', response_data)


def toollist(request):
    categories = ['Storage', 'Category2', 'Category3', 'Category4']
    allTools = Tool.objects.order_by('toolName')
    return render(request, 'components/toollist.html', {'allTools': allTools, 'categories': categories})


def tooladd(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        toolName = request.POST.get('releaseName')
        category = request.POST['category']
        document = request.FILES['document']
        platform = json.loads(request.POST.get('platform'))
        # extension = os.path.splitext(document.name)[1]
        toolName = request.POST['toolName']  # + extension
        filepath = os.path.join(toolbasedir, category, toolName).replace("\\", "/")
        if not os.path.exists(os.path.join(toolbasedir, category).replace("\\", "/")):
            os.makedirs(os.path.join(toolbasedir, category).replace("\\", "/"))
        location = filepath
        try:
            newtool = Tool.objects.create(toolName=toolName, category=category, location=location,
                                          softLocation=location)
        except:
            msg = "Tool can't be saved"
        newtool.save()
        for plat in platform:
            p = Platform.objects.get(id=plat)
            newtool.platform.add(p)
            newtool.save()
        with open(filepath, 'wb+') as destination:
            for chunk in document.chunks():
                destination.write(chunk)
        msg = "tool " + newtool.toolName + " Added."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/toollist.html', response_data)


def firmwareDelete(request, firmwareid):
    Firmware.objects.filter(id=firmwareid).delete()
    return HttpResponseRedirect('/components/firmwarelist/')


def firmwareEdit(request, firmwareid):
    response_data = {}
    response_data['firmwareid'] = firmwareid
    call = Component.objects.all()
    rall = Release.objects.all()
    pall = Platform.objects.all()
    ctrlOptionsComp = []
    for c in call:
        ctrlOptionsComp.append(c.description)
    ctrlOptionsRel = []
    for r in rall:
        ctrlOptionsRel.append(r.releaseName)
    ctrlOptionsPlat = []
    for p in pall:
        ctrlOptionsPlat.append(p.platformName)

    response_data['ctrlOptionsComp'] = json.dumps(ctrlOptionsComp)

    response_data['ctrlOptionsRel'] = json.dumps(ctrlOptionsRel)

    response_data['ctrlOptionsPlat'] = json.dumps(ctrlOptionsPlat)
    t = Firmware.objects.get(id=firmwareid)
    firmwarea = FirmwareAssociation.objects.filter(firmware=t)
    initm = []
    for taq in firmwarea:
        initm.append({'release': '', 'component': taq.component.description, 'platform': taq.platform.platformName,
                      'firmware': taq.firmware.firmwareName})
    response_data['initm'] = json.dumps(initm)

    if request.method == 'POST' and request.is_ajax():
        firmwares_association = json.loads(request.POST.get('firmwares_association'))
        try:
            firmwarea.delete()
        except:
            msg = "objects not deleted from table firmware association"
        for firmware in firmwares_association:
            try:
                rel = Release.objects.get(releaseName=firmware['release'])
                plat = Platform.objects.get(platformName=firmware['platform'])
                comp = Component.objects.get(description=firmware['component'])
                firmwareassociation = FirmwareAssociation(firmware=t, release=rel, component=comp, platform=plat)
                firmwareassociation.save()
                msg = "Firmware " + firmware.firmwareName + " associated with " + plat.platformName + " " + comp.description + "."
            except:
                msg = "Firmware association failed."
        msg = "Firmware associated successfully"
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'components/firmwareedit.html', response_data)


def firmwarelist(request):
    categories = ['Storage', 'Category2', 'Category3', 'Category4']
    allFirmwares = Firmware.objects.order_by('firmwareName')
    '''
    'firmwareassociation':firmwareassociation, 'allPlatforms':allPlatforms, 'allComponents':allComponents, 'allReleases':allReleases,
    allReleases = Release.objects.order_by('releaseName')
    allComponents = Component.objects.order_by('uniqueName')
    allPlatforms = Platform.objects.order_by('platformName')
    firmwareassociation = FirmwareAssociation.objects.all()
    '''
    return render(request, 'components/firmwarelist.html', {'allFirmwares': allFirmwares, 'categories': categories})


def firmwareadd(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        firmwareName = request.POST.get('releaseName')
        category = request.POST['category']
        document = request.FILES['document']
        platform = json.loads(request.POST.get('platform'))
        # extension = os.path.splitext(document.name)[1]
        firmwareName = request.POST['firmwareName']  # + extension
        filepath = os.path.join(firmwarebasedir, category, firmwareName).replace("\\", "/")
        if not os.path.exists(os.path.join(firmwarebasedir, category).replace("\\", "/")):
            os.makedirs(os.path.join(firmwarebasedir, category).replace("\\", "/"))
        location = filepath
        try:
            newfirmware = Firmware.objects.create(firmwareName=firmwareName, category=category, location=location,
                                                  softLocation=location)
        except:
            msg = "firmware can't be saved"
        newfirmware.save()
        for plat in platform:
            p = Platform.objects.get(id=plat)
            newfirmware.platform.add(p)
            newfirmware.save()
        with open(filepath, 'wb+') as destination:
            for chunk in document.chunks():
                destination.write(chunk)
        msg = "Firmware " + newfirmware.firmwareName + " added."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    return render(request, 'components/firmwarelist.html', response_data)


def addfirmware(request, firmware_id=''):
    response_data = {}
    firmware = ''
    # allComponents = Adaptor.objects.order_by('comp')
    # allPlatforms = Platform.objects.order_by('platformName')
    if request.method == 'POST':
        document = request.FILES['document']
        firmwareName = request.POST['firmwareName']
        destination = request.POST['destination']
        upload_path = request.POST['upload_path']

        filepath = os.path.join(request.session['ws_path'], 'third_party/tools_rhel', upload_path.strip('/'),
                                firmwareName.strip('/'))  # .replace("\\","/")
        u_path = os.path.join(request.session['ws_path'], 'third_party/tools_rhel', upload_path.strip('/'))
        if not os.path.exists(u_path):
            os.makedirs(u_path)
        location = filepath

        if firmware_id == '':
            print("Creating New Firmware")
            newfirmware = Firmware.objects.create(firmwareName=firmwareName, location=upload_path, softLocation=destination)
            newfirmware.save()
        else:
            print("Using Old Firmware")
            oldfirmware =  Firmware.objects.get(id=firmware_id)
            oldfirmware.firmwareName = firmwareName
            oldfirmware.location = upload_path
            oldfirmware.softLocation = destination
            oldfirmware.uploaded_at = timezone.now()
            oldfirmware.save()

        with open(filepath, 'wb+') as destination:
            for chunk in document.chunks():
                destination.write(chunk)

        return HttpResponseRedirect('/components/firmwarelist')
    if firmware_id:
        try:
            firmware = Firmware.objects.get(id=firmware_id)
        except:
            firmware = ''
    response_data['firmware'] = firmware
    return render(request, 'components/addfirmware.html', response_data)


def hooks(request):
    response_data = {}
    from django.db.models import Count
    try:
        discovery_hook = DiscoveryHook.objects.all()
        li = []
        dis_hook = []
        for h in discovery_hook:
            if not h.dhookName in li:
                dis_hook.append(h)
                li.append(h.dhookName)
    except:
        discovery_hook = ''
        DatabaseError

    try:
        update_hook = UpdateHook.objects.all()
    except:
        update_hook = ''
        DatabaseError
    try:
        hook_list = DiscoveryHook.objects.values('dhookName').distinct()
        # raw('SELECT DISTINCT dhookName FROM components_discoveryhook;')#distinct('dhookName')
    except:
        discovery_hook = ''
        DatabaseError
    hook_list = []
    #     for dis in discovery_hook:
    #         if dis.dhookName in hook_list:
    #             del(discovery_hook.dis)

    response_data['discovery_hook'] = dis_hook
    response_data['update_hook'] = update_hook
    response_data['hook_list'] = 'all'
    return render(request, 'components/hooks.html', response_data)


def downloadjson(request):
    ws_path = request.session['ws_path']
    if 'platform' in request.GET:
        message = 'You searched for: %r' % request.GET['platform']
    else:
        message = 'You submitted an empty form.'
    print(message)
    platform = request.GET['platform']
    print(platform)
    content_disposition = 'attachment; filename=' + str(platform) + ".json"

    os.system("rm " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(platform) + "_catalog.json")
    print(
            "python2.7 " + ws_path + "/deltas/post-build/rootfs/root/CBL/Utilities/CBL_Db2Json.py " + ws_path + "/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3 " + str(
        platform).upper() + " > " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(
        platform) + "_catalog.json")
    os.system(
        "python2.7 " + ws_path + "/deltas/post-build/rootfs/root/CBL/Utilities/CBL_Db2Json.py " + ws_path + "/deltas/post-build/rootfs/root/CBL/DB/db.sqlite3 " + str(
            platform).upper() + " > " + ws_path + "/deltas/post-build/rootfs/root/CBL/JSON/" + str(
            platform) + "_catalog.json")

    json_data = open(ws_path + '/deltas/post-build/rootfs/root/CBL/JSON/' + str(platform) + '_catalog.json', "r").read()
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = content_disposition
    return response

from django import forms
from django.forms import ModelForm
from components.models import Component, DiscoveryHook, UpdateHook, PSU, MiscComponent, CPU, Memory, Storage, Nvme


class EditComponent(ModelForm):
    vendorId = forms.CharField(max_length=5)
    deviceId = forms.CharField(max_length=5)
    subVendorId = forms.CharField(max_length=5)
    subDeviceId = forms.CharField(max_length=5)
    uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)
    vendorString = forms.CharField(max_length=64, required=False)
    platform = forms.CharField(max_length=1024, required=False)
    vid = forms.CharField(max_length=64, required=False)

    # verifyApi = forms.CharField(max_length=1500, required=False)  # check with velu
    pmax = forms.CharField(max_length=5, required=False)
    pmin = forms.CharField(max_length=5, required=False)
    pid = forms.CharField(max_length=100, required=True)
    #version_id = forms.CharField(max_length=50, required=True)
    sku = forms.CharField(max_length=100, required=True)
    oem_part_number = forms.CharField(max_length=100, required=True)
    part_number = forms.CharField(max_length=100, required=True)
    lff = forms.CharField(max_length=100, required=True)
    peripheral_type = forms.CharField(max_length=100, required=True)
    no_of_temp_sensor = forms.CharField(max_length=100, required=True)
    temp_sensor_i2cslaveaddr = forms.CharField(max_length=100, required=True)
    # fanpolicy = forms.CharField(max_length=100, required=False)
    secure_firmware_support = forms.CharField(max_length=100, required=False)
    secure_firmware_update_i2cslaveaddr = forms.CharField(max_length=100, required=False)
    command = forms.CharField(max_length=100, required=False)
    lock_payload = forms.CharField(max_length=100, required=False)
    unlock_payload = forms.CharField(max_length=100, required=False)
    # card_threshold_offset = forms.CharField(max_length=100, required=False)
    fru_major_type = forms.CharField(max_length=100, required=True)
    fru_minor_type = forms.CharField(max_length=100, required=True)
    pci_attribute = forms.CharField(max_length=100, required=False)
    mctp_supported = forms.CharField(max_length=100, required=False)
    mctp_interfaces_supported = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = MiscComponent
        fields = (
            'vendorId', 'deviceId', 'subVendorId', 'subDeviceId', 'uniqueName', 'description',
            'packageVersion',
            'vendorString', 'pmin', 'pmax', 'pid', 'vid', 'sku', 'oem_part_number', 'part_number', 'lff', 'peripheral_type',
            'no_of_temp_sensor', 'model', 'oem_name',
            'temp_sensor_i2cslaveaddr', 'secure_firmware_support', 'secure_firmware_update_i2cslaveaddr', 'command',
            'lock_payload', 'unlock_payload', 'fru_major_type', 'fru_minor_type', 'pci_attribute', 'mctp_supported',
            'mctp_interfaces_supported')  # ,'verifyApi')


'''
class AddCPU(ModelForm):
class AddMemory(ModelForm):
'''
class AddNvme(ModelForm):
    match = forms.CharField(max_length=100, required=False)
    init = forms.CharField(max_length=100, required=False)
    max_drives = forms.CharField(max_length=100, required=False)
    slot_map_strategy = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Nvme
        fields = ('match', 'init', 'max_drives', 'slot_map_strategy')


class EditNvme(ModelForm):
    match = forms.CharField(max_length=100, required=False)
    init = forms.CharField(max_length=100, required=False)
    max_drives = forms.CharField(max_length=100, required=False)
    slot_map_strategy = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Nvme
        fields = ('match', 'init', 'max_drives', 'slot_map_strategy')

class AddPSU(ModelForm):
    psu_model_type = forms.CharField(max_length=100, required=False)
    psu_description = forms.CharField(max_length=100, required=False)
    psu_vendor_name = forms.CharField(max_length=100, required=False)
    psu_part_number = forms.CharField(max_length=100, required=False)
    max_power_wattage = forms.CharField(max_length=100, required=False)
    min_correction_time = forms.CharField(max_length=100, required=False)

    class Meta:
        model = PSU
        fields = ('psu_model_type', 'psu_description', 'psu_vendor_name', 'psu_part_number', 'max_power_wattage',
                  'min_correction_time')


class EditPSU(ModelForm):
    psu_model_type = forms.CharField(max_length=100, required=False)
    psu_description = forms.CharField(max_length=100, required=False)
    psu_vendor_name = forms.CharField(max_length=100, required=False)
    psu_part_number = forms.CharField(max_length=100, required=False)
    max_power_wattage = forms.CharField(max_length=100, required=False)
    min_correction_time = forms.CharField(max_length=100, required=False)

    class Meta:
        model = PSU
        fields = ('psu_model_type', 'psu_description', 'psu_vendor_name', 'psu_part_number', 'max_power_wattage',
                  'min_correction_time')


class AddMemory(ModelForm):
    vendor = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    revision = forms.CharField(max_length=100, required=False)
    name = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=100, required=False)
    vid = forms.CharField(max_length=100, required=False)
    part_number = forms.CharField(max_length=100, required=False)
    sku_id = forms.CharField(max_length=100, required=False)
    oem = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Memory
        fields = (
        'vendor', 'model', 'revision', 'name', 'pid', 'vid', 'part_number', 'sku_id', 'oem', 'oem_part_number')

class EditMemory(ModelForm):
    vendor = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    revision = forms.CharField(max_length=100, required=False)
    name = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=100, required=False)
    vid = forms.CharField(max_length=100, required=False)
    part_number = forms.CharField(max_length=100, required=False)
    sku_id = forms.CharField(max_length=100, required=False)
    oem = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Memory
        fields = (
        'vendor', 'model', 'revision', 'name', 'pid', 'vid', 'part_number', 'sku_id', 'oem', 'oem_part_number')


class AddCPU(ModelForm):
    vendor = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    revision = forms.CharField(max_length=100, required=False)
    name = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=100, required=False)
    vid = forms.CharField(max_length=100, required=False)
    part_number = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)
    sku_id = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CPU
        fields = ('vendor', 'model', 'revision', 'name', 'pid', 'vid', 'part_number', 'sku_id', 'oem_name', 'oem_part_number')

class EditCPU(ModelForm):
    vendor = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    revision = forms.CharField(max_length=100, required=False)
    name = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=100, required=False)
    vid = forms.CharField(max_length=100, required=False)
    part_number = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)
    sku_id = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CPU
        fields = ('vendor', 'model', 'revision', 'name', 'pid', 'vid', 'part_number', 'sku_id', 'oem_name', 'oem_part_number')

class AddHDD(ModelForm):
    #uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)
    vendorString = forms.CharField(max_length=64, required=False)
    model = forms.CharField(max_length=64, required=False) # new field
    part_number = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=5, required=False)
    vid = forms.CharField(max_length=5, required=False)
    sku = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False) # new field
    lff = forms.CharField(max_length=100, required=False)
    pmax = forms.CharField(max_length=5, required=False)
    pmin = forms.CharField(max_length=5, required=False)

    class Meta:
        model = MiscComponent
        fields = ( 'description',
        'packageVersion', 'vendorString', 'model', 'part_number', 'pid', 'vid', 'sku', 'oem_part_number', 'oem_name', 'lff', 'pmax', 'pmin')  # ,'verifyApi')

class EditHDD(ModelForm):
    #uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)
    vendorString = forms.CharField(max_length=64, required=False)
    model = forms.CharField(max_length=64, required=False) # new field
    part_number = forms.CharField(max_length=100, required=False)
    pid = forms.CharField(max_length=5, required=False)
    vid = forms.CharField(max_length=5, required=False)
    sku = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False) # new field
    lff = forms.CharField(max_length=100, required=False)
    pmax = forms.CharField(max_length=5, required=False)
    pmin = forms.CharField(max_length=5, required=False)

    class Meta:
        model = MiscComponent
        fields = ( 'description',
        'packageVersion', 'vendorString', 'model', 'part_number', 'pid', 'vid', 'sku', 'oem_part_number', 'oem_name', 'lff', 'pmax', 'pmin')  # ,'verifyApi')

class AddServer(ModelForm):

    description = forms.CharField(max_length=1024)
    uniqueName = forms.CharField(max_length=100)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)

    class Meta:
        model = MiscComponent
        fields = ( 'description','uniqueName','packageVersion')

class EditServer(ModelForm):
    #
    description = forms.CharField(max_length=1024)
    uniqueName = forms.CharField(max_length=100)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)

    class Meta:
        model = MiscComponent
        fields = ( 'description', 'uniqueName', 'packageVersion' )

class AddExpander(ModelForm):
    description = forms.CharField(max_length=1024)
    uniqueName = forms.CharField(max_length=100)
    packageVersion = forms.CharField(max_length=1024)

    class Meta:
        model = MiscComponent
        fields = ( 'description', 'uniqueName', 'packageVersion' )

class EditExpander(ModelForm):
    description = forms.CharField(max_length=1024)
    uniqueName = forms.CharField(max_length=100)
    packageVersion = forms.CharField(max_length=1024)

    class Meta:
        model = MiscComponent
        fields = ('description', 'uniqueName', 'packageVersion')

class AddMswitch(ModelForm):
    vendorId = forms.CharField(max_length=5)
    deviceId = forms.CharField(max_length=5)
    uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    packageVersion = forms.CharField(max_length=1024)
    class Meta:
        model = MiscComponent
        fields = ( 'vendorId', 'deviceId', 'uniqueName', 'description', 'packageVersion' )

class EditMswitch(ModelForm):
    vendorId = forms.CharField(max_length=5)
    deviceId = forms.CharField(max_length=5)
    uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    packageVersion = forms.CharField(max_length=1024)
    class Meta:
        model = MiscComponent
        fields = ( 'vendorId', 'deviceId', 'uniqueName', 'description', 'packageVersion' )

class AddComponent(ModelForm):
    vendorId = forms.CharField(max_length=5)
    deviceId = forms.CharField(max_length=5)
    subVendorId = forms.CharField(max_length=5)
    subDeviceId = forms.CharField(max_length=5)
    uniqueName = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1024)
    #exists = forms.BooleanField(required=False)
    packageVersion = forms.CharField(max_length=1024, required=False)
    vendorString = forms.CharField(max_length=64, required=False)
    # tools = forms.CharField(max_length=1500, required=False)  # check with velu
    # firmware = forms.CharField(max_length=1500, required=False)  # check with velu
    # verifyApi = forms.CharField(max_length=1500, required=False)  # check with velu
    # ---newly added fields for ModelForm
    pmax = forms.CharField(max_length=5, required=False)
    pmin = forms.CharField(max_length=5, required=False)
    pid = forms.CharField(max_length=100, required=False)
    vid = forms.CharField(max_length=50, required=False)
    sku = forms.CharField(max_length=100, required=False)
    oem_part_number = forms.CharField(max_length=100, required=False)
    part_number = forms.CharField(max_length=100, required=False)
    lff = forms.CharField(max_length=100, required=False)
    peripheral_type = forms.CharField(max_length=100, required=False)
    no_of_temp_sensor = forms.CharField(max_length=100, required=False)
    temp_sensor_i2cslaveaddr = forms.CharField(max_length=100, required=False)
    # fanpolicy = forms.CharField(max_length=100, required=False)
    secure_firmware_support = forms.CharField(max_length=100, required=False)
    secure_firmware_update_i2cslaveaddr = forms.CharField(max_length=100, required=False)
    command = forms.CharField(max_length=100, required=False)
    lock_payload = forms.CharField(max_length=100, required=False)
    unlock_payload = forms.CharField(max_length=100, required=False)
    # card_threshold_offset = forms.CharField(max_length=100, required=False)
    fru_major_type = forms.CharField(max_length=100, required=False)
    fru_minor_type = forms.CharField(max_length=100, required=False)
    pci_attribute = forms.CharField(max_length=100, required=False)
    mctp_supported = forms.CharField(max_length=100, required=False)
    mctp_interfaces_supported = forms.CharField(max_length=100, required=False)
    model = forms.CharField(max_length=100, required=False)
    oem_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = MiscComponent
        fields = (
        'vendorId', 'deviceId', 'subVendorId', 'subDeviceId', 'uniqueName', 'description', 'packageVersion',
        'vendorString', 'pmin', 'pmax', 'pid', 'vid', 'sku', 'oem_part_number', 'part_number', 'lff', 'peripheral_type', 'no_of_temp_sensor',
        'temp_sensor_i2cslaveaddr', 'secure_firmware_support', 'secure_firmware_update_i2cslaveaddr', 'command',
        'lock_payload', 'unlock_payload', 'fru_major_type', 'fru_minor_type', 'pci_attribute', 'mctp_supported',
        'mctp_interfaces_supported','model','oem_name')  # ,'verifyApi')

class AddStorage(ModelForm):
    match = forms.CharField(max_length=100, required=False)
    init = forms.CharField(max_length=100, required=False)
    max_drives = forms.CharField(max_length=100, required=False)
    slot_map_strategy = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Storage
        fields = ('match', 'init', 'max_drives', 'slot_map_strategy')


class EditStorage(ModelForm):
    match = forms.CharField(max_length=100, required=False)
    init = forms.CharField(max_length=100, required=False)
    max_drives = forms.CharField(max_length=100, required=False)
    slot_map_strategy = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Storage
        fields = ('match', 'init', 'max_drives', 'slot_map_strategy')


class DiscoveryEdit(ModelForm):
    dhookName = forms.CharField(max_length=1024)
    dpreHook = forms.CharField(max_length=1024, widget=forms.Textarea)
    dinHook = forms.CharField(max_length=1024, widget=forms.Textarea)
    dpostHook = forms.CharField(max_length=1024, widget=forms.Textarea)

    class Meta:
        model = DiscoveryHook
        fields = ('dpreHook', 'dinHook', 'dpostHook')


class UpdateEdit(ModelForm):
    preHook = forms.CharField(max_length=1024, widget=forms.Textarea)
    inHook = forms.CharField(max_length=1024, widget=forms.Textarea)
    postHook = forms.CharField(max_length=1024, widget=forms.Textarea)

    class Meta:
        model = UpdateHook
        fields = ('preHook', 'inHook', 'postHook')

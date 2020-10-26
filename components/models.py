from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Platform(models.Model):
    platformName = models.CharField(max_length=256)

    def __str__(self):
        return self.platformName + ' - ' + str(self.id)

    class Meta:
        app_label = 'components'


class Nvme(models.Model):
    match = models.CharField(max_length=100)
    init = models.CharField(max_length=100)
    max_drives = models.CharField(max_length=100)
    slot_map_strategy = models.CharField(max_length=100)
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.match + ' - ' + self.init + ' - ' + self.max_drives + ' - ' + self.slot_map_strategy

    class Meta:
        app_label = 'components'


class NvmeSwitch(models.Model):
    pci_slot_name = models.CharField(max_length=100)
    switch_i2c_channel = models.CharField(max_length=100)
    switch_i2c_dev_address = models.CharField(max_length=100)
    nvme = models.ForeignKey(Nvme)

    def __str__(self):
        return self.pci_slot_name + ' - ' + self.switch_i2c_channel + ' - ' + self.switch_i2c_dev_address

    class Meta:
        app_label = 'components'


class NvmeSwitchPort(models.Model):
    drive_name = models.CharField(max_length=100)
    usp_port_num = models.CharField(max_length=100)
    dsp_port_num = models.CharField(max_length=100)
    usp_pcie_fn_num = models.CharField(max_length=100)
    dsp_pcie_fn_num = models.CharField(max_length=100)
    nvme_index = models.CharField(max_length=100)
    nvmeswitch = models.ForeignKey(NvmeSwitch)

    def __str__(self):
        return self.drive_name + ' - ' + self.usp_port_num + ' - ' + self.dsp_port_num + ' - ' + self.usp_pcie_fn_num + ' - ' + self.dsp_pcie_fn_num + ' - ' + self.nvme_index

    class Meta:
        app_label = 'components'


class NvmeCtrlInfo(models.Model):
    pci_slot_name = models.CharField(max_length=100)
    i2c_channel = models.CharField(max_length=100)
    i2c_dev_address = models.CharField(max_length=100)
    info_id = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    nvme_type = models.CharField(max_length=100)
    nvme_parent_type = models.CharField(max_length=100)
    nvme = models.ForeignKey(Nvme)

    def __str__(self):
        return self.pci_slot_name + ' - ' + self.i2c_channel + ' - ' + self.i2c_dev_address + ' - ' + self.id + ' - ' + self.vendor + ' - ' + self.nvme_type + ' - ' + self.nvme_parent_type

    class Meta:
        app_label = 'components'


# Create your models here.
class Component(models.Model):
    vendorId = models.CharField(max_length=5)
    deviceId = models.CharField(max_length=5)
    subVendorId = models.CharField(max_length=5)
    subDeviceId = models.CharField(max_length=5)
    uniqueName = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # exists = models.BooleanField(default=True)
    packageVersion = models.CharField(max_length=1024, blank=True, null=True)
    vendorString = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)

    # verifyApi = models.CharField(max_length=1500, blank=True, null=True)  #check with velu
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.vendorId + ' - ' + self.deviceId + ' - ' + self.subVendorId + ' - ' + self.subDeviceId + ' - ' + self.uniqueName + ' - ' + self.description + ' - ' + self.packageVersion + ' - ' + self.vendorString + ' - ' + self.model + ' - ' + self.device_type  # + ' - ' + self.pmin + ' - ' + self.pmax# + ' - ' + self.verifyApi

    class Meta:
        app_label = 'components'


class MiscComponent(Component):
    pmax = models.CharField(max_length=5, default='', blank=True, null=True)
    pmin = models.CharField(max_length=5, default='', blank=True, null=True)
    pid = models.CharField(max_length=100, default='', blank=True, null=True)
    vid = models.CharField(max_length=100, default='', blank=True, null=True)
    sku = models.CharField(max_length=100, default='', blank=True, null=True)
    oem_part_number = models.CharField(max_length=100, default='', blank=True, null=True)

    part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    lff = models.CharField(max_length=100, default='', blank=True, null=True)  # newly addded
    peripheral_type = models.CharField(max_length=100, default='', blank=True, null=True)
    no_of_temp_sensor = models.CharField(max_length=100, default='', blank=True, null=True)
    temp_sensor_i2cslaveaddr = models.CharField(max_length=100, default='', blank=True, null=True)
    # fanpolicy = models.CharField(max_length=100, default='', blank=True, null=True)
    secure_firmware_support = models.CharField(max_length=100, default='', blank=True, null=True)
    secure_firmware_update_i2cslaveaddr = models.CharField(max_length=100, default='', blank=True, null=True)
    command = models.CharField(max_length=100, default='', blank=True, null=True)
    lock_payload = models.CharField(max_length=100, default='', blank=True, null=True)
    unlock_payload = models.CharField(max_length=100, default='', blank=True, null=True)
    # card_threshold_offset = models.CharField(max_length=100, default='', blank=True, null=True)
    fru_major_type = models.CharField(max_length=100, default='', blank=True, null=True)
    fru_minor_type = models.CharField(max_length=100, default='', blank=True, null=True)
    pci_attribute = models.CharField(max_length=100, default='', blank=True, null=True)
    mctp_supported = models.CharField(max_length=100, default='', blank=True, null=True)
    mctp_interfaces_supported = models.CharField(max_length=100, default='', blank=True, null=True)

    oem_name = models.CharField(max_length=100, default='', blank=True, null=True)  # newly addded

    # policy = models.ManyToManyField(Policy)
    def __str__(self):
        return self.pmax + ' - ' + self.pmin + ' - ' + self.pid + ' - ' + self.vid + ' - ' + self.sku + ' - ' + \
               self.oem_part_number + ' - ' + self.part_number + ' - ' + self.lff + ' - ' + self.oem_name + ' - ' + \
               self.peripheral_type + ' - ' + self.no_of_temp_sensor + ' - ' + self.temp_sensor_i2cslaveaddr + ' - ' + \
               self.secure_firmware_support + ' - ' + self.secure_firmware_update_i2cslaveaddr + ' - ' + self.command + \
               ' - ' + self.lock_payload + ' - ' + self.unlock_payload + ' - ' + self.fru_major_type + ' - ' + \
               self.fru_minor_type + ' - ' + self.pci_attribute + ' - ' + self.vendorId + ' - ' + self.deviceId + \
               ' - ' + self.subVendorId + ' - ' + self.subDeviceId + ' - ' + self.uniqueName + ' - ' + \
               self.description + ' - ' + self.packageVersion + ' - ' + \
               self.vendorString + ' - ' + self.mctp_supported + ' - ' + self.mctp_interfaces_supported

    class Meta:
        app_label = 'components'


# class HDD(models.Model):
#     uniqueName = models.CharField(max_length=100, default='', blank=True, null=True)
#     description = models.CharField(max_length=100, default='', blank=True, null=True)
#     # exists = forms.BooleanField(required=False)
#     packageVersion = models.CharField(max_length=100, default='', blank=True, null=True)
#     vendorString = models.CharField(max_length=100, default='', blank=True, null=True)
#     model = models.CharField(max_length=100, default='', blank=True, null=True)
#     part_number = models.CharField(max_length=100, default='', blank=True, null=True)
#     pid = models.CharField(max_length=100, default='', blank=True, null=True)
#     version_id = models.CharField(max_length=100, default='', blank=True, null=True)
#     sku = models.CharField(max_length=100, default='', blank=True, null=True)
#     oem_part_number = models.CharField(max_length=100, default='', blank=True, null=True)
#     oem_name = models.CharField(max_length=100, default='', blank=True, null=True)
#     lff = models.CharField(max_length=100, default='', blank=True, null=True)
#     pmax = models.CharField(max_length=100, default='', blank=True, null=True)
#     pmin = models.CharField(max_length=100, default='', blank=True, null=True)
#     platform = models.ManyToManyField(Platform)
#
#     def __str__(self):
#         return self.uniqueName + ' - ' + self.description + ' - ' + self.packageVersion + ' - ' \
#                + self.vendorString + ' - ' + self.model + ' - ' + self.part_number + ' - ' \
#                + self.pid + ' - ' + self.version_id + ' - ' + self.sku + ' - ' + self.oem_part_number \
#                + ' - ' + self.oem_name + ' - ' + self.lff + ' - ' + self.pmax + ' - ' + self.pmin
#
#     class Meta:
#         app_label = 'components'


class Policy(models.Model):
    # platform = models.ManyToManyField(Platform)
    fanpolicy = models.CharField(max_length=100, default='', blank=True, null=True)
    card_threshold_offset = models.CharField(max_length=100, default='', blank=True, null=True)

    # misc_component_id = models.ForeignKey(MiscComponent)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'components'


class PolicyAssociation(models.Model):
    component = models.ForeignKey(Component)
    policy = models.ForeignKey(Policy)
    platform = models.ForeignKey(Platform)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'components'


class PSU(models.Model):
    psu_model_type = models.CharField(max_length=100, default='', blank=True, null=True)
    psu_description = models.CharField(max_length=100, default='', blank=True, null=True)
    psu_vendor_name = models.CharField(max_length=100, default='', blank=True, null=True)
    psu_part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    max_power_wattage = models.CharField(max_length=100, default='', blank=True, null=True)
    min_correction_time = models.CharField(max_length=100, default='', blank=True, null=True)
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.psu_model_type + ' - ' + self.psu_description + ' - ' + self.psu_vendor_name + ' - ' + self.psu_part_number + ' - ' + self.max_power_wattage + ' - ' + self.min_correction_time

    class Meta:
        app_label = 'components'


class Storage_pcie_slots(models.Model):
    pci_slot_name = models.CharField(max_length=100, default='', blank=True, null=True)
    i2c_dev_address = models.CharField(max_length=100, default='', blank=True, null=True)
    i2c_channel = models.CharField(max_length=100, default='', blank=True, null=True)
    unique_id = models.CharField(max_length=100, default='', blank=True, null=True)
    chassis_pos = models.CharField(max_length=100, default='', blank=True, null=True)
    vendor = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.pci_slot_name + ' - ' + self.i2c_dev_address + ' - ' + self.i2c_channel + ' - ' + self.unique_id + ' - ' + self.chassis_pos + ' - ' + self.vendor

    class Meta:
        app_label = 'components'


class Storage(models.Model):
    match = models.CharField(max_length=100, default='', blank=True, null=True)
    init = models.CharField(max_length=100, default='', blank=True, null=True)
    max_drives = models.CharField(max_length=100, default='', blank=True, null=True)
    slot_map_strategy = models.CharField(max_length=100, default='', blank=True, null=True)
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.match + ' - ' + self.init + ' - ' + self.max_drives + ' - ' + self.slot_map_strategy

    class Meta:
        app_label = 'components'


class StorageAssociation(models.Model):
    storage = models.ForeignKey(Storage)
    storage_pcie_slots = models.ForeignKey(Storage_pcie_slots)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'components'


class CPU(models.Model):
    vendor = models.CharField(max_length=100, default='', blank=True, null=True)
    model = models.CharField(max_length=100, default='', blank=True, null=True)
    revision = models.CharField(max_length=100, default='', blank=True, null=True)
    name = models.CharField(max_length=100, default='', blank=True, null=True)
    pid = models.CharField(max_length=100, default='', blank=True, null=True)
    vid = models.CharField(max_length=100, default='', blank=True, null=True)
    part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    sku_id = models.CharField(max_length=100, default='', blank=True, null=True)
    oem = models.CharField(max_length=100, default='', blank=True, null=True)
    oem_part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.vendor + ' - ' + self.model + ' - ' + self.revision + ' - ' + self.name + ' - ' + self.pid + ' - ' + self.vid + ' - ' + self.part_number + ' - ' + self.sku_id + ' - ' + self.oem + ' - ' + self.oem_part_number

    class Meta:
        app_label = 'components'


class Memory(models.Model):
    vendor = models.CharField(max_length=100, default='', blank=True, null=True)
    model = models.CharField(max_length=100, default='', blank=True, null=True)
    revision = models.CharField(max_length=100, default='', blank=True, null=True)
    name = models.CharField(max_length=100, default='', blank=True, null=True)
    pid = models.CharField(max_length=100, default='', blank=True, null=True)
    vid = models.CharField(max_length=100, default='', blank=True, null=True)
    part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    sku_id = models.CharField(max_length=100, default='', blank=True, null=True)
    oem = models.CharField(max_length=100, default='', blank=True, null=True)
    oem_part_number = models.CharField(max_length=100, default='', blank=True, null=True)
    platform = models.ManyToManyField(Platform)

    def __str__(self):
        return self.vendor + ' - ' + self.model + ' - ' + self.revision + ' - ' + self.name + ' - ' + self.pid + ' - ' + self.vid + ' - ' + self.part_number + ' - ' + self.sku_id + ' - ' + self.oem + ' - ' + self.oem_part_number

    class Meta:
        app_label = 'components'


class DiscoveryHook(models.Model):
    id = models.IntegerField(primary_key=True)
    dcomp = models.ForeignKey(Component, on_delete=models.CASCADE)
    dcomponentId = models.CharField(max_length=5)
    dhookName = models.CharField(max_length=25)
    dpreHook = models.CharField(max_length=1024)
    dinHook = models.CharField(max_length=1024)
    dpostHook = models.CharField(max_length=1024)
    dplatform = models.CharField(max_length=1024)

    def __str__(self):
        return self.dcomponentId + ' - ' + self.dhookName + '-' + self.dpreHook + '-' + str(self.id)

    class Meta:
        app_label = 'components'


class UpdateHook(models.Model):
    comp = models.ForeignKey(Component, on_delete=models.CASCADE)
    componentId = models.CharField(max_length=5)
    hookName = models.CharField(max_length=25)
    preHook = models.CharField(max_length=1024)
    inHook = models.CharField(max_length=1024)
    postHook = models.CharField(max_length=1024)
    platform = models.CharField(max_length=1024)

    def __str__(self):
        return self.componentId + ' - ' + self.hookName + '-' + self.preHook + '-' + str(self.id)

    class Meta:
        app_label = 'components'


class Release(models.Model):
    releaseName = models.CharField(max_length=25)
    platforms = models.ManyToManyField(Platform)

    def __str__(self):
        return self.releaseName + '-' + str(self.id)

    class Meta:
        app_label = 'components'


class Firmware(models.Model):
    firmwareName = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    location = models.URLField(max_length=200)
    softLocation = models.URLField(max_length=200)
    # document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    # component = models.ManyToManyField(Component)
    def __str__(self):
        return self.firmwareName + '-' + str(self.id)

    class Meta:
        app_label = 'components'


class Tool(models.Model):
    toolName = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    location = models.URLField(max_length=200)
    softLocation = models.URLField(max_length=200)
    # document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    # component = models.ManyToManyField(Component)

    def __str__(self):
        return self.toolName + '-' + str(self.id)

    class Meta:
        app_label = 'components'


class ToolAssociation(models.Model):
    tool = models.ForeignKey(Tool)
    release = models.ForeignKey(Release)
    component = models.ForeignKey(Component)
    platform = models.ForeignKey(Platform)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'components'


class FirmwareAssociation(models.Model):
    firmware = models.ForeignKey(Firmware)
    release = models.ForeignKey(Release)
    component = models.ForeignKey(Component)
    platform = models.ForeignKey(Platform)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'components'

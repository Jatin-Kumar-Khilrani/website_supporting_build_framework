# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-22 10:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorId', models.CharField(max_length=5)),
                ('deviceId', models.CharField(max_length=5)),
                ('subVendorId', models.CharField(max_length=5)),
                ('subDeviceId', models.CharField(max_length=5)),
                ('uniqueName', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('exists', models.BooleanField(default=True)),
                ('packageVersion', models.CharField(blank=True, max_length=1024, null=True)),
                ('vendorString', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('model', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('revision', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('name', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('pid', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('vid', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('sku_id', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('oem', models.CharField(blank=True, default=b'', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscoveryHook',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dcomponentId', models.CharField(max_length=5)),
                ('dhookName', models.CharField(max_length=25)),
                ('dpreHook', models.CharField(max_length=1024)),
                ('dinHook', models.CharField(max_length=1024)),
                ('dpostHook', models.CharField(max_length=1024)),
                ('dplatform', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firmwareName', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('location', models.URLField()),
                ('softLocation', models.URLField()),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FirmwareAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('model', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('revision', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('name', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('pid', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('vid', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('sku_id', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('oem', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('oem_part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nvme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.CharField(max_length=100)),
                ('init', models.CharField(max_length=100)),
                ('max_drives', models.CharField(max_length=100)),
                ('slot_map_strategy', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NvmeCtrlInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pci_slot_name', models.CharField(max_length=100)),
                ('i2c_channel', models.CharField(max_length=100)),
                ('i2c_dev_address', models.CharField(max_length=100)),
                ('info_id', models.CharField(max_length=100)),
                ('vendor', models.CharField(max_length=100)),
                ('nvme_type', models.CharField(max_length=100)),
                ('nvme_parent_type', models.CharField(max_length=100)),
                ('nvme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Nvme')),
            ],
        ),
        migrations.CreateModel(
            name='NvmeSwitch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pci_slot_name', models.CharField(max_length=100)),
                ('switch_i2c_channel', models.CharField(max_length=100)),
                ('switch_i2c_dev_address', models.CharField(max_length=100)),
                ('nvme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Nvme')),
            ],
        ),
        migrations.CreateModel(
            name='NvmeSwitchPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drive_name', models.CharField(max_length=100)),
                ('usp_port_num', models.CharField(max_length=100)),
                ('dsp_port_num', models.CharField(max_length=100)),
                ('usp_pcie_fn_num', models.CharField(max_length=100)),
                ('dsp_pcie_fn_num', models.CharField(max_length=100)),
                ('nvme_index', models.CharField(max_length=100)),
                ('nvmeswitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.NvmeSwitch')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platformName', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fanpolicy', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('card_threshold_offset', models.CharField(blank=True, default=b'', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolicyAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PSU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psu_model_type', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('psu_description', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('psu_vendor_name', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('psu_part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('max_power_wattage', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('min_correction_time', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('platform', models.ManyToManyField(to='components.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('releaseName', models.CharField(max_length=25)),
                ('platforms', models.ManyToManyField(to='components.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('init', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('max_drives', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('slot_map_strategy', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('platform', models.ManyToManyField(to='components.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Storage_pcie_slots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pci_slot_name', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('i2c_dev_address', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('i2c_channel', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('unique_id', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('chassis_pos', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('vendor', models.CharField(blank=True, default=b'', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StorageAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Storage')),
                ('storage_pcie_slots', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Storage_pcie_slots')),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toolName', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('location', models.URLField()),
                ('softLocation', models.URLField()),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ToolAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('componentId', models.CharField(max_length=5)),
                ('hookName', models.CharField(max_length=25)),
                ('preHook', models.CharField(max_length=1024)),
                ('inHook', models.CharField(max_length=1024)),
                ('postHook', models.CharField(max_length=1024)),
                ('platform', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='MiscComponent',
            fields=[
                ('component_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='components.Component')),
                ('pmax', models.CharField(blank=True, default=b'', max_length=5, null=True)),
                ('pmin', models.CharField(blank=True, default=b'', max_length=5, null=True)),
                ('pid', models.CharField(blank=True, default=b'', max_length=5, null=True)),
                ('vid', models.CharField(blank=True, default=b'', max_length=5, null=True)),
                ('sku', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('oem_part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('part_number', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('lff', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('peripheral_type', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('no_of_temp_sensor', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('temp_sensor_i2cslaveaddr', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('secure_firmware_support', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('secure_firmware_update_i2cslaveaddr', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('command', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('lock_payload', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('unlock_payload', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('fru_major_type', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('fru_minor_type', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('pci_attribute', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('mctp_supported', models.CharField(blank=True, default=b'', max_length=100, null=True)),
                ('mctp_interfaces_supported', models.CharField(blank=True, default=b'', max_length=100, null=True)),
            ],
            bases=('components.component',),
        ),
        migrations.AddField(
            model_name='updatehook',
            name='comp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Component'),
        ),
        migrations.AddField(
            model_name='toolassociation',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Component'),
        ),
        migrations.AddField(
            model_name='toolassociation',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Platform'),
        ),
        migrations.AddField(
            model_name='toolassociation',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Release'),
        ),
        migrations.AddField(
            model_name='toolassociation',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Tool'),
        ),
        migrations.AddField(
            model_name='policyassociation',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Component'),
        ),
        migrations.AddField(
            model_name='policyassociation',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Platform'),
        ),
        migrations.AddField(
            model_name='policyassociation',
            name='policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Policy'),
        ),
        migrations.AddField(
            model_name='nvme',
            name='platform',
            field=models.ManyToManyField(to='components.Platform'),
        ),
        migrations.AddField(
            model_name='memory',
            name='platform',
            field=models.ManyToManyField(to='components.Platform'),
        ),
        migrations.AddField(
            model_name='firmwareassociation',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Component'),
        ),
        migrations.AddField(
            model_name='firmwareassociation',
            name='firmware',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Firmware'),
        ),
        migrations.AddField(
            model_name='firmwareassociation',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Platform'),
        ),
        migrations.AddField(
            model_name='firmwareassociation',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Release'),
        ),
        migrations.AddField(
            model_name='discoveryhook',
            name='dcomp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='components.Component'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='platform',
            field=models.ManyToManyField(to='components.Platform'),
        ),
        migrations.AddField(
            model_name='component',
            name='platform',
            field=models.ManyToManyField(to='components.Platform'),
        ),
    ]

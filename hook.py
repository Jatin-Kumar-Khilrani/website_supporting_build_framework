import logging

from Component import Component
from Update_CBL import Components

log = logging.getLogger(__name__)

class Discovery_Hooks(Component):
    pass

    def __init__(self):
        'Initialize the hook'

    def hook(self,component):
        """
            Hook for <hook name> hook component
            Here, fill the necessary values needed for prior to discovery operation.
            Component class object passed as input argument for the given component
            and any field can be modified here using class member

            :parameter component: Object of type Component which has details about <component name> component
            :return: True - Success
                     False - Failure
        """
        log.info("Discovery hook called for :", component.get_unique_name())

class Update_Hooks(Component):
    pass

    def __init__(self):
        'Initialize the hook'

    def pre_hook(self,component,scheduled_q,lock):
        """
            In this hook, Do necessary validation before kicking off the update.

            :parameter component: Object of type Component which has details about <component name> component
            :param scheduled_q: This list contains list of component schduled for update and this is shared accross all update threads.
            :param lock: This lock is used to protect schduled_q variable, because this is shared accross all update threads
            :return: True - Success
                     False - Any failure, fill the appropriate error description using set_update_description()
                     None - Skip the remaining hook like hook() and post_hook()
        """

        log.info("Update Pre hook called for :", component.get_unique_name())

        '''
        ' -- Vendor ID -- ' 
        vendor = component.get_vendor()
        '''

        '''
        ' -- Device ID -- '
        device = component.get_device()
        '''

        '''
        ' -- Running Version -- '
        component.set_running_version('XX.YY.ZZ')
        '''

        '''
        Please refer Class Component further for more detail
        '''

        component._set_update_status(Component.UPDATE_STATUS_PROGRESS)

        return True

    def in_hook(self,component):
        """
            In this hook, Do the actual update of the component.

            :parameter component: Object of type Component which has details about CIMC component
            :return: True - Success
                     False - Any failure, fill the appropriate error description using set_update_description()
                     None - Skip the remaining hook like hook() and post_hook()
        """

        log.info("Update In hook called for :", component.get_unique_name())

        '''
        '-- Get the required firmware for update --' 
        firmware = component.get_firmware_by_name(firmware_name="sample_firmware")

        ' -- In case of error, status and description is filled by get_firmware_by_name() API -- ' 
        if ( firmware == None):
            return False
        
        '''

        '''
        '-- Get the required tool for update --'
        tool = component.get_tool_by_name(tool_name="sample_tool")
        
        ' -- In case of error, status and description is filled by get_tool_by_name() API --' 
        if ( tool == None):
            return False

        '''

        ''' 
            Trigger the update and do not wait until it completes, 
            post hook should check the update status
        '''
        component.set_update_description("Successfully triggered update.")
        component._set_update_status(Component.UPDATE_STATUS_PROGRESS)

        return True

    def post_hook(self,component):
        'post hook'

        log.info("Update Post hook called for :", component.get_unique_name())

        '''
        '-- Verify the update status --'
        '''

        '''
        '-- Set varies status based on the progress -- '
        'component.set_update_status(Component.UPDATE_STATUS_SUCCEEDED)'
        'component.set_update_status(Component.UPDATE_STATUS_FAILED)'
        'component.set_update_status(Component.UPDATE_STATUS_PROGRESS)'
        '''

        component.set_update_status(Component.UPDATE_STATUS_SUCCEEDED)
        return True

    def __del__(self):
        '''
        print ("Update : Finished ")
        '''

class Activate_Hook(Component):
    pass

    def activate(self,component):
        'perform activate operation'
        log.info("Activate hook called for :", component.get_unique_name())

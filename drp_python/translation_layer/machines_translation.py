# Copyright 2018 Cable Television Laboratories, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from api_http import ApiHttp
from drp_python.exceptions.http_exceptions import AuthorizationError, \
    ConnectionError
from drp_python.exceptions.drb_exceptions import NotFoundError
from drp_python.model_layer.machine_model import MachineModel
import logging

logger = logging.getLogger('drp-python')


class MachineTranslation(ApiHttp):
    """
     All HTTP based API Calls related to Machines
    """

    def __init__(self, session):
        super(MachineTranslation, self).__init__(session)
        logger.info('__init__')

    def get_machine(self, machine_uuid):
        logger.info('get_machine')
        drp_obj = self.session.get('machines', machine_uuid)
        machine_model = convert_to_client(drp_obj)
        return machine_model

    def get_machine_by_name(self, machine_name):
        logger.debug('get_machine_by_name')
        drp_obj = self.session.get('machines?Name=' + machine_name)
        if len(drp_obj) > 0:
            drp_obj = drp_obj[0]
            machine_model = convert_to_client(drp_obj)
            return machine_model
        else:
            raise NotFoundError('Test', 'Test')

    def create_machine(self, machine_config_model):
        logger.info('create_machine')
        drp_object = convert_to_drp(machine_config_model)
        drp_object = self.session.post('machines', drp_object)
        machine_model = convert_to_client(drp_object)
        logger.info('Created ' + machine_model.name)
        return machine_model

    def update_machine(self, machine_config_model, machine_uuid):
        logger.info('update_machine')
        drp_object = convert_to_drp(machine_config_model)
        drp_object = self.session.put('machines', drp_object, machine_uuid)
        machine_model = convert_to_client(drp_object)
        logger.info('Updated ' + machine_uuid)
        return machine_model

    def delete_machine(self, machine_uuid):
        logger.info('delete_machine')
        result = self.session.delete('machines', machine_uuid)
        logger.info('Deleted ' + machine_uuid)
        return

    def add_machine_params(self, params_config_model, machine_uuid):
        logger.info('add params to machine')
        value = params_config_model.value
        param = params_config_model.name
        temp = self.session.post('machines/' + machine_uuid +
                                 '/params/' + param, value)
        machine_model = self.get_machine(machine_uuid)
        logger.info('Updated ' + machine_uuid)
        return machine_model


def convert_to_drp(machine_model):
    logger.info('convert_to_drp')
    drp_object = {
        "Address": machine_model.ip,
        "Description": machine_model.type,
        "HardwareAddrs": [
            machine_model.mac
        ],
        "Name": machine_model.name,
        "OS": machine_model.os,
        "Runnable": True,
        "Workflow": machine_model.workflow
    }
    logger.info('Converted client to drp')
    logger.info(drp_object)
    return drp_object


def convert_to_client(drp_object):
    logger.info(drp_object)
    mac = drp_object.get('HardwareAddrs')
    if mac is not None:
        mac = mac[0]
    machine_model_dict = {
        'ip': drp_object.get('Address'),
        'mac': mac,
        'name': drp_object.get('Name'),
        'type': drp_object.get('Description'),
        'os': drp_object.get('OS'),
        'uuid': drp_object.get('Uuid'),
        'workflow': drp_object.get('Workflow'),

        'available': drp_object.get('Available'),
        'errors': drp_object.get('Errors'),
        'read_only': drp_object.get('ReadOnly'),
        'validated': drp_object.get('Validated'),
        'params': drp_object.get('Params')
    }
    logger.info('Converted drp to client')
    machine_model = MachineModel(**machine_model_dict)
    logger.info(machine_model)
    return machine_model


def get_all_machines(session):
    logger.info('get_all_machines')
    try:
        result = session.get('machines')
        logger.info('Fetched all machines')
        return result
    except AuthorizationError as error:
        logger.error(error)
        raise error
    except ConnectionError as error:
        logger.error(error)
        raise error

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
from http_exceptions import AuthorizationError, ConnectionError
from drb_exceptions import  ActionError


class SubnetsHttp(ApiHttp):
    """
     All HTTP based API Calls related to Subnets
    """
    def __init__(self, host, login, verifyCert=False):
        ApiHttp.__init__(self, host, login, verifyCert)

    def get_all_subnets(self):
        try:
            result = self.httpProxy.get('subnets')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet(self, subnet_name):
        try:
            result = self.httpProxy.get('subnets', subnet_name)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def create_subnet(self, subnet):
        try:
            result = self.httpProxy.post('subnets', subnet)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def update_subnet(self, subnet, subnet_name):
        try:
            result = self.httpProxy.put('subnets', subnet, subnet_name)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def delete_subnet(self, subnet_name):
        try:
            result = self.httpProxy.delete('subnets', subnet_name)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet_all_actions(self, subnet_name):
        try:
            result = self.httpProxy.get('subnets/' + subnet_name + '/actions')
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def get_subnet_action(self, subnet_name, cmd):
        try:
            result = self.httpProxy.get('subnets/' + subnet_name + '/actions', cmd)
            return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

    def execute_subnet_action(self, subnet_name, cmd):
        try:
            result = self.httpProxy.post('subnets/' + subnet_name + '/actions/' + cmd, {})
            if result == 400:
                raise ActionError(cmd, 'Action is not available on subnet ' + subnet_name)
            else:
                return result
        except AuthorizationError as error:
            print error
            raise error
        except ConnectionError as error:
            print error
            raise error

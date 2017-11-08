# Copyright 2016 NEC Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from tempest import test as test

from tripleo_common_tempest_plugin.services import mistral_client


class TestCase(test.BaseTestCase):
    credentials = ['admin', 'primary', 'alt']

    @classmethod
    def resource_setup(cls):
        """Client authentication.

        This method allows to initialize authentication before
        each test case and define parameters of Mistral API Service.
        """
        super(TestCase, cls).resource_setup()
        cls.mistralclient = mistral_client.MistralClientV2(
            cls.os_admin.auth_provider, "workflowv2")

    def setUp(self):
        super(TestCase, self).setUp()
        workbooks = '/usr/share/openstack-tripleo-common/workbooks'
        for workbook in [f for f in os.listdir(workbooks)
                         if os.path.isfile(os.path.join(workbooks, f))]:
            with open(os.path.join(workbooks, workbook)) as f:
                wb = f.read()
            self.mistralclient.create_workbook(wb)

    def tearDown(self):
        super(TestCase, self).tearDown()

        for wb in self.mistralclient.workbooks:
            self.mistralclient.delete_obj('workbooks', wb)

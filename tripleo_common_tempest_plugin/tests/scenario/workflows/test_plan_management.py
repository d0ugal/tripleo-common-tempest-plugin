# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import uuid

from tempest.lib import decorators

from tripleo_common_tempest_plugin.tests import base


class StackWorkflowTestCase(base.TestCase):

    @decorators.idempotent_id('a001f2f0-0ca4-452a-8adf-b511c3fbd29b')
    def test_create_plan(self):

        # TODO(d0ugal): Generating passwords requires some extra setup,
        # including creating the tripleo.undercloud-config Mistral environment.
        # We should look into enabling this later.
        resp, execution = self.mistralclient.create_execution(
            "tripleo.plan_management.v1.create_default_deployment_plan",
            {
                'container': str(uuid.uuid4()),
                'generate_passwords': False,
            }
        )

        self.assertEqual(201, resp.status)
        completed = self.mistralclient.wait_execution_success(execution)
        self.assertEqual('SUCCESS', completed['state'])
        output = json.loads(completed['output'])
        self.assertEqual('Plan created.', output["message"]["message"])

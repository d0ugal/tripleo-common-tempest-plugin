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

import json

from tempest import config

from tripleo_common_tempest_plugin.services import base

CONF = config.CONF


class MistralClientV2(base.MistralClientBase):

    def post_request(self, url_path, file_name):
        headers = {"headers": "Content-Type:text/plain"}

        return self.post(
            url_path,
            base.get_resource(file_name),
            headers=headers
        )

    def get_request(self, url_path):
        headers = {"headers": "Content-Type:application/json"}

        return self.get(url_path, headers=headers)

    def post_json(self, url_path, obj, extra_headers={}):
        headers = {"Content-Type": "application/json"}
        headers = dict(headers, **extra_headers)
        return self.post(url_path, json.dumps(obj), headers=headers)

    def update_request(self, url_path, file_name):
        headers = {"headers": "Content-Type:text/plain"}

        resp, body = self.put(
            url_path,
            base.get_resource(file_name),
            headers=headers
        )

        return resp, json.loads(body)

    def create_execution(self, workflow_name, wf_input=None):
        body = {"workflow_name": workflow_name}

        if wf_input:
            body.update({'input': json.dumps(wf_input)})

        resp, body = self.post('executions', json.dumps(body))

        self.executions.append(json.loads(body)['id'])

        return resp, json.loads(body)

    def create_action_execution(self, request_body, extra_headers={}):
        resp, body = self.post_json('action_executions', request_body,
                                    extra_headers)

        params = json.loads(request_body.get('params', '{}'))
        if params.get('save_result', False):
            self.action_executions.append(json.loads(body)['id'])

        return resp, json.loads(body)

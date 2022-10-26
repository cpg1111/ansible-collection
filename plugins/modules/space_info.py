#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: space_info

author:
  - Polona Mihalič (@PolonaM)
short_description: Returns info about network spaces.
description:
  - Plugin returns information about all network spaces or specific network space if I(name) is provided.
version_added: 1.0.0
extends_documentation_fragment:
  - canonical.maas.cluster_instance
seealso: []
options:
  name:
    description:
      - Name of the network space to be listed.
      - Serves as unique identifier of the network space.
    type: str
"""

EXAMPLES = r"""
- name: Get list of all network spaces
  canonical.maas.space_info:
    cluster_instance:
      host: host-ip
      token_key: token-key
      token_secret: token-secret
      customer_key: customer-key

- name: Get info about a specific network space
  canonical.maas.space_info:
    cluster_instance:
      host: host-ip
      token_key: token-key
      token_secret: token-secret
      customer_key: customer-key
    name: my-network-space
"""

RETURN = r""" # TODO: UPDATE RETURN
records:
  description:
    - Network space info list.
  returned: success
  type: list
  sample:
    name=None
    id=None
    vlans=[]
    resource_uri=None
    subnets=[]
"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, errors
from ..module_utils.client import Client
from ..module_utils.space import Space


def run(module, client: Client):
    if module.params["name"]:
        space = Space.get_by_name(module, must_exist=True)
        response = [space.get(client)]
    else:
        response = client.get("/api/2.0/spaces/").json
    return response


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            name=dict(type="str"),
        ),
    )

    try:
        cluster_instance = module.params["cluster_instance"]
        host = cluster_instance["host"]
        consumer_key = cluster_instance["customer_key"]
        token_key = cluster_instance["token_key"]
        token_secret = cluster_instance["token_secret"]

        client = Client(host, token_key, token_secret, consumer_key)
        records = run(module, client)
        module.exit_json(changed=False, records=records)
    except errors.MaasError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()

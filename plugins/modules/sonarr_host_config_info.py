#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_host_config_info

short_description: Get information about Sonarr host config.

version_added: "1.4.0"

description: Get information about Sonarr host config. Secrets are not returned.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch host config
- name: fetch host config
  devopsarr.sonarr.sonarr_host_config_info:
'''

RETURN = r'''
id:
    description: Host config ID.
    type: int
    returned: always
    sample: 1
bind_address:
    description: Address Sonarr listens on (C(*) for all interfaces).
    returned: always
    type: str
    sample: '*'
port:
    description: HTTP port.
    returned: always
    type: int
    sample: 8989
ssl_port:
    description: HTTPS port.
    returned: always
    type: int
    sample: 9898
enable_ssl:
    description: Enable HTTPS.
    returned: always
    type: bool
    sample: false
launch_browser:
    description: Open a browser on start.
    returned: always
    type: bool
    sample: true
authentication_method:
    description: Authentication method.
    returned: always
    type: str
    sample: 'external'
authentication_required:
    description: When authentication is required.
    returned: always
    type: str
    sample: 'enabled'
analytics_enabled:
    description: Send anonymous usage and error information.
    returned: always
    type: bool
    sample: false
username:
    description: Username for basic or forms authentication.
    returned: always
    type: str
    sample: 'admin'
log_level:
    description: Log level.
    returned: always
    type: str
    sample: 'info'
log_size_limit:
    description: Log size limit in MiB.
    returned: always
    type: int
    sample: 1
console_log_level:
    description: Console log level.
    returned: always
    type: str
    sample: ''
branch:
    description: Update branch.
    returned: always
    type: str
    sample: 'main'
ssl_cert_path:
    description: Path of the HTTPS certificate.
    returned: always
    type: str
    sample: ''
url_base:
    description: URL base, for reverse proxy sub-folder setups.
    returned: always
    type: str
    sample: ''
instance_name:
    description: Instance name.
    returned: always
    type: str
    sample: 'Sonarr'
application_url:
    description: Application URL used in links sent to external applications.
    returned: always
    type: str
    sample: ''
allowed_hosts:
    description: Allowed hosts.
    returned: always
    type: str
    sample: ''
trusted_networks:
    description: Trusted networks.
    returned: always
    type: str
    sample: ''
update_automatically:
    description: Install updates automatically.
    returned: always
    type: bool
    sample: false
update_mechanism:
    description: Update mechanism.
    returned: always
    type: str
    sample: 'docker'
update_script_path:
    description: Path of the update script.
    returned: always
    type: str
    sample: ''
proxy_enabled:
    description: Use a proxy.
    returned: always
    type: bool
    sample: false
proxy_type:
    description: Proxy type.
    returned: always
    type: str
    sample: 'http'
proxy_hostname:
    description: Proxy host name.
    returned: always
    type: str
    sample: ''
proxy_port:
    description: Proxy port.
    returned: always
    type: int
    sample: 8080
proxy_username:
    description: Proxy username.
    returned: always
    type: str
    sample: ''
proxy_bypass_filter:
    description: Comma separated list of addresses that bypass the proxy.
    returned: always
    type: str
    sample: ''
proxy_bypass_local_addresses:
    description: Bypass the proxy for local addresses.
    returned: always
    type: bool
    sample: true
certificate_validation:
    description: Certificate validation.
    returned: always
    type: str
    sample: 'enabled'
backup_folder:
    description: Backup folder.
    returned: always
    type: str
    sample: 'Backups'
backup_interval:
    description: Backup interval in days.
    returned: always
    type: int
    sample: 7
backup_retention:
    description: Backup retention in days.
    returned: always
    type: int
    sample: 28
trust_cgnat_ip_addresses:
    description: Treat CGNAT addresses as local addresses.
    returned: always
    type: bool
    sample: false
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_config_utils import SonarrConfigHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

SECRETS = ['password', 'password_confirmation', 'api_key', 'ssl_cert_password', 'proxy_password']


def get_host_config(result):
    try:
        return helper.get()
    except sonarr.ApiException as e:
        module.fail_json('Error getting host config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting host config: {}'.format(to_native(e)), **result)


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    helper = SonarrConfigHelper(module.api, '/api/v3/config/host', SECRETS)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(helper.view(get_host_config(result)))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

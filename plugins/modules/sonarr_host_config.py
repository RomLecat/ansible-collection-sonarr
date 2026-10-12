#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_host_config

short_description: Manages Sonarr host config.

version_added: "1.4.0"

description:
    - Manages Sonarr host config (Settings, General).
    - Every option is optional. Only the options passed to the module are compared with the current config and written, the others are left untouched.

options:
    bind_address:
        description: Address Sonarr listens on (C(*) for all interfaces).
        required: false
        type: str
    port:
        description: HTTP port.
        required: false
        type: int
    ssl_port:
        description: HTTPS port.
        required: false
        type: int
    enable_ssl:
        description: Enable HTTPS.
        required: false
        type: bool
    launch_browser:
        description: Open a browser on start.
        required: false
        type: bool
    authentication_method:
        description: Authentication method.
        required: false
        type: str
        choices: [none, basic, forms, external]
    authentication_required:
        description: When authentication is required.
        required: false
        type: str
        choices: [enabled, disabledForLocalAddresses]
    analytics_enabled:
        description: Send anonymous usage and error information.
        required: false
        type: bool
    username:
        description: Username for basic or forms authentication.
        required: false
        type: str
    password:
        description: Password for basic or forms authentication. Sonarr never returns it, see O(update_secrets).
        required: false
        type: str
    password_confirmation:
        description: Confirmation of O(password). Sonarr never returns it, see O(update_secrets).
        required: false
        type: str
    log_level:
        description: Log level.
        required: false
        type: str
    log_size_limit:
        description: Log size limit in MiB.
        required: false
        type: int
    console_log_level:
        description: Console log level.
        required: false
        type: str
    branch:
        description: Update branch.
        required: false
        type: str
    api_key:
        description: API key of the Sonarr instance. Changing it makes the O(sonarr_api_key) of the following tasks invalid.
        required: false
        type: str
    ssl_cert_path:
        description: Path of the HTTPS certificate.
        required: false
        type: str
    ssl_cert_password:
        description: Password of the HTTPS certificate. Sonarr never returns it, see O(update_secrets).
        required: false
        type: str
    url_base:
        description: URL base, for reverse proxy sub-folder setups.
        required: false
        type: str
    instance_name:
        description: Instance name.
        required: false
        type: str
    application_url:
        description: Application URL used in links sent to external applications.
        required: false
        type: str
    allowed_hosts:
        description: Allowed hosts (not exposed by the generated sonarr-py model, handled by this module).
        required: false
        type: str
    trusted_networks:
        description: Trusted networks (not exposed by the generated sonarr-py model, handled by this module).
        required: false
        type: str
    update_automatically:
        description: Install updates automatically.
        required: false
        type: bool
    update_mechanism:
        description: Update mechanism.
        required: false
        type: str
        choices: [builtIn, script, external, apt, docker]
    update_script_path:
        description: Path of the update script.
        required: false
        type: str
    proxy_enabled:
        description: Use a proxy.
        required: false
        type: bool
    proxy_type:
        description: Proxy type.
        required: false
        type: str
        choices: [http, socks4, socks5]
    proxy_hostname:
        description: Proxy host name.
        required: false
        type: str
    proxy_port:
        description: Proxy port.
        required: false
        type: int
    proxy_username:
        description: Proxy username.
        required: false
        type: str
    proxy_password:
        description: Proxy password. Sonarr never returns it, see O(update_secrets).
        required: false
        type: str
    proxy_bypass_filter:
        description: Comma separated list of addresses that bypass the proxy.
        required: false
        type: str
    proxy_bypass_local_addresses:
        description: Bypass the proxy for local addresses.
        required: false
        type: bool
    certificate_validation:
        description: Certificate validation.
        required: false
        type: str
        choices: [enabled, disabledForLocalAddresses, disabled]
    backup_folder:
        description: Backup folder.
        required: false
        type: str
    backup_interval:
        description: Backup interval in days.
        required: false
        type: int
    backup_retention:
        description: Backup retention in days.
        required: false
        type: int
    trust_cgnat_ip_addresses:
        description: Treat CGNAT addresses as local addresses.
        required: false
        type: bool
    update_secrets:
        description:
            - Sonarr masks the secrets it stores with C(********).
            - Secrets passed to the module cannot be compared with the masked value, so by default they are only written when the stored value is not masked.
            - Set to V(true) to always write the secrets passed to the module.
        required: false
        default: false
        type: bool

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update only the options listed
- name: Disable analytics and set the instance name
  devopsarr.sonarr.sonarr_host_config:
    analytics_enabled: false
    instance_name: Sonarr

- name: Enable forms authentication
  devopsarr.sonarr.sonarr_host_config:
    authentication_method: forms
    authentication_required: enabled
    username: admin
    password: "{{ sonarr_admin_password }}"
    password_confirmation: "{{ sonarr_admin_password }}"
'''

RETURN = r'''
# The resulting config. Secrets (password, password_confirmation, proxy_password, ssl_cert_password and api_key) are never returned.
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
# Sonarr returns these masked with ********, unlike the api key.
MASKED_SECRETS = ['password', 'password_confirmation', 'ssl_cert_password', 'proxy_password']


OPTIONS = [
    'bind_address',
    'port',
    'ssl_port',
    'enable_ssl',
    'launch_browser',
    'authentication_method',
    'authentication_required',
    'analytics_enabled',
    'username',
    'password',
    'password_confirmation',
    'log_level',
    'log_size_limit',
    'console_log_level',
    'branch',
    'api_key',
    'ssl_cert_path',
    'ssl_cert_password',
    'url_base',
    'instance_name',
    'application_url',
    'allowed_hosts',
    'trusted_networks',
    'update_automatically',
    'update_mechanism',
    'update_script_path',
    'proxy_enabled',
    'proxy_type',
    'proxy_hostname',
    'proxy_port',
    'proxy_username',
    'proxy_password',
    'proxy_bypass_filter',
    'proxy_bypass_local_addresses',
    'certificate_validation',
    'backup_folder',
    'backup_interval',
    'backup_retention',
    'trust_cgnat_ip_addresses',
]


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        bind_address=dict(type='str'),
        port=dict(type='int'),
        ssl_port=dict(type='int'),
        enable_ssl=dict(type='bool'),
        launch_browser=dict(type='bool'),
        authentication_method=dict(type='str', choices=['none', 'basic', 'forms', 'external']),
        authentication_required=dict(type='str', choices=['enabled', 'disabledForLocalAddresses']),
        analytics_enabled=dict(type='bool'),
        username=dict(type='str'),
        password=dict(type='str', no_log=True),
        password_confirmation=dict(type='str', no_log=True),
        log_level=dict(type='str'),
        log_size_limit=dict(type='int'),
        console_log_level=dict(type='str'),
        branch=dict(type='str'),
        api_key=dict(type='str', no_log=True),
        ssl_cert_path=dict(type='str'),
        ssl_cert_password=dict(type='str', no_log=True),
        url_base=dict(type='str'),
        instance_name=dict(type='str'),
        application_url=dict(type='str'),
        allowed_hosts=dict(type='str'),
        trusted_networks=dict(type='str'),
        update_automatically=dict(type='bool'),
        update_mechanism=dict(type='str', choices=['builtIn', 'script', 'external', 'apt', 'docker']),
        update_script_path=dict(type='str'),
        proxy_enabled=dict(type='bool'),
        proxy_type=dict(type='str', choices=['http', 'socks4', 'socks5']),
        proxy_hostname=dict(type='str'),
        proxy_port=dict(type='int'),
        proxy_username=dict(type='str'),
        proxy_password=dict(type='str', no_log=True),
        proxy_bypass_filter=dict(type='str', no_log=False),
        proxy_bypass_local_addresses=dict(type='bool'),
        certificate_validation=dict(type='str', choices=['enabled', 'disabledForLocalAddresses', 'disabled']),
        backup_folder=dict(type='str'),
        backup_interval=dict(type='int'),
        backup_retention=dict(type='int'),
        trust_cgnat_ip_addresses=dict(type='bool'),
        update_secrets=dict(type='bool', default=False),
    )


def read_host_config(result):
    try:
        return helper.get()
    except sonarr.ApiException as e:
        module.fail_json('Error getting host config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting host config: {}'.format(to_native(e)), **result)


def update_host_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except sonarr.ApiException as e:
            module.fail_json('Error updating host config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating host config: {}'.format(to_native(e)), **result)
        result.update(helper.view(response))
    else:
        result.update(helper.view(want))
    # No need to exit module since it will exit by default either way


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    helper = SonarrConfigHelper(module.api, '/api/v3/config/host', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_host_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS, MASKED_SECRETS, module.params['update_secrets'])

    # Update an existing resource.
    if changed:
        update_host_config(want, result)
        if module._diff:
            result['diff'] = dict(before=helper.view(state), after=helper.view(want))

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

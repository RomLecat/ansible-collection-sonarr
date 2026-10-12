#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_ui_config_info

short_description: Get information about Sonarr UI config.

version_added: "1.4.0"

description: Get information about Sonarr UI config.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch UI config
- name: fetch UI config
  devopsarr.sonarr.sonarr_ui_config_info:
'''

RETURN = r'''
id:
    description: UI config ID.
    type: int
    returned: always
    sample: 1
first_day_of_week:
    description: First day of the week.
    returned: always
    type: int
    sample: 1
calendar_week_column_header:
    description: Calendar week column header format.
    returned: always
    type: str
    sample: 'ddd DD/MM'
short_date_format:
    description: Short date format.
    returned: always
    type: str
    sample: 'DD MMM YYYY'
long_date_format:
    description: Long date format.
    returned: always
    type: str
    sample: 'dddd, D MMMM YYYY'
time_format:
    description: Time format.
    returned: always
    type: str
    sample: 'HH:mm'
show_relative_dates:
    description: Show relative dates.
    returned: always
    type: bool
    sample: true
enable_color_impaired_mode:
    description: Color impaired mode.
    returned: always
    type: bool
    sample: false
theme:
    description: UI theme.
    returned: always
    type: str
    sample: 'auto'
ui_language:
    description: UI language ID.
    returned: always
    type: int
    sample: 1
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_config_utils import SonarrConfigHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

SECRETS = []


def get_ui_config(result):
    try:
        return helper.get()
    except sonarr.ApiException as e:
        module.fail_json('Error getting UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting UI config: {}'.format(to_native(e)), **result)


def run_module():
    global helper
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    helper = SonarrConfigHelper(module.api, '/api/v3/config/ui', SECRETS)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(helper.view(get_ui_config(result)))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_ui_config

short_description: Manages Sonarr UI config.

version_added: "1.4.0"

description:
    - Manages Sonarr UI config (Settings, UI).
    - Every option is optional. Only the options passed to the module are compared with the current config and written, the others are left untouched.

options:
    first_day_of_week:
        description: First day of the week. 0 - 'Sunday' 1 - 'Monday' 2 - 'Tuesday' 3 - 'Wednesday' 4 - 'Thursday' 5 - 'Friday' 6 - 'Saturday'.
        required: false
        type: int
        choices: [0, 1, 2, 3, 4, 5, 6]
    calendar_week_column_header:
        description: Calendar week column header format.
        required: false
        type: str
    short_date_format:
        description: Short date format.
        required: false
        type: str
    long_date_format:
        description: Long date format.
        required: false
        type: str
    time_format:
        description: Time format.
        required: false
        type: str
    show_relative_dates:
        description: Show relative dates (Today, Yesterday...).
        required: false
        type: bool
    enable_color_impaired_mode:
        description: Enable the color impaired mode.
        required: false
        type: bool
    theme:
        description: UI theme.
        required: false
        type: str
        choices: [auto, dark, light]
    ui_language:
        description: UI language ID. 1 is English.
        required: false
        type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update only the options listed
- name: Update UI config
  devopsarr.sonarr.sonarr_ui_config:
    first_day_of_week: 1
    theme: dark
    time_format: 'HH:mm'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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

OPTIONS = [
    'first_day_of_week',
    'calendar_week_column_header',
    'short_date_format',
    'long_date_format',
    'time_format',
    'show_relative_dates',
    'enable_color_impaired_mode',
    'theme',
    'ui_language',
]

SECRETS = []


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        first_day_of_week=dict(type='int', choices=[0, 1, 2, 3, 4, 5, 6]),
        calendar_week_column_header=dict(type='str'),
        short_date_format=dict(type='str'),
        long_date_format=dict(type='str'),
        time_format=dict(type='str'),
        show_relative_dates=dict(type='bool'),
        enable_color_impaired_mode=dict(type='bool'),
        theme=dict(type='str', choices=['auto', 'dark', 'light']),
        ui_language=dict(type='int'),
    )


def read_ui_config(result):
    try:
        return helper.get()
    except sonarr.ApiException as e:
        module.fail_json('Error getting UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting UI config: {}'.format(to_native(e)), **result)


def update_ui_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = helper.update(want)
        except sonarr.ApiException as e:
            module.fail_json('Error updating UI config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating UI config: {}'.format(to_native(e)), **result)
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
    helper = SonarrConfigHelper(module.api, '/api/v3/config/ui', SECRETS)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_ui_config(result)
    result.update(helper.view(state))

    # Overlay only the options passed on the current resource.
    want, changed = helper.merge(state, module.params, OPTIONS)

    # Update an existing resource.
    if changed:
        update_ui_config(want, result)
        if module._diff:
            result['diff'] = dict(before=helper.view(state), after=helper.view(want))

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

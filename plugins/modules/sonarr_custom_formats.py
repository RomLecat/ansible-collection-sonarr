#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_custom_formats

short_description: Manages a list of Sonarr custom formats.

version_added: "1.4.0"

description:
    - Manages a list of Sonarr custom formats with a single API client and a single listing.
    - Custom formats are matched by exact name, the missing ones are created and the different ones are updated.
    - Custom formats that are not listed are never deleted.

options:
    custom_formats:
        description: Custom format list.
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Name.
                required: true
                type: str
            include_custom_format_when_renaming:
                description: Include custom format when renaming flag.
                type: bool
            specifications:
                description: Specification list.
                type: list
                elements: dict
                suboptions:
                    negate:
                        description: Negate flag.
                        type: bool
                    required:
                        description: Required flag.
                        type: bool
                    name:
                        description: Specification name.
                        type: str
                    implementation:
                        description: Implementation.
                        type: str
                    fields:
                        description: Configuration field list.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description: Field name.
                                type: str
                            value:
                                description: Field value.
                                type: raw

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create or update custom formats
- name: Create or update custom formats
  devopsarr.sonarr.sonarr_custom_formats:
    custom_formats:
    - name: "Language"
      include_custom_format_when_renaming: false
      specifications:
      - name: "arabic"
        implementation: "LanguageSpecification"
        negate: false
        required: true
        fields:
        - name: "value"
          value: 26
    - name: "x265"
      include_custom_format_when_renaming: false
      specifications:
      - name: "x265"
        implementation: "ReleaseTitleSpecification"
        negate: false
        required: true
        fields:
        - name: "value"
          value: "(x|h)\\.?265"
'''

RETURN = r'''
created:
    description: Names of the created custom formats.
    returned: always
    type: list
    elements: str
    sample: ["Language"]
updated:
    description: Names of the updated custom formats.
    returned: always
    type: list
    elements: str
    sample: ["x265"]
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_diff import build_diff
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_specification_utils import SpecificationHelper, custom_format_changed
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def init_module_args(specification_helper):
    # define available arguments/parameters a user can pass to the module
    custom_format_args = dict(
        name=dict(type='str', required=True),
        include_custom_format_when_renaming=dict(type='bool'),
        specifications=dict(type='list', elements='dict', options=specification_helper.specification_args),
    )
    return dict(
        custom_formats=dict(type='list', elements='dict', required=True, options=custom_format_args),
    )


def list_custom_formats(client, module, result):
    try:
        return client.list_custom_format()
    except sonarr.ApiException as e:
        module.fail_json('Error listing custom formats: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing custom formats: {}'.format(to_native(e)), **result)


def create_custom_format(client, module, result, want):
    try:
        client.create_custom_format(custom_format_resource=want)
    except sonarr.ApiException as e:
        module.fail_json('Error creating custom format {}: {}\n body: {}'.format(want.name, to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error creating custom format {}: {}'.format(want.name, to_native(e)), **result)


def update_custom_format(client, module, result, want):
    try:
        client.update_custom_format(custom_format_resource=want, id=str(want.id))
    except sonarr.ApiException as e:
        module.fail_json('Error updating custom format {}: {}\n body: {}'.format(want.name, to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error updating custom format {}: {}'.format(want.name, to_native(e)), **result)


def item_diff(name, before, after):
    diff = build_diff(before, after)
    if diff is not None:
        diff['before_header'] = name
        diff['after_header'] = name
    return diff


def check_names(module, result):
    names = [item['name'] for item in module.params['custom_formats']]
    duplicates = sorted(set(name for name in names if names.count(name) > 1))
    if duplicates:
        module.fail_json('Duplicate custom format names: {}'.format(', '.join(duplicates)), **result)


def run_module():
    specification_helper = SpecificationHelper()

    module = SonarrModule(
        argument_spec=init_module_args(specification_helper),
        supports_check_mode=True,
    )

    client = sonarr.CustomFormatApi(module.api)
    result = dict(
        changed=False,
        created=[],
        updated=[],
    )
    diffs = []

    check_names(module, result)

    current = dict((custom_format.name, custom_format) for custom_format in list_custom_formats(client, module, result))

    for item in module.params['custom_formats']:
        want = sonarr.CustomFormatResource(
            name=item['name'],
            include_custom_format_when_renaming=item['include_custom_format_when_renaming'],
            specifications=specification_helper.populate_specifications(item['specifications'], 'custom_format'),
        )
        state = current.get(item['name'])

        if state is None:
            diffs.append(item_diff(item['name'], None, want))
            if not module.check_mode:
                create_custom_format(client, module, result, want)
            result['created'].append(item['name'])
        else:
            want.id = state.id
            if custom_format_changed(state, want):
                diffs.append(item_diff(item['name'], state, want))
                if not module.check_mode:
                    update_custom_format(client, module, result, want)
                result['updated'].append(item['name'])

    result['changed'] = bool(result['created'] or result['updated'])
    if module._diff and result['changed']:
        result['diff'] = [diff for diff in diffs if diff is not None]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

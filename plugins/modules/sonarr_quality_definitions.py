#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_quality_definitions

short_description: Manages a list of Sonarr quality definitions.

version_added: "1.4.0"

description:
    - Manages a list of Sonarr quality definitions with a single API client, a single listing and a single bulk update.
    - Quality definitions are matched by exact quality name and only the different ones are sent.

options:
    quality_definitions:
        description: Quality definition list.
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Name.
                required: true
                type: str
            title:
                description: Title.
                type: str
            min_size:
                description: Minimum size.
                type: float
            max_size:
                description: Maximum size.
                type: float
            preferred_size:
                description: Preferred size.
                type: float

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update qualities
- name: Update qualities
  devopsarr.sonarr.sonarr_quality_definitions:
    quality_definitions:
    - name: HDTV-2160p
      title: HDTV-2160p
      max_size: 200.0
      min_size: 35.0
      preferred_size: 95.0
    - name: WEBRip-480p
      title: WEBRip-480p
      max_size: 130.0
      min_size: 1.0
      preferred_size: 20.0
'''

RETURN = r'''
updated:
    description: Names of the updated quality definitions.
    returned: always
    type: list
    elements: str
    sample: ["HDTV-2160p"]
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_diff import build_diff
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    quality_args = dict(
        name=dict(type='str', required=True),
        title=dict(type='str'),
        min_size=dict(type='float'),
        max_size=dict(type='float'),
        preferred_size=dict(type='float'),
    )
    return dict(
        quality_definitions=dict(type='list', elements='dict', required=True, options=quality_args),
    )


def list_qualities(client, module, result):
    try:
        return client.list_quality_definition()
    except sonarr.ApiException as e:
        module.fail_json('Error listing qualities: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing qualities: {}'.format(to_native(e)), **result)


def update_qualities(client, module, result, wanted):
    try:
        client.put_quality_definition_update(quality_definition_resource=wanted)
    except sonarr.ApiException as e:
        module.fail_json('Error updating qualities: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error updating qualities: {}'.format(to_native(e)), **result)


def item_diff(name, before, after):
    diff = build_diff(before, after)
    if diff is not None:
        diff['before_header'] = name
        diff['after_header'] = name
    return diff


def check_names(module, result):
    names = [item['name'] for item in module.params['quality_definitions']]
    duplicates = sorted(set(name for name in names if names.count(name) > 1))
    if duplicates:
        module.fail_json('Duplicate quality names: {}'.format(', '.join(duplicates)), **result)


def run_module():
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    client = sonarr.QualityDefinitionApi(module.api)
    result = dict(
        changed=False,
        updated=[],
    )
    diffs = []
    wanted = []

    check_names(module, result)

    current = dict((quality.quality.name, quality) for quality in list_qualities(client, module, result))

    for item in module.params['quality_definitions']:
        state = current.get(item['name'])
        if state is None:
            module.fail_json('Quality {} not found'.format(item['name']), **result)

        want = sonarr.QualityDefinitionResource(
            title=item['title'],
            min_size=item['min_size'],
            max_size=item['max_size'],
            preferred_size=item['preferred_size'],
        )
        want.id = state.id
        want.weight = state.weight
        want.quality = state.quality
        if want != state:
            diffs.append(item_diff(item['name'], state, want))
            wanted.append(want)
            result['updated'].append(item['name'])

    if wanted and not module.check_mode:
        update_qualities(client, module, result, wanted)

    result['changed'] = bool(wanted)
    if module._diff and result['changed']:
        result['diff'] = [diff for diff in diffs if diff is not None]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

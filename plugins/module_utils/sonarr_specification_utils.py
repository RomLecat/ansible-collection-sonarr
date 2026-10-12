# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper


class SpecificationHelper():
    def __init__(self):
        # type: () -> None
        self.field_helper = FieldHelper()

        self.specification_args = dict(
            name=dict(type='str'),
            implementation=dict(type='str'),
            negate=dict(type='bool'),
            required=dict(type='bool'),
            fields=dict(type='list', elements='dict', options=self.field_helper.field_args),
        )

    def populate_specifications(self, specification_list, type):
        # type: (list, str) -> list
        specifications = []

        for specification in specification_list:
            spec = {
                'name': specification['name'],
                'implementation': specification['implementation'],
                'negate': specification['negate'],
                'required': specification['required'],
                'fields': self.field_helper.populate_fields(specification['fields']),
            }

            if type == "custom_format":
                specifications.append(
                    sonarr.CustomFormatSpecificationSchema(**spec),
                )
            if type == "auto_tag":
                specifications.append(
                    sonarr.AutoTaggingSpecificationSchema(**spec),
                )

        return specifications


def custom_format_changed(status, want):
    # Check if the basic attributes are different
    if (
        want.name != status.name
        or want.include_custom_format_when_renaming != status.include_custom_format_when_renaming
        or len(want.specifications) != len(status.specifications)
    ):
        return True

    # Create a dictionary to store specifications by name for faster lookup
    status_specs = {spec.name: spec for spec in status.specifications}

    # Check if any specification is different
    for want_spec in want.specifications:
        status_spec = status_specs.get(want_spec.name)
        if (
            status_spec is None
            or want_spec.implementation != status_spec.implementation
            or want_spec.required != status_spec.required
            or want_spec.negate != status_spec.negate
        ):
            return True

        # Check if any field within the specification is different
        for want_field in want_spec.fields:
            status_field = next(
                (field for field in status_spec.fields if field.name == want_field.name),
                None,
            )
            if status_field is None or want_field.value != status_field.value:
                return True

    return False

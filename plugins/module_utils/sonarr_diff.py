# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import re

MASK = '********'
SECRET_RE = re.compile(r'apikey|api_key|password|passkey|cookie|token|secret|pid|rsskey|username|key$', re.IGNORECASE)
SORTED_LISTS = ('fields', 'specifications', 'format_items')
NOT_STATE = ('changed', 'diff')
# Read-only attributes computed by the server, hidden from both sides of the diff.
IGNORED_KEYS = ('info_link', 'implementation_name', 'message', 'presets', 'unmapped_folders', 'free_space', 'accessible', 'statistics', 'images')
IGNORED_PREFIX = 'supports_'


def _plain(obj):
    # Pydantic object or dict to json compatible dict, snake case.
    if obj is None:
        return {}
    if hasattr(obj, 'model_dump'):
        obj = obj.model_dump(by_alias=False)
    return json.loads(json.dumps(obj, default=str))


def _is_secret(name, value):
    return value not in (None, '') and (value == MASK or bool(SECRET_RE.search(name or '')))


def _clean_field(field):
    # A provider field is reduced to what is sent to the api, with secrets hidden.
    value = field.get('value')
    return {'name': field.get('name'), 'value': MASK if _is_secret(field.get('name'), value) else value}


def _clean(value):
    if isinstance(value, list):
        return [_clean(item) for item in value]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if not isinstance(value, dict):
        return value
    out = {}
    for key, item in value.items():
        if item is None or key in IGNORED_KEYS or key.startswith(IGNORED_PREFIX):
            continue
        if key == 'fields' and isinstance(item, list):
            out[key] = [_clean_field(field) for field in item]
        elif not isinstance(item, (dict, list)) and _is_secret(key, item):
            out[key] = MASK
        else:
            out[key] = _clean(item)
        if key in SORTED_LISTS and isinstance(out[key], list):
            out[key] = sorted(out[key], key=lambda i: str(i.get('name')))
        if key == 'tags' and isinstance(out[key], list):
            out[key] = sorted(out[key])
    return out


def set_diff(module, result, want=None):
    """Add the diff of a create (no current state), an update or a delete (want is None) to the result.

    The current state is the one held by result, so call it before result is updated.
    """
    if not module._diff:
        return
    after = _clean(_plain(want))
    before = {}
    if result.get('id'):
        before = _clean(_plain(dict((key, item) for key, item in result.items() if key not in NOT_STATE)))
    # The protocol is derived by the server from the implementation when it is not sent.
    if after and 'protocol' not in after:
        before.pop('protocol', None)
    result['diff'] = dict(before=before, after=after)


def build_diff(before, after):
    """Return dict(before, after) for one resource, cleaned like set_diff does."""
    return dict(before=_clean(_plain(before)), after=_clean(_plain(after)))

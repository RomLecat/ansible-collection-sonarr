# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import re

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

AUTH_SETTINGS = ['X-Api-Key']
MASK = '********'


def to_camel(name):
    # ssl_cert_path -> sslCertPath
    first, *others = name.split('_')
    return first + ''.join(part.capitalize() for part in others)


def to_snake(name):
    # sslCertPath -> ssl_cert_path
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


class SonarrConfigHelper(object):
    """Read and update a singleton configuration endpoint, e.g. /api/v3/config/host.

    The configuration is handled as the raw JSON document sent by the server.
    Only the options explicitly passed are overlaid on it, so every other
    property, including the ones unknown to the sonarr-py models, is sent back
    unchanged.
    """

    def __init__(self, api_client, resource_path, secrets=None):
        self.api_client = api_client
        self.resource_path = resource_path
        self.secrets = secrets or []

    def _request(self, method, path, path_params=None, body=None):
        headers = {'Accept': 'application/json'}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        method, url, headers, body, post_params = self.api_client.param_serialize(
            method=method,
            resource_path=path,
            path_params=path_params,
            header_params=headers,
            body=body,
            auth_settings=AUTH_SETTINGS,
        )
        response = self.api_client.call_api(method, url, header_params=headers, body=body, post_params=post_params)
        response.read()
        if not 200 <= response.status < 300:
            raise sonarr.ApiException.from_response(
                http_resp=response,
                body=response.data.decode('utf-8', 'replace'),
                data=None,
            )
        return json.loads(response.data)

    def get(self):
        return self._request('GET', self.resource_path)

    def update(self, want):
        return self._request('PUT', self.resource_path + '/{id}', path_params={'id': str(want['id'])}, body=want)

    def merge(self, current, params, options, masked=None, force_masked=False):
        """Overlay the passed options on the current configuration.

        Sonarr may return a secret masked with ********: it cannot be compared with
        the value passed, so a masked secret (listed in masked) is only written
        when force_masked is set.

        Returns the configuration to send and whether it differs from the current one.
        """
        masked = masked or []
        want = dict(current)
        for option in options:
            value = params.get(option)
            if value is None:
                continue
            if option in masked and current.get(to_camel(option)) == MASK and not force_masked:
                continue
            want[to_camel(option)] = value
        return want, want != current

    def view(self, config):
        """Snake case representation of a configuration, without secrets."""
        return dict((to_snake(key), value) for key, value in config.items() if to_snake(key) not in self.secrets)

# This file is part of Restifier
#
# Restifier is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Restifier is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Restifier.  If not, see <http://www.gnu.org/licenses/>.
import logging


class WhiteListIPMiddleware(object):
    """
    """
    def __init__(self, app, allowed_addresses=None, check_address=None,
                 allows_by_default=False, raise_on_error=False):
        """
        :param app: the WSGI app we will that comes after us
        :param allowed_addresses: list of remote addresses from which to allow
        access
        :type allowed_addresses: list
        """
        self.app = app
        self.allowed_addresses = allowed_addresses
        self.check_address = check_address
        self.allows_by_default = allows_by_default
        self.log = logging.getLogger(self.__class__.__name__)
        self.raise_on_error = raise_on_error

    def __call__(self, environ, start_response):
        addr = environ.get('REMOTE_ADDR', 'UNKNOWN')

        if self.check_address:
            try:
                allowed = self.check_address(addr)
            except Exception, ex:
                self.log.debug(repr(ex))
                if self.raise_on_error:
                    raise ex

                allowed = self.allows_by_default
        elif isinstance(self.allowed_addresses, list) and \
             addr in self.allowed_addresses:
            allowed = True
        else:
            allowed = self.allows_by_default

        if allowed:  # pass through to the next app
            return self.app(environ, start_response)
        else:  # put up a response denied
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return ['You are forbidden to view this resource']

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
from __future__ import absolute_import
from nose.tools import ok_, eq_
from webtest import TestApp, AppError
from webtest.debugapp import debug_app
from restifier.middleware.whitelist import WhiteListIPMiddleware
from .base import BaseMiddlewareTest


def raise_exception(*args, **kwargs):
    raise Exception()


class TestWhiteListIPMiddleware(BaseMiddlewareTest):
    def setup(self):
        super(self.__class__, self).setup()
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 allowed_addresses=["127.0.0.2"]))

    def test_forbidden(self):
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '192.168.0.1'},
                            expect_errors=True)
        eq_(resp.status_code, 403)

    def test_accept(self):
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'})
        eq_(resp.status_code, 200)

    def test_accept_with_callable(self):
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 check_address=lambda addr: True))
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'})
        eq_(resp.status_code, 200)

    def test_fobidden_with_callable(self):
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 check_address=lambda addr: False))
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'},
                            expect_errors=True)
        eq_(resp.status_code, 403)

    def test_accept_with_callable_and_error(self):
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 check_address=raise_exception,
                                                 allows_by_default=True))
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'})
        eq_(resp.status_code, 200)

    def test_fobidden_with_callable_and_error(self):
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 check_address=raise_exception,
                                                 allows_by_default=False))
        resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'},
                            expect_errors=True)
        eq_(resp.status_code, 403)

    def test_fobidden_with_callable_and_raise_error(self):
        self.app = TestApp(WhiteListIPMiddleware(self.demo_app,
                                                 check_address=raise_exception,
                                                 allows_by_default=False,
                                                 raise_on_error=True))
        try:
            resp = self.app.get("/", extra_environ={"REMOTE_ADDR": '127.0.0.2'},
                                expect_errors=True)
            ok_(False, "expecting error: %s" % resp)
        except Exception:
            pass

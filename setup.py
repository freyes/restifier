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
import sys
import os.path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="restifier",
      version="0.1dev",
      author="Felipe Reyes",
      author_email="freyes@tty.cl",
      description="Simple library to provide REST features",
      tests_require=['tox'],
      cmdclass = {'test': Tox},
      license="GPLv3",
      keywords="wsgi rest",
      url="https://github.com/freyes/restifiert",
      packages=find_packages(),
      long_description=read("README.rst"),
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
        )

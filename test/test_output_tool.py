# -*- coding: utf-8 -*-
#
# This tool helps you to rebase package to the latest version
# Copyright (C) 2013-2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Petr Hracek <phracek@redhat.com>
#          Tomas Hozza <thozza@redhat.com>

import os

from .base_test import BaseTest
from rebasehelper.output_tool import OutputTool
from rebasehelper.settings import REBASE_HELPER_RESULTS_LOG
from rebasehelper.base_output import OutputLogger

class TestOutputTool(BaseTest):
    """
    Class is used for testing OutputTool
    """

    def get_data(self):
        data = {'old': {'patches_full': {0: ['mytest.patch', '-p1', 0],
                                         1: ['mytest2.patch', '-p1', 1]},
                        'srpm': './test-1.2.0-1.src.rpm',
                        'rpm': ['./test-1.2.0-1.x86_64.rpm', './test-devel-1.2.0-1.x86_64.rpm'],
                        'logs': ['logfile1.log', 'logfile2.log']
                        },
                'new': {'patches_full': {0: ['mytest.patch', 0, '-p1'],
                                         1: ['mytest2.patch', 1, '-p1']},
                        'srpm': './test-1.2.2-1.src.rpm',
                        'rpm': ['./test-1.2.2-1.x86_64.rpm', './test-devel-1.2.2-1.x86_64.rpm'],
                        'logs': ['logfile3.log', 'logfile4.log']},
                'summary_info': {'deleted': ['mytest2.patch']},
                'results_dir': self.WORKING_DIR,
                'moved': ['/usr/sbin/test', '/usr/sbin/test2'],
                }
        return data

    def get_expected_output(self):
        expected_output = """Patches were neither modified nor deleted.

Old (S)RPM packages:
---------------------
SRPM package(s): are in directory  :
- test-1.2.0-1.src.rpm
RPM package(s): are in directory . :
- test-1.2.0-1.x86_64.rpm
- test-devel-1.2.0-1.x86_64.rpm
Available Old logs:
- logfile1.log
- logfile2.log

New (S)RPM packages:
---------------------
SRPM package(s): are in directory  :
- test-1.2.2-1.src.rpm
RPM package(s): are in directory . :
- test-1.2.2-1.x86_64.rpm
- test-devel-1.2.2-1.x86_64.rpm
Available New logs:
- logfile3.log
- logfile4.log
Following files were moved:
/usr/sbin/test
/usr/sbin/test2"""
        return expected_output

    def test_text_output(self):
        output = OutputTool('text')
        data = self.get_data()
        OutputLogger.set_build_data('old', data['old'])
        OutputLogger.set_build_data('new', data['new'])
        OutputLogger.set_checker_output('Following files were moved', '\n'.join(data['moved']))

        logfile = os.path.join(self.TESTS_DIR, REBASE_HELPER_RESULTS_LOG)
        output.print_information(logfile)

        with open(logfile) as f:
            assert f.read().strip() == self.get_expected_output()

        os.unlink(logfile)

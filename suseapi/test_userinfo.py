# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2013 Michal Čihař <mcihar@suse.cz>
#
# This file is part of python-suseapi <https://github.com/nijel/python-suseapi>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''
Testing of Bugzilla connector
'''

from unittest import TestCase
from mockldap import MockLdap

from suseapi.userinfo import UserInfo


class UserInfoTest(TestCase):
    def test_department(self):
        mockldap = MockLdap({
            'o=Novell': {'o': 'Novell'},
            'cn=mcihar,o=Novell': {
                'cn': 'mcihar',
                'uid': 'mcihar',
                'email': 'mcihar@suse.com',
                'ou': ['L3/Maintenance'],
            },
        })
        mockldap.start()
        try:
            userinfo = UserInfo('ldap://ldap', 'o=Novell')
            self.assertEqual(
                'L3/Maintenance',
                userinfo.get_department('mcihar')
            )
            self.assertEqual(
                'L3/Maintenance',
                userinfo.get_department('mcihar@suse.com')
            )
            self.assertEqual(
                'Security team',
                userinfo.get_department('security-team@suse.de')
            )
        finally:
            mockldap.stop()
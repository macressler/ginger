#
# Project Ginger
#
# Copyright IBM Corp, 2016
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import mock
import unittest

from wok.plugins.ginger.model.powermanagement import PowerProfilesModel
from wok.plugins.ginger.model.powermanagement import PowerProfileModel


def mock_powerprofiles_init(self):
    self.error = None


def mock_powerprofile_init(self):
    self.active_powerprofile = 'default'


class PowerManagementTests(unittest.TestCase):

    def setUp(self):
        PowerProfilesModel.__init__ = mock_powerprofiles_init
        self.power_profiles_model = PowerProfilesModel()

        PowerProfileModel.__init__ = mock_powerprofile_init
        self.power_profile_model = PowerProfileModel()

    @mock.patch('wok.plugins.ginger.model.powermanagement.run_command')
    def test_powermanagement_get_list(self, mock_run_command):
        mock_run_command.return_value = ["", "", 0]
        self.power_profiles_model.get_list()
        mock_run_command.assert_called_once_with(['tuned-adm', 'list'])

    def test_powermanagement_lookup(self):
        lookup = self.power_profile_model.lookup('test_profile')
        self.assertEqual(lookup, {"name": 'test_profile', "active": False})

    @mock.patch('wok.plugins.ginger.model.powermanagement.run_command')
    def test_powermanagement_update(self, mock_run_command):
        mock_run_command.return_value = ["", "", 0]
        self.power_profile_model.update(
            'test_active_profile',
            {'active': True}
        )
        tuned_cmd = ["tuned-adm", "profile", "test_active_profile"]
        mock_run_command.assert_called_once_with(tuned_cmd)

        self.power_profile_model.update('default', {'active': True})
        tuned_cmd = ["tuned-adm", "profile", "default"]
        mock_run_command.assert_called_with(tuned_cmd)

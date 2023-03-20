#
# Copyright 2019 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Test the principal cleaner."""
from unittest.mock import patch

from rest_framework import status

from management.group.model import Group
from management.principal.cleaner import clean_tenant_principals
from management.principal.model import Principal
from tests.identity_request import IdentityRequest


class PrincipalCleanerTests(IdentityRequest):
    """Test the principal cleaner functions."""

    def setUp(self):
        """Set up the principal cleaner tests."""
        super().setUp()
        self.group = Group(name="groupA", tenant=self.tenant)
        self.group.save()

    def test_principal_cleanup_none(self):
        """Test that we can run a principal clean up on a tenant with no principals."""
        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 0)

    @patch(
        "management.principal.proxy.PrincipalProxy._request_principals",
        return_value={"status_code": status.HTTP_200_OK, "data": []},
    )
    def test_principal_cleanup_skip_cross_account_principals(self, mock_request):
        """Test that principal clean up on a tenant will skip cross account principals."""
        Principal.objects.create(user_id="123456", tenant=self.tenant)
        Principal.objects.create(user_id="111111", cross_account=True, tenant=self.tenant)
        self.assertEqual(Principal.objects.count(), 2)

        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 1)

    @patch(
        "management.principal.proxy.PrincipalProxy._request_principals",
        return_value={"status_code": status.HTTP_200_OK, "data": []},
    )
    def test_principal_cleanup_principal_in_group(self, mock_request):
        """Test that we can run a principal clean up on a tenant with a principal in a group."""
        self.principal = Principal(user_id="123456", tenant=self.tenant)
        self.principal.save()
        self.group.principals.add(self.principal)
        self.group.save()
        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 0)

    @patch(
        "management.principal.proxy.PrincipalProxy._request_principals",
        return_value={"status_code": status.HTTP_200_OK, "data": []},
    )
    def test_principal_cleanup_principal_not_in_group(self, mock_request):
        """Test that we can run a principal clean up on a tenant with a principal not in a group."""
        self.principal = Principal(user_id="123456", tenant=self.tenant)
        self.principal.save()
        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 0)

    @patch(
        "management.principal.proxy.PrincipalProxy._request_principals",
        return_value={"status_code": status.HTTP_200_OK, "data": [{"user_id": "123456"}]},
    )
    def test_principal_cleanup_principal_exists(self, mock_request):
        """Test that we can run a principal clean up on a tenant with an existing principal."""
        self.principal = Principal(user_id="123456", tenant=self.tenant)
        self.principal.save()
        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 1)

    @patch(
        "management.principal.proxy.PrincipalProxy._request_principals",
        return_value={"status_code": status.HTTP_504_GATEWAY_TIMEOUT},
    )
    def test_principal_cleanup_principal_error(self, mock_request):
        """Test that we can handle a principal clean up with an unexpected error from proxy."""
        self.principal = Principal(user_id="123456", tenant=self.tenant)
        self.principal.save()
        try:
            clean_tenant_principals(self.tenant)
        except Exception:
            self.fail(msg="clean_tenant_principals encountered an exception")
        self.assertEqual(Principal.objects.count(), 1)

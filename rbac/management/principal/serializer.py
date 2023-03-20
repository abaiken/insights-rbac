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

"""Serializer for principal management."""
from management.serializer_override_mixin import SerializerCreateOverrideMixin
from rest_framework import serializers

from .model import Principal


class PrincipalSerializer(SerializerCreateOverrideMixin, serializers.ModelSerializer):
    """Serializer for the Principal model."""

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metadata for the serializer."""

        model = Principal
        fields = ("user_id",)


class PrincipalInputSerializer(serializers.Serializer):
    """Serializer for the Principal model."""

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        """Metadata for the serializer."""

        fields = ("user_id",)

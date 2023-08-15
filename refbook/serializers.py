from rest_framework import serializers
from refbook.models import Refbook


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook

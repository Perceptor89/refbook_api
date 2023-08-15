from rest_framework import serializers
from refbook.models import Refbook


class RefbookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Refbook

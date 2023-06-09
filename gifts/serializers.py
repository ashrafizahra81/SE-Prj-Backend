from rest_framework import serializers
from Backend import settings
from .models import *

class GiftInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        # exclude = ('discount_code', 'type', 'id')
        fields = ('description', 'score', 'date')
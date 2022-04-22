from rest_framework import serializers
from .models import *


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'user_phone_number', 'user_postal_code', 'user_address')
        extera_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserEditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'user_phone_number', 'user_postal_code', 'user_address')


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ('style_description', 'style_image_url')

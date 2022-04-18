from rest_framework import serializers
from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'USER_PASSWORD', 'USER_NAME', 'USER_PHONE_NUM', 'USER_POSTAL_CODE', 'USER_ADDRESS')
        extera_kwargs = {
            'USER_PASSWORD': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['USER_PASSWORD'])
        user.save()
        return user

    def save(self):
        user = User(
            email=self.validated_data['email'],
            USER_NAME=self.validated_data['USER_NAME'],
            USER_PHONE_NUM=self.validated_data['USER_PHONE_NUM'],
            USER_POSTAL_CODE=self.validated_data['USER_POSTAL_CODE'],
            USER_ADDRESS=self.validated_data['USER_ADDRESS'],
        )
        USER_PASSWORD = self.validated_data['USER_PASSWORD']
        user.set_password(USER_PASSWORD)
        user.save()
        return user

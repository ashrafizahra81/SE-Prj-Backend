from rest_framework import serializers
from accounts.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'USER_PASSWORD', 'USER_NAME', 'USER_PHONE_NUM', 'USER_POSTAL_CODE', 'USER_ADDRESS', 'password2']
        extera_kwargs = {
            'USER_PASSWORD':{'write_only':True}
        }
    def save(self):
        user = User(
            email = self.validated_data['email'],
            USER_NAME = self.validated_data['USER_NAME'],
            USER_PHONE_NUM = self.validated_data['USER_PHONE_NUM'],
            USER_POSTAL_CODE = self.validated_data['USER_POSTAL_CODE'],
            USER_ADDRESS = self.validated_data['USER_ADDRESS'],
        )
        USER_PASSWORD = self.validated_data['USER_PASSWORD']
        password2 = self.validated_data['password2']

        if USER_PASSWORD != password2:
            raise serializers.ValidationError({'password': 'passwords must match.'})

        user.set_password(USER_PASSWORD)
        user.save()
        return user

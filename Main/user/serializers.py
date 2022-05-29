from user.models import user
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class RegisterUserSerializer(serializers.ModelSerializer):
    validation_code=serializers.CharField(max_length=50, read_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model=user
        fields = '__all__'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

class ConfirmRegistrationVerificationCodeSerializer(serializers.Serializer):
    email=serializers.EmailField()
    validation_code=serializers.CharField(max_length=255)




class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=user
        exclude = ['password', 'validation_code', 'createdAt', 'updatedAt']
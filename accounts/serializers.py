from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name = validated_data['first_name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password'],
            is_active = False,
        )
        code = user.generate_verify_code()
        return {
            'message': 'Confirmation code is sent to your phone number',
            'code': code
        }


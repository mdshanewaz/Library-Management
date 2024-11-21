from AuthApp.models import CustomUser
from rest_framework import serializers 


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
        'input_type': 'password',
        })

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = CustomUser.objects.create_user(email, password)
        return user
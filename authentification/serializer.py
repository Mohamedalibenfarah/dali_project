from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Auth
from django.contrib.auth.hashers import make_password

class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Auth
        fields = ['regNo', 'name', 'email', 'password', 'mobile', 'created_at']

    def create(self, validated_data):
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        # Create the Auth instance
        auth_instance = Auth.objects.create(
            regNo=validated_data['regNo'],
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            mobile=validated_data['mobile'],
        )

        return auth_instance
    

    def update(self, instance, validated_data):
        # Update the fields
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)

        # Update the password if provided
        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.save()
        return instance

class AuthLoginSerializer(serializers.Serializer):
    regNo = serializers.CharField()
    password = serializers.CharField()
        
class AuthGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = '__all__'


class AuthUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['name', 'mobile']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()
        return instance
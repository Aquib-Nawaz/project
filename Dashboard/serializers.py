from rest_framework import serializers
from Dashboard.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], 
            validated_data["email"], 
            validated_data["password"]
        )
        user.role = "student"
        user.save()
        return user
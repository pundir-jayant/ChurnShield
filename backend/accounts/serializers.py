from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=["admin", "analyst", "manager"], write_only=True, default="analyst")

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "analyst")
        user = User.objects.create_user(**validated_data)
        user.groups.get_or_create(name=role)[0].user_set.add(user)
        return user


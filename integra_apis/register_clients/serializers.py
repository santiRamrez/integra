from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Cliente


# Serializer for your Cliente (company)
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "name", "legal_id", "industry"]


# Serializer for the UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    # You can nest the ClienteSerializer here if you want
    # This will show the full company details, not just the ID
    cliente = ClienteSerializer(read_only=True)

    # Use this if you only want to send the ID
    # cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), source='cliente')

    class Meta:
        model = UserProfile
        fields = ["job_title", "cliente"]


# Serializer for the main User model
class UserSerializer(serializers.ModelSerializer):
    # This 'profile' must match the related_name you set on UserProfile.user
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",  # This will nest the profile data
        ]

    def update(self, instance, validated_data):
        # This handles saving the nested profile data
        profile_data = validated_data.pop("profile", {})
        profile = instance.profile

        # Update user fields
        instance.email = validated_data.get("email", instance.email)
        # ... other user fields ...
        instance.save()

        # Update profile fields
        profile.job_title = profile_data.get("job_title", profile.job_title)
        # ... other profile fields ...
        profile.save()

        return instance

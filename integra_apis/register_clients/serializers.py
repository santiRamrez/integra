from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Cliente, Chat


# Serializer for your Cliente (company)
class ClienteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Cliente
        fields = ["id", "name", "legal_id", "industry"]


# Serializer for the UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    # You can nest the ClienteSerializer here if you want
    # This will show the full company details, not just the ID
    empresa = ClienteSerializer()

    # Use this if you only want to send the ID
    # cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), source='cliente')

    class Meta:
        model = UserProfile
        fields = ["id", "job_title", "cliente"]


# Serializer for the main User model
class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
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
            "is_active",
            "profile",  # This will nest the profile data
        ]

    def create(self, validated_data):

        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        # This handles saving the nested profile data
        profile_data = validated_data.pop("profile", {})
        profile = instance.profile

        # Update user fields
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        # 2. Update Profile fields
        if profile_data:
            profile = instance.profile
            empresa_data = profile_data.pop("empresa", None)

            # Update simple profile fields
            profile.job_title = profile_data.get("job_title", profile.job_title)

            # 3. Handle Nested Empresa Safely
            if empresa_data:
                # Case A: The profile already has a company linked -> Update it
                if profile.empresa:
                    empresa = profile.empresa
                    empresa.name = empresa_data.get("name", empresa.name)
                    empresa.legal_id = empresa_data.get("legal_id", empresa.legal_id)
                    empresa.industry = empresa_data.get("industry", empresa.industry)
                    empresa.save()

                # Case B: The profile has NO company linked yet -> Create/Link one
                else:
                    # If the JSON includes an ID, try to find that existing company first
                    empresa_id = empresa_data.get("id")
                    if empresa_id:
                        try:
                            empresa = Cliente.objects.get(id=empresa_id)
                            # Update fields if needed, or just link it
                            empresa.name = empresa_data.get("name", empresa.name)
                            empresa.save()
                        except Cliente.DoesNotExist:
                            # ID provided but not found? Create new
                            empresa = Cliente.objects.create(**empresa_data)
                    else:
                        # No ID provided -> Create brand new company
                        empresa = Cliente.objects.create(**empresa_data)

                    # Finally, link the company to the profile
                    profile.empresa = empresa

            profile.save()

        return instance


class ChatSerializer(serializers.ModelSerializer):
    whatsapp = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Chat
        fields = ("sessionID", "messages", "whatsapp")

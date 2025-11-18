from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel
from django.contrib.auth.models import User


class Pais(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=3, null=True)

    class Meta:
        db_table = "Pais"

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=250)
    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT,  # Prevents deleting a Pais that has Regiones
        related_name="regiones",  # Lets us find all regiones for a pais
    )

    class Meta:
        db_table = "Region"

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=250)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="municipalidades",
    )

    class Meta:
        db_table = "Municipality"

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = "Industry"

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=250)
    currency = models.CharField(max_length=3, default="USD")
    value = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        db_table = "Plan"

    def __str__(self):
        return self.name


class Cliente(models.Model):
    name = models.CharField(max_length=250)
    legal_id = models.CharField(max_length=250)
    industry = models.CharField(max_length=250, null=True)
    email_admin = models.CharField(max_length=250)
    phone = models.CharField(max_length=100)
    street_num = models.CharField(max_length=250)
    muni = models.ForeignKey(Municipality, null=True, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, null=True, on_delete=models.PROTECT)
    country = models.ForeignKey(Pais, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = "Clientes"

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    # This links the profile to the built-in auth User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # --- THIS IS THE KEY ---
    # This links the user to their "Company" (the Cliente)
    # We allow null=True, blank=True so you can have
    # "Super Admin" users who don't belong to any company.
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,  # If a company is deleted, delete its users' profiles
        null=True,
        blank=True,
        related_name="user_profiles",  # Lets you do cliente.user_profiles.all()
    )

    # You can add other *person-specific* fields here
    job_title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Whatsapp(models.Model):
    phone = models.CharField(max_length=250)
    email_fb = models.CharField(max_length=250)
    pass_fb = models.CharField(max_length=250)
    id_app_fb = models.CharField(max_length=250)
    secret_pass_app_fb = models.CharField(max_length=250)
    token_user_fb = models.CharField(max_length=250)
    business_acount_id = models.CharField(max_length=250)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,  # If a company is deleted, delete its users' profiles
        null=True,
        blank=True,
        related_name="whatsapp_accounts",  # Lets you do cliente.user_profiles.all()
    )

    class Meta:
        db_table = "Whatsapp"

    def __str__(self):
        return self.phone


class Chat(models.Model):
    sessionID = models.CharField(max_length=250, null=True, blank=True)
    messages = models.JSONField(
        default=list, help_text="Chats from whatsapp", null=True, blank=True
    )
    whatsapp = models.ForeignKey(
        Whatsapp,
        on_delete=models.CASCADE,  # If a whatsapp_client is deleted, delete its users' profiles
        null=True,
        blank=True,
        related_name="chats_whatsapp",  # Lets you do cliente.user_profiles.all()
    )

    class Meta:
        db_table = "Chat_whatsapp"
        managed = False

    def __str__(self):
        return self.sessionID

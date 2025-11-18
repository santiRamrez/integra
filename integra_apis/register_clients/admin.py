from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Cliente,
    Municipality,
    Pais,
    Region,
    Plan,
    UserProfile,
    Whatsapp,
    Chat,
)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    This is the admin for the "Grandparent" model.
    We just need to tell Django that it can be
    searched by its 'name'.
    """

    list_display = ("name", "value", "currency")
    search_fields = ("name",)  # <-- This is ESSENTIAL for autocomplete


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    """
    This is the admin for the "Grandparent" model.
    We just need to tell Django that it can be
    searched by its 'name'.
    """

    list_display = ("name",)
    search_fields = ("name",)  # <-- This is ESSENTIAL for autocomplete


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """
    This is the "Parent" model.
    1. We make it searchable by 'name' (so Municipalidad can find it).
    2. We turn its 'pais' dropdown into an autocomplete box.
    """

    list_display = ("name", "pais")  # Show the country in the list
    search_fields = ("name",)  # <-- ESSENTIAL

    # --- This is the key ---
    # Turns the 'pais' <select> box into a search box
    autocomplete_fields = ("pais",)


@admin.register(Municipality)
class MunicipalidadAdmin(admin.ModelAdmin):
    """
    This is the "Child" model.
    1. We turn its 'region' dropdown into an autocomplete box.
    """

    list_display = ("name", "region")
    search_fields = ("name",)

    # --- This is the key ---
    # Turns the 'region' <select> box into a search box
    autocomplete_fields = ("region",)


# 1. Define an "inline" admin for the UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Don't allow deleting the profile from the user page
    verbose_name_plural = "Profile"
    fk_name = "user"


# 2. Define a new User admin that includes the profile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# 3. Re-register the User model with your new admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("name", "legal_id", "email_admin")
    search_fields = ("name", "legal_id")


# 4. Register your Cliente model so you can manage it
@admin.register(Whatsapp)
class WhatsappAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "email_fb",
        "pass_fb",
        "id_app_fb",
        "secret_pass_app_fb",
        "token_user_fb",
        "business_acount_id",
        "cliente",
    )
    search_fields = ("phone", "email_fb")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("sessionID", "messages", "whatsapp")
    search_fields = ("sessionID", "whatsapp")

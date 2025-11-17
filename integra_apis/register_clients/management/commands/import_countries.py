import json
from django.core.management.base import BaseCommand
from register_clients.models import Pais

# Data: Latin American countries + Spain and Portugal
# Using 2-letter ISO codes for 'country_code'
PAISES_DATA = [
    {"name": "Argentina", "code": "AR"},
    {"name": "Bolivia", "code": "BO"},
    {"name": "Brasil", "code": "BR"},
    {"name": "Chile", "code": "CL"},
    {"name": "Colombia", "code": "CO"},
    {"name": "Costa Rica", "code": "CR"},
    {"name": "Cuba", "code": "CU"},
    {"name": "Ecuador", "code": "EC"},
    {"name": "El Salvador", "code": "SV"},
    {"name": "España", "code": "ES"},
    {"name": "Guatemala", "code": "GT"},
    {"name": "Honduras", "code": "HN"},
    {"name": "México", "code": "MX"},
    {"name": "Nicaragua", "code": "NI"},
    {"name": "Panamá", "code": "PA"},
    {"name": "Paraguay", "code": "PY"},
    {"name": "Perú", "code": "PE"},
    {"name": "Portugal", "code": "PT"},
    {"name": "Puerto Rico", "code": "PR"},
    {"name": "República Dominicana", "code": "DO"},
    {"name": "Uruguay", "code": "UY"},
    {"name": "Venezuela", "code": "VE"},
]


class Command(BaseCommand):
    help = "Loads the list of Latin American countries + Spain/Portugal into the Pais model"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting to load countries..."))

        created_count = 0
        updated_count = 0

        for pais_data in PAISES_DATA:
            # update_or_create is safe to run multiple times.
            # It will find a Pais by 'name' or create a new one.
            obj, created = Pais.objects.update_or_create(
                name=pais_data["name"], defaults={"code": pais_data["code"]}
            )

            if created:
                created_count += 1
                self.stdout.write(f"  Created: {obj.name}")
            else:
                updated_count += 1
                self.stdout.write(f"  Updated: {obj.name}")

        self.stdout.write(self.style.SUCCESS(f"\nFinished!"))
        self.stdout.write(self.style.SUCCESS(f"Total created: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"Total updated: {updated_count}"))

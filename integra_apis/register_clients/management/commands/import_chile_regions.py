from django.core.management.base import BaseCommand

# Import both models
from register_clients.models import Pais, Region

# A list of the 16 regions of Chile
REGIONES_CHILE = [
    "Arica y Parinacota",
    "Tarapacá",
    "Antofagasta",
    "Atacama",
    "Coquimbo",
    "Valparaíso",
    "Región Metropolitana de Santiago",
    "O'Higgins",
    "Maule",
    "Ñuble",
    "Biobío",
    "La Araucanía",
    "Los Ríos",
    "Los Lagos",
    "Aysén",
    "Magallanes y de la Antártica Chilena",
]


class Command(BaseCommand):
    help = 'Loads the 16 regions of Chile and links them to the "Chile" Pais'

    def handle(self, *args, **options):

        # --- Step 1: Find the "Chile" Pais object ---
        try:
            chile_obj = Pais.objects.get(name="Chile")
        except Pais.DoesNotExist:
            self.stdout.write(self.style.ERROR('Error: Pais "Chile" not found.'))
            self.stdout.write(
                self.style.ERROR('Please run "py manage.py import_paises" first.')
            )
            return  # Stop the command

        self.stdout.write(
            self.style.SUCCESS(
                f"Found Pais: {chile_obj.name}. Starting to load regions..."
            )
        )

        created_count = 0
        updated_count = 0

        # --- Step 2: Loop through the list and create each region ---
        for region_name in REGIONES_CHILE:

            # Use update_or_create to be safe
            # We look for a region with this name *and* this parent
            obj, created = Region.objects.update_or_create(
                name=region_name, pais=chile_obj  # <-- This is the link!
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

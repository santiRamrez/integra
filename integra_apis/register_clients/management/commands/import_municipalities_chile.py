from django.core.management.base import BaseCommand
from register_clients.models import Region, Municipality

# Source data: All 346 municipalities ("comunas") of Chile,
# grouped by the 16 regions.
MUNI_DATA = {
    "Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Tarapacá": [
        "Iquique",
        "Alto Hospicio",
        "Pozo Almonte",
        "Camiña",
        "Colchane",
        "Huara",
        "Pica",
    ],
    "Antofagasta": [
        "Antofagasta",
        "Mejillones",
        "Sierra Gorda",
        "Taltal",
        "Calama",
        "Ollagüe",
        "San Pedro de Atacama",
        "Tocopilla",
        "María Elena",
    ],
    "Atacama": [
        "Copiapó",
        "Caldera",
        "Tierra Amarilla",
        "Chañaral",
        "Diego de Almagro",
        "Vallenar",
        "Alto del Carmen",
        "Freirina",
        "Huasco",
    ],
    "Coquimbo": [
        "La Serena",
        "Coquimbo",
        "Andacollo",
        "La Higuera",
        "Paiguano",
        "Vicuña",
        "Illapel",
        "Canela",
        "Los Vilos",
        "Salamanca",
        "Ovalle",
        "Combarbalá",
        "Monte Patria",
        "Punitaqui",
        "Río Hurtado",
    ],
    "Valparaíso": [
        "Valparaíso",
        "Casablanca",
        "Concón",
        "Juan Fernández",
        "Puchuncaví",
        "Quintero",
        "Viña del Mar",
        "Isla de Pascua",
        "Los Andes",
        "Calle Larga",
        "Rinconada",
        "San Esteban",
        "La Ligua",
        "Cabildo",
        "Papudo",
        "Petorca",
        "Zapallar",
        "Quillota",
        "Calera",
        "Hijuelas",
        "La Cruz",
        "Nogales",
        "San Antonio",
        "Algarrobo",
        "Cartagena",
        "El Quisco",
        "El Tabo",
        "Santo Domingo",
        "San Felipe",
        "Catemu",
        "Llaillay",
        "Panquehue",
        "Putaendo",
        "Santa María",
        "Quilpué",
        "Limache",
        "Olmué",
        "Villa Alemana",
    ],
    "Región Metropolitana de Santiago": [
        "Santiago",
        "Cerrillos",
        "Cerro Navia",
        "Conchalí",
        "El Bosque",
        "Estación Central",
        "Huechuraba",
        "Independencia",
        "La Cisterna",
        "La Florida",
        "La Granja",
        "La Pintana",
        "La Reina",
        "Las Condes",
        "Lo Barnechea",
        "Lo Espejo",
        "Lo Prado",
        "Macul",
        "Maipú",
        "Ñuñoa",
        "Pedro Aguirre Cerda",
        "Peñalolén",
        "Providencia",
        "Pudahuel",
        "Quilicura",
        "Quinta Normal",
        "Recoleta",
        "Renca",
        "San Joaquín",
        "San Miguel",
        "San Ramón",
        "Vitacura",
        "Puente Alto",
        "Pirque",
        "San José de Maipo",
        "Colina",
        "Lampa",
        "Tiltil",
        "San Bernardo",
        "Buin",
        "Calera de Tango",
        "Paine",
        "Melipilla",
        "Alhué",
        "Curacaví",
        "María Pinto",
        "San Pedro",
        "Talagante",
        "El Monte",
        "Isla de Maipo",
        "Padre Hurtado",
        "Peñaflor",
    ],
    "O'Higgins": [
        "Rancagua",
        "Codegua",
        "Coinco",
        "Coltauco",
        "Doñihue",
        "Graneros",
        "Las Cabras",
        "Machalí",
        "Malloa",
        "Mostazal",
        "Olivar",
        "Peumo",
        "Pichidegua",
        "Quinta de Tilcoco",
        "Rengo",
        "Requínoa",
        "San Vicente",
        "Pichilemu",
        "La Estrella",
        "Litueche",
        "Marchihue",
        "Navidad",
        "Paredones",
        "San Fernando",
        "Chépica",
        "Chimbarongo",
        "Lolol",
        "Nancagua",
        "Palmilla",
        "Peralillo",
        "Placilla",
        "Pumanque",
        "Santa Cruz",
    ],
    "Maule": [
        "Talca",
        "Constitución",
        "Curepto",
        "Empedrado",
        "Maule",
        "Pelarco",
        "Pencahue",
        "Río Claro",
        "San Clemente",
        "San Rafael",
        "Cauquenes",
        "Chanco",
        "Pelluhue",
        "Curicó",
        "Hualañé",
        "Licantén",
        "Molina",
        "Rauco",
        "Romeral",
        "Sagrada Familia",
        "Teno",
        "Vichuquén",
        "Linares",
        "Colbún",
        "Longaví",
        "Parral",
        "Retiro",
        "San Javier",
        "Villa Alegre",
        "Yerbas Buenas",
    ],
    "Ñuble": [
        "Chillán",
        "Bulnes",
        "Chillán Viejo",
        "El Carmen",
        "Pemuco",
        "Pinto",
        "Quillón",
        "San Ignacio",
        "Yungay",
        "Quirihue",
        "Cobquecura",
        "Coelemu",
        "Ninhue",
        "Portezuelo",
        "Ránquil",
        "Treguaco",
        "San Carlos",
        "Coihueco",
        "Ñiquén",
        "San Fabián",
        "San Nicolás",
    ],
    "Biobío": [
        "Concepción",
        "Coronel",
        "Chiguayante",
        "Florida",
        "Hualqui",
        "Lota",
        "Penco",
        "San Pedro de la Paz",
        "Santa Juana",
        "Talcahuano",
        "Tomé",
        "Hualpén",
        "Lebu",
        "Arauco",
        "Cañete",
        "Contulmo",
        "Curanilahue",
        "Los Álamos",
        "Tirúa",
        "Los Ángeles",
        "Antuco",
        "Cabrero",
        "Laja",
        "Mulchén",
        "Nacimiento",
        "Negrete",
        "Quilaco",
        "Quilleco",
        "San Rosendo",
        "Santa Bárbara",
        "Tucapel",
        "Yumbel",
        "Alto Biobío",
    ],
    "La Araucanía": [
        "Temuco",
        "Carahue",
        "Cunco",
        "Curarrehue",
        "Freire",
        "Galvarino",
        "Gorbea",
        "Lautaro",
        "Loncoche",
        "Melipeuco",
        "Nueva Imperial",
        "Padre las Casas",
        "Perquenco",
        "Pitrufquén",
        "Pucón",
        "Saavedra",
        "Teodoro Schmidt",
        "Toltén",
        "Vilcún",
        "Villarrica",
        "Cholchol",
        "Angol",
        "Collipulli",
        "Curacautín",
        "Ercilla",
        "Lonquimay",
        "Los Sauces",
        "Lumaco",
        "Purén",
        "Renaico",
        "Traiguén",
        "Victoria",
    ],
    "Los Ríos": [
        "Valdivia",
        "Corral",
        "Lanco",
        "Los Lagos",
        "Máfil",
        "Mariquina",
        "Paillaco",
        "Panguipulli",
        "La Unión",
        "Futrono",
        "Lago Ranco",
        "Río Bueno",
    ],
    "Los Lagos": [
        "Puerto Montt",
        "Calbuco",
        "Cochamó",
        "Fresia",
        "Frutillar",
        "Los Muermos",
        "Llanquihue",
        "Maullín",
        "Puerto Varas",
        "Castro",
        "Ancud",
        "Chonchi",
        "Curaco de Vélez",
        "Dalcahue",
        "Puqueldón",
        "Queilén",
        "Quellón",
        "Quemchi",
        "Quinchao",
        "Osorno",
        "Puerto Octay",
        "Purranque",
        "Puyehue",
        "Río Negro",
        "San Juan de la Costa",
        "San Pablo",
        "Chaitén",
        "Futaleufú",
        "Hualaihué",
        "Palena",
    ],
    "Aysén": [
        "Coyhaique",
        "Lago Verde",
        "Aysén",
        "Cisnes",
        "Guaitecas",
        "Cochrane",
        "O'Higgins",
        "Tortel",
        "Chile Chico",
        "Río Ibáñez",
    ],
    "Magallanes y de la Antártica Chilena": [
        "Punta Arenas",
        "Laguna Blanca",
        "Río Verde",
        "San Gregorio",
        "Cabo de Hornos (Ex-Navarino)",
        "Antártica",
        "Porvenir",
        "Primavera",
        "Timaukel",
        "Natales",
        "Torres del Paine",
    ],
}


class Command(BaseCommand):
    help = (
        "Loads all municipalities of Chile, linking them to their respective regions."
    )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Starting to load municipalities of Chile...")
        )

        regions_found = 0
        regions_not_found = 0
        total_munis_created = 0

        # Loop through the data dictionary
        # 'region_name' is the key (e.g., "Tarapacá")
        # 'municipalities_list' is the value (e.g., ["Iquique", "Alto Hospicio", ...])
        for region_name, municipalities_list in MUNI_DATA.items():

            # --- Step 1: Find the parent Region object ---
            try:
                # Find the region in the DB that matches the key
                region_obj = Region.objects.get(name=region_name)
                regions_found += 1
            except Region.DoesNotExist:
                # If the region isn't in the DB, warn the user and skip it
                self.stdout.write(
                    self.style.WARNING(
                        f'  WARNING: Region "{region_name}" not found. Skipping...'
                    )
                )
                regions_not_found += 1
                continue  # Move to the next region in the list

            # --- Step 2: Clear any existing municipalities for this region ---
            # This makes the script safe to re-run without creating duplicates.
            deleted_count, _ = Municipality.objects.filter(region=region_obj).delete()
            if deleted_count > 0:
                self.stdout.write(
                    f"  Cleared {deleted_count} old municipalities from {region_name}."
                )
            else:
                self.stdout.write(f"  Found Region: {region_name}.")

            # --- Step 3: Prepare the bulk create list ---
            munis_to_create = []
            for muni_name in municipalities_list:
                munis_to_create.append(
                    Municipality(
                        name=muni_name,
                        region=region_obj,  # <-- This is the foreign key link!
                    )
                )

            # --- Step 4: Create all municipalities in one database "chunk" ---
            if munis_to_create:
                Municipality.objects.bulk_create(munis_to_create)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    -> Bulk created {len(munis_to_create)} municipalities."
                    )
                )
                total_munis_created += len(munis_to_create)

        # --- Final Summary ---
        self.stdout.write(self.style.SUCCESS(f"\nFinished!"))
        self.stdout.write(self.style.SUCCESS(f"Processed {regions_found} regions."))
        self.stdout.write(
            self.style.SUCCESS(f"Total municipalities created: {total_munis_created}")
        )
        if regions_not_found > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipped {regions_not_found} regions (not found in database)."
                )
            )

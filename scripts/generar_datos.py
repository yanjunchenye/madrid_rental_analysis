import random  
from madrid_rental.extraction.store import save_anuncios

# Precio de referencia por m² (€/mes) según barrio
BARRIOS = {
    "Salamanca": 22,
    "Chamberí": 20,
    "Centro": 19,
    "Retiro": 18,
    "Chamartín": 17,
    "Tetuán": 15,
    "Arganzuela": 16,
    "Carabanchel": 12,
    "Usera": 12,
    "Vallecas": 11,
}

def generar_anuncios(i):

    barrio = random.choice(list(BARRIOS.keys()))#elige un barrio al azar y lo guarda en la variable barrio

    precio_base = BARRIOS[barrio]

    metros = random.randint(40, 200)
    precio = round(metros * precio_base * random.uniform(0.85, 1.15), 2)#multiplica el precio por un numero decimal entre 0.85 y 1.15 
                                                                        #para añadir una variacion de +-15% para que dos pisos iguales no cuesten lo mismo
    return {
        "propertyCode": str(i),
        "price": precio,
        "size": metros,
        "rooms": random.randint(1, 4),
        "bathrooms": random.randint(1, 3),
        "neighborhood": barrio,
        "district": barrio,
        "url": f"https://example.com/inmueble/{i}/",
    }

if __name__ == "__main__":
    anuncios = [generar_anuncios(i) for i in range(1000,2000)]
    save_anuncios(anuncios)
    print(f"Generados y guardados {len(anuncios)} anuncios")
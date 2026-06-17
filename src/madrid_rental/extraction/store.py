from sqlalchemy import text
from madrid_rental.database.connection import get_engine

def get_or_create_barrio(conn, nombre):

    #a ver si el barrio ya existe
    resultado = conn.execute(
        text("SELECT id FROM barrios WHERE nombre = :nombre"),
        {"nombre": nombre}
    ).fetchone()

    #si existe, devolver id
    if resultado is not None:
        return resultado[0]
    
    #si no, crearlo y devolver nuevo id
    nuevo = conn.execute(
        text("INSERT INTO barrios (nombre) VALUES (:nombre) RETURNING id"),
        {"nombre": nombre}
    ).fetchone()
    return nuevo[0]


def save_anuncios(anuncios):
    engine = get_engine()
    with engine.begin() as conn:
        for a in anuncios:
            barrio_id = get_or_create_barrio(conn, a["neighborhood"])
            
            conn.execute(
                text("""
                    INSERT INTO anuncios (id_idealista, barrio_id, precio, superficie, habitaciones, banos, url)
                    VALUES (:id_idealista, :barrio_id, :precio, :superficie, :habitaciones, :banos, :url)
                """),
                {
                    "id_idealista": a["propertyCode"],
                    "barrio_id": barrio_id,
                    "precio": a["price"],
                    "superficie": a["size"],
                    "habitaciones": a["rooms"],
                    "banos": a["bathrooms"],
                    "url": a["url"],
                }
            )


if __name__ == "__main__":
    from madrid_rental.extraction.idealista_client import get_anuncios
    anuncios = get_anuncios()
    save_anuncios(anuncios)
    print("Anuncios guardados ✅")
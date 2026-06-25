from sqlalchemy import text
from madrid_rental.database.connection import get_engine

def get_or_create_barrio(conn, nombre):
    """Get the id of a neighbourhood, creating it if it doesn't exist.

    - If neighbourhood exists, return its id
    - If not, create it and return the new id
    """

    #check if exists
    resultado = conn.execute(
        text("SELECT id FROM barrios WHERE nombre = :nombre"),
        {"nombre": nombre}
    ).fetchone()

    #if exists
    if resultado is not None:
        return resultado[0]
    
    #if it doesn't
    nuevo = conn.execute(
        text("INSERT INTO barrios (nombre) VALUES (:nombre) RETURNING id"),
        {"nombre": nombre}
    ).fetchone()
    return nuevo[0]


def save_anuncios(anuncios):
    """Save or update listings in the database.

    - If the listing is new: insert it into the database and record its price in the price history.
    - If it already exists but the price has changed: update the price and record the change in the price history.
    - If it already exists and the price is the same: leave it unchanged.
    """

    engine = get_engine()
    with engine.begin() as conn:
        for a in anuncios:
            barrio_id = get_or_create_barrio(conn, a["neighborhood"])

            existente = conn.execute(
                text("SELECT id, precio FROM anuncios WHERE id_idealista = :id"),
                {"id" : a["propertyCode"]}
            ).fetchone()
            
            if existente is None:
                nuevo_id = conn.execute(
                    text("""
                        INSERT INTO anuncios (id_idealista, barrio_id, precio, superficie, habitaciones, banos, url)
                        VALUES (:id_idealista, :barrio_id, :precio, :superficie, :habitaciones, :banos, :url) RETURNING id
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
                ).fetchone()

                conn.execute(
                    text("""
                        INSERT INTO historico_precios (anuncio_id, precio) VALUES (:anuncio_id, :precio)
                     """),
                     {
                         "anuncio_id": nuevo_id[0],
                         "precio": a["price"]
                     }
                )
            else:
                if existente[1] != a["price"]:
                    conn.execute(
                        text("""
                            UPDATE anuncios SET precio = :precio_nuevo WHERE id = :id
                        """),
                        {"precio_nuevo" : a["price"], 
                         "id" : existente[0]})
                    conn.execute(
                        text("""
                            INSERT INTO historico_precios (anuncio_id, precio) VALUES (:anuncio_id, :precio) 
                        """),
                        {"anuncio_id": existente[0],
                         "precio" : a["price"]}
                    )
                else:
                    pass
                    


if __name__ == "__main__":
    from madrid_rental.extraction.idealista_client import get_anuncios
    anuncios = get_anuncios()
    save_anuncios(anuncios)
    print("Anuncios guardados ✅")
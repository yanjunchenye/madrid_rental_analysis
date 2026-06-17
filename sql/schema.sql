CREATE TABLE IF NOT EXISTS barrios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    distrito TEXT
);

CREATE TABLE IF NOT EXISTS anuncios (
    id SERIAL PRIMARY KEY,
    id_idealista TEXT NOT NULL UNIQUE,
    barrio_id INTEGER REFERENCES barrios(id),
    precio NUMERIC NOT NULL,
    superficie NUMERIC,
    habitaciones INTEGER, 
    banos INTEGER,
    url TEXT
);

CREATE TABLE IF NOT EXISTS historico_precios(
    id SERIAL PRIMARY KEY,
    anuncio_id INTEGER NOT NULL REFERENCES anuncios(id),
    precio NUMERIC NOT NULL,
    registrado_en TIMESTAMPTZ NOT NULL DEFAULT now()
);
import joblib
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from madrid_rental.database.connection import get_engine

MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "modelo_precio.joblib"

def train():
    engine = get_engine()

    query = """
        SELECT a.precio, a.superficie, a.habitaciones, a.banos, b.nombre AS barrio
        FROM anuncios a
        JOIN barrios b ON a.barrio_id = b.id
    """

    df = pd.read_sql(query, engine)

    df_modelo = pd.get_dummies(df, columns=["barrio"])

    y = df_modelo["precio"]
    X = df_modelo.drop(columns=["precio"])

    modelo = RandomForestRegressor(
        n_estimators=150,
        max_depth=10,
        min_samples_leaf=1,
        random_state=42
    )
    modelo.fit(X, y)

    # Crear la carpeta models/ si no existe
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Guardar el modelo y las columnas que espera
    joblib.dump({"modelo": modelo, "columnas": list(X.columns)}, MODEL_PATH)

    print(f"Modelo entrenado y guardado en {MODEL_PATH}")

if __name__ == "__main__":
    train()
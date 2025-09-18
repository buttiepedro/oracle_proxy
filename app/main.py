import os
import csv
import uuid
import time
import oracledb
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Inicializar cliente Oracle en modo thick
oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient_21_13")

app = FastAPI()

# Función para obtener conexión
def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SID')}"
    )

# Carpeta temporal para guardar CSVs
CSV_DIR = "/tmp/csv_exports"
os.makedirs(CSV_DIR, exist_ok=True)

# Tiempo de expiración en segundos (6 horas)
CSV_EXPIRATION = 6 * 60 * 60

def cleanup_old_csvs():
    now = time.time()
    for filename in os.listdir(CSV_DIR):
        filepath = os.path.join(CSV_DIR, filename)
        if os.path.isfile(filepath):
            age = now - os.path.getmtime(filepath)
            if age > CSV_EXPIRATION:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"No se pudo borrar {filepath}: {e}")

@app.post("/query")
async def run_query(request: Request):
    try:
        body = await request.json()
        sql = body.get("query")

        if not sql:
            return JSONResponse({"error": "Falta el parámetro 'query'"}, status_code=400)

        # Limpiar CSVs antiguos
        cleanup_old_csvs()

        # Ejecutar consulta
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # Generar nombre de archivo único
        filename = f"{uuid.uuid4().hex}.csv"
        filepath = os.path.join(CSV_DIR, filename)

        # Guardar CSV
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        cursor.close()
        conn.close()

        # Retornar link de descarga
        download_url = f"/download/{filename}"
        return {"download_url": download_url}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/download/{filename}")
def download_csv(filename: str):
    filepath = os.path.join(CSV_DIR, filename)
    if not os.path.isfile(filepath):
        return JSONResponse({"error": "Archivo no encontrado"}, status_code=404)
    return FileResponse(filepath, media_type="text/csv", filename=filename)

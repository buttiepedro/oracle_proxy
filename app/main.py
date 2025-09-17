import os
import oracledb
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Inicializar cliente Oracle en modo thick
# Asegúrate de que esta ruta coincida con tu Dockerfile
oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient_21_13")

app = FastAPI()

# Función para obtener conexión
def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SID')}"
    )

@app.post("/query")
async def run_query(request: Request):
    try:
        body = await request.json()
        sql = body.get("query")

        if not sql:
            return JSONResponse({"error": "Falta el parámetro 'query'"}, status_code=400)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        # Convertir resultados a JSON
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return {"data": results}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

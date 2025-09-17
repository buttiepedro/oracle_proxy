from fastapi import FastAPI, Request
import oracledb
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

app = FastAPI()

# Configuración conexión Oracle desde variables de entorno
host = os.getenv("ORACLE_HOST")
port = os.getenv("ORACLE_PORT", "1521")
sid = os.getenv("ORACLE_SID")
dsn = f"{host}:{port}/{sid}"
user = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")

@app.post("/query")
async def run_query(request: Request):
    try:
        body = await request.json()
        sql = body.get("query")

        if not sql:
            return {"success": False, "error": "Falta parámetro 'query'"}

        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        cur = conn.cursor()
        cur.execute(sql)

        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, row)) for row in cur]

        cur.close()
        conn.close()

        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}

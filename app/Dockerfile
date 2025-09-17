FROM python:3.11-slim

WORKDIR /app

# Dependencias necesarias
RUN apt-get update && apt-get install -y wget unzip libaio1 && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip -O /tmp/instantclient.zip \
    && unzip /tmp/instantclient.zip -d /opt/oracle \
    && rm /tmp/instantclient.zip \
    && ln -s /opt/oracle/instantclient*/libclntsh.so* /usr/lib/

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

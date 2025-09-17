FROM python:3.11-slim

WORKDIR /app

# Dependencias necesarias
RUN apt-get update && apt-get install -y wget unzip libaio-dev && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip -O instantclient.zip && \
    unzip instantclient.zip -d /opt/oracle && \
    rm instantclient.zip && \
    echo /opt/oracle/instantclient_21_13 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig


# Variables de entorno para modo thick
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_23_5
ENV ORACLE_HOME=/opt/oracle/instantclient_23_5

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

CMD ["python", "main.py"]

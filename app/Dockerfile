FROM python:3.11-slim

WORKDIR /app

# Dependencias para Oracle Instant Client
RUN apt-get update && \
    apt-get install -y wget unzip libaio1 libncurses6 && \
    rm -rf /var/lib/apt/lists/*

# Descargar e instalar Oracle Instant Client 21.13
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basiclite-linux.x64-21.13.0.0.0dbru.zip -O /tmp/instantclient.zip && \
    unzip /tmp/instantclient.zip -d /opt/oracle && \
    rm /tmp/instantclient.zip && \
    echo /opt/oracle/instantclient_21_13 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

# Variables de entorno para modo thick
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13
ENV ORACLE_HOME=/opt/oracle/instantclient_21_13

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Usa una imagen oficial de Python como imagen base
FROM python:3.8-slim
FROM apache/nifi:1.28.1

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
# Usa una imagen oficial de Python como imagen base
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app

# Instala los paquetes necesarios especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 80 al mundo exterior
EXPOSE 80

# Define una variable de entorno
ENV NAME World


# Ejecuta app.py cuando el contenedor se inicie
CMD ["python", "app.py"]
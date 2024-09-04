# Utilizar la imagen oficial de Debian como base
FROM debian:latest

# Actualizar los paquetes e instalar Python y otras dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar todos los archivos del repositorio en el contenedor en el directorio /app
COPY . /app

# Dar permisos de ejecución al script tetri_server.py si es necesario
RUN chmod +x /app/tetri_server.py

# Exponer el puerto TCP 5432
EXPOSE 5432

# Ejecutar el script tetri_server.py con Python
CMD ["python3", "/app/tetri_server.py"]

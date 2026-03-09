# 1. Imagen base de Python
FROM python:3.12-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar archivo de dependencias (usando tu nombre: requeriments.txt)
COPY requeriments.txt .

# 4. Instalar librerías (FastAPI, Uvicorn, etc.)
RUN pip install --no-cache-dir -r requeriments.txt

# 5. Copiar el contenido de tu carpeta local 'app' a la carpeta 'app' del contenedor
COPY ./app ./app

# 6. Exponer el puerto donde correrá la app error significa que debo cambiar el contenedor:docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint autos (24b482b0f239332e375943545ab4db25b7ea2fcb8f3de8fe26818e804d64a115): Bind for 0.0.0.0:5000 failed: port is already allocated
EXPOSE 7000

# 7. Ejecutar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]
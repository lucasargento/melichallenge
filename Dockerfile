# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 para tráfico externo
EXPOSE 8000

# Define el comando para ejecutar la app usando uvicorn
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]
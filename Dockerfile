# Usar una imagen oficial de Miniconda con Python 3.11
FROM continuumio/miniconda3:latest

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar y crear el entorno con Conda
COPY environment.yml .
RUN conda env create -f environment.yml

# Asegurar que el entorno se usa por defecto
ENV CONDA_DEFAULT_ENV=melichallenge
ENV PATH="/opt/conda/envs/melichallenge/bin:$PATH"

# Copiar el código fuente al contenedor
COPY . .

# Exponer el puerto en el que se ejecutará el servidor
EXPOSE 8000

# Usar bash en el CMD para que `conda` funcione correctamente
SHELL ["/bin/bash", "-c"]

# Comando para ejecutar el servidor FastAPI
CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]

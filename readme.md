# MeliChallenge | Lucas Argento

## Instalación de dependencias

Para instalar las dependencias necesarias usando conda, sigue estos pasos:

1. Asegúrate de tener conda instalado en tu sistema.
2. Navega al directorio raíz del repositorio y ejecuta el siguiente comando para crear un nuevo entorno conda e instalar las dependencias:
    ```bash
    conda env create -f environment.yml
    ```

3. Activa el entorno conda:
    ```bash
    conda activate meli-challenge-env
    ```

## Notebooks

En la raíz del repositorio, se encuentran dos notebooks. Uno con el EDA, los insights obtenidos y el entrenamiento del modelo, y otro con testeos sencillos de la implementacion del pipeline de inferencia.

Para ejecutar estos notebooks, asegúrate de tener el entorno conda activado y ejecuta el siguiente comando en la raíz del repositorio:

```bash
jupyter notebook
```

## Cómo correr el script de inferencia localmente

Para ejecutar el script `run_inference.sh`, sigue estos pasos:

1. Asegúrate de que el script tenga permisos de ejecución. Si no es así, puedes otorgar permisos con el siguiente comando:
    ```bash
    chmod +x run_inference.sh
    ```

2. Ejecuta el script con el siguiente comando:
    ```bash
    ./run_inference.sh
    ```

Este script agregará la ruta necesaria al `PYTHONPATH` y luego ejecutará el archivo `inference_pipeline.py`.

## Cómo correr el server localmente

Para ejecutar el servidor `server.py` de manera local, sigue estos pasos:

1. Asegúrate de tener el entorno conda activado:
    ```bash
    conda activate meli-challenge-env
    ```

2. Desde el root del proyecto:
    ```bash
    python server/server.py
    ```

El servidor proporcionará una API para realizar inferencias utilizando el modelo entrenado. Se expondrá una app sencilla que permitira visualizar las predicciones del modelo para el test_set.

## Correr el server usando docker en local

Para ejecutar el servidor `server.py` utilizando Docker, sigue estos pasos:

1. Asegúrate de tener Docker instalado en tu sistema.

2. Navega al directorio raíz del repositorio y construye la imagen de Docker con el siguiente comando:
  ```bash
  docker build -t meli-challenge-server .
  ```

3. Una vez que la imagen se haya construido correctamente, ejecuta el contenedor con el siguiente comando:
  ```bash
  docker run -p 5000:5000 meli-challenge-server
  ```

Esto iniciará el servidor en un contenedor de Docker y expondrá la API en `http://localhost:5000`, permitiendo realizar inferencias utilizando el modelo entrenado.

## Visitar la webapp deployeada online



## Distribución del repositorio

El repositorio está organizado de la siguiente manera:

- **components/**: Contiene los componentes principales del pipeline, como el preprocesador y el pipeline de clasificación.
  - [preprocessor.py](http://_vscodecontentref_/0): Contiene la clase `Preprocessor` y sus métodos para la preprocesamiento de datos.
  - `pipeline.py`: Contiene la clase `ClassificationPipeline` y sus métodos para la clasificación.
  - [qa_functions.py](http://_vscodecontentref_/1): Contiene funciones auxiliares para la evaluación de la calidad de los datos.

- **pipelines/**: Contiene los scripts para ejecutar los pipelines de inferencia y entrenamiento.
  - `inference_pipeline.py`: Script para ejecutar el pipeline de inferencia.
  - [training_pipeline.py](http://_vscodecontentref_/2): Sin desarrollar, pero dejamos el placeholder para futuras iteraciones

- **outputs/**: Contiene los archivos de salida generados por los pipelines, como los archivos CSV con las predicciones. Simula un sink de big query en donde se guardarian los resultados de batch inference.

- **server/**: Contiene el script del servidor y sus configuraciones.
  - `server.py`: Script para ejecutar el servidor que expone una API para realizar inferencias.

## TODOs y Mejoras

- [ ] Crear el script [training_pipeline.py](http://_vscodecontentref_/3) para ejecutar el pipeline de entrenamiento utilizando el preprocesador y `ClassificationPipeline` en modo entrenamiento.
- [ ] Mejorar la gestión de errores y excepciones en los scripts de pipeline.
- [ ] Reemplazar prints por logs usando logger() especifico de donde sea deployeada la solucion.
- [ ] Añadir pruebas unitarias para asegurar la calidad del código.
- [ ] Desarrollar un endpoint de inferencia realtime que pueda recibir data points puntuales o una serie de ellos y devolver los valores predichos para los mismos.
- [ ] Realizar conexiones de datos reales a data wharehouses como BigQuery, leer de tablas de input y escribir los resultados en tablas de output.

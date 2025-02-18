# MeliChallenge

#### Lucas Argento

## About

Este repositorio contiene el código para el desafio Meli de Febrero 2024. El mismo consistió en analizar un dataset de transacciones financieras para una serie limitada de clientes. A partir de éste, se realizaron las siguientes tareas:

- EDA y QA de los datos. En el notebook de expliracion y entrenamiento, se desarrolló un primer analisis exploratorio del dataset, en el cual tambien se verificaron métricas de calidad de los datos y se limpiaron los mismos.
- Se extrajeron insights y conclusiones, desde una óptica de negocio, con el objetivo de entender mejor los datos y generar valor apartir de ellos.
- Analisis de potenciales casos de uso de ML: se listaron algunos de los potenciales casos de usos de Machine Learning que podria tener este dataset.
- Entrenamiento de un clasificador: se entrenó un modelo de clasificiación multiclase para clasificar transacciones en diferentes categorías, con el objetivo de tener mejor entendimiento del comportamiento de nuestros clientes y poder oferecerles mejores tratos/productos a futuro y detecter potenciales casos de fraude, si existieran.
- Se desarrollaron componentes modulares para la puesta del modelo en producción, con el objetivo de simplificar la reutilización del código y hacer mas eficiente la iteración futura.
- Se desarrollaron pipelines de inferencia y entrenamiento del modelo, utilizando los componentes mencionados, para automatizar la predicción y el futuro re entrenamiento del modelo en caso de que hiciera falta.
- Se desarrolló una WebApp simple con FastAPI para mostrar el funcionamiento del entrenamiento + inferencia del modelo.
- Para asegurar de la replicabilidad de la solución, se generaron archivos de entorno para conda (environment.yml), pip (requirements.txt) y un dockerfile para correr la webapp containerizada.
- Se generaró un "Model Registry" y "Conexiones a BigQuery" simuladas con directorios dentro del repositorio, para representar un caso de uso en la vida real, y que si en algun momento se optara por utilizar estos servicios u otros similiares, la integración sea mas sencilla.
- En el flujo de entrenamiento + inferencia de la webapp, se separó una fracción del dataset raw (previo al entrenamiento) para utilizar como data out-of-sample sobre la cual predecir con el modelo entrenado, simulando datos "nuevos" que el mismo nunca vió.

## Distribución del repositorio

El repositorio está organizado de la siguiente manera:

- **components/**: Contiene los componentes modulares previamente mencionados: el modelo, el preprocesador y "conector de datos" que se encarga de la carga de los mismos. Además, encontramos dentro de la carpeta "utils", funciones útiles para creacion de features y QA de los datos.
  - `preprocessor.py`: Contiene la clase `Preprocessor` y sus métodos para la preprocesamiento de datos.
  - `classifier.py`: Contiene la clase `ClassificationPipeline` y sus métodos para la clasificación, inferencia y entrenamiento.
  - `qa_functions.py`: Contiene funciones auxiliares para la evaluación de la calidad de los datos.
  - `feature_functions.py`: Contiene funciones auxiliares para la creacion de features.

- **pipelines/**: Contiene los scripts para ejecutar los pipelines de inferencia y entrenamiento.
  - `inference_pipeline.py`: Busca la ultima version del modelo entrenado y realiza inferencia.
  - `training_pipeline.py`: Entrena al modelo y lo guarda en el "registry".

- **outputs/**: Contiene los archivos de salida generados por el pipeline de inferencia. Simula un sink de big query en donde se guardarian los resultados de batch inference.

- **data/**: Contiene los datos de entrada con los cuales se entrena al modelo y sobre los cuales se realiza la inferencia. Simula un data wharehouse sobre el cual corre un proceso batch de inferencia.

- **registry/**: Simula un model registry. En este direcotorio se versionan y guardan los pesos de los modelos entrenados.

- **server/**: Contiene el script del servidor: webapp simple en FastAPI.
  - `server.py`: Script para ejecutar el servidor.

## Instalación de dependencias

**Para instalar las dependencias necesarias usando conda, sigue estos pasos:**

1. Asegúrate de tener conda instalado en tu sistema.
2. Navega al directorio raíz del repositorio y ejecuta el siguiente comando para crear un nuevo entorno conda e instalar las dependencias:
    ```bash
    conda env create -f environment.yml
    ```

3. Activa el entorno conda:
    ```bash
    conda activate meli-challenge-env
    ```

**Para instalar las dependencias necesarias usando pip:**

1. Asegúrate de tener conda instalado en tu sistema.
2. Navega al directorio raíz del repositorio y ejecuta el siguiente comando para crear un nuevo entorno conda e instalar las dependencias:
    ```bash
    conda env create -f environment.yml
    ```

3. Activa el entorno conda:
    ```bash
    conda activate meli-challenge-env
    ```

## Notebook con EDA y Entrenamiento

En la raíz del repositorio, se encuentran el notebook con el EDA, QA y entrenamiento del modelo de clasificación.

Para ejecutar estos notebooks, asegúrate de tener el entorno conda activado y ejecuta el siguiente comando en la raíz del repositorio:

```bash
jupyter notebook
```

## Cómo correr el script de inferencia localmente

Ejecuta el script `run_inference.sh`, siguiendo estos pasos:

1. Asegúrate de que el script tenga permisos de ejecución. Si no es así, puedes otorgar permisos con el siguiente comando:
    ```bash
    chmod +x run_inference.sh
    ```

2. Ejecuta el script con el siguiente comando:
    ```bash
    ./run_inference.sh
    ```

## Cómo correr la WebApp Localmente

Para ejecutar el servidor `server.py` de manera local, sigue estos pasos:

1. Asegúrate de tener el entorno conda activado:
    ```bash
    conda activate meli-challenge-env
    ```

2. Desde el root del proyecto:
    ```bash
    python server/server.py
    ```

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

Esto iniciará el servidor en un contenedor de Docker y expondrá la API en `http://localhost:5000`, permitiendo realizar inferencias y entrenar nuevos modelos.

## TODOs y Mejoras

- [ ] Reemplazar prints por logs usando logger() especifico de donde sea deployeada la solucion.
- [ ] Añadir pruebas unitarias para asegurar la calidad del código.
- [ ] Desarrollar un endpoint de inferencia realtime que pueda recibir data points en formato json o raw text (o una serie de ellos) y devolver los valores predichos para los mismos.
- [ ] Realizar conexiones de datos reales a fuentes de datos en la nube /onprem como BigQuery o SQLServer, leer de tablas de input y escribir los resultados en tablas de output.
- [ ] Desarrollar un pipeline de evaluacion de modelos que decida si promover o no un modelo cuando corre el pipeline de entrenamiento
- [ ] Desarrollar un pipeline de monitoreo que verifique que no haya drifts a lo largo del tiempo. 
- [ ] CI/CD con github actions para deployear y/o testear el codigo en ciertas branches o luego de PRs.

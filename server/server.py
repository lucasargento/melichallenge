from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import pandas as pd
import os
from pipelines.inference_pipeline import run_inference
from pipelines.training_pipeline import run_training

app = FastAPI()

def model_exists():
    return any(fname.endswith('.pkl') for fname in os.listdir('registry'))

def predictions_exist():
    return any(fname.endswith('.csv') for fname in os.listdir('outputs'))


@app.get("/", response_class=HTMLResponse)
async def root():
    model_ready = model_exists()
    # Página de menú con tres botones
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Menú de Inferencia</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
        <h1 class="text-4xl font-bold mb-8">Menú de Inferencia</h1>
        <div class="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
            <button class="bg-white text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow hover:bg-blue-100 transition duration-300" onclick="location.href='/train_model'">Train Model</button>
            <button class="bg-white text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow hover:bg-blue-100 transition duration-300" onclick="location.href='/realtime_inference'" {'disabled' if not model_ready else ''}>Realtime Inference Endpoint</button>
            <button class="bg-white text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow hover:bg-blue-100 transition duration-300" onclick="location.href='/batch_inference'" {'disabled' if not model_ready else ''}>Batch Inference Endpoint</button>
        </div>
        <div class="mt-4 text-center p-4">
            {'<p class="text-red-500">Parece que no hay modelos en el Registry por ahora. Entrena tu primer modelo para testear la inferencia.</p>' if not model_ready else ''}
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/train_model", response_class=HTMLResponse)
async def train_model(request: Request, background_tasks: BackgroundTasks):
    # Ejecutar el script de entrenamiento en segundo plano
    background_tasks.add_task(run_training)
    
    # Mostrar una página de progreso
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Progreso del Entrenamiento</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .spinner { margin: 100px auto; width: 50px; height: 50px; border: 5px solid #ccc; border-top: 5px solid #1d72b8; border-radius: 50%; animation: spin 1s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h1>Entrenando el Modelo...</h1>
        <div class="spinner"></div>
        <p>Por favor, espera mientras entrenamos el modelo 🧠</p>
        <script>
            async function checkModel() {
                const response = await fetch('/check_model');
                const data = await response.json();
                if (data.model_ready) {
                    window.location.href = "/";
                } else {
                    setTimeout(checkModel, 2000);  // Volver a chequear en 5 segundos
                }
            }
            checkModel();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/check_model")
async def check_model():
    model_ready = model_exists()
    return {"model_ready": model_ready}

@app.get("/check_predictions")
async def check_model():
    preds_ready = predictions_exist()
    return {"preds_ready": preds_ready}

@app.get("/batch_inference", response_class=HTMLResponse)
async def batch_inference(request: Request, background_tasks: BackgroundTasks):
    # Ejecutar el script de inferencia en segundo plano
    background_tasks.add_task(run_inference)

    # Mostrar una página de progreso
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Progreso de la Inferencia</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .spinner { margin: 100px auto; width: 50px; height: 50px; border: 5px solid #ccc; border-top: 5px solid #1d72b8; border-radius: 50%; animation: spin 1s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h1>Realizando Inferencia...</h1>
        <div class="spinner"></div>
        <p>Por favor, espera mientras nuestros modelos piensan 🧠</p>
            <script>
            async function checkModel() {
                const response = await fetch('/check_predictions');
                const data = await response.json();
                if (data.preds_ready) {
                    window.location.href = "/inference_results";
                } else {
                    setTimeout(checkModel, 2000);  // Volver a chequear en 5 segundos
                }
            }
            checkModel();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/inference_results", response_class=HTMLResponse)
async def inference_results(request: Request):
    # Leer el archivo de resultados
    cwd = os.getcwd()
    results_df = pd.read_csv(f"{cwd}/outputs/predictions.csv")

    # Convertir los resultados a HTML
    results_html = results_df.to_html(index=False, classes="table table-striped")

    # Crear una página HTML sencilla para mostrar los resultados
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resultados de la Inferencia</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 50px; font-size: 14px; }}
            table {{ width: 100%; border-collapse: collapse; border-radius: 8px; overflow: hidden; }}
            th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            table, th, td {{ border-radius: 8px; }}
            h2 {{ font-weight: normal; }}
            div {{ padding-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>Prediccion de categorias de transacciones</h1>
        <h2>Predicciones en la última columna</h2>
        <div>{results_html}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/realtime_inference", response_class=HTMLResponse)
async def realtime_inference():
    # Mostrar una página de "Todavía en construcción"
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Inference</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .construction { margin: 100px auto; width: 50px; height: 50px; border: 5px solid #ccc; border-top: 5px solid #ff5733; border-radius: 50%; animation: spin 1s linear infinite; }
            @keyframes spin { 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h1>Real-Time Inference</h1>
        <h1>🛠️</h1>
        <p>Esta funcionalidad está todavía en construcción. Vuelve Pronto!</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
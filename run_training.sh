#!/bin/bash

# Agregar la ruta al PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH

# Ejecutar el script inference_pipeline.py
python pipelines/training_pipeline.py
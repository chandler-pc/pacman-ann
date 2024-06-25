# Instalación

## Requisitos

- Python 3.9 o superior
- pip
- virtualenv

## Pasos para instalar

1. Clonar el repositorio
2. Crear un entorno virtual
   - En linux `python3 -m venv venv`
   - En Windows `python -m venv venv`
3. Instalar las dependencias
   - En linux `source venv/bin/activate`
   - En Windows `venv\Scripts\activate`
   - `pip install -e .`

## Pasos para ejecutar

1. Activar el entorno virtual
   - En linux `source venv/bin/activate`
   - En Windows `venv\Scripts\activate`
2. Ejecutar el script en el entorno virtual
   - Ejecutar el juego `run-pacman`
   - Entrenar el modelo `train-pacman`
   - Probar el modelo `test-pacman`

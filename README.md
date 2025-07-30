# Green Software Monitor (Windows)

[![Windows Support](https://img.shields.io/badge/Windows-Supported-blue)](https://www.microsoft.com/windows)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Monitor de consumo energético y emisiones de CO₂ para sistemas Windows

## Instalación

### Método 1: Ejecutable (recomendado)
1. Descargar el archivo `main.exe` de la carpeta `dist`
2. Ejecutar directamente (no requiere instalación)

### Método 2: Desde código fuente
Requisitos:
- Python 3.9+
- Windows 10/11

```bash
# Clonar repositorio
git clone https://github.com/turepositorio/greensoftware_windows.git
cd greensoftware_windows

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py

La aplicación muestra en tiempo real:
 Uso de CPU y RAM
 Consumo energético actual y promedio
 Emisiones de CO₂ acumuladas

Características principales

Monitoreo en tiempo real del consumo energético

Cálculo de huella de carbono basado en:
 Uso del procesador (modelo no lineal)
 Consumo de memoria RAM
 Parámetros ajustables según hardware
 Interfaz visual con efectos de transparencia
 Datos presentados en formato claro (Wattios y gramos de CO₂)

Integrantes del proyecto
 Sofia Vidallet
 Milagros Veron
 Ignacio Bernardis
 Bianca Longoni
Proyecto académico para UTN FRRE

# ⚽ FootballInsights

Dashboard interactivo de jugadores de fútbol construido con Streamlit y Python.

## 🚀 Descripción

FootballInsights es una aplicación de análisis de datos que permite explorar estadísticas de jugadores, apariciones, valuaciones de mercado y partidos.

El objetivo del proyecto es aplicar técnicas de análisis y visualización con herramientas del ecosistema de Python sobre datasets de fútbol.

## 🧠 Funcionalidades

- 📊 Selección de jugadores desde un listado interactivo
- 📈 Métricas agregadas de partidos, minutos, goles y asistencias
- 🟨 Seguimiento de tarjetas amarillas y rojas
- 💶 Visualización de la evolución del valor de mercado
- 🗓️ Tabla con los últimos partidos del jugador seleccionado

## 🛠️ Tecnologías

- Python
- Streamlit
- pandas
- matplotlib


## 📊 Dataset

El proyecto usa archivos CSV ubicados en `data/`, entre ellos:

- `players.csv`
- `appearances.csv`
- `player_valuations.csv`
- `games.csv`

Estos archivos alimentan el dashboard para combinar información de jugadores, apariciones, valuaciones y partidos.

## 🎯 Objetivo del proyecto

Este proyecto forma parte de mi aprendizaje en:

Data Analysis
Python para análisis de datos
Visualización de información
Construcción de dashboards con Streamlit

## ▶️ Cómo ejecutar la app

1. Instalar las dependencias:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. Ejecutar la app desde la raíz del proyecto:

```powershell
.\venv\Scripts\python.exe -m streamlit run app\main.py
```

Alternativamente, podés activar el entorno virtual y luego ejecutar:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run app\main.py
```

Si PowerShell bloquea la activación del entorno virtual, ejecutá:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\venv\Scripts\Activate.ps1
python -m streamlit run app\main.py
```

## 👨‍💻 Autor

Tomás Rivetta
🔗 https://totoridev.netlify.app/


# 🌊 धारा (DHARA) - National Hydrological Disaster & Mountain Flash Flood Early Warning System

> **Initiative:** Crisis Before Crisis (IIITN)  
> **Domain:** Disaster Management, Hydrological AI/ML & National Early Warning Systems  
> **Key Agencies Integrated:** Central Water Commission (CWC), India Meteorological Department (IMD), National Disaster Management Authority (NDMA), State Disaster Management Authorities (SDMA), Copernicus GloFAS

---

## 📌 Executive Summary

**DHARA (धारा)** is an AI-powered Hydrological Disaster Early Warning Intelligence System designed for vulnerable Himalayan river basins and flash-flood-prone mountain catchments. 

By unifying **physics-informed hydrology** with **real-time satellite telemetry**, **dynamic Census of India spatial buffers**, and **machine learning stacking ensembles**, DHARA delivers actionable zero-false-alarm flood intelligence to disaster response forces (NDRF/SDRF), district magistrates, and citizens.

---

## 🚀 Key Architectural Innovations

### 1. 5-Factor Environmental Synthesis
Unlike traditional systems that rely solely on upstream rainfall gauges, DHARA synthesizes five real-time environmental factors:
- **Precipitation Accumulation**: Live 24h millimeter rainfall depth.
- **Topsoil Volumetric Saturation**: Antecedent Soil Moisture Index (ASMI) measuring pore water pressure.
- **Topographic Gradient & Elevation**: Digital Elevation Models (DEM) evaluating runoff acceleration.
- **Catchment Discharge Flow**: Upstream river hydraulic volume (m³/s).
- **Historical High Flood Level (HFL)**: Benchmarked against CWC danger and warning thresholds.

### 2. Dual-Engine Hydrological Triage (Fluvial vs. Pluvial)
- **Engine 1: Fluvial (Riverine & Dam Releases)**: Monitors river stage crests, upstream barrage sluice gates, and embankment breach threats.
- **Engine 2: Pluvial (Urban Stormwater & Sump Choke)**: Evaluates localized rainfall intensity vs. municipal sump drain capacity independently of mainstem river stage.

### 3. Dynamic Census of India & SDMA Asset Impact Exposure
- Computes spatial population exposure dynamically over 3 km, 5 km, and 10 km inundation buffers.
- Grounded in official **Census of India administrative block/tehsil registry** and **SDMA disaster inventories**.
- Identifies verified emergency trauma hospitals, designated high-ground school relief shelters, and vulnerable national highway corridors (e.g. NH-3, NH-5, NH-107).

### 4. Interactive Dam Sluice Gate What-If Simulator
- Simulates real-time hydrodynamic surge propagation and downstream river stage rise from upstream dam releases (e.g., Pandoh Dam, Larji Dam, Tehri Dam).

### 5. Multi-Horizon AI/ML Predictive Forecasting
- Forecasts flood probability across **+1 Hour, +6 Hours, +24 Hours, and +72 Hours**.
- High-efficiency inference engine executing in < 5 ms.

---

## 📁 Repository Structure

`
dhara_project/
├── frontend/                     # React 19 + Vite + Leaflet GIS Dashboard
│   ├── src/
│   │   ├── App.jsx               # Core Command Dashboard & Operations Modals
│   │   ├── App.css               # Matte Titanium & Glassmorphic UI Theme
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
├── backend/                      # FastAPI Python Inference Engine
│   ├── main.py                   # REST API routes & Health telemetry
│   ├── api.py                    # Predictive ML pipeline & Risk models
│   ├── schemas.py                # Pydantic data validation contracts
│   └── river_data.py             # CWC basin telemetry & station registry
├── project_assets/               # Presentation graphics, icons, and diagrams
├── DHARA_Judge_Master_Defense_Guide.html
├── DHARA_Comprehensive_Defense_Report.html
└── README.md
`

---

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Leaflet, Esri World Imagery Satellite Tiles, Lucide Icons
- **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic, NumPy, SciPy
- **Data Ingestion**: Open-Meteo Ingest, Copernicus GloFAS, CWC Water Stage Gauges
- **Design System**: Matte Charcoal Titanium & Monsoon Dusk with Glassmorphism

---

## ⚡ Quickstart Guide

### 1. Backend Setup
`ash
cd backend
pip install fastapi uvicorn pydantic numpy requests
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
`
The FastAPI backend will start at: http://localhost:8000  
Interactive API docs (Swagger): http://localhost:8000/docs

### 2. Frontend Setup
`ash
cd frontend
npm install
npm run dev
`
The UI dashboard will launch at: http://localhost:5173

---

## 👥 Authors & Team
- **GitHub**: [@Kanishkk23](https://github.com/Kanishkk23)

---

## 📜 License
Developed for **Crisis Before Crisis (IIITN)**. All rights reserved.

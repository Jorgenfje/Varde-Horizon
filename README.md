# Varde Horizon

A cloud-native OSINT platform for real-time maritime tracking, anomaly detection, and automated satellite intelligence in the Arctic and Norwegian waters.

## Overview
Varde Horizon is a geospatial intelligence system designed to monitor maritime traffic and safeguard critical undersea infrastructure (subsea cables, pipelines, and offshore installations). The platform ingests real-time AIS vessel data, flags behavioral anomalies, and automatically triggers satellite imagery acquisition and AI-driven change detection over areas of interest.

Inspired by traditional Norwegian coastal beacons (*varder*), the project translates historical maritime surveillance into a modern, cloud-native software architecture.

## Key features
- **Real-time AIS streaming:** Ingests live vessel positions across Norwegian maritime zones via the BarentsWatch API.
- **Maritime anomaly detection:** Flags suspicious behavior, such as vessels stopping or idling over critical subsea infrastructure or disabling transponders.
- **Automated satellite acquisition:** Triggers API requests to the Copernicus Data Space Ecosystem to fetch fresh Sentinel-1 (SAR) and Sentinel-2 (optical) imagery over flagged locations.
- **Computer vision & AI analysis:** Runs serverless PyTorch/OpenCV models for vessel detection and change analysis in satellite imagery.
- **Interactive map dashboard:** Web interface featuring live vessel rendering, spatial query overlays, and incident sidebars.

## Tech stack
- **Frontend:** Next.js, TypeScript, TailwindCSS, Mapbox GL / Leaflet
- **Backend:** Python, FastAPI, WebSockets, Pydantic
- **Database:** PostgreSQL with PostGIS extension for geospatial queries
- **AI & Computer vision:** PyTorch, OpenCV, Serverless GPU (Modal / Replicate)
- **Cloud & DevOps:** Docker, GitHub Actions (CI/CD), Vercel (Frontend), Railway (Backend)

## Getting started

### Prerequisites
- Python 3.10+
- BarentsWatch Developer Account (for AIS API credentials)

### Local setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Jorgenfje/varde-horizon.git](https://github.com/Jorgenfje/varde-horizon.git)
   cd varde-horizon

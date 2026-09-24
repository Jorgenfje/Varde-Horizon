# Varde Horizon 🛰️🌊

## Overblikk
Varde Horizon er en sky-nativ OSINT-plattform (Open Source Intelligence) designet for sanntidsovervåking og anomali-deteksjon i norske og nordlige havområder. Plattformen kombinerer sanntids AIS-posisjonsdata med automatisert henteprosess for satellittbilder (Copernicus) og AI-basert bildeanalyse.

## Nøkkelfunksjoner
- **Sanntids sporing:** Ingestering og visualisering av maritime data (AIS) via BarentsWatch API.
- **Sikkerhetsmønster & Anomali-deteksjon:** Automatiske varsler dersom fartøy utviser avvikende oppførsel nær kritisk undersjøisk infrastruktur.
- **Automatisert Satellitt-innhenting:** Trigger-basert oppslag mot Copernicus Data Space Ecosystem for henting av ferske Sentinel-2/Sentinel-1 satellittbilder over avviksposisjoner.
- **AI/CV-analyse:** Computer vision-modell for endringsdeteksjon og objektgjenkjenning i satellittutsnitt.
- **Interaktivt Dashboard:** Webbasert 2D/3D-kartgrensesnitt for operativ oversikt.

## Teknologistakk
- **Frontend:** Next.js, TypeScript, TailwindCSS, Mapbox GL / Leaflet
- **Backend:** Python, FastAPI, WebSockets
- **Database:** PostgreSQL med PostGIS (Geografiske spørringer)
- **AI / Computer Vision:** PyTorch, OpenCV, Serverless GPU (Modal / Replicate)
- **Infrastruktur & Cloud:** Docker, GitHub Actions (CI/CD), Vercel (Frontend), Railway/Render (Backend)

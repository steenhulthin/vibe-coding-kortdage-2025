# ArcGIS Dashboards

- Gem exports og konfigurationer i `arcgis/dashboards/`.
- Dokumentér webmaps/feature layers og deling (organisation/offentlig).
- Forvent, at ArcGIS Online-licens er tilgængelig, og opret alle nye items i mappen `kortdage_2025`.
- Brug ArcGIS API for Python som primær værktøjskæde til opsætning, publicering og opdatering.
- Vælg Living Atlas som standardkilde til geografiske datasæt (landegrænser m.m.), når det er muligt.

## Miljø

- ArcGIS API for Python kræver en ældre pandas-version. Opret et separat virtuelt miljø til ArcGIS-arbejde:
  ```powershell
  python -m venv .venv_arcgis
  .\.venv_arcgis\Scripts\activate
  pip install -r requirements-arcgis.txt
  ```
- Den eksisterende `.venv` bruges fortsat til Streamlit/Dash/Shiny (pandas 2.3.3). Skift miljø alt efter platform.
- Har du ArcGIS Pro installeret og er allerede logget ind dér, kan scripts køres med ArcGIS Pro’s Python (inkl. `arcpy`) uden særskilt login:
  ```powershell
  "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" arcgis\dashboards\create_nordic_covid_scene.py
  ```

## Population reference

- 2022-befolkningstal bruges i den nordiske COVID-19 scene og ligger i `python/data/nordic_population_2022.csv`.
- Kilder (officiel statistik):
  - Danmark: Statistics Denmark (Population 1 January 2022)
  - Finland: Statistics Finland (Population structure 31 December 2022)
  - Island: Statistics Iceland (Population 1 January 2022)
  - Norge: Statistics Norway (Population 1 January 2022)
  - Sverige: Statistics Sweden (Year-end population 2022)

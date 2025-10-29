# GitHub Pages setup

- `index.html` er en landingsside, der linker til de enkelte dashboard-demoer (fx `streamlit.html`).
- `streamlit.html` bruger [stlite](https://github.com/whitphx/stlite) til at køre `python/streamlit_app/app.py` direkte i browseren.
- Datafilen `python/data/owid_covid_global_monthly.csv` og app-scriptet er duplikeret ind i `docs/python/...` for at kunne hostes statisk.
- Publicér mappen `docs/` via **GitHub Pages → Deploy from branch** (main branch, `/docs` folder). Siden vil derefter være tilgængelig på `https://<org>.github.io/<repo>/`.
- Lokal test: `python -m http.server --directory docs` og åbn `http://localhost:8000/` i en browser. Landingsside: `/`, Streamlit-demo: `/streamlit.html`.

## Nordisk webscene (`scene.html`)

- Embed-siden læser konfiguration direkte fra `SCENE_CONFIG` nederst i `scene.html`. Opdater feltet `webSceneId` til item-ID'et fra ArcGIS Online (Share → Embed → kopier ID'et).
- Tilpas `title`, `description`, `sourcesIntro` og listen `sources` for at ændre tekst og kildereferencer, fx hvis scenen eller datasættet skiftes ud.
- Hvis du sætter `instantAppUrl`, indlæses den direkte (fx Instant App 3D Viewer). Uden den falder siden tilbage til Scene Viewer embed (`https://www.arcgis.com/apps/sceneviewer/index.html?webscene=...&embed=1`).
- Living Atlas-referencen peger på FeatureServer-endpointet `https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Countries_(Generalized)/FeatureServer`. Hvis datasættet skifter, opdater både linket og feltet i `SCENE_CONFIG.sources`.

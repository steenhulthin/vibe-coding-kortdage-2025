# Vibe coding · COVID-19 dashboards (Kortdage 2025)

Dette repository samler alt materiale til Kortdage-oplægget om vibe coding og AI-assisteret udvikling: Python-dashboards, ArcGIS-scripts, Power BI dashboards og de statiske webdemoer på GitHub Pages.

## Struktur

- `arcgis/` – scripts og dokumentation til ArcGIS Online webscenen og relaterede assets.
- `powerbi/` – Power BI-projekter og eksportfiler.
- `python/` – kildekode til Streamlit, Dash og Shiny apps plus data og utils.
- `docs/` – statiske filer som publiceres via GitHub Pages (præsentation, demoer m.m.).
- `prompts.md` / `prompts2codex.md` – log over alle prompts og svar under udviklingen.
- `praesentation.md` – outline til selve oplægget (læses også af `docs/praesentation.html`).

## Kom godt i gang

1. Opret (eller aktiver) dit Python-miljø:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Datafiler ligger i `python/data/` (OWID, SSI, osv.). Eksterne filer hentes via scripts eller er checket ind som placeholders.
3. Agent- og promptloggene beskriver øvrige arbejdsgange og beslutninger.

## Python dashboards

- **Streamlit**: `streamlit run python/streamlit_app/app.py`
- **Dash**: `python python/dash_app/app.py`
- **Shiny**: `shiny run --reload python/shiny_app/app.py`

### Hostede dashboards

- **Streamlit Cloud**: https://vibe-coding-kortdage-2025.streamlit.app/
- **Shinyapps.io**: https://steenhulthin.shinyapps.io/covid-19-regionalt-overblik/
  - Installer `rsconnect-python` én gang: `pip install rsconnect-python`
  - Log ind: `rsconnect login --server shinyapps.io --token <TOKEN> --secret <SECRET>`
  - Deploy fra repoet: `rsconnect deploy shiny python/shiny_app/app.py --title covid-19-regionalt-overblik`
  - Efter første deploy kan appen genudgives via `rsconnect deploy shiny python/shiny_app/app.py`

Shiny-appen kan eksporteres til Shinylive med:
```powershell
shinylive export python/shiny_app docs/shiny_app
```

## ArcGIS workflow

- Hovedscriptet `arcgis/dashboards/create_nordic_covid_scene.py` kører via ArcGIS Pro Python (`propy.bat`) for at genopbygge den nordiske webscene, opdatere hosted layers og publicere scenen i mappen `kortdage_2025`.
- Datasæt og populationstal til scenen findes i `python/data/` og dokumenteres i `arcgis/README.md`.
- Efter kørsel kan scenen indlejres i ArcGIS Dashboards eller Experience Builder (se `docs/scene.html` for eksempel).

## Power BI

- Power BI-ressourcer ligger i `powerbi/`. Projektet benytter Fill Maps og kræver enterprise-adgang for publicering.
- Se `powerbi/`-mappen for eksportfiler, noter og begrænsninger (fx licenser og hosting).

## GitHub Pages og demoer

- `docs/index.html` er landingssiden med links til præsentation, Streamlit-demo, Shinylive-dashboard og ArcGIS webscenen.
- `docs/praesentation.html` loader `praesentation.md` og viser oplæggets outline direkte fra GitHub Pages.
- `docs/streamlit.html` viderestiller til den hostede version på Streamlit Cloud.
- `docs/shiny_app/` indeholder Shinylive-exporten.
- `docs/scene.html` embedder webscenen (Instant App/Scene Viewer) og beskriver datakilderne.
- Publicér via **GitHub Pages → Deploy from branch** (vælg `trunk` og `/docs`). Lokal test: `python -m http.server --directory docs` og åbn `http://localhost:8000/`.

## Licens og attribution

- Projektet er licenseret under **CC BY-NC-SA 4.0** (se `LICENSE`).
- Eksterne datasæt (OWID, SSI, nationale statistik-kilder m.fl.) refereres i appene og dokumentationen.

## Support og videre arbejde

- `todo.md` samler åbne opgaver og idéer (geometrier, hosting, præsentationsforbedringer m.m.).
- `pros_cons.md` giver en sammenligning af teknologierne ud fra vibe coding-oplevelsen.
- Brug `prompts.md` og `prompts2codex.md` for at se præcise prompts, beslutninger og fallback-planer.

# GitHub Pages setup

- `index.html` loader bruger [stlite](https://github.com/whitphx/stlite) til at køre `python/streamlit_app/app.py` direkte i browseren.
- Datafilen `python/data/owid_covid_global.csv` og app-scriptet er duplikeret ind i `docs/python/...` for at kunne hostes statisk.
- Publicér mappen `docs/` via **GitHub Pages → Deploy from branch** (main branch, `/docs` folder). Siden vil derefter være tilgængelig på `https://<org>.github.io/<repo>/`.
- For lokal test: `python -m http.server --directory docs` og åbn `http://localhost:8000/` i en browser.

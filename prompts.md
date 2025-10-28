# Codex Session Log

User:
<user_instructions>

﻿# agents.md — Vibe coding guide (Codex + VS Code)

## Formål
- Holde AI-agenten (Codex/ChatGPT) på sporet: mål, regler og kontekst.

## Projektmål (kort)
- Samme COVID-19 KPI’er på tværs af platforme (ArcGIS, Power BI, Python: Streamlit/Shiny/Dash).
- Enkle, hurtige demoer; minimér opsætning.

## Ground rules
- **Forklar før du skriver større mængder kode.**
- **Ingen destruktive bulk-ændringer** uden godkendelse.
- Følg PEP8, brug typer når det hjælper.
- Filstruktur og navne som i repoet her.
- ArcGIS-arbejde skal som udgangspunkt løses med ArcGIS API for Python og bruge Living Atlas for geografiske datasæt, når det er muligt.

## Kontekst (pin/copy til AI-chat)
- Rod: `arcgis/`, `powerbi/`, `python/` (3 platforme)
- Python apps: `python/streamlit_app/app.py`, `python/shiny_app/app.py`, `python/dash_app/app.py`
- Delte utils og data: `python/utils/`, `python/data/`

## Dataschema (placeholder)
- Kolonner: `date`, `level` ∈ {Global, EU, Nordic, DK}, `metric`, `value`
- CSV i `python/data/…` (indsættes senere)

## UI/Design
- Konsekvente KPI-navne og akser.
- Farver og labels ens på tværs.

## Sikkerhed
- Ingen nøgler/secrets i repo. Brug env-vars.

## Kommandoliste (Windows)
- Opret miljø: `Tasks: Install requirements` (Ctrl+Shift+P → “Run Task”)
- Kør apps: VS Code “Run and Debug”:
  - **Streamlit**, **Dash**, **Shiny**

## Prompt-skabeloner
**“Refactor utils”**  
> Gennemgå `python/utils/…` og foreslå 2 forbedringer. Forklar kort, lav små PR-venlige diffs.

**“Add KPI chart”**  
> Tilføj linjegraf for `metric="cases_7d"` i alle tre Python-apps. Vis legend og ens aksetitler.

**“Data adapter”**  
> Skriv en helper der indlæser CSV og standardiserer kolonner → pandas DataFrame.


</user_instructions>

User:
<environment_context>
  <cwd>c:\Users\b246800\Documents\prj\vibe_coding</cwd>
  <approval_policy>on-request</approval_policy>
  <sandbox_mode>workspace-write</sandbox_mode>
  <network_access>restricted</network_access>
  <shell>powershell.exe</shell>
</environment_context>

User:
# Context from my IDE setup:

## Active file: prompts2codex.md

## Open tabs:
- agents.md: agents.md
- create_nordic_covid_scene.py: arcgis/dashboards/create_nordic_covid_scene.py
- prompts2codex.md: prompts2codex.md
- app.py: python/shiny_app/app.py

## My request for Codex:
update prompt loggen. Den skal være i utf-8.

Assistant:
Rewrote `prompts2codex.md:1` so every Danish character renders correctly and the file is now saved explicitly as UTF-8 (PowerShell `Set-Content -Encoding utf8` writes a BOM to keep Windows tools happy). Added the current request as item 56 and cleaned up a few earlier entries while I was normalizing the text (e.g. fixed “månedsniveau”, “kommandoen”, consistent hyphenation, capitalized “Danmark”, corrected `\vibe_coding\…` path). Verified the file loads without decoding errors via `Path('prompts2codex.md').read_text(encoding='utf-8')`.

- **Next steps**: 1. Commit the updated prompt log when ready.

User:
# Context from my IDE setup:

## Active file: arcgis/dashboards/create_nordic_covid_scene.py

## Open tabs:
- agents.md: agents.md
- create_nordic_covid_scene.py: arcgis/dashboards/create_nordic_covid_scene.py
- prompts2codex.md: prompts2codex.md
- app.py: python/shiny_app/app.py

## My request for Codex:
Jeg har slettet indholdet i kortdage_2025 mappen på arcgis online mappen. hvad var kommandoen til at regenerere scenen?

Assistant:
Kør bare scriptet igen:

- `python arcgis/dashboards/create_nordic_covid_scene.py`

Det genetablerer `kortdage_2025`-mappen, genskaber det hostede feature layer og publicerer scenen på ArcGIS Online.

User:
# Context from my IDE setup:

## Active file: arcgis/dashboards/create_nordic_covid_scene.py

## Open tabs:
- agents.md: agents.md
- create_nordic_covid_scene.py: arcgis/dashboards/create_nordic_covid_scene.py
- prompts2codex.md: prompts2codex.md
- app.py: python/shiny_app/app.py

## My request for Codex:
Ja, men jeg skal køre det med propy ikke?

Assistant:
Yes—run it with ArcGIS Pro’s Python so it can reuse your Pro login/profile. From a regular PowerShell/CMD prompt:

- "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" arcgis/dashboards/create_nordic_covid_scene.py

(Adjust the Pro install path if yours differs.) That will sign in via your ArcGIS Pro profile and rebuild the scene in `kortdage_2025`.

User:
# Context from my IDE setup:

## Active file: arcgis/dashboards/create_nordic_covid_scene.py

## Open tabs:
- agents.md: agents.md
- create_nordic_covid_scene.py: arcgis/dashboards/create_nordic_covid_scene.py
- prompts2codex.md: prompts2codex.md
- app.py: python/shiny_app/app.py

## My request for Codex:
Det ville være rart, hvis du kunne huske, hvad vi talte om i går. Er det muligt? 

Jeg har en user installation af arcgis pro: Det korrekte var: 
%Userprofile%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\Scripts\propy.bat arcgis\dashboards\create_nordic_covid_scene.py

Assistant:
Jeg kan kun huske det, vi har skrevet i den aktuelle chat-session; tidligere samtaler følger ikke med automatisk. Hvis du vil have mig til at bruge noget fra i går, så nævn det igen (eller gem det i prompt-loggen).

Til din user-installation er kommandoen:

- `%Userprofile%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\Scripts\propy.bat arcgis/dashboards/create_nordic_covid_scene.py`

Så får scriptet Pro-profilerne med og genskaber scenen i `kortdage_2025`.

User:
# Context from my IDE setup:

## Active file: arcgis/dashboards/create_nordic_covid_scene.py

## Open tabs:
- agents.md: agents.md
- create_nordic_covid_scene.py: arcgis/dashboards/create_nordic_covid_scene.py
- prompts2codex.md: prompts2codex.md
- app.py: python/shiny_app/app.py

## My request for Codex:
Lad os få lavet en mere komplet prompt log (i tillæg til den eksisterende) , navngiv den prompts.md. Indholdet skal være en eksakt kopi/klon af codex-vinduet (dette vinduet) - både min prompts og dine svar. Hvis der findes noget indbygget er det også fint, men jeg vil gerne have, at det kommer med i git repo'et, som en fil.

# Teknologier – fordele og ulemper ift. generativ AI

| Parameter | Shiny (Shinylive/ShinyApps) | Dash | Streamlit | ArcGIS Scene / 3D Viewer | Power BI |
| --- | --- | --- | --- | --- | --- |
| Opsætningshastighed | Middel – kræver strukturering af UI/server, men let CLI-deploy via Shinylive/ShinyApps | Middel – Python + layout-komponenter, mere boilerplate | Hurtig – enkel `st.*` API, godt til prototyper | Længere – JSON-/scene-script skal bruges, afhængig af ArcGIS-konto | Middel – grafisk designer, men datamodel skal bygges |
| AI-assistance | God – Copilot/ChatGPT klarer `ui`, `server` og `plotly`-snippets | God – AI genererer callbacks/layout, men debugging kræver manuel viden | Fremragende – AI laver komplette apps | Begrænset – AI kan generere JSON, men ArcGIS-specifikke felter kræver erfaring | Middel – AI hjælper med M/DAX, men visuals er UI-styrede |
| Udvidelsesmuligheder | Høj – full Python, kan tilføje JS/Plotly | Høj – støtter custom komponenter, API-integration | Middel – Python + begrænset custom JS | Lav – Scene Viewer/Instant Apps styres af Esri-skabeloner | Lav – Custom visuals kræver TypeScript SDK |
| Deployment friction | Lav – Shinylive (static), ShinyApps (PAAS) | Middel – Heroku/Fly/Render e.l. | Lav – Streamlit Cloud/Huggingface | Høj – kræver ArcGIS Online publicering | Middel/Høj – kræver Power BI Service/Premium |
| Performance + datahåndtering | God – Pandas + caching muligt | God – FastAPI/WSGI kombi | Middel – Pandas i runtime, mindre tuning | Scenen håndterer store datasæt men 3D kræver optimering | Fremragende til aggregeret data, men kompleks modelleringslag |
| Visuel fleksibilitet | Middel – Plotly mv., CSS muligt | Høj – fuld kontrol, men mere arbejde | Middel – standard layout men temaer lidt begrænsede | Høj for 3D, men UI-frit | Middel – visuals faste, branding via temaer |
| Samarbejde & kontrol | Git-venlig, dependabot muligt | Git-venlig, CI/CD muligt | Git-venlig, CLI eksport | Scene JSON/py scripts versioneres, men UI via web | PBIX binær, kræver BI-proces |
| Publikumsoplevelse | Interaktivt, dashboards web-friendly | Interaktivt, men mere "app-lignende" | Hurtig at demonstrere, men standard look | Stor "wow" faktor, 3D og tidsstyring | Kendt BI-oplevelse, gode filtre |

**Bemærk:** Parametervægtene er skaleret mod Kortdage-demoens fokus: hurtig udvikling med generativ AI, lav friction ved deling, og førstepersons indtryk for publikum.

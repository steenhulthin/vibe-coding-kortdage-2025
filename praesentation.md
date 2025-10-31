# Vibe coding og AI-assisteret udvikling af geodata-dashboards

## Slide 1 - Velkommen
- AI + data => dashboards på rekordtid

## Slide 2 - Hvem er på scenen?
- Hvordan arbejder vi med [AI](https://en.wikipedia.org/wiki/Generative_artificial_intelligence) og hvad/hvem er [SSI](https://ssi.dk)?
    * SSI er under Indenrigs- og Sundhedsministeriet. SSI forebygger og bekæmper infektionssygdomme og medfødte sygdomme. 
    * har nedskrevne retninglinjer for brug og muligheder for at søge om at benytte AI på nye måder eller nye sammenhænge
    * [bruger AI seriøst](https://www.ssi.dk/aktuelt/nyheder/2024/millionstoette-til-ai-drevet-forskning-i-blodforgiftning)
    * har en godkendt AI-prompt
- Hvem er [Steen Hulthin Rasmussen](https://www.linkedin.com/in/steenhulthin/) 
    * ![Steen Hulthin Rasmussen på cykel i rummet, hvor der er en regnbue... (don't ask)](assests_praesentation/DEK_2026.png)
    * er datadomptør/udvikler/kaffedrikker
    * arbejder til daglig med datapipelines og udvikling af dashboards
    * synes AI er lige dele fremtiden, et fantastisk værktøj, skræmmende, fascinerende og kildekritikfremkaldende

## Slide 3 - Vibe coding vs. AI-assisteret udvikling
- Hvad er “vibe coding” og kan AI hjælpe med kode?
    - TODO: tilføj coining af term og reference (evt. reference til wikipedia eller lignende)
    - Vibe coding: AI som makker i [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment)’et (autofuldførelse, chat, kodeforslag)
    - AI-assisteret udvikling: manuel prompt-workflow udenfor IDE’et (den almindelige prompt)
    - Samme grundidé, men forskellige tilgange

## Slide 4 - Mission briefing (mål, data, værktøjer, tidsramme)
- Mission briefing
    - **Mål:** bygge dashboards hurtigt og spare Kortdage-deltagerne for faldgruberne
    - **Data:** COVID-19 tal på globalt, EU-, nordisk og dansk niveau
    - **Værktøjer:** Streamlit, Shiny, Dash, ArcGIS (API + Dashboards/Viewer), Power BI
    - **Tidsramme:** 5 fredage (som var lige i underkanten) → 20 minutters præsentation

## Slide 5 - Ambitionen (aka "det var ret ambitiøst...")
- Ambitionen (eller "det var ret ambitiøst...")
    - 3 datasæt, fem platforme
    - 3 Python-teknologier + ArcGIS dashboard + Power BI dashboard
    - Lær, forstå og videreformidl
    - Lad alt materiale være tilgængelig
    - Kom så langt som muligt
    - Hav det sjovt

## Slide 6 - Første aha-oplevelse
- PowerPoint-eksperimentet der sparkede projektet i gang
- Hvad AI ramte plet med, og hvor mennesket måtte overtage

## Slide 7 - Tool sprint: Python-trioen
- **Streamlit:** prompts → global prototype; link til streamlit.app
- **Shiny:** sidebar/timelapse; Shinylive-export som backup; hosting-status
- **Dash:** geojson-dansefest, simplificering og prompts der fejlede (og blev reddet)

## Slide 8 - Tool sprint: ArcGIS & Power BI
- **ArcGIS 3D scene:** propy-workflow, Living Atlas, tidsregulator
- **Power BI:** AI-assistance vs. enterprise-friktion (licenser, hosting, maps)
- Et par prompt-eksempler hvor det ikke lykkedes – og hvad der virkede i stedet

## Slide 9 - Hvad er AI særligt velegnet til?
- Lyn-prototyper og idéafprøvning
- Review/korrektur og dokumentation
- Teknologier med stor community-hjælp
- Workflows der kan scriptes eller automatiseres

## Slide 10 - Tips til at bruge AI effektivt
- Del kontekst – ellers gætter AI forkert
- Bed AI’en stille dig spørgsmål før løsningen
- Log dine prompts (prompts.md) og gem hits som skabeloner

## Slide 11 - Overvejelser og sikkerhed
- Må du bruge AI på arbejdet? Hvad siger politikkerne?
- Vibe coding vs. AI-assisteret udvikling ift. compliance og logging
- Datafølsomhed og hosting (cloud vs. on-prem)

## Slide 12 - Læring og takeaways
- Hvor gav AI størst værdi, og hvornår spildte vi tiden?
- Hvad ville vi gøre anderledes næste gang?
- Konkrete råd til at prøve vibe coding på dit eget dashboard

## Slide 13 - Afslutning og næste skridt
- AI er makker, ikke magi – du styrer retningen
- QR/link til repo + invitation til at dele erfaringer med SSI-teamet
- Q&A og tak for nu

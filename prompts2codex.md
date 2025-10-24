# Prompts to Codex

1. Jeg har brug for covid-19 data på globalt niveau. Hvor kan jeg downloade det?
2. Lad os fokusere på indlæggelser og dødsfald. Kan du lægge data fra OWID og fra ECDC i datamappen (i et format der er læsbart med pandas)?
3. Jeg kan ikke se der er lavet et python venv? Kan du gøre det?
4. Ok, lad os fortsætte med at få hentet data.
5. Lad os også lige få hentet det danske data fra SSI: https://sseruminstitut.maps.arcgis.com/sharing/rest/content/items/67a8aedc7ff9466e8920951540c2097f/data
6. Lad os skære ned på datamængden i OWID datasættet. Behold kolonner med geografisk placering, indlæggelser og død.
7. Commit datafilerne, men dog ikke ssi_denmark_data.zip – ignorer den i stedet.
8. Kan du lave en prompts2codex.log (eller .md alt efter hvad der giver bedst mening) i roden af projektet. Den skal indeholde de prompts, jeg har givet dig.
9. Perfekt. Commit den.
10. Push både til github og origin.
11. Jeg vil bruge GitHub Pages til at hoste python dashboardsene (er det muligt med dash - det burde være muligt med shiny via shinylive og med streamlit via stlite). Kan du gøre en docs mappe klar til ghpages?
12. Det lyder godt. Lad os lave dashboards. Lad os starte med Streamlit. Streamlit skal være med OWID data. Der skal øverst være et kort over verden. Landene skal være farvet efter indlæggelser per capita og skraveret efter dødsfald per capita (hvis det er muligt). Der skal være en periodevælger, hvor der kan vælges år og måned. Tallene skal summeres over den valgte periode. Det skal være muligt at vælge et specifikt land. Under kortet skal der være en graf der viser indlæggelser og død per capita over tid (summeret på månedniveau) for det valgte land (og ellers for hele verden).
13. Make it so!
14. Kan du starte streamlit?
15. Ok, tilføj streamlit til requirement og installér i venv.
16. Ja, kør den.
17. Jeg får en lang fejl, men jeg tror noget går galt med choropleth: (fejltrace).
18. Start serveren igen, så ser vi.
19. Så fint. Commit det.
20. Lad os lige stlite til at fungere og se det i ghpages.
21. Serveren kører og jeg ser index.html siden, men jeg får: Fejl under indlæsning: stlite is not defined.
22. Ok, nu får jeg dog: Fejl under indlæsning: The `entrypoint` field is required.
23. Hvor lang tid forventer du det tager at loade?
24. Ok, vi skal måske tænke på stream.app hosting. Nå, kan du løbende tilføje mine prompts til prompts2codex? og lige tilføje de manglende i hvert fald.
25. Nå, min computer gik ned (ikke relateret til projektet). Kan vi lave et datasæt til streamlit dashboardet, som er præaggregeret på månedsniveau?
26. Ja, lad os se om det ikke bare er sagen. :) Og lad mig lige få commandoen til at serve stlite på den lokale webserver igen også.
27. Husk at få tilføjet prompts til prompt-loggen. ;)
28. Hm, det ser ud som om det hænger. bruger det det reducerede datasæt?
29. ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:43] "GET / HTTP/1.1" 200 - (::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /python/streamlit_app/app.py HTTP/1.1" 200 - ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /python/data/owid_covid_global_monthly.csv HTTP/1.1" 200 - ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] code 404, message File not found ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /favicon.ico HTTP/1.1" 404 -)
30. Ok, der sker ikke noget. Men prøv at pushe til begge remotes. Jeg har slået ghpages til, så måske fungerer det der.
31. Drevet var blevet disconnected. Tilføj lige prompt logs, commit og push igen.

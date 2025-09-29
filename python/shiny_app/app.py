from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Vibe Demo – Shiny (Python)"),
    ui.p("KPI’er – data indsættes senere.")
)

def server(input, output, session):
    pass

app = App(app_ui, server)

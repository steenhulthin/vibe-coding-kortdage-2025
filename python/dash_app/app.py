from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)
app.title = "Vibe Demo – Dash"

df = pd.DataFrame({"level":["Global","EU","Nordic","DK"], "value":[None,None,None,None]})
fig = px.bar(df, x="level", y="value")

app.layout = html.Div([
    html.H1("Vibe Demo – Dash"),
    html.P("KPI’er – data indsættes senere."),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)

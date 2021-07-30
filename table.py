import dash
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
    }
)

app.layout = dbc.Table.from_dataframe(df,
                                      bordered=True,
                                      dark=True,
                                      hover=True,
                                      responsive=True,
                                      striped=True)

if __name__ == "__main__":
    app.run_server()

from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__)

def flatten(l):
    return [item for sublist in l for item in sublist]

num_ccalls = 3
num_calcs = 2

contract_calls = html.Div(
    flatten([
        [
            # html.Div(children=f"{counter_contract_calls+1}"),
            dcc.Input(id=f"res_{counter_contract_calls+1}", placeholder="Var name", type="text", style={'width':'60px', "margin-left": "20px"}),
            dcc.Input(id=f"call_{counter_contract_calls+1}", placeholder="Function name", type="text", style={"margin-left": "10px"}),
            dcc.Input(id=f"inputs_{counter_contract_calls+1}", placeholder="Inputs, comma seperated", type="text", style={"margin-left": "10px"}),
            html.Br(),
            html.Br(),
        ]
        for counter_contract_calls in range(num_ccalls)
    ])
)

calculations = html.Div(
    flatten([
        [
            dbc.Input(id=f"mat_res_{counter_calculations}", placeholder="Math variable name", type="text", style={'width':'60px', "margin-left": "20px"}),
            dbc.Input(id=f"formula_{counter_calculations}", placeholder="Formula involving variables", type="text", style={'width':'500px', "margin-left": "15px"}),
            html.Br(),
            html.Br(),
        ]
        for counter_calculations in range(num_calcs)
    ])
)


app.layout = html.Div([
    html.H1(children='Chain state', style={'textAlign':'center'}),
    html.H2(children='Contract calls'),
    contract_calls,
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2(children='Maths'),
    calculations

], style={"margin-left": "300px"})


# @app.callback(Output("output", "children"), [Input("input", "value")])
# def output_text(value):
#     return value

if __name__ == '__main__':
    app.run_server(debug=True)
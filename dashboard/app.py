from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__)

chain_list = ['Ethereum', 'Polygon', 'Arbitrum']
protocol_list = ['UniSwap v2', 'UniSwap v3']

query_variables = html.Div(
    [
        dcc.Dropdown(options=chain_list, id="chain_id", placeholder="Chain", style={'width':'200px', "margin-left": "10px"}),
        html.Br(),
        dbc.Input(id="wallet_address", placeholder="Wallet address", type="text", style={'width':'350px', "margin-left": "20px"}),
        html.Br(),
        html.Br(),
        dbc.Input(id="block_number", placeholder="Blocknumber", type="text", style={'width':'350px', "margin-left": "20px"}),
        html.Br(),
        html.Br(),
        html.Div(id='contracts'),
    ]
)

api_ids = html.Div([
        dbc.Input(id="api_address", placeholder="API address", type="text", style={'width':'350px', "margin-left": "20px"}),
        html.Br(),
        html.Br(),
        dbc.Input(id="api_key", placeholder="API key", type="text", style={'width':'350px', "margin-left": "20px"}),
])

app.layout = html.Div([
    html.Center([
        html.H1(children='Chain state'),
        dcc.Dropdown(options=protocol_list, id="dex_id", placeholder="Protocol", style = {'width': '200px', 'textAlign':'left'}),
    ]),

    html.Div(
    [
        html.Div(
            [
                html.H2(children='API variables'),
                api_ids,
            ]
        ),
        html.Div(
            [
                html.H2(children='Query variables'),
                query_variables,
            ]
        ),
    ], style={'display':'inline-block'}
    )

])

@app.callback(
    Output("contracts", "children"), 
    Input("dex_id", "value"))
def set_contract_fields(value):
    if value == protocol_list[0]:
        return dbc.Input(id="pool_contract_address", placeholder="Pool contract address", type="text", style={'width':'350px', "margin-left": "20px"}),
    elif value == protocol_list[1]:
        fields = [
            dbc.Input(id="pool_contract_address", placeholder="Pool contract address", type="text", style={'width':'350px', "margin-left": "20px"}),
            html.Br(),
            html.Br(),
            dbc.Input(id="nft_contract_address", placeholder="NFT contract address", type="text", style={'width':'350px', "margin-left": "20px"}),
            html.Br(),
            html.Br(),
            dbc.Input(id="nft_id", placeholder="NFT ID", type="text", style={'width':'350px', "margin-left": "20px"}),
        ]
        return fields
    else:
        return html.Div('Please select protocol version first.', style={'margin-left':'20px'})

# https://github.com/plotly/dash/issues/475

if __name__ == '__main__':
    app.run_server(debug=True)
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__)

chain_list = ["Ethereum", "Polygon", "Arbitrum"]
protocol_list = ["UniSwap v2", "UniSwap v3"]
radio_v3_options = ["Transaction ID", "Pool and NFT details"]

protocol_select = dcc.Dropdown(
    options=protocol_list,
    id="dex_id",
    placeholder="Protocol",
    style={"width": "200px", "textAlign": "left"},
)

etherscan_api = html.Div(
    [
        dbc.Input(
            id="etherscan_rpc_endpoint",
            placeholder="Etherscan RPC endpoint",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        dbc.Input(
            id="etherscan_api_key",
            placeholder="Etherscan API key",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        dcc.Checklist(id='checklist_mainnet', options=[{'label': '  Contract is not on Ethereum mainnet', 'value':'mainnet'}], ),
    ],
    style={"margin-left": "20px"},
)

other_scan_api = html.Div(
    [
        html.H3(children="Other scanner"),
        html.Br(),
        dbc.Input(
            id="otherscan_rpc_endpoint",
            placeholder="RPC endpoint for chain of interest",
            type="text",
            style={"width": "350px", "margin-left": "20px"},
        ),
        html.Br(),
        html.Br(),
        dbc.Input(
            id="otherscan_api_key",
            placeholder="API key for RPC of interest",
            type="text",
            style={"width": "350px", "margin-left": "20px"},
        ),
    ],
)

query_variables = html.Div(
    [
        dbc.Input(
            id="wallet_address",
            placeholder="Wallet address",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        dbc.Input(
            id="block_number",
            placeholder="Blocknumber",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        html.Div(id="contracts"),
    ],
    style={"margin-left": "20px"},
)

v3_lp_fields = html.Div(
    [
        html.Br(),
        dbc.Input(
            id="pool_contract_address",
            placeholder="Pool contract address",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        dbc.Input(
            id="nft_contract_address",
            placeholder="NFT contract address",
            type="text",
            style={"width": "350px"},
        ),
        html.Br(),
        html.Br(),
        dbc.Input(
            id="nft_id", placeholder="NFT ID", type="text", style={"width": "350px"}
        ),
    ],
    style={"margin-left": "20px"},
)

v3_transcation_fields = html.Div(
    [
        html.Br(),
        dbc.Input(
            id="transaction_hash",
            placeholder="Transaction ID",
            type="text",
            style={"width": "350px"},
        ),
    ],
    style={"margin-left": "20px"},
)

radio_v3 = html.Div(
    [
        dcc.RadioItems(id="radio_v3", options=radio_v3_options),
        html.Div(id="radio_v3_children"),
    ],
    style={"margin-left": "20px"},
)

app.layout = html.Div(
    [
        html.Center(
            [
                html.H1(children="Chain state"),
                protocol_select,
            ]
        ),
        html.Div(
            [
                html.H2(children="API variables"),
                html.Div(
                    [
                        html.H3(children="Etherscan"),
                        etherscan_api,
                        html.Div(id="other_scanner"),
                    ],
                    style={"margin-left": "20px"},
                ),
            ]
        ),
        html.Div(
            [
                html.H2(children="Query variables"),
                query_variables,
            ]
        ),
    ]
)


@app.callback(Output("other_scanner", "children"), Input("checklist_mainnet", "value"))
def set_otherscanner(value):
    if value == ['mainnet']:  # other scanner needed
        return other_scan_api
    else:
        pass
@app.callback(Output("contracts", "children"), Input("dex_id", "value"))
def set_dex_fields(value):
    if value == protocol_list[0]:  # v2
        return (
            dbc.Input(
                id="pool_contract_address",
                placeholder="Pool contract address",
                type="text",
                style={"width": "350px", "margin-left": "20px"},
            ),
        )
    elif value == protocol_list[1]:  # v3
        return radio_v3
    else:
        return html.Div(
            "Please select protocol version first.", style={"margin-left": "20px"}
        )


@app.callback(Output("radio_v3_children", "children"), Input("radio_v3", "value"))
def set_radio_fields(value):
    if value == radio_v3_options[0]:
        return v3_transcation_fields
    elif value == radio_v3_options[1]:
        return v3_lp_fields
    else:
        return html.Div(
            [
                html.Br(),
                html.Div(
                    "Please select type of input first.", style={"margin-left": "20px"}
                ),
            ]
        )

if __name__ == "__main__":
    app.run_server(debug=True)

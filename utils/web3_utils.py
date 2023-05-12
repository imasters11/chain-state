import urllib.parse

import requests
from web3 import Web3

from env_utils import get_env_variable


def get_w3_provider(chain) -> Web3:
    if chain == 'ethereum':
        return Web3(Web3.HTTPProvider(get_env_variable("ETH_RPC_URL")))
    assert False


# TODO: more chains
def construct_scanner_url(params) -> str:
    base_url='https://api.etherscan.io'
    url = f'{base_url}?{urllib.parse.urlencode(params)}'
    url += "&apikey={}".format(get_w3_provider("ETHERSCAN_API_KEY"))
    return url


def get_abi(address: str) -> dict:
    abi_request_params = {
        "module": "contract",
        "action": "getabi",
        "address": address
    }

    url = construct_scanner_url(abi_request_params)
    resp = requests.get(url)
    return resp.json()['result']


def contract_call_at_block(interface_address, implementation_address, fn_name, fn_args, block_no, chain, abi=None):
    w3 = get_w3_provider(chain)

    if not abi:
        abi = get_abi(implementation_address)
    contract = w3.eth.contract(address=Web3.toChecksumAddress(interface_address), abi=abi)

    contract_fn = getattr(contract.functions, fn_name)
    res = contract_fn(*fn_args).call(block_identifier=block_no)
    return res

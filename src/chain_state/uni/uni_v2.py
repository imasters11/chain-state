import json
from typing import Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from decimal import Decimal

from chain_state.utils.web3_utils import contract_call_at_block

E18 = Decimal(10 ** 18)


@dataclass_json
@dataclass(frozen=True)
class PoolToken:
    index: int
    address: str
    symbol: str
    decimals: int


@dataclass_json
@dataclass(frozen=True)
class V2LiquiditySnapshot:
    block: Optional[int]
    num_lp_tokens: Decimal
    token0: PoolToken
    num_token0_underlying: Decimal
    token1: PoolToken
    num_token1_underlying: Decimal


def get_pool_token_info(pool_address: str, token_index: int) -> PoolToken:
    assert token_index == 0 or token_index == 1
    fn_name = f"token{token_index}"

    token_address: str = contract_call_at_block(interface_address=pool_address,
                                                implementation_address=pool_address,
                                                fn_name=fn_name,
                                                fn_args=[],
                                                chain='ethereum')

    with open('./token_contract_abi.json') as abi_file:
        abi = json.load(abi_file)

    token_decimals = contract_call_at_block(interface_address=token_address,
                                            implementation_address=token_address,
                                            fn_name='decimals',
                                            fn_args=[],
                                            chain='ethereum',
                                            abi=abi)

    token_symbol = contract_call_at_block(interface_address=token_address,
                                          implementation_address=token_address,
                                          fn_name='symbol',
                                          fn_args=[],
                                          chain='ethereum',
                                          abi=abi)

    return PoolToken(token_index, token_address, token_symbol, int(token_decimals))


def get_underlying_balances_address(pool_address: str, wallet_address: str, block_no: Optional[int] = None) -> V2LiquiditySnapshot:
    wallet_lp_balance_result = contract_call_at_block(interface_address=pool_address,
                                                      implementation_address=pool_address,
                                                      fn_name='balanceOf',
                                                      fn_args=[wallet_address],
                                                      block_no=block_no,
                                                      chain='ethereum')
    wallet_lp_balance = Decimal(wallet_lp_balance_result) / E18

    return get_underlying_balances_lp_tokens(pool_address, wallet_lp_balance, block_no)


def get_underlying_balances_lp_tokens(pool_address: str, wallet_lp_balance: Decimal, block_no: Optional[int]) -> V2LiquiditySnapshot:
    token0 = get_pool_token_info(pool_address, 0)
    token1 = get_pool_token_info(pool_address, 1)

    pool_total_supply_result = contract_call_at_block(interface_address=pool_address,
                                                      implementation_address=pool_address,
                                                      fn_name='totalSupply',
                                                      fn_args=[],
                                                      block_no=block_no,
                                                      chain='ethereum')
    pool_total_supply = Decimal(pool_total_supply_result) / E18

    reserves_result = contract_call_at_block(interface_address=pool_address,
                                             implementation_address=pool_address,
                                             fn_name='getReserves',
                                             fn_args=[],
                                             block_no=block_no,
                                             chain='ethereum')
    token0_reserves = Decimal(reserves_result[0]) / Decimal(10 ** token0.decimals)
    token1_reserves = Decimal(reserves_result[1]) / Decimal(10 ** token1.decimals)

    wallet_share_of_lp = wallet_lp_balance / pool_total_supply
    token0_underlying_lp = token0_reserves * wallet_share_of_lp
    token1_underlying_lp = token1_reserves * wallet_share_of_lp

    return V2LiquiditySnapshot(block_no, wallet_lp_balance, token0, token0_underlying_lp, token1, token1_underlying_lp)


if __name__ == "__main__":
    liquidity_snapshot = get_underlying_balances_address('0x33d39eA02D1A569ECc77FBFcbBDCD4300fA0b010', '0xE05DE631122d95eF347f6fCA85d1bB149Fcc6Df2')
    print(liquidity_snapshot.to_dict())
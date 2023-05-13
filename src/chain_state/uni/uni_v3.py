from dataclasses_json import dataclass_json
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from chain_state.uni.uni_v2 import E18, PoolToken, get_pool_token_info
from chain_state.utils.web3_utils import contract_call_at_block


@dataclass_json
@dataclass(frozen=True)
class V3LiquiditySnapshot:
    block: Optional[int]
    token_id: int
    current_ratio: Decimal
    lower_tick: Decimal
    upper_tick: Decimal
    token0: PoolToken
    num_token0_underlying: Decimal
    token1: PoolToken
    num_token1_underlying: Decimal


def q64_96_to_decimal(q64_96_number: int) -> Decimal:
    return Decimal(q64_96_number) / Decimal(2**96)


def tick_to_price(tick_index: int) -> Decimal:
    return Decimal('1.0001') ** tick_index


def price_outside_below(tick_lower: Decimal, tick_upper: Decimal, liquidity: Decimal) -> Decimal:
    return liquidity * (tick_upper.sqrt() - tick_lower.sqrt()) / (tick_lower.sqrt() * tick_lower.sqrt())


def price_outside_above(tick_lower: Decimal, tick_upper: Decimal, liquidity: Decimal) -> Decimal:
    return liquidity * (tick_upper.sqrt() - tick_lower.sqrt())


def price_inbetween(price: Decimal, tick_lower: Decimal, tick_upper: Decimal, liquidity: Decimal) -> Tuple[Decimal, Decimal]:
    token0_position_virtual = liquidity * (tick_upper.sqrt() - price.sqrt()) / (price.sqrt() * tick_lower.sqrt())
    token1_position_virtual = liquidity * (price.sqrt() - tick_lower.sqrt())
    return token0_position_virtual, token1_position_virtual


def get_underlying_balances(pool_address: str, nft_address: str, nft_impl_address: str, nft_id: int, block_no: Optional[int] = None) -> V3LiquiditySnapshot:
    token0 = get_pool_token_info(pool_address, 0)
    token1 = get_pool_token_info(pool_address, 1)
    decimal_adustment = Decimal(10 ** (token0.decimals - token1.decimals))

    pool_info_result = contract_call_at_block(interface_address=pool_address,
                                              implementation_address=pool_address,
                                              fn_name='slot0',
                                              fn_args=[],
                                              block_no=block_no)

    sqrt_price_x96 = pool_info_result[0]
    price = q64_96_to_decimal(sqrt_price_x96) ** Decimal(2)
    pool_tick = pool_info_result[1]

    positions_info_result = contract_call_at_block(interface_address=nft_address,
                                                   implementation_address=nft_impl_address,
                                                   fn_name='positions',
                                                   fn_args=[nft_id],
                                                   block_no=block_no)

    fee = positions_info_result[4]
    tickLower = positions_info_result[5]
    lower_tick_price = tick_to_price(tickLower)
    tickUpper = positions_info_result[6]
    upper_tick_price = tick_to_price(tickUpper)
    liquidity = positions_info_result[7]

    if price > upper_tick_price:
        token0_position_virtual = Decimal(0)
        token1_position_virtual = price_outside_above(lower_tick_price, upper_tick_price, Decimal(liquidity))
    elif price < lower_tick_price:
        token0_position_virtual = price_outside_below(lower_tick_price, upper_tick_price, Decimal(liquidity))
        token1_position_virtual = Decimal(0)
    else:
        token0_position_virtual, token1_position_virtual = price_inbetween(price, lower_tick_price, upper_tick_price, Decimal(liquidity))

    token0_position = token0_position_virtual / Decimal(10 ** token0.decimals)
    token1_position = token1_position_virtual / Decimal(10 ** token1.decimals)

    snapshot = V3LiquiditySnapshot(block=block_no,
                                   token_id=nft_id,
                                   current_ratio=price * decimal_adustment,
                                   lower_tick=lower_tick_price * decimal_adustment,
                                   upper_tick=upper_tick_price * decimal_adustment,
                                   token0=token0,
                                   num_token0_underlying=token0_position,
                                   token1=token1,
                                   num_token1_underlying=token1_position,
                                   )
    print(snapshot)
    return snapshot


if __name__ == '__main__':
    get_underlying_balances(pool_address='0xc63B0708E2F7e69CB8A1df0e1389A98C35A76D52',
                            nft_address='0xC36442b4a4522E871399CD717aBDD847Ab11FE88',
                            nft_impl_address='0xc36442b4a4522e871399cd717abdd847ab11fe88',
                            nft_id=196378
                            )
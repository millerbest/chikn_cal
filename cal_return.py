"""The function that calculates the returns"""

import pandas as pd
import plotly.express as px
from chicken import Chicken
from egg_stake import EggStake
from feeds import Feeds

RESULT_TEMPLATE = pd.DataFrame(
    columns=[
        "Days",
        "Level",
        "Staked Eggs",
        "Feeds",
        "Egg value [USDT]",
        "Gain/Loss [USDT]",
    ]
)


def get_chicken(base_price: float, level: int):
    return Chicken(base_price=base_price, level=level)


def get_egg_stack(staked_eggs: float = 0):
    return EggStake(staked_eggs=staked_eggs)


def get_feeds(amount: float = 0):
    return Feeds(amount=amount)


def cal_return(
    base_price: float,
    level: int,
    egg_price: float,
    sim_days: int,
    egg_stake: float = 0,
    feeds_amount: float = 0,
):
    chicken = get_chicken(base_price=base_price, level=level)
    egg_stake = get_egg_stack(staked_eggs=egg_stake)
    feeds = get_feeds(amount=feeds_amount)

    results = RESULT_TEMPLATE.copy()
    for num_day in range(sim_days):
        feeds.add_feeds(egg_stake.feeds_per_day)
        if feeds.amount >= chicken.max_feed:
            feeds.use_feeds(chicken.max_feed)
            chicken.feed(chicken.max_feed)

        egg_stake.add_eggs(chicken.egg_per_day)

        results = pd.concat(
            (
                results,
                pd.DataFrame(
                    [
                        [
                            num_day,
                            chicken.level,
                            egg_stake.staked_eggs,
                            feeds.amount,
                            egg_stake.staked_eggs * egg_price * 0.916667,
                            egg_stake.staked_eggs * egg_price * 0.916667 - base_price,
                        ]
                    ],
                    columns=[
                        "Days",
                        "Level",
                        "Staked Eggs",
                        "Feeds",
                        "Egg value [USDT]",
                        "Gain/Loss [USDT]",
                    ],
                ),
            ),
            ignore_index=True,
        )

    return results


def get_plot(results: pd.DataFrame):
    """Plot the figure"""
    fig = px.line(data_frame=results, x="Days", y="Gain/Loss [USDT]")
    return fig

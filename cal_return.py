"""The function that calculates the returns"""

from typing import List
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from chicken import Chicken
from egg_stake import EggStake
from feeds import Feeds
import numpy as np

RESULT_TEMPLATE = pd.DataFrame(
    columns=[
        "Days",
        "Chicken Idx",
        "Level",
        "Staked Eggs",
        "Feeds",
        "Egg value [USDT]",
    ]
)


def get_chickens(base_prices: List[float], levels: List[int]) -> List[Chicken]:
    return [
        Chicken(base_price=base_price, level=level)
        for base_price, level in zip(base_prices, levels)
    ]


def get_egg_stake(staked_eggs: float = 0):
    return EggStake(staked_eggs=staked_eggs)


def get_feeds(amount: float = 0):
    return Feeds(amount=amount)


def get_lowest_level_chicken(list_chicken: List[Chicken]) -> Chicken:
    return min(list_chicken, key=lambda x: x.level)


def cal_return(
    base_prices: List[float],
    levels: List[int],
    egg_price: float,
    sim_days: int,
    init_egg_stake: float = 0,
    feeds_amount: float = 0,
):

    chickens = get_chickens(base_prices=base_prices, levels=levels)
    egg_stake = get_egg_stake(staked_eggs=init_egg_stake)
    feeds = get_feeds(amount=feeds_amount)
    results = RESULT_TEMPLATE.copy()
    for num_day in range(sim_days):
        feeds.add_feeds(egg_stake.feeds_per_day)
        lowest_level_chicken = get_lowest_level_chicken(chickens)
        if feeds.amount >= lowest_level_chicken.max_feed:
            feeds.use_feeds(lowest_level_chicken.max_feed)
            lowest_level_chicken.feed(lowest_level_chicken.max_feed)

        egg_stake.add_eggs(sum(chicken.egg_per_day for chicken in chickens))
        for chicken_idx, chicken in enumerate(chickens):
            results = pd.concat(
                (
                    results,
                    pd.DataFrame(
                        [
                            [
                                num_day,
                                f"chicken #{chicken_idx+1}",
                                chicken.level,
                                egg_stake.staked_eggs,
                                feeds.amount,
                                egg_stake.staked_eggs * egg_price * 0.916667,
                            ]
                        ],
                        columns=[
                            "Days",
                            "Chicken Idx",
                            "Level",
                            "Staked Eggs",
                            "Feeds",
                            "Egg value [USDT]",
                        ],
                    ),
                ),
                ignore_index=True,
            ).astype({"Level": "int32"})
    results = results.pivot_table(
        index=["Days", "Staked Eggs", "Feeds", "Egg value [USDT]"],
        columns="Chicken Idx",
        values="Level",
        dropna=True,  # drop N/A data)
    )
    results = results.reset_index(level=[0, 1, 2, 3])
    results.columns = results.columns.to_list()
    results["Gain/Loss [USDT]"] = (
        results["Staked Eggs"] * egg_price * 0.916667
        - sum(chicken.base_price for chicken in chickens)
    ) - init_egg_stake * egg_price
    results.Days += 1
    results.index += 1
    return results


def plot_formatter(
    x: pd.Series, y: pd.Series, fig: Figure, title: str, xlabel: str, ylabel: str
):
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        xaxis=dict(
            tickmode="linear",
            tick0=0,
            dtick=round(
                (np.max(x) - np.min(x)) / 20,
                -len(str(int((np.max(x) - np.min(x)) / 20))) + 1,
            ),
        ),
        yaxis_title=ylabel,
        yaxis=dict(
            tickmode="linear",
            dtick=round(
                (np.max(y) - np.min(y)) / 10,
                -len(str(int((np.max(y) - np.min(y)) / 10))) + 1,
            ),
        ),
        font=dict(family="Segoe UI, Arial", size=16),
        showlegend=False,
        hovermode="x",
    )
    return fig


def get_gain_loss_plot(results: pd.DataFrame):
    """Plot the gain/loss figure"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=results["Days"],
            y=results["Gain/Loss [USDT]"],
            line={"color": "green"},
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=results["Days"],
            y=results["Gain/Loss [USDT]"].where(results["Gain/Loss [USDT]"] >= 0),
            line={"color": "green"},
            name="Gain",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=results["Days"],
            y=results["Gain/Loss [USDT]"].where(results["Gain/Loss [USDT]"] <= 0),
            line={"color": "red"},
            name="Loss",
        )
    )
    fig = plot_formatter(
        x=results.Days,
        y=results["Gain/Loss [USDT]"],
        fig=fig,
        title="Predicted Gain/Loss",
        xlabel="Days",
        ylabel="Gain/Loss [USDT]",
    )
    return fig


def get_level_plot(results: pd.DataFrame):
    """Plot the level figure"""
    fig = go.Figure()
    for col in results.columns:
        if col.startswith("chicken #"):
            fig.add_trace(
                go.Scatter(
                    x=results["Days"],
                    y=results[col],
                    name=col,
                )
            )
    fig = plot_formatter(
        x=results.Days,
        y=results["chicken #1"],
        fig=fig,
        title="Chicken Level (Weight in KG)",
        xlabel="Days",
        ylabel="Level (Weight in KG)",
    )
    fig.update_layout(showlegend=True)
    return fig


def get_eggs_plot(results: pd.DataFrame):
    """Plot the level figure"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=results["Days"],
            y=results["Staked Eggs"],
            line={"color": "black"},
            name="Staked Eggs",
        )
    )
    fig = plot_formatter(
        x=results.Days,
        y=results["Staked Eggs"],
        fig=fig,
        title="Staked Eggs",
        xlabel="Days",
        ylabel="Staked Eggs",
    )
    return fig


def get_payback_days(results: pd.DataFrame) -> int:
    """Get the number of payback days"""
    try:
        return results.loc[
            [results.loc[results["Gain/Loss [USDT]"] > 0, "Gain/Loss [USDT]"].idxmin()]
        ].Days.to_list()[0]
    except ValueError:
        return -1


if __name__ == "__main__":

    df = cal_return(
        base_prices=[400],
        levels=[1],
        egg_price=5,
        sim_days=100,
        init_egg_stake=0,
        feeds_amount=0,
    )

    print(df)

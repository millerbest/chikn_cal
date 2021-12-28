"""The function that calculates the returns"""

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
        "Level",
        "Staked Eggs",
        "Feeds",
        "Egg value [USDT]",
        "Gain/Loss [USDT]",
    ]
)


def get_chicken(base_price: float, level: int):
    return Chicken(base_price=base_price, level=level)


def get_egg_stake(staked_eggs: float = 0):
    return EggStake(staked_eggs=staked_eggs)


def get_feeds(amount: float = 0):
    return Feeds(amount=amount)


def cal_return(
    base_price: float,
    level: int,
    egg_price: float,
    sim_days: int,
    init_egg_stake: float = 0,
    feeds_amount: float = 0,
):
    chicken = get_chicken(base_price=base_price, level=level)
    egg_stake = get_egg_stake(staked_eggs=init_egg_stake)
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
                            egg_stake.staked_eggs * egg_price * 0.916667
                            - base_price
                            - init_egg_stake * egg_price,
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
    fig.add_trace(
        go.Scatter(
            x=results["Days"], y=results["Level"], line={"color": "black"}, name="Level"
        )
    )
    fig = plot_formatter(
        x=results.Days,
        y=results.Level,
        fig=fig,
        title="Chicken Level (Weight in KG)",
        xlabel="Days",
        ylabel="Level (Weight in KG)",
    )
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
        title="Chicken Level (Weight in KG)",
        xlabel="Days",
        ylabel="Staked Eggs",
    )
    return fig


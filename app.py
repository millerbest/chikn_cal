import streamlit as st
from cal_return import (
    cal_return,
    get_eggs_plot,
    get_gain_loss_plot,
    get_level_plot,
    get_payback_days,
)
from egg_price import get_egg_price

HIDE_STREAMLIT_STYLE = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""


def show_results(
    chicken_price: float,
    level: int,
    egg_price: float,
    invested_eggs: float,
    sim_days: int,
) -> None:

    results = cal_return(
        base_price=chicken_price,
        level=level,
        egg_price=egg_price,
        init_egg_stake=invested_eggs,
        sim_days=sim_days,
    )
    payback_days = get_payback_days(results)
    if payback_days != -1:
        st.markdown(
            f"**Payback in <font color='green'>{payback_days}</font> days**",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"**<font color='red'>Please use larger sim days</font>**",
            unsafe_allow_html=True,
        )
    with st.expander("Gain/Loss"):
        fig_gain_loss = get_gain_loss_plot(results=results)
        st.plotly_chart(fig_gain_loss)

    with st.expander("Levels"):
        fig_levels = get_level_plot(results=results)
        st.plotly_chart(fig_levels)

    with st.expander("Eggs"):
        fig_stacked_eggs = get_eggs_plot(results=results)
        st.plotly_chart(fig_stacked_eggs)

    csv = results.to_csv(index=False)
    st.download_button("Export CSV", csv, "chiken_returns.csv", mime="csv")
    st.dataframe(results, width=1500, height=500)


def main():
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
    st.title("CHIKN Return Calculator")
    level = st.sidebar.number_input("Chicken Level", min_value=1, max_value=100)
    sim_days = st.sidebar.number_input(
        "Sim Days", min_value=1, max_value=1000, value=100
    )
    chicken_price = st.sidebar.number_input(
        "Chicken Price [USDT]", min_value=0.0, step=0.001, format="%.03f", value=400.0
    )
    invested_eggs = st.sidebar.number_input("Initial Invested Eggs", min_value=0)
    egg_price = st.sidebar.number_input(
        "Egg Price [USDT]",
        min_value=0.0,
        step=0.001,
        format="%.03f",
        value=get_egg_price(),
    )

    if st.sidebar.button("Calculate"):
        show_results(
            chicken_price=chicken_price,
            level=level,
            egg_price=egg_price,
            invested_eggs=invested_eggs,
            sim_days=sim_days,
        )


if __name__ == "__main__":
    main()

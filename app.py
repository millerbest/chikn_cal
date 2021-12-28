import streamlit as st
from cal_return import cal_return


def main():
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
        "Egg Price [USDT]", min_value=0.0, step=0.001, format="%.03f", value=3.0
    )
    if st.sidebar.button("Calculate"):
        results = cal_return(
            base_price=chicken_price,
            level=level,
            egg_price=egg_price,
            init_egg_stake=invested_eggs,
            sim_days=sim_days,
        )
        st.write(results, width=1500)


if __name__ == "__main__":
    main()

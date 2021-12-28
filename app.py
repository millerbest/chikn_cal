import streamlit as st
from cal_return import cal_return


def main():
    st.title("CHIKN Return Calculator")
    level = st.sidebar.number_input("Chicken Level", min_value=1, max_value=45)
    sim_days = st.sidebar.number_input("Sim Days", min_value=1, max_value=1000)
    chicken_price = st.sidebar.number_input(
        "Chicken Price [USDT]", min_value=0.0, step=0.001, format="%.03f"
    )
    egg_price = st.sidebar.number_input(
        "Egg Price [USDT]", min_value=0.0, step=0.001, format="%.03f"
    )
    if st.sidebar.button("Calculate"):
        results = cal_return(
            base_price=chicken_price,
            level=level,
            egg_price=egg_price,
            sim_days=sim_days,
        )
        st.write(results)


if __name__ == "__main__":
    main()

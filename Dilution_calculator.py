import streamlit as st

st.title("🧪 Dilution Calculator")

st.write("Calculate dilution using C₁V₁ = C₂V₂")

col1, col2 = st.columns(2)

with col1:
    stock = st.number_input(
        "Stock concentration",
        min_value=0.0,
        value=10.0
    )

    stock_unit = st.selectbox(
        "Stock unit",
        ["M", "mM", "µM", "nM"]
    )

with col2:
    target = st.number_input(
        "Target concentration",
        min_value=0.0,
        value=250.0
    )

    target_unit = st.selectbox(
        "Target unit",
        ["M", "mM", "µM", "nM"]
    )

final_volume = st.number_input(
    "Final volume",
    min_value=0.0,
    value=1000.0
)

volume_unit = st.selectbox(
    "Volume unit",
    ["L", "mL", "µL"]
)


if st.button("Calculate"):

    # Convert target to M
    factors = {
        "M": 1,
        "mM": 1e-3,
        "µM": 1e-6,
        "nM": 1e-9
    }

    stock_M = stock * factors[stock_unit]
    target_M = target * factors[target_unit]

    # Convert final volume to L
    volume_factors = {
        "L": 1,
        "mL": 1e-3,
        "µL": 1e-6
    }

    final_L = final_volume * volume_factors[volume_unit]

    # C1V1 = C2V2
    stock_L = (target_M * final_L) / stock_M

    diluent_L = final_L - stock_L

    # Convert back to user's volume unit
    stock_final = stock_L / volume_factors[volume_unit]
    diluent_final = diluent_L / volume_factors[volume_unit]

    st.success("Calculation complete!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Stock needed",
            f"{stock_final:.2f} {volume_unit}"
        )

    with col2:
        st.metric(
            "Diluent needed",
            f"{diluent_final:.2f} {volume_unit}"
        )

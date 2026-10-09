
import streamlit as st


def show_calculator():

    st.title("🧪 Dilution Calculator")
    st.write("Calculate dilution using C₁V₁ = C₂V₂")

    col1, col2 = st.columns(2)

    with col1:
        stock = st.number_input(
            "Stock concentration",
            min_value=0.0,
            value=10.0,
            format="%.6g"
        )
        stock_unit = st.selectbox(
            "Stock unit", ["M", "mM", "µM", "nM"]
        )

    with col2:
        target = st.number_input(
            "Target concentration",
            min_value=0.0,
            value=250.0,
            format="%.6g"
        )
        target_unit = st.selectbox(
            "Target unit", ["M", "mM", "µM", "nM"]
        )

    final_volume = st.number_input(
        "Final volume",
        min_value=0.0,
        value=1000.0,
        format="%.6g"
    )
    volume_unit = st.selectbox(
        "Volume unit", ["L", "mL", "µL"]
    )

    if st.button("Calculate", type="primary"):
        factors = {
            "M": 1.0,
            "mM": 1e-3,
            "µM": 1e-6,
            "nM": 1e-9
        }
        volume_factors = {
            "L": 1.0,
            "mL": 1e-3,
            "µL": 1e-6
        }

        stock_M = stock * factors[stock_unit]
        target_M = target * factors[target_unit]

        if stock <= 0:
            st.error("Stock concentration must be greater than zero.")
        elif final_volume <= 0:
            st.error("Final volume must be greater than zero.")
        elif target_M <= 0:
            st.error("Target concentration must be greater than zero.")
        elif target_M > stock_M:
            st.error(
                "Target concentration cannot exceed stock concentration "
                "for a simple dilution."
            )
        else:
            final_L = final_volume * volume_factors[volume_unit]
            stock_L = (target_M * final_L) / stock_M
            diluent_L = final_L - stock_L

            stock_needed = stock_L / volume_factors[volume_unit]
            diluent_needed = diluent_L / volume_factors[volume_unit]

            st.success("Calculation complete!")
            col1, col2 = st.columns(2)

            col1.metric(
                "Stock needed",
                f"{stock_needed:.4g} {volume_unit}"
            )
            col2.metric(
                "Diluent needed",
                f"{diluent_needed:.4g} {volume_unit}"
            )

            st.caption(
                "Assumes additive volumes and a simple dilution. "
                "Check units and practical preparation limits before use."
            )

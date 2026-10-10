
import streamlit as st


def show_calculator():
    st.title("Buffer & Reagent Preparation Calculator")
    st.write(
        "Calculate reagent quantities for preparing laboratory "
        "solutions from powders, concentrated stocks, or percentages."
    )

    powder_tab, stock_tab, percent_tab = st.tabs(
        [
            "Prepare from Powder",
            "Dilute Stock Solution",
            "Percentage Solution",
        ]
    )

    # --------------------------------------------------
    # TAB 1: Prepare a solution from powder
    # --------------------------------------------------
    with powder_tab:
        st.subheader("Prepare a solution from powder")
        st.caption(
            "Calculate the mass of solid reagent needed for a "
            "specified final volume and molar concentration."
        )

        col1, col2 = st.columns(2)

        with col1:
            powder_name = st.text_input(
                "Reagent name (optional)",
                value="Tris base",
                key="powder_name",
            )
            molecular_weight = st.number_input(
                "Molecular weight (g/mol)",
                min_value=0.000001,
                value=121.14,
                format="%.5f",
                key="powder_mw",
            )

        with col2:
            target_molarity = st.number_input(
                "Target concentration",
                min_value=0.000001,
                value=1.0,
                format="%.6f",
                key="powder_conc",
            )
            molarity_unit = st.selectbox(
                "Concentration unit",
                ["M", "mM", "µM"],
                key="powder_unit",
            )

        final_volume = st.number_input(
            "Desired final solution volume",
            min_value=0.001,
            value=500.0,
            key="powder_volume",
        )
        volume_unit = st.selectbox(
            "Volume unit",
            ["mL", "L", "µL"],
            key="powder_volume_unit",
        )

        if st.button("Calculate powder required", key="powder_btn"):
            concentration_factors = {
                "M": 1,
                "mM": 1e-3,
                "µM": 1e-6,
            }
            volume_factors = {
                "L": 1,
                "mL": 1e-3,
                "µL": 1e-6,
            }

            concentration_M = (
                target_molarity * concentration_factors[molarity_unit]
            )
            volume_L = final_volume * volume_factors[volume_unit]

            mass_g = molecular_weight * concentration_M * volume_L
            mass_mg = mass_g * 1000

            st.success(
                f"Weigh {mass_g:.6g} g ({mass_mg:.6g} mg) "
                f"of {powder_name or 'reagent'}."
            )
            st.info(
                f"Dissolve in less than {final_volume:g} {volume_unit} "
                f"of solvent, then adjust to a final volume of "
                f"{final_volume:g} {volume_unit}."
            )

    # --------------------------------------------------
    # TAB 2: Dilute a stock solution
    # --------------------------------------------------
    with stock_tab:
        st.subheader("Dilute a stock solution")
        st.caption(
            "Calculate the stock and diluent volumes using C1V1 = C2V2. "
            "Stock and target concentrations must use the same units."
        )

        col1, col2 = st.columns(2)

        with col1:
            stock_conc = st.number_input(
                "Stock concentration",
                min_value=0.000001,
                value=10.0,
                key="stock_conc",
            )
            target_conc = st.number_input(
                "Desired final concentration",
                min_value=0.000001,
                value=1.0,
                key="target_conc",
            )

        with col2:
            stock_unit = st.selectbox(
                "Concentration unit",
                ["M", "mM", "µM", "nM", "%"],
                key="stock_unit",
            )
            stock_final_volume = st.number_input(
                "Desired final volume",
                min_value=0.001,
                value=100.0,
                key="stock_final_volume",
            )

        stock_volume_unit = st.selectbox(
            "Volume unit",
            ["mL", "L", "µL"],
            key="stock_volume_unit",
        )

        if st.button("Calculate stock dilution", key="stock_btn"):
            if target_conc > stock_conc:
                st.error(
                    "The target concentration cannot exceed the stock "
                    "concentration for a simple dilution."
                )
            else:
                stock_volume = (
                    target_conc / stock_conc
                ) * stock_final_volume
                diluent_volume = stock_final_volume - stock_volume

                st.success(
                    f"Use {stock_volume:.6g} {stock_volume_unit} "
                    f"of stock solution."
                )
                st.info(
                    f"Add diluent to reach a final volume of "
                    f"{stock_final_volume:g} {stock_volume_unit}. "
                    f"The nominal diluent volume is "
                    f"{diluent_volume:.6g} {stock_volume_unit}."
                )

    # --------------------------------------------------
    # TAB 3: Percentage solutions
    # --------------------------------------------------
    with percent_tab:
        st.subheader("Prepare a percentage solution")
        st.caption(
            "% w/v = grams per 100 mL final solution. "
            "% v/v = mL per 100 mL final solution."
        )

        percentage_type = st.selectbox(
            "Solution type",
            ["% w/v (solid in liquid)", "% v/v (liquid in liquid)"],
            key="percentage_type",
        )

        percentage = st.number_input(
            "Target percentage (%)",
            min_value=0.000001,
            value=5.0,
            key="percentage",
        )

        percent_final_volume = st.number_input(
            "Desired final solution volume",
            min_value=0.001,
            value=100.0,
            key="percent_final_volume",
        )

        percent_volume_unit = st.selectbox(
            "Volume unit",
            ["mL", "L", "µL"],
            key="percent_volume_unit",
        )

        if st.button(
            "Calculate percentage solution",
            key="percentage_btn",
        ):
            volume_to_mL = {
                "mL": 1,
                "L": 1000,
                "µL": 0.001,
            }

            final_mL = (
                percent_final_volume
                * volume_to_mL[percent_volume_unit]
            )

            amount = percentage / 100 * final_mL

            if percentage_type == "% w/v (solid in liquid)":
                st.success(
                    f"Weigh {amount:.6g} g of solid reagent."
                )
                st.info(
                    f"Dissolve the reagent and bring the solution "
                    f"to a final volume of "
                    f"{percent_final_volume:g} {percent_volume_unit}."
                )
            else:
                st.success(
                    f"Measure {amount:.6g} mL of liquid reagent."
                )
                st.info(
                    f"Add solvent and bring the solution to a final "
                    f"volume of {final_mL:.6g} mL."
                )

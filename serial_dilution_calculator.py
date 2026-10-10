
import streamlit as st


def show_calculator():
    st.title("Serial Dilution Calculator")
    st.write(
        "Calculate sample transfer volumes, diluent volumes, "
        "and concentrations for a serial dilution series."
    )

    st.subheader("Starting conditions")

    col1, col2 = st.columns(2)

    with col1:
        initial_concentration = st.number_input(
            "Starting concentration",
            min_value=0.000001,
            value=1000.0,
            format="%.6f",
        )

        concentration_unit = st.selectbox(
            "Concentration unit",
            ["µM", "nM", "mM", "M", "mg/mL", "µg/mL", "ng/mL", "AU/mL"],
        )

    with col2:
        dilution_factor = st.number_input(
            "Dilution factor per step (e.g., 10 for 1:10)",
            min_value=1.01,
            value=10.0,
            step=1.0,
        )

        number_of_steps = st.number_input(
            "Number of dilution tubes",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
        )

    st.subheader("Tube preparation")

    col3, col4 = st.columns(2)

    with col3:
        final_volume = st.number_input(
            "Desired final volume per tube",
            min_value=0.001,
            value=1000.0,
            step=100.0,
        )

    with col4:
        volume_unit = st.selectbox(
            "Volume unit",
            ["µL", "mL"],
        )

    # Calculate volumes for the selected final volume.
    transfer_volume = final_volume / dilution_factor
    diluent_volume = final_volume - transfer_volume

    st.info(
        f"For each {dilution_factor:g}-fold dilution, transfer "
        f"{transfer_volume:g} {volume_unit} of sample and add "
        f"{diluent_volume:g} {volume_unit} of diluent."
    )

    if st.button("Calculate serial dilution", type="primary"):
        results = []

        for step in range(1, int(number_of_steps) + 1):
            concentration = (
                initial_concentration / dilution_factor**step
            )

            results.append(
                {
                    "Tube": f"Tube {step}",
                    "Sample source": (
                        "Starting stock" if step == 1
                        else f"Tube {step - 1}"
                    ),
                    "Sample to transfer": round(transfer_volume, 6),
                    "Diluent to add": round(diluent_volume, 6),
                    "Final volume": round(final_volume, 6),
                    "Relative dilution": f"1:{dilution_factor**step:g}",
                    f"Concentration ({concentration_unit})": concentration,
                }
            )

        st.subheader("Serial dilution results")

        st.caption(
            "Volumes are calculated assuming each tube is prepared "
            "to the specified final volume before transferring sample "
            "to the next tube."
        )

        st.dataframe(results, use_container_width=True, hide_index=True)

        final_concentration = (
            initial_concentration / dilution_factor**int(number_of_steps)
        )

        st.metric(
            "Final tube concentration",
            f"{final_concentration:.6g} {concentration_unit}",
        )

        csv_data = __import__("pandas").DataFrame(results).to_csv(
            index=False
        )

        st.download_button(
            "Download results as CSV",
            data=csv_data,
            file_name="serial_dilution_results.csv",
            mime="text/csv",
        )


import streamlit as st

st.set_page_config(
    page_title="Bio Lab Tools",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Bio Lab Tools")
st.write(
    "A collection of calculators for molecular biology, "
    "biochemistry, and protein science."
)

st.sidebar.title("🧪 Lab Calculators")

calculator = st.sidebar.selectbox(
    "Choose a calculator",
    [
        "Home",
        "Dilution Calculator",
        "Molarity Calculator",
        "Protein Concentration Calculator",
        "Serial Dilution Calculator",
        "ELISA Plate Planner",
        "Buffer & Reagent Preparation Calculator"
    ]
)

if calculator == "Home":
    st.subheader("Welcome to Bio Lab Tools!")
    st.write("Choose a calculator from the sidebar to get started.")

    st.markdown("### Available and planned tools")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🧪 Dilution Calculator")
        st.write("Calculate stock and diluent volumes using C₁V₁ = C₂V₂.")

        st.markdown("#### ⚗️ Molarity Calculator")
        st.write("Calculate molar concentration from mass and volume.")

    with col2:
        st.markdown("#### 🧬 Protein Concentration")
        st.write("Estimate protein concentration from absorbance.")

        st.markdown("#### 🧫 ELISA Plate Planner")
        st.write("Plan sample and control positions on a plate.")

elif calculator == "Dilution Calculator":
    from Dilution_calculator import show_calculator

    show_calculator()

elif calculator == "Molarity Calculator":
    st.subheader("⚗️ Molarity Calculator")
    st.info("This calculator is planned for a future update.")

elif calculator == "Protein Concentration Calculator":
    from protein_concentration_calculator import show_calculator

    show_calculator()

elif calculator == "Serial Dilution Calculator":
    from serial_dilution_calculator import show_calculator

    show_calculator()


elif calculator == "Buffer & Reagent Preparation Calculator":
    from buffer_reagent_calculator import show_calculator

    show_calculator()


elif calculator == "ELISA Plate Planner":
    st.subheader("🧫 ELISA Plate Planner")
    st.info("This tool is planned for a future update.")


import streamlit as st
from Bio.SeqUtils.ProtParam import ProteinAnalysis


def show_calculator():
    st.title("🧬 Protein Analysis & Concentration Calculator")

    st.write(
        "Calculate molecular weight and extinction coefficient from "
        "a protein sequence, then estimate protein concentration "
        "from measured absorbance at 280 nm."
    )

    st.subheader("1. Protein sequence")

    sequence_input = st.text_area(
        "Paste amino acid sequence",
        height=150,
        placeholder=(
            ">MyProtein\n"
            "MKWVTFISLLLLFSSAYS..."
        ),
        help="One-letter amino acid sequence; FASTA headers are accepted.",
        key="protein_sequence_input"
    )

    if not sequence_input.strip():
        st.info("Paste a protein sequence to begin.")
        return

    # Accept FASTA or plain sequence, and remove whitespace.
    sequence_lines = [
        line.strip()
        for line in sequence_input.splitlines()
        if line.strip() and not line.strip().startswith(">")
    ]
    sequence = "".join(sequence_lines).upper()

    # Standard amino acids supported by this calculator.
    valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
    invalid = sorted(set(sequence) - valid_amino_acids)

    if not sequence:
        st.warning("Please enter an amino acid sequence.")
        return

    if invalid:
        st.error(
            "Unsupported character(s) found: "
            + ", ".join(invalid)
            + ". Use the 20 standard amino acid letters. "
            "Remove gaps, stop symbols, and ambiguous residues."
        )
        return

    # Calculate sequence properties.
    protein = ProteinAnalysis(sequence)
    molecular_weight = protein.molecular_weight()

    # Biopython returns:
    # (extinction coefficient with reduced cysteines,
    #  extinction coefficient with cysteines paired as disulfides)

    # Calculate extinction coefficients at 280 nm
    tyrosine = sequence.count("Y")
    tryptophan = sequence.count("W")
    cysteine = sequence.count("C")

    extinction_reduced = (
        5500 * tryptophan
        + 1490 * tyrosine
    )

    extinction_oxidized = (
        extinction_reduced
        + 125 * (cysteine // 2)
    )

    st.subheader("2. Calculated protein properties")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Sequence length", f"{len(sequence)} aa")
        st.metric("Molecular weight", f"{molecular_weight:,.2f} Da")

    with col2:
        st.metric(
            "Extinction coefficient — reduced",
            f"{extinction_reduced:,.0f} M⁻¹ cm⁻¹"
        )
        st.metric(
            "Extinction coefficient — disulfide-bonded",
            f"{extinction_oxidized:,.0f} M⁻¹ cm⁻¹"
        )

    st.caption(
        "Molecular weight is calculated from the unmodified sequence. "
        "Extinction coefficients are theoretical estimates at 280 nm."
    )

    st.subheader("3. Experimental absorbance")

    epsilon_choice = st.radio(
        "Which extinction coefficient should be used?",
        [
            "Reduced cysteines",
            "Disulfide-bonded cysteines"
        ],
        help=(
            "Choose based on the expected cysteine/disulfide state "
            "of your measured protein."
        ),
        key="protein_epsilon_choice"
    )

    epsilon = (
        extinction_reduced
        if epsilon_choice == "Reduced cysteines"
        else extinction_oxidized
    )

    col1, col2 = st.columns(2)

    with col1:
        absorbance = st.number_input(
            "Blank-corrected A280",
            min_value=0.0,
            value=0.500,
            format="%.6f",
            key="protein_absorbance"
        )

        path_length = st.number_input(
            "Optical path length (cm)",
            min_value=0.0,
            value=1.0,
            format="%.4f",
            key="protein_path_length"
        )

    with col2:
        dilution_factor = st.number_input(
            "Dilution factor",
            min_value=1.0,
            value=1.0,
            step=1.0,
            format="%.4g",
            help="For a 1:10 dilution, enter 10.",
            key="protein_dilution_factor"
        )

    if st.button("Calculate concentration", type="primary"):
        if path_length <= 0:
            st.error("Path length must be greater than zero.")
        elif epsilon <= 0:
            st.error(
                "The selected extinction coefficient is zero. "
                "A280 cannot quantify this sequence using this method."
            )
        else:
            # Beer–Lambert law: A = epsilon * c * path length
            measured_M = absorbance / (epsilon * path_length)

            # Correct for dilution to recover the original sample.
            original_M = measured_M * dilution_factor

            concentration_uM = original_M * 1e6
            concentration_nM = original_M * 1e9

            # M * g/mol = g/L; numerically, g/L = mg/mL.
            concentration_mg_mL = original_M * molecular_weight

            st.subheader("4. Protein concentration results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Molar concentration",
                f"{concentration_uM:.4g} µM"
            )

            col2.metric(
                "Mass concentration",
                f"{concentration_mg_mL:.4g} mg/mL"
            )

            col3.metric(
                "Molar concentration",
                f"{concentration_nM:.4g} nM"
            )

            st.caption(
                "Concentration refers to the original, undiluted sample. "
                "Assumes a valid blank-corrected absorbance, path length, "
                "and extinction coefficient. Protein mixtures, "
                "contaminants, and modifications may affect accuracy."
            )

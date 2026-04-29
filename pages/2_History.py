import streamlit as st
from src.db import init_db
from src.services import get_formulations_with_ingredient_count, get_formulation_by_id
from src.calculations import calculate_formulation_parameters

init_db()

st.title("History")

df = get_formulations_with_ingredient_count()

if df.empty:
    st.info("No formulations found.")
else:
    st.subheader("Saved Formulations")
    st.dataframe(df, use_container_width=True)

    formulation_ids = df["id"].tolist()
    selected_id = st.selectbox("Select a formulation to inspect", formulation_ids)

    formulation, ingredients = get_formulation_by_id(selected_id)

    if formulation is not None:
        st.subheader("Formulation Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Project Name:** {formulation['project_name']}")
            st.write(f"**Product Type:** {formulation['product_type']}")
            st.write(f"**Version:** {formulation['version']}")
            st.write(f"**Author:** {formulation['author']}")
            st.write(f"**Notes:** {formulation['notes']}")

        with col2:
            st.write(f"**Created At:** {formulation['created_at']}")

    if ingredients is not None and not ingredients.empty:
        params = calculate_formulation_parameters(ingredients)

        st.subheader("Calculated Parameters")
        calc_col1, calc_col2 = st.columns(2)

        with calc_col1:
            st.metric("Total Amount (g)", params["total_amount_g"])
            st.metric("Resin Solids (g)", params["resin_solids_g"])
            st.metric("Total Solids (g)", params["total_solids_g"])
            st.metric("Total Solids (%)", params["total_solids_pct"])

        with calc_col2:
            st.metric("Pigment Amount (g)", params["pigment_amount_g"])
            st.metric("Resin Amount (g)", params["resin_amount_g"])
            st.metric(
                "Pigment/Resin Ratio",
                params["pigment_resin_ratio"] if params["pigment_resin_ratio"] is not None else "N/A"
            )
            st.metric("PVC", "Pending densities")

        st.subheader("Measured Parameters")
        meas_col1, meas_col2 = st.columns(2)

        with meas_col1:
            st.metric("Measured Viscosity", formulation.get("measured_viscosity", 0))
            st.metric("Measured pH", formulation.get("measured_ph", 0))

        with meas_col2:
            st.metric("Measured Density", formulation.get("measured_density", 0))
            st.metric("Measured Solids (%)", formulation.get("measured_solids", 0))

        st.subheader("Ingredients")

        display_df = ingredients.copy()
        display_df = display_df[[
            "category",
            "material_name",
            "amount",
            "unit",
            "solids_pct",
            "solids_g",
            "percentage"
        ]]

        display_df = display_df.rename(columns={
            "amount": "amount_g",
            "solids_pct": "resin_solids_pct",
            "percentage": "percentage_of_total"
        })

        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No ingredients found for this formulation.")
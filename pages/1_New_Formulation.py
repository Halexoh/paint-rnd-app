import streamlit as st
from src.db import init_db
from src.models import Formulation, Ingredient
from src.services import create_formulation

init_db()

st.title("New Formulation")

CATEGORY_CONFIG = {
    "Resin": 5,
    "Pigment": 5,
    "Solvent": 5,
    "Additive": 5
}


def collect_ingredients():
    ingredients = []

    for category, max_items in CATEGORY_CONFIG.items():
        st.subheader(f"{category}s")

        for position in range(1, max_items + 1):
            if category == "Resin":
                col1, col2, col3, col4 = st.columns([3, 1.2, 1, 1.2])

                with col1:
                    material_name = st.text_input(
                        f"{category} {position} - Material",
                        key=f"{category.lower()}_{position}_material"
                    )

                with col2:
                    amount = st.number_input(
                        f"{category} {position} - Amount (g)",
                        min_value=0.0,
                        format="%.3f",
                        key=f"{category.lower()}_{position}_amount"
                    )

                with col3:
                    unit = st.text_input(
                        f"{category} {position} - Unit",
                        value="g",
                        key=f"{category.lower()}_{position}_unit"
                    )

                with col4:
                    solids_pct = st.number_input(
                        f"{category} {position} - Resin Solids %",
                        min_value=0.0,
                        max_value=100.0,
                        format="%.2f",
                        key=f"{category.lower()}_{position}_solids"
                    )

            else:
                col1, col2, col3 = st.columns([3, 1.2, 1])

                with col1:
                    material_name = st.text_input(
                        f"{category} {position} - Material",
                        key=f"{category.lower()}_{position}_material"
                    )

                with col2:
                    amount = st.number_input(
                        f"{category} {position} - Amount (g)",
                        min_value=0.0,
                        format="%.3f",
                        key=f"{category.lower()}_{position}_amount"
                    )

                with col3:
                    unit = st.text_input(
                        f"{category} {position} - Unit",
                        value="g",
                        key=f"{category.lower()}_{position}_unit"
                    )

                solids_pct = None

            if material_name.strip():
                ingredients.append(
                    Ingredient(
                        category=category,
                        material_name=material_name.strip(),
                        amount=amount,
                        unit="g",
                        position=position,
                        solids_pct=solids_pct
                    )
                )

    return ingredients


with st.form("new_formulation_form"):
    st.subheader("General Information")

    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name")
        product_type = st.selectbox(
            "Product Type",
            ["Architectural", "Industrial", "Wood Coating", "Primer", "Other"]
        )
        version = st.text_input("Version", value="v1")
        author = st.text_input("Author")

    with col2:
        measured_viscosity = st.number_input(
            "Measured Viscosity",
            min_value=0.0,
            format="%.2f"
        )
        measured_ph = st.number_input(
            "Measured pH",
            min_value=0.0,
            max_value=14.0,
            format="%.2f"
        )
        measured_solids = st.number_input(
            "Measured Solids (%)",
            min_value=0.0,
            max_value=100.0,
            format="%.2f"
        )
        measured_density = st.number_input(
            "Measured Density",
            min_value=0.0,
            format="%.2f"
        )

    notes = st.text_area("Notes")

    st.divider()
    st.subheader("Ingredients")

    ingredients = collect_ingredients()

    # ---- Calculations / validations preview ----
    total_amount = sum(
        ingredient.amount for ingredient in ingredients
        if ingredient.amount is not None
    )

    resin_amount = sum(
        ingredient.amount for ingredient in ingredients
        if ingredient.category == "Resin" and ingredient.amount is not None
    )

    pigment_amount = sum(
        ingredient.amount for ingredient in ingredients
        if ingredient.category == "Pigment" and ingredient.amount is not None
    )

    st.divider()
    st.subheader("Formulation Preview")

    met1, met2, met3 = st.columns(3)

    with met1:
        st.metric("Total Batch (g)", f"{total_amount:.2f}")

    with met2:
        st.metric("Total Resin (g)", f"{resin_amount:.2f}")

    with met3:
        st.metric("Total Pigment (g)", f"{pigment_amount:.2f}")

    zero_solids_resins = [
        ingredient.material_name
        for ingredient in ingredients
        if ingredient.category == "Resin"
        and ingredient.material_name.strip()
        and (ingredient.solids_pct is None or ingredient.solids_pct == 0)
    ]

    if total_amount == 0:
        st.warning("Total formulation amount is currently 0 g.")

    elif total_amount < 100:
        st.info(
            "Total batch is below 100 g. That may be fine for lab scale, "
            "but verify that it matches your intended batch size."
        )

    if zero_solids_resins:
        resin_names = ", ".join(zero_solids_resins)
        st.warning(
            f"The following resins have 0% solids assigned: {resin_names}. "
            "Please verify before saving."
        )

    submitted = st.form_submit_button("Save Formulation")

    if submitted:
        if not project_name.strip():
            st.error("Project Name is required.")

        elif not version.strip():
            st.error("Version is required.")

        elif len(ingredients) == 0:
            st.error("At least one ingredient must be added.")

        elif total_amount <= 0:
            st.error("Total formulation amount must be greater than 0 g.")

        else:
            formulation = Formulation(
                project_name=project_name.strip(),
                product_type=product_type,
                version=version.strip(),
                author=author.strip(),
                notes=notes.strip(),
                measured_viscosity=measured_viscosity,
                measured_ph=measured_ph,
                measured_density=measured_density,
                measured_solids=measured_solids,
                ingredients=ingredients
            )

            new_id = create_formulation(formulation)
            st.success(f"Formulation saved successfully. ID: {new_id}")
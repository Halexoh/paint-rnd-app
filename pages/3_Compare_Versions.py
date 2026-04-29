import streamlit as st
from src.db import init_db
from src.services import get_all_formulations, get_formulation_by_id
from src.compare import compare_metadata, compare_ingredients

init_db()

st.title("Compare Versions")

df = get_all_formulations()

if df.empty or len(df) < 2:
    st.info("At least two formulations are required for comparison.")
else:
    options = df.apply(
        lambda row: f"{row['id']} | {row['project_name']} | {row['version']} | {row['created_at']}",
        axis=1
    ).tolist()

    col1, col2 = st.columns(2)

    with col1:
        selected_a = st.selectbox("Select version A", options, key="a")

    with col2:
        selected_b = st.selectbox("Select version B", options, key="b")

    if st.button("Compare"):
        id_a = int(selected_a.split("|")[0].strip())
        id_b = int(selected_b.split("|")[0].strip())

        formula_a, ingredients_a = get_formulation_by_id(id_a)
        formula_b, ingredients_b = get_formulation_by_id(id_b)

        metadata_diff = compare_metadata(formula_a, formula_b)
        ingredient_diff = compare_ingredients(ingredients_a, ingredients_b)

        st.subheader("Metadata Changes")
        if metadata_diff.empty:
            st.success("No metadata differences found.")
        else:
            st.dataframe(metadata_diff, use_container_width=True)

        st.subheader("Ingredient Changes")
        if ingredient_diff.empty:
            st.success("No ingredient differences found.")
        else:
            st.dataframe(ingredient_diff, use_container_width=True)
import pandas as pd


def compare_metadata(formula_a: dict, formula_b: dict):
    ignored_fields = {"id", "created_at"}
    differences = []

    keys = set(formula_a.keys()).union(set(formula_b.keys()))

    for key in keys:
        if key in ignored_fields:
            continue
        value_a = formula_a.get(key)
        value_b = formula_b.get(key)
        if value_a != value_b:
            differences.append({
                "field": key,
                "version_a": value_a,
                "version_b": value_b
            })

    return pd.DataFrame(differences)


def compare_ingredients(ingredients_a: pd.DataFrame, ingredients_b: pd.DataFrame):
    if ingredients_a is None:
        ingredients_a = pd.DataFrame()
    if ingredients_b is None:
        ingredients_b = pd.DataFrame()

    cols = ["category", "material_name", "amount", "unit", "solids_pct"]

    for col in cols:
        if col not in ingredients_a.columns:
            ingredients_a[col] = None
        if col not in ingredients_b.columns:
            ingredients_b[col] = None

    # Comparar por material_name en lugar de position
    merged = ingredients_a[cols].merge(
        ingredients_b[cols],
        on=["category", "material_name"],
        how="outer",
        suffixes=("_a", "_b")
    )

    differences = []

    for _, row in merged.iterrows():
        amount_a = row.get("amount_a")
        amount_b = row.get("amount_b")
        unit_a = row.get("unit_a")
        unit_b = row.get("unit_b")
        solids_a = row.get("solids_pct_a")
        solids_b = row.get("solids_pct_b")

        # Ingrediente solo en A
        if pd.isna(amount_b) and pd.notna(amount_a):
            status = "Removed in B"
        # Ingrediente solo en B
        elif pd.isna(amount_a) and pd.notna(amount_b):
            status = "Added in B"
        # Ingrediente en ambos pero con diferencias
        elif amount_a != amount_b or unit_a != unit_b or solids_a != solids_b:
            status = "Modified"
        else:
            continue

        differences.append({
            "status": status,
            "category": row["category"],
            "material_name": row["material_name"],
            "amount_a": amount_a,
            "unit_a": unit_a,
            "solids_pct_a": solids_a,
            "amount_b": amount_b,
            "unit_b": unit_b,
            "solids_pct_b": solids_b,
        })

    return pd.DataFrame(differences)

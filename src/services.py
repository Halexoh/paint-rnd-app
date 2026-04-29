import pandas as pd
from src.db import get_connection
from src.models import Formulation


def create_formulation(formulation: Formulation):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO formulations (
        project_name, product_type, version, author, notes,
        measured_viscosity, measured_ph, measured_density, measured_solids
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        formulation.project_name,
        formulation.product_type,
        formulation.version,
        formulation.author,
        formulation.notes,
        formulation.measured_viscosity,
        formulation.measured_ph,
        formulation.measured_density,
        formulation.measured_solids
    ))

    formulation_id = cursor.lastrowid

    for ingredient in formulation.ingredients:
        cursor.execute("""
        INSERT INTO ingredients (
            formulation_id, category, material_name, amount, unit, position, solids_pct
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            formulation_id,
            ingredient.category,
            ingredient.material_name,
            ingredient.amount,
            "g",
            ingredient.position,
            ingredient.solids_pct
        ))

    conn.commit()
    conn.close()
    return formulation_id


def get_all_formulations():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM formulations ORDER BY created_at DESC",
        conn
    )
    conn.close()
    return df


def get_formulation_by_id(formulation_id: int):
    conn = get_connection()

    formulation_df = pd.read_sql_query(
        "SELECT * FROM formulations WHERE id = ?",
        conn,
        params=(formulation_id,)
    )

    ingredients_df = pd.read_sql_query(
        """
        SELECT * FROM ingredients
        WHERE formulation_id = ?
        ORDER BY category, position
        """,
        conn,
        params=(formulation_id,)
    )

    conn.close()

    if formulation_df.empty:
        return None, None

    if not ingredients_df.empty:
        total_amount = ingredients_df["amount"].fillna(0).sum()

        if total_amount > 0:
            ingredients_df["percentage"] = (
                ingredients_df["amount"].fillna(0) / total_amount * 100
            ).round(2)
        else:
            ingredients_df["percentage"] = 0.0

        ingredients_df["solids_pct"] = ingredients_df["solids_pct"].fillna(0)
        ingredients_df["solids_g"] = (
            ingredients_df["amount"].fillna(0) * ingredients_df["solids_pct"] / 100
        ).round(2)

    return formulation_df.iloc[0].to_dict(), ingredients_df


def get_formulations_with_ingredient_count():
    conn = get_connection()
    df = pd.read_sql_query(
        """
        SELECT
            f.*,
            COUNT(i.id) AS ingredient_count
        FROM formulations f
        LEFT JOIN ingredients i ON f.id = i.formulation_id
        GROUP BY f.id
        ORDER BY f.created_at DESC
        """,
        conn
    )
    conn.close()
    return df
import pandas as pd


def calculate_formulation_parameters(ingredients_df: pd.DataFrame) -> dict:
    if ingredients_df is None or ingredients_df.empty:
        return {
            "total_amount_g": 0.0,
            "total_solids_g": 0.0,
            "total_solids_pct": 0.0,
            "resin_solids_g": 0.0,
            "pigment_amount_g": 0.0,
            "resin_amount_g": 0.0,
            "pigment_resin_ratio": None,
            "pvc": None,
        }

    df = ingredients_df.copy()
    df["amount"] = df["amount"].fillna(0.0)
    df["solids_pct"] = df["solids_pct"].fillna(0.0)
    df["density"] = df["density"].fillna(0.0) if "density" in df.columns else 0.0

    total_amount_g = df["amount"].sum()

    resin_df = df[df["category"] == "Resin"].copy()
    pigment_df = df[df["category"] == "Pigment"].copy()

    resin_amount_g = resin_df["amount"].sum()
    pigment_amount_g = pigment_df["amount"].sum()

    # Solidos de resina
    resin_df["resin_solids_g"] = resin_df["amount"] * resin_df["solids_pct"] / 100
    resin_solids_g = resin_df["resin_solids_g"].sum()

    # Solidos de pigmento (pigmentos son 100% solidos por defecto)
    pigment_df["pigment_solids_g"] = pigment_df["amount"] * pigment_df["solids_pct"].replace(0, 100) / 100
    pigment_solids_g = pigment_df["pigment_solids_g"].sum()

    total_solids_g = resin_solids_g + pigment_solids_g

    total_solids_pct = 0.0
    if total_amount_g > 0:
        total_solids_pct = total_solids_g / total_amount_g * 100

    pigment_resin_ratio = None
    if resin_amount_g > 0:
        pigment_resin_ratio = pigment_amount_g / resin_amount_g

    # PVC = Vol_pigmento / (Vol_pigmento + Vol_aglutinante)
    # Requiere densidades — se calcula si estan disponibles
    pvc = None
    if "density" in df.columns:
        pigment_df_d = df[df["category"] == "Pigment"].copy()
        resin_df_d = df[df["category"] == "Resin"].copy()

        pigment_df_d["volume"] = pigment_df_d.apply(
            lambda r: r["amount"] / r["density"] if r["density"] > 0 else 0, axis=1
        )
        resin_df_d["volume"] = resin_df_d.apply(
            lambda r: (r["amount"] * r["solids_pct"] / 100) / r["density"] if r["density"] > 0 else 0, axis=1
        )

        vol_pigment = pigment_df_d["volume"].sum()
        vol_binder = resin_df_d["volume"].sum()

        if (vol_pigment + vol_binder) > 0:
            pvc = round(vol_pigment / (vol_pigment + vol_binder) * 100, 2)

    return {
        "total_amount_g": round(total_amount_g, 2),
        "total_solids_g": round(total_solids_g, 2),
        "total_solids_pct": round(total_solids_pct, 2),
        "resin_solids_g": round(resin_solids_g, 2),
        "pigment_solids_g": round(pigment_solids_g, 2),
        "pigment_amount_g": round(pigment_amount_g, 2),
        "resin_amount_g": round(resin_amount_g, 2),
        "pigment_resin_ratio": round(pigment_resin_ratio, 4) if pigment_resin_ratio is not None else None,
        "pvc": pvc,
    }

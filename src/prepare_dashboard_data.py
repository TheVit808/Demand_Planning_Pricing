from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "sample"
DASH_DIR = ROOT / "data" / "dashboard"
REPORT_DIR = ROOT / "reports"

FACT_PATH = DATA_DIR / "fact_demand_pricing_daily.parquet"
PRED_PATH = REPORT_DIR / "trilha_b" / "predictions_test.parquet"
PRODUCT_METRICS_PATH = REPORT_DIR / "trilha_b" / "metrics_by_product.csv"
REGION_METRICS_PATH = REPORT_DIR / "trilha_b" / "metrics_by_region.csv"
EXPERIMENTS_PATH = REPORT_DIR / "trilha_b" / "experiments.csv"
PRICING_PATH = REPORT_DIR / "trilha_c" / "pricing_scenarios_summary.csv"
PRICING_PRODUCT_PATH = REPORT_DIR / "trilha_c" / "pricing_scenarios_by_product.csv"


def read_optional(path: Path, **kwargs):
    if not path.exists():
        return None
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, **kwargs)


def wape(actual, predicted):
    denominator = np.abs(actual).sum()
    if denominator == 0:
        return np.nan
    return np.abs(actual - predicted).sum() / denominator


def main():
    DASH_DIR.mkdir(parents=True, exist_ok=True)

    fact = pd.read_parquet(FACT_PATH)
    fact["date"] = pd.to_datetime(fact["date"])
    fact = fact.sort_values(["date", "product_id", "region_id"])

    # Seleciona o modelo final da Trilha B quando a tabela de experimentos existir.
    experiments = read_optional(EXPERIMENTS_PATH)
    selected_model = "Não informado"
    if experiments is not None and not experiments.empty:
        validation = experiments[
            experiments["split"].astype(str).str.lower().eq("validation")
        ].copy()
        if not validation.empty and "wape" in validation.columns:
            validation["wape"] = pd.to_numeric(validation["wape"], errors="coerce")
            validation = validation.dropna(subset=["wape"])
            if not validation.empty:
                selected_model = validation.sort_values("wape").iloc[0]["model"]

    predictions = read_optional(PRED_PATH, parse_dates=["date"])
    if predictions is not None and not predictions.empty:
        predictions["date"] = pd.to_datetime(predictions["date"])
        rename_map = {}
        if "prediction_rf" in predictions.columns:
            rename_map["prediction_rf"] = "prediction"
        if "predicted_units" in predictions.columns:
            rename_map["predicted_units"] = "prediction"
        predictions = predictions.rename(columns=rename_map)

        join_cols = ["date", "product_id", "region_id"]
        prediction_cols = [c for c in [
            *join_cols,
            "prediction",
            "lower_bound",
            "upper_bound",
            "model",
            "forecast_horizon",
        ] if c in predictions.columns]
        predictions = predictions[prediction_cols].drop_duplicates(join_cols)
        dashboard = fact.merge(predictions, on=join_cols, how="left")
    else:
        dashboard = fact.copy()
        dashboard["prediction"] = dashboard["lag_7_units"].fillna(0)
        dashboard["model"] = "seasonal_naive_7d_fallback"
        dashboard["forecast_horizon"] = 7

    dashboard["prediction"] = pd.to_numeric(
        dashboard["prediction"], errors="coerce"
    ).fillna(dashboard["lag_7_units"].fillna(0)).clip(lower=0)

    # Se não houver intervalos, usa uma faixa explicável baseada no erro histórico.
    if "lower_bound" not in dashboard.columns:
        residual = dashboard["units_sold"] - dashboard["prediction"]
        error_scale = float(residual.abs().quantile(0.90))
        error_scale = max(error_scale, 1.0)
        dashboard["lower_bound"] = (
            dashboard["prediction"] - error_scale
        ).clip(lower=0)
        dashboard["upper_bound"] = dashboard["prediction"] + error_scale

    dashboard["lower_bound"] = pd.to_numeric(
        dashboard["lower_bound"], errors="coerce"
    ).fillna(dashboard["prediction"]).clip(lower=0)
    dashboard["upper_bound"] = pd.to_numeric(
        dashboard["upper_bound"], errors="coerce"
    ).fillna(dashboard["prediction"])
    dashboard["forecast_horizon"] = dashboard.get(
        "forecast_horizon", pd.Series(1, index=dashboard.index)
    ).fillna(1).astype(int)
    dashboard["model"] = dashboard.get(
        "model", pd.Series(selected_model, index=dashboard.index)
    ).fillna(selected_model)

    dashboard["forecast_error_units"] = (
        dashboard["units_sold"] - dashboard["prediction"]
    )
    dashboard["absolute_error_units"] = dashboard["forecast_error_units"].abs()
    dashboard["error_pct"] = np.where(
        dashboard["units_sold"] > 0,
        dashboard["absolute_error_units"] / dashboard["units_sold"],
        np.nan,
    )
    dashboard["interval_width_units"] = (
        dashboard["upper_bound"] - dashboard["lower_bound"]
    ).clip(lower=0)
    dashboard["within_prediction_interval"] = (
        dashboard["units_sold"] >= dashboard["lower_bound"]
    ) & (dashboard["units_sold"] <= dashboard["upper_bound"])
    dashboard["selected_model"] = selected_model

    # Regras de exceção para a página operacional.
    dashboard["exception_type"] = np.select(
        [
            dashboard["stockout_flag"].astype(bool),
            dashboard["forecast_error_units"] < -dashboard["interval_width_units"].clip(lower=1) / 2,
            dashboard["forecast_error_units"] > dashboard["interval_width_units"].clip(lower=1) / 2,
            dashboard["anomaly_flag"].astype(bool),
        ],
        [
            "stockout",
            "underforecast",
            "overforecast",
            "data_anomaly",
        ],
        default="none",
    )
    dashboard["severity"] = np.select(
        [
            (dashboard["exception_type"] == "stockout") & (dashboard["lost_sales_estimate_units"] >= 2),
            (dashboard["exception_type"].isin(["underforecast", "overforecast"])) & (dashboard["error_pct"] >= 0.50),
            dashboard["exception_type"] != "none",
        ],
        ["high", "high", "medium"],
        default="low",
    )
    dashboard["exception_status"] = np.where(
        dashboard["exception_type"] == "none", "not_applicable", "open"
    )
    dashboard["exception_id"] = (
        dashboard["date"].dt.strftime("%Y%m%d") + "_" +
        dashboard["product_id"].astype(str) + "_" +
        dashboard["region_id"].astype(str)
    )

    dashboard_daily_cols = [
        "date", "product_id", "product_name", "category", "abc_class",
        "region_id", "region_name", "state", "units_sold", "prediction",
        "lower_bound", "upper_bound", "forecast_horizon", "model",
        "selected_model", "within_prediction_interval", "promo_flag",
        "discount_pct", "net_unit_price_brl", "available_stock_units",
        "stockout_flag", "lost_sales_estimate_units", "revenue_brl",
        "gross_margin_brl", "gross_margin_pct", "dataset_split",
        "exception_type", "severity", "exception_status",
    ]
    dashboard_daily = dashboard[
        [c for c in dashboard_daily_cols if c in dashboard.columns]
    ].copy()

    exceptions_cols = [
        "exception_id", "date", "product_id", "product_name", "category",
        "abc_class", "region_id", "region_name", "exception_type", "severity",
        "exception_status", "units_sold", "prediction", "forecast_error_units",
        "absolute_error_units", "error_pct", "stockout_flag",
        "lost_sales_estimate_units", "promo_flag", "discount_pct",
        "available_stock_units", "selected_model",
    ]
    dashboard_exceptions = dashboard.loc[
        dashboard["exception_type"] != "none",
        [c for c in exceptions_cols if c in dashboard.columns],
    ].copy()

    # Métricas globais e por segmento para a página de avaliação.
    metric_rows = []

    def add_metric(model, split, segment_type, segment_value, frame):
        if frame.empty:
            return
        actual = frame["units_sold"].to_numpy()
        predicted = frame["prediction"].to_numpy()
        metric_rows.append({
            "model": model,
            "split": split,
            "segment_type": segment_type,
            "segment_value": str(segment_value),
            "wape": wape(actual, predicted),
            "mae": float(np.abs(actual - predicted).mean()),
            "rmse": float(np.sqrt(np.mean((actual - predicted) ** 2))),
            "observations": int(len(frame)),
            "coverage_rate": float(frame["within_prediction_interval"].mean()),
            "is_selected_model": model == selected_model,
        })

    eval_frame = dashboard[dashboard["prediction"].notna()].copy()
    add_metric(selected_model, "available", "global", "all", eval_frame)
    for key, group in eval_frame.groupby("product_id"):
        add_metric(selected_model, "available", "product", key, group)
    for key, group in eval_frame.groupby("region_id"):
        add_metric(selected_model, "available", "region", key, group)
    for key, group in eval_frame.groupby("category"):
        add_metric(selected_model, "available", "category", key, group)
    model_metrics = pd.DataFrame(metric_rows)

    pricing = read_optional(PRICING_PRODUCT_PATH)
    if pricing is None:
        pricing = read_optional(PRICING_PATH)
    if pricing is None:
        pricing = pd.DataFrame()

    # Exportação em formatos consumíveis por Power BI e Plotly.
    outputs = {
        "dashboard_daily": dashboard_daily,
        "dashboard_exceptions": dashboard_exceptions,
        "dashboard_model_metrics": model_metrics,
        "dashboard_pricing_scenarios": pricing,
    }
    for name, frame in outputs.items():
        frame.to_csv(DASH_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")
        frame.to_parquet(DASH_DIR / f"{name}.parquet", index=False)

    print(f"Modelo selecionado: {selected_model}")
    for name, frame in outputs.items():
        print(f"{name}: {len(frame):,} linhas; {len(frame.columns)} colunas")


if __name__ == "__main__":
    main()
# ==========================================
# pages/3_Performance.py
# ==========================================
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import plotly.graph_objects as go

# --- Page Config ---
def performance_page(): 
    #--- Helper functions ---
    @st.cache_data
    def load_forecast_csv(path="data/forecast_all_warehouse.csv"):
        """Load forecast dataframe. Adjust path if needed."""
        try:
            df = pd.read_csv(path, parse_dates=["date"])
            return df
        except Exception as e:
            st.error(f"Could not load file at `{path}`. Error: {e}")
            return pd.DataFrame()

    def summary_metrics(df):
        """Compute per-warehouse and per-model performance metrics."""
        metrics = []
        for (wh, model), sub in df.groupby(["warehouse", "model"]):
            if sub.empty:
                continue
            mae = np.mean(np.abs(sub["actual"] - sub["forecast"]))
            rmse = np.sqrt(np.mean((sub["actual"] - sub["forecast"]) ** 2))
            bias = np.mean(sub["forecast"] - sub["actual"])

            # Interpret MAE
            if mae < 100:
                interpretation = "Excellent accuracy ✅"
            elif mae < 300:
                interpretation = "Good performance 👍"
            elif mae < 600:
                interpretation = "Moderate accuracy ⚠️"
            else:
                interpretation = "Poor accuracy ❌"

            metrics.append({
                "Warehouse": wh,
                "Model": model,
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2),
                "Bias": round(bias, 2),
                "Interpretation": interpretation
            })
        return pd.DataFrame(metrics)

    def to_csv_bytes(df):
        b = BytesIO()
        df.to_csv(b, index=False)
        b.seek(0)
        return b

    # --- Page Title ---
    st.title("📈 Model Performance Overview")
    st.markdown("""
    This page summarizes **forecast model performance per warehouse and model type**.  
    Use the filters on the sidebar to narrow down results and visualize weekly performance trends.
    """)

    # --- Load Data ---
    DATA_PATH = "data/forecast_all_warehouse.csv"
    df = load_forecast_csv(DATA_PATH)
    if df.empty:
        st.info("No forecast data found. Ensure `forecast_all_warehouse.csv` exists in `data/` folder.")
        st.stop()

    df.columns = [c.strip().lower() for c in df.columns]

    # --- Sidebar Filters ---
    st.sidebar.header("⚙️ Performance Control")
    warehouse_list = ["All"] + sorted(df["warehouse"].unique().tolist())
    model_list = ["All"] + sorted(df["model"].unique().tolist())

    sel_warehouse = st.sidebar.selectbox("🏭 Select warehouse", warehouse_list)
    sel_model = st.sidebar.selectbox("🎯 Select model", model_list)
    sel_start = st.sidebar.date_input("📅 Start date", df["date"].min().date())
    sel_end = st.sidebar.date_input("📅 End date", df["date"].max().date())

    # --- Filter Data ---
    df_filtered = df.copy()
    df_filtered = df_filtered[(df_filtered["date"] >= pd.to_datetime(sel_start)) & (df_filtered["date"] <= pd.to_datetime(sel_end))]

    if sel_warehouse != "All":
        df_filtered = df_filtered[df_filtered["warehouse"] == sel_warehouse]
    if sel_model != "All":
        df_filtered = df_filtered[df_filtered["model"] == sel_model]

    # --- Summary Metrics Table ---
    st.subheader("📊 Model Performance Metrics")

    perf_df = summary_metrics(df_filtered)
    if perf_df.empty:
        st.info("No performance metrics available for current filters.")
    else:
        st.dataframe(perf_df.sort_values(["Warehouse", "Model"]).reset_index(drop=True), use_container_width=True)

    # --- Download Button ---
    csv_bytes = to_csv_bytes(perf_df)
    st.download_button(
        label="⬇️ Download Performance Summary (CSV)",
        data=csv_bytes,
        file_name="model_performance_summary.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # --- Weekly Trend Plot (Same Style as Dashboard) ---
    st.subheader("📉 Actual vs Forecast — Weekly Trend")

    if df_filtered.empty:
        st.info("No data available for the selected filters.")
    else:
        # Aggregate by week
        agg = df_filtered.groupby(["date", "warehouse"]).agg({
            "actual": "sum",
            "forecast": "sum",
            "lower_95": "mean" if "lower_95" in df_filtered else "sum",
            "upper_95": "mean" if "upper_95" in df_filtered else "sum"
        }).reset_index()

        fig = go.Figure()

        if sel_warehouse == "All":
            # Plot each warehouse separately
            for wh in sorted(df_filtered["warehouse"].unique()):
                sub = agg[agg["warehouse"] == wh]
                fig.add_trace(go.Scatter(
                    x=sub["date"], y=sub["actual"],
                    mode="lines+markers",
                    name=f"{wh} — Actual",
                    line=dict(width=2),
                    marker=dict(size=5)
                ))
                fig.add_trace(go.Scatter(
                    x=sub["date"], y=sub["forecast"],
                    mode="lines+markers",
                    name=f"{wh} — Forecast",
                    line=dict(width=2, dash="dot"),
                    marker=dict(size=5)
                ))
        else:
            # Single warehouse mode with CI
            wh_agg = agg[agg["warehouse"] == sel_warehouse]
            if "lower_95" in df_filtered.columns and "upper_95" in df_filtered.columns:
                fig.add_traces([
                    go.Scatter(
                        x=wh_agg["date"], y=wh_agg["upper_95"],
                        mode="lines", line=dict(width=0),
                        showlegend=False
                    ),
                    go.Scatter(
                        x=wh_agg["date"], y=wh_agg["lower_95"],
                        mode="lines", line=dict(width=0),
                        fill='tonexty', fillcolor='rgba(128,128,128,0.2)',
                        name="95% Confidence Interval"
                    )
                ])
            fig.add_trace(go.Scatter(
                x=wh_agg["date"], y=wh_agg["actual"],
                mode="lines+markers",
                name="Actual",
                line=dict(color="#1f77b4", width=2),
                marker=dict(size=5)
            ))
            fig.add_trace(go.Scatter(
                x=wh_agg["date"], y=wh_agg["forecast"],
                mode="lines+markers",
                name="Forecast",
                line=dict(color="#ff7f0e", width=2, dash="dot"),
                marker=dict(size=5)
            ))

        fig.update_layout(
            template="plotly_white",
            height=450,
            margin=dict(l=20, r=20, t=40, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            xaxis_title="Date",
            yaxis_title="Total Quantity",
            title=dict(
                text=f"Actual vs Forecast — {sel_warehouse if sel_warehouse != 'All' else 'All Warehouses'}",
                x=0.5, xanchor="center"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption("Developed for Smarter Stocking Analytics © 2025")

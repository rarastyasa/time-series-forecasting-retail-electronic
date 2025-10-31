import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

# ===============================
# PAGE SETUP
# ===============================
def dashboard_page(): 
    # --- Page Title ---
    st.title("📊 Forecasting Dashboard — Warehouse Overview")
    st.markdown("""
    This dashboard provides an overview of **actual sales, forecasts, and confidence intervals**  
    for each warehouse, helping evaluate model performance and demand trends.
    """)

    # ===============================
    # LOAD DATA
    # ===============================
    weekly_path = os.path.join("data", "weekly_sales_by_warehouse.csv")
    forecast_path = os.path.join("data", "forecast_all_warehouse.csv")

    if not os.path.exists(weekly_path) or not os.path.exists(forecast_path):
        st.error("❌ Data files not found. Please ensure both files exist in the `/data` folder:\n"
                "- `weekly_sales_by_warehouse.csv`\n"
                "- `forecast_all_warehouse.csv`")
        st.stop()

    weekly_df = pd.read_csv(weekly_path)
    forecast_df = pd.read_csv(forecast_path)

    # ===============================
    # DATA CLEANING & NORMALIZATION
    # ===============================
    weekly_df.columns = [c.lower().strip() for c in weekly_df.columns]
    forecast_df.columns = [c.lower().strip() for c in forecast_df.columns]

    if "warehouse" in forecast_df.columns and "nearest_warehouse" not in forecast_df.columns:
        forecast_df.rename(columns={"warehouse": "nearest_warehouse"}, inplace=True)

    if "nearest_warehouse" not in forecast_df.columns:
        forecast_df["nearest_warehouse"] = "unknown"

    weekly_df["date"] = pd.to_datetime(weekly_df["date"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])

    # ===============================
    # MERGE DATA
    # ===============================
    merged = pd.merge(
        weekly_df,
        forecast_df,
        on=["nearest_warehouse", "date"],
        how="outer",
        suffixes=("_actual", "_forecast")
    ).sort_values("date")

    # ===============================
    # SIDEBAR FILTER
    # ===============================
    st.sidebar.header("⚙️ Dashboard Controls")

    warehouses = sorted(merged["nearest_warehouse"].dropna().unique())
    warehouses = ["All"] + warehouses  # Add "All" option
    selected_wh = st.sidebar.selectbox("🏭 Select Warehouse", warehouses)

    if selected_wh == "All":
        df_plot = merged.copy()
    else:
        df_plot = merged[merged["nearest_warehouse"] == selected_wh].copy()

    # ===============================
    # KPI CALCULATIONS
    # ===============================
    if selected_wh == "All":
        total_sales = merged["total_quantity"].sum()
        avg_weekly_sales = merged["total_quantity"].mean()
    else:
        total_sales = df_plot["total_quantity"].sum()
        avg_weekly_sales = df_plot["total_quantity"].mean()

    # MAE (Mean Absolute Error)
    if "forecast" in df_plot.columns and df_plot["forecast"].notna().any():
        df_valid = df_plot.dropna(subset=["forecast", "total_quantity"])
        mae = np.mean(np.abs(df_valid["forecast"] - df_valid["total_quantity"]))
    else:
        mae = np.nan

    # ===============================
    # KPI DISPLAY SECTION
    # ===============================
    st.subheader(f"📈 Key Performance Indicators — {selected_wh if selected_wh != 'All' else 'All Warehouses'}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Weekly Sales", f"{total_sales:,.0f}")
    col2.metric("Average Weekly Sales", f"{avg_weekly_sales:,.0f}")
    col3.metric("MAE", f"{mae:,.2f}" if not np.isnan(mae) else "N/A")

    st.markdown("---")

    # ===============================
    # PLOT — VISUALIZATION
    # ===============================

    # 🎨 Warna disesuaikan dengan contoh referensi
    color_map = {
        "bakers": "rgb(0,123,255)",      # biru tua
        "nickolson": "rgb(102,179,255)", # biru muda
        "thompson": "rgb(255,51,51)"     # merah
    }

    rgba_map = {
        "bakers": "rgba(0,123,255,0.15)",
        "nickolson": "rgba(102,179,255,0.15)",
        "thompson": "rgba(255,51,51,0.15)"
    }

    fig = go.Figure()

    if selected_wh == "All":
        for wh in merged["nearest_warehouse"].dropna().unique():
            wh_df = merged[merged["nearest_warehouse"] == wh]
            line_color = color_map.get(wh.lower(), "rgb(128,128,128)")
            fig.add_trace(go.Scatter(
                x=wh_df["date"],
                y=wh_df["total_quantity"],
                mode="lines+markers",
                name=f"{wh.capitalize()} — Actual",
                line=dict(color=line_color, width=2.5),
                marker=dict(size=5, color=line_color)
            ))
    else:
        line_color = color_map.get(selected_wh.lower(), "rgb(128,128,128)")
        fill_color = rgba_map.get(selected_wh.lower(), "rgba(128,128,128,0.15)")
        
        # Actual line
        fig.add_trace(go.Scatter(
            x=df_plot["date"],
            y=df_plot["total_quantity"],
            mode="lines+markers",
            name="Actual Sales",
            line=dict(color=line_color, width=2.5),
            marker=dict(size=5, color=line_color)
        ))

        # Forecast line
        if "forecast" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot["date"],
                y=df_plot["forecast"],
                mode="lines+markers",
                name="Forecast",
                line=dict(color="rgba(50,50,50,0.6)", width=2, dash="dot"),
                marker=dict(size=5, color="rgba(50,50,50,0.6)")
            ))

        # Confidence Interval
        if "lower_95" in df_plot.columns and "upper_95" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=pd.concat([df_plot["date"], df_plot["date"][::-1]]),
                y=pd.concat([df_plot["upper_95"], df_plot["lower_95"][::-1]]),
                fill="toself",
                fillcolor=fill_color,
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=True,
                name="95% Confidence Interval"
            ))

    # ===============================
    # FINAL STYLING
    # ===============================
    title_text = (
        f"📊 Weekly Sales & Forecast — {selected_wh} Warehouse"
        if selected_wh != "All"
        else "📊 Weekly Sales Trend by Warehouse"
    )

    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=26, color="rgba(20,20,20,0.95)", family="Arial Black"),
            x=0.02
        ),
        xaxis_title="Date",
        yaxis_title="Total Sales Quantity",
        template="plotly_white",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=70, b=50, l=60, r=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.3)', showgrid=False)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.3)', showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    # ===============================
    # FOOTER
    # ===============================
    st.markdown("---")
    st.caption("Developed as part of the AI-Powered Warehouse Forecasting Project © 2025")

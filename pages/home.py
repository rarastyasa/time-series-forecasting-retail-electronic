import streamlit as st
import pandas as pd
import plotly.express as px

def home_page(): 
    # --- Page Title ---
    st.title("📦 Smarter Stocking Starts Here — AI-Powered Sales Forecasting Dashboard")

    # --- Company Overview ---
    st.header("🏢 Company Overview")
    st.markdown("""
    Our retail electronics company operates through **three main warehouses — Nickolson, Thompson, and Bakers.**  
    Each warehouse serves different regional markets, playing a critical role in ensuring timely delivery and efficient stock management.  

    However, fluctuating demand patterns and supply chain inconsistencies across regions have made inventory forecasting increasingly complex.  
    To address this, the company leverages **AI-driven time series forecasting** to improve accuracy, optimize stock levels, and enhance operational decisions.
    """)

    # --- Weekly Sales Trends ---
    st.header("📊 Weekly Sales Trends per Warehouse")

    data_path = "data/weekly_sales_by_warehouse.csv"
    try:
        df_weekly = pd.read_csv(data_path)
        df_weekly['date'] = pd.to_datetime(df_weekly['date'])
        df_weekly.rename(columns={
            'nearest_warehouse': 'Warehouse',
            'total_quantity': 'Total Quantity'
        }, inplace=True)

        fig = px.line(
            df_weekly,
            x='date',
            y='Total Quantity',
            color='Warehouse',
            markers=True,
            title="Weekly Sales Trend by Warehouse",
            labels={'date': 'Date', 'Total Quantity': 'Total Sales Quantity'}
        )

        fig.update_layout(
            title_x=0.05,
            title_font_size=18,
            legend_title_text='Warehouse',
            template='plotly_white',
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    except FileNotFoundError:
        st.warning("⚠️ Weekly sales data not found. Please upload `weekly_sales_all_warehouses.csv` to the `/data` folder.")
    except Exception as e:
        st.error(f"Error loading weekly trend data: {e}")

    # --- Footer ---
    st.markdown("---")
    st.caption("Developed as part of the AI-Powered Warehouse Forecasting Project © 2025")

    # --- Business Problem ---
    st.header("🏭 Business Problem")
    st.markdown("""
    The company experiences **inconsistent sales performance** across its three primary warehouses — **Nickolson**, **Thompson**, and **Bakers**.  
    Daily sales data exhibit high volatility, with frequent zero-sale days, sudden demand spikes from promotions, and occasional delays in supply.  
    This instability makes daily forecasting less reliable and difficult to apply in stock planning.

    Since **replenishment and supplier orders are managed weekly**, analyzing and forecasting data on a **weekly basis** offers a more stable and actionable view of true demand patterns.  
    Each warehouse demonstrates distinct sales characteristics:

    - **Nickolson** — steady weekly demand with mild seasonality.  
    - **Thompson** — high-volume but volatile due to promotions and regional dynamics.  
    - **Bakers** — irregular and unpredictable demand, possibly linked to inconsistent local orders.

    These differences create challenges in balancing stock between locations, leading to overstock in some warehouses and shortages in others.
    """)

    # --- Project Objectives ---
    st.header("🎯 Project Objectives")
    st.markdown("""
    This project aims to develop **warehouse-specific weekly forecasting models** that adapt to each location’s demand behavior.  
    The main objectives are to:

    - **Improve forecast accuracy** by reducing noise from daily fluctuations.  
    - **Support better inventory planning** to minimize both overstock and stockout risks.  
    - **Capture localized demand patterns** to optimize procurement and distribution strategies.  

    By building a reliable forecasting system, the company can achieve **a more efficient supply chain**, reduce costs,  
    and ensure that product availability consistently meets customer demand across all regions.
    """)

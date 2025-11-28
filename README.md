# 📦 Smarter Stocking Starts Here — AI-Powered Sales Forecasting Dashboard 
### **Time Series Forecasting for Multi-Warehouse Inventory Optimization**

This project develops a **multi-model time series forecasting system** to predict weekly product demand across three major warehouses in a retail electronics company: **Nickolson**, **Thompson**, and **Bakers**.

By applying **SARIMAX**, **Hybrid Prophet + SARIMAX** and **Hybrid Prophet + XGBoost Regression**, the project identifies the best forecasting model for each warehouse based on historical sales behavior, demand seasonality, and volatility. The forecasts support **inventory planning**, **replenishment strategies**, and **operational decision-making**.

🔗 **Live Streamlit Dashboard:**  
👉 https://time-series-forecasting-retail-electronic.streamlit.app/

---

## 🚀 Project Overview

Daily sales data shows instability with:

- Frequent **zero-sale days**  
- Sudden **promotional spikes**  
- Occasional **supplier delays**  
- Different patterns across warehouses  

To produce more stable and actionable forecasts, the data is aggregated into **weekly sales**, aligned with the company’s weekly stock replenishment cycle.

This project provides:

- Accurate **6-week ahead forecasting**
- Comparison of SARIMAX, Hybrid Prophet + SARIMAX, and Hybrid Prophet + XGBoost models
- Warehouse-specific insights
- Cleaned & engineered time-series features
- An interactive **Streamlit dashboard** for visualization

This supports improvements in:
✔ Stock availability  
✔ Replenishment scheduling  
✔ Promotion planning  
✔ Warehouse-level decision-making  

---

## 🗂️ Project Structure
```
📦 Smarter Stocking
│
├── assets/
│ ├── script.js
│ └── styles.css
│
├── data/
│ ├── dirty_data.csv
│ ├── forecast_all_warehouse.csv
│ ├── weekly_sales_by_warehouse.csv
│ └── warehouse/
│
├── pages/
│ ├── pycache/
│ ├── init.py
│ ├── business_impact.py
│ ├── contact.py
│ ├── dashboard.py
│ ├── home.py
│ └── performance.py
│
├── (2)_Final_Project_Data_Science_Rahma_Anggana_Rarastyasa.ipynb
├── README.md
```
---

## 🧠 Key Features

### 🔵 1. Time Series Aggregation & Cleaning
- Converts daily → weekly sales
- Handles missing values and outliers
- Explores weekly patterns and volatility

### 🟣 2. Feature Engineering
- Lag features (1, 2, 3 weeks)
- Rolling windows (3, 4, 8 weeks)
- Calendar features (week, month, year)
- Demand trend encoding

### 🟠 3. Multi-Model Forecasting
Three forecasting models are applied:

| Model | Strengths | Best For |
|-------|-----------|----------|
| **Prophet** | Trend & seasonality modeling | Stable patterns (Thompson) |
| **SARIMAX** | Captures autocorrelation & seasonality | Seasonal warehouses (Nickolson) |
| **XGBoost** | Handles irregular spikes | Highly volatile demand (Bakers) |

### 🟢 4. Forecast Evaluation
Evaluation metrics include:

- RMSE  
- MAE  
- Residual analysis  
- Confidence interval inspection  

---

## 🔍 Warehouse Insights & Best Models

### 🏭 **Nickolson Warehouse**
- Contains moderate demand fluctuations  
- Exhibits short-term seasonal patterns  
- **Best Model: Hybrid Prophet + SARIMAX**  
- Consistent, smooth forecasts with low RMSE  

### 🏭 **Thompson Warehouse**
- Most stable sales pattern  
- Smooth upward/downward weekly trends  
- **Best Model: Hybrid Prophet + XGboost**  
- Captures long-term trends accurately  

### 🏭 **Bakers Warehouse**
- Highly volatile and promotion-driven  
- Frequent sudden demand spikes  
- **Best Model: Hybrid Prophet + SARIMAX**  
- Best at capturing non-linear patterns  

---

## 🗺️ Interactive Streamlit Dashboard

it dashboard provides an end-to-end view of forecasting performance across all three warehouses. It includes the following sections and interactive components.

### ✔ Model Comparison
Compare the performance of multiple time-series forecasting models:
- **Prophet + SARIMAX**
- **Prophet + XGBoost**
- Model evaluation table (MAE / RMSE)
- Error visualizations and ranking across warehouses

### ✔ Forecast Visualization
Interactive forecasting charts for operational use:
- **6-week ahead demand prediction**
- **Confidence interval shading** to display forecast uncertainty
- **Actual vs Predicted** time series (train / test / forecast)
- Interactive controls to choose forecast horizon and confidence level

### ✔ Warehouse Drill-Down Analysis
Per-warehouse insights and visualizations:
- **Nickolson** — weekly forecast, residuals, and metrics
- **Thompson** — hybrid model results and short-term peak analysis
- **Bakers** — trend analysis, event (promo/holiday) impact
- Side-by-side visual comparison between warehouses

### ✔ Business & Operational Panels
- **Business impact** summary (MAE → financial impact estimates)
- **Recommendations** (retraining cadence, inventory thresholds, cross-warehouse actions)
- **Download/export** forecast CSV for integration with ERP/ordering systems

### 🌐 Live App
Open the interactive dashboard here:  
https://time-series-forecasting-retail-electronic.streamlit.app/



---

## 📓 Notebook Reference

All analytical steps — including EDA, preprocessing, model training, and evaluation — are documented in:

**`Final_Project_Data_Science_Rahma_Anggana_Rarastyasa.ipynb`**

This notebook serves as the analytical foundation for the forecasting models and the Streamlit app.

---

## 💡 Business Impact Summary

The forecasting system delivers strong value in operational improvement:

### 🚀 Key Benefits
- 📦 **Improved inventory allocation** across warehouses  
- 🔄 **Optimized replenishment cycles** based on weekly forecasts  
- 📈 **Higher forecast accuracy** for planning and budgeting  
- 💸 **Reduced stockout and overstock costs**  
- 🛒 **Data-backed promotion planning**  
- ⚙️ **More efficient supply chain operations**  

These insights enable proactive and reliable warehouse management.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas, NumPy**
- **Prophet**
- **Statsmodels (SARIMAX)**
- **XGBoost**
- **scikit-learn**
- **Matplotlib, Seaborn**


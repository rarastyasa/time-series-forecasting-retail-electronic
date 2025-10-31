# pages/business_impact.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
import streamlit.components.v1 as components

# Top-level page config (call once)
st.set_page_config(page_title="💰 Business Impact", layout="wide")


def business_impact_page():
    # --- Header ---
    st.title("💰 Business Impact & Forecast ROI Analysis")
    st.markdown(
        """
        This dashboard translates **forecasting performance** into **financial and operational impact**.  
        It identifies how forecast accuracy influences costs, savings, and ROI across warehouses,  
        followed by automatically generated **recommended actions**.
        """
    )

    # --- Business Summary Data ---
    summary_data = {
        "Warehouse": ["Nickolson", "Thompson", "Bakers"],
        "Forecast Accuracy (%)": [83.7, 80.9, 74.2],
        "FCR (%)": [2.85, 3.35, 4.51],
        "CPO (Rp)": [28451, 50268, 54097],
        "Monthly Cost (Rp)": [1223372, 2629838, 1512021],
        "Model ROI (%)": [58.7, 126.2, 72.6]
    }
    summary_df = pd.DataFrame(summary_data)

    # --- Prepare a display-friendly dataframe (format numbers as strings for dataframe)
    display_df = summary_df.copy()
    display_df["Forecast Accuracy (%)"] = display_df["Forecast Accuracy (%)"].map(lambda x: f"{x:.1f}")
    display_df["FCR (%)"] = display_df["FCR (%)"].map(lambda x: f"{x:.2f}")
    display_df["CPO (Rp)"] = display_df["CPO (Rp)"].map(lambda x: f"Rp{int(x):,}")
    display_df["Monthly Cost (Rp)"] = display_df["Monthly Cost (Rp)"].map(lambda x: f"Rp{int(x):,}")
    display_df["Model ROI (%)"] = display_df["Model ROI (%)"].map(lambda x: f"{x:.1f}")

    # --- Display Business Summary Table ---
    st.subheader("📊 Business Metrics Summary")
    st.dataframe(display_df, use_container_width=True)

    # --- Visualization Section ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💹 ROI Comparison per Warehouse")
        fig_roi = go.Figure()
        fig_roi.add_trace(
            go.Bar(
                x=summary_df["Warehouse"],
                y=summary_df["Model ROI (%)"],
                text=summary_df["Model ROI (%)"].round(1).astype(str) + "%",
                textposition="auto",
                marker_color=['#90EE90', '#87CEEB', '#FFB6C1']
            )
        )
        fig_roi.update_layout(template="plotly_white", yaxis_title="ROI (%)", height=380)
        st.plotly_chart(fig_roi, use_container_width=True)

    with col2:
        st.markdown("#### 💵 Monthly Cost Impact (Rp)")
        fig_cost = go.Figure()
        fig_cost.add_trace(
            go.Bar(
                x=summary_df["Warehouse"],
                y=summary_df["Monthly Cost (Rp)"],
                text=[f"Rp{v:,.0f}" for v in summary_df["Monthly Cost (Rp)"]],
                textposition="auto",
                marker_color=['#FFB6C1', '#ADD8E6', '#FFE5B4']
            )
        )
        fig_cost.update_layout(template="plotly_white", yaxis_title="Monthly Cost (Rp)", height=380)
        st.plotly_chart(fig_cost, use_container_width=True)

    st.markdown("---")

    # --- Recommended Actions Section ---
    st.subheader("🧭 Recommended Actions")

    # Recommendation logic (kept simple & deterministic)
    def determine_condition(acc, fcr):
        if acc >= 82.0 and fcr < 3.0:
            return "High Demand"
        elif (75.0 <= acc < 82.0) or (3.0 <= fcr <= 4.0):
            return "Moderate Demand"
        else:
            return "Low Demand"

    recommendations = []
    for _, row in summary_df.iterrows():
        wh = row["Warehouse"]
        cond = determine_condition(row["Forecast Accuracy (%)"], row["FCR (%)"])

        if wh == "Nickolson":
            if cond == "High Demand":
                priority = "Smoothly scale staffing and just-in-time replenishment"
                next_step = "Lock favorable shipping rates; steady reorder policy"
            else:
                priority = "Maintain steady workforce and monitor restock rate"
                next_step = "Review inventory buffer policy"
        elif wh == "Thompson":
            if cond == "Moderate Demand":
                priority = "Use flexible workforce; monitor promo impact closely"
                next_step = "Coordinate with marketing on promo timing"
            else:
                priority = "Deploy temporary staff and adjust replenishment window"
                next_step = "Strengthen logistics monitoring"
        elif wh == "Bakers":
            if cond == "Low Demand":
                priority = "Tighten procurement; implement micro-promos"
                next_step = "Audit SKU-level performance & reduce slow movers"
            else:
                priority = "Stabilize order flow and reduce lead-time variance"
                next_step = "Reassess supplier contracts"

        recommendations.append(
            {
                "Warehouse": wh,
                "Forecast Condition": cond,
                "Priority Action": priority,
                "Next Step": next_step,
            }
        )

    reco_df = pd.DataFrame(recommendations)

    # --- Build robust HTML for the recommendation table ---
    def build_reco_table_html(df):
        # Note: produce clean HTML string starting with <table> (no stray backticks/newlines)
        html = (
            "<style>"
            "table.custom-table{width:100%;border-collapse:collapse;font-family:Inter,system-ui,Arial;}"
            "table.custom-table th{background:#f8f9fa;padding:10px;border-bottom:2px solid #dee2e6;text-align:left;}"
            "table.custom-table td{padding:10px;border-bottom:1px solid #e9ecef;vertical-align:top;}"
            ".high{background:#c7f9cc;padding:6px;border-radius:4px;}"
            ".moderate{background:#a0c4ff;padding:6px;border-radius:4px;}"
            ".low{background:#ffadad;padding:6px;border-radius:4px;}"
            "</style>"
        )
        html += "<table class='custom-table'><thead><tr><th>📦 Warehouse</th><th>📈 Forecast Condition</th><th>✅ Priority Action</th><th>⚡ Next Step</th></tr></thead><tbody>"
        for _, r in df.iterrows():
            cls = "moderate"
            if r["Forecast Condition"] == "High Demand":
                cls = "high"
            elif r["Forecast Condition"] == "Low Demand":
                cls = "low"
            html += (
                "<tr>"
                f"<td><strong>{r['Warehouse']}</strong></td>"
                f"<td class='{cls}'>{r['Forecast Condition']}</td>"
                f"<td>{r['Priority Action']}</td>"
                f"<td>{r['Next Step']}</td>"
                "</tr>"
            )
        html += "</tbody></table>"
        return html

    html = build_reco_table_html(reco_df)

    # Optional debug: uncomment to inspect raw HTML (helps find stray chars)
    # st.text_area("DEBUG HTML (first 400 chars)", value=html[:400], height=150)

    # Render HTML safely with height — components.v1.html WILL render HTML (not as code)
    components.html(html, height=300, scrolling=True)

    st.markdown("---")

    # --- Download Button ---
    csv_buffer = BytesIO()
    summary_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="⬇️ Download Business Impact (CSV)",
        data=csv_buffer,
        file_name="business_impact_summary.csv",
        mime="text/csv",
    )

    st.caption("Developed for Smarter Stocking Analytics © 2025 — Business Impact Visualization")


# Run directly for local test
if __name__ == "__main__":
    business_impact_page()

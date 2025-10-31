import streamlit as st

# ===================================
# PAGE CONFIGURATION
# ===================================
st.set_page_config(
    page_title="Smarter Stocking Analytics",
    page_icon="📦",
    layout="wide"
)

# ===================================
# LOAD CSS & JS
# ===================================
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_js(current_page):
    with open("assets/script.js") as f:
        js_code = f.read().replace("{{CURRENT_PAGE}}", current_page)
        st.markdown(f"<script>{js_code}</script>", unsafe_allow_html=True)

# ===================================
# INITIALIZE SESSION STATE
# ===================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# ===================================
# NAVIGATION
# ===================================
nav_options = [
    "🏠 Home",
    "📊 Dashboard",
    "📈 Performance",
    "💸 Business Impact" ,
    "☎️ Contact"
]

# Load CSS
load_css()

# Custom Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title">📦 Smarter Stocking Analytics</div>', unsafe_allow_html=True)

    for option in nav_options:
        if st.button(option, key=option):
            st.session_state.current_page = option
            st.rerun()

    st.markdown('<div class="sidebar-footer">Developed by Rahma Anggana Rarastyasa © 2025</div>', unsafe_allow_html=True)

# Load JS
load_js(st.session_state.current_page)

# ===================================
# PAGE ROUTER
# ===================================
if st.session_state.current_page == "🏠 Home":
    from pages.home import home_page
    home_page()

elif st.session_state.current_page == "📊 Dashboard":
    from pages.dashboard import dashboard_page
    dashboard_page()

elif st.session_state.current_page == "📈 Performance":
    from pages.performance import performance_page
    performance_page()

elif st.session_state.current_page == "💸 Business Impact":
    from pages.business_impact import business_impact_page
    business_impact_page()

elif st.session_state.current_page == "☎️ Contact":
    from pages.contact import contact_page
    contact_page()


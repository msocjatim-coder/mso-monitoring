import streamlit as st
from datetime import datetime, timedelta

class ModernSidebar:
    @staticmethod
    def render():
        with st.sidebar:
            # Header dengan gradient
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                margin-bottom: 1.5rem;
                text-align: center;
                color: white;
            ">
                <h2 style="margin:0; font-size: 1.5rem;">📊 OSS Telkom</h2>
                <p style="margin:0; opacity:0.9; font-size: 0.9rem;">Monitoring Dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation
            st.markdown("### 🧭 Navigasi")
            page = st.radio(
                "",
                ["🏠 Dashboard", "📤 Upload Data", "📋 Data Viewer", "⚙️ Settings"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # Filter Section (untuk dashboard)
            if page == "🏠 Dashboard":
                st.markdown("### 🔍 Filter Data")
                
                # Date range filter
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input(
                        "Dari",
                        datetime.now() - timedelta(days=30)
                    )
                with col2:
                    end_date = st.date_input(
                        "Sampai",
                        datetime.now()
                    )
                
                # Region filter
                regions = ["Semua", "Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
                selected_region = st.selectbox("📍 Region", regions)
                
                # Status filter
                status = ["Semua", "Active", "Maintenance", "Down"]
                selected_status = st.selectbox("⚡ Status", status)
                
                # Alert threshold
                alert_threshold = st.slider(
                    "⚠️ Alert Threshold",
                    min_value=0,
                    max_value=10,
                    value=3
                )
                
                return {
                    'page': page.replace("🏠 ", "").replace("📤 ", "").replace("📋 ", "").replace("⚙️ ", ""),
                    'filters': {
                        'start_date': start_date,
                        'end_date': end_date,
                        'region': selected_region,
                        'status': selected_status,
                        'alert_threshold': alert_threshold
                    }
                }
            
            # Stats card di sidebar
            st.markdown("---")
            st.markdown("### 📈 Quick Stats")
            
            # Placeholder stats - nanti akan diupdate dari database
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Sites", "150", "+12")
            with col2:
                st.metric("Active", "142", "94%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Uptime", "99.2%", "+0.3%")
            with col2:
                st.metric("Alerts", "8", "-2")
            
            return {'page': page.replace("🏠 ", "").replace("📤 ", "").replace("📋 ", "").replace("⚙️ ", ""), 'filters': {}}

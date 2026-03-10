import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.charts import ModernCharts

class ModernDashboard:
    @staticmethod
    def render(data: pd.DataFrame, filters: dict):
        if data.empty:
            st.info("📭 Belum ada data. Silakan upload data terlebih dahulu.")
            return
        
        # Hero Section dengan Key Metrics
        st.markdown("## 📊 Overview Dashboard")
        
        # Metrics Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sites = len(data)
            delta_sites = "+5"  # Ini bisa dihitung dari data sebelumnya
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <p style="margin:0; font-size:0.9rem; opacity:0.9;">Total Sites</p>
                <h2 style="margin:0; font-size:2rem;">{total_sites}</h2>
                <p style="margin:0; font-size:0.8rem;">{delta_sites} dari bulan lalu</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            active_sites = len(data[data['status'] == 'Active']) if 'status' in data.columns else 0
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <p style="margin:0; font-size:0.9rem; opacity:0.9;">Active Sites</p>
                <h2 style="margin:0; font-size:2rem;">{active_sites}</h2>
                <p style="margin:0; font-size:0.8rem;">{active_sites/total_sites*100:.1f}% dari total</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_uptime = data['uptime_percentage'].mean() if 'uptime_percentage' in data.columns else 0
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <p style="margin:0; font-size:0.9rem; opacity:0.9;">Avg Uptime</p>
                <h2 style="margin:0; font-size:2rem;">{avg_uptime:.1f}%</h2>
                <p style="margin:0; font-size:0.8rem;">Target: 99.9%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_alerts = data['alert_count'].sum() if 'alert_count' in data.columns else 0
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <p style="margin:0; font-size:0.9rem; opacity:0.9;">Total Alerts</p>
                <h2 style="margin:0; font-size:2rem;">{total_alerts}</h2>
                <p style="margin:0; font-size:0.8rem;">Critical: {len(data[data['alert_count'] > filters.get('alert_threshold', 3)])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                ModernCharts.status_distribution(data),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                ModernCharts.uptime_by_region(data),
                use_container_width=True
            )
        
        # Second row of charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                ModernCharts.bandwidth_usage(data),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                ModernCharts.alerts_timeline(data),
                use_container_width=True
            )
        
        # Recent Alerts Table
        st.markdown("### ⚠️ Recent Alerts")
        alerts_data = data[data['alert_count'] > filters.get('alert_threshold', 3)].head(5)
        
        if not alerts_data.empty:
            # Styling table
            st.dataframe(
                alerts_data[['site_name', 'region', 'alert_count', 'status']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "site_name": "Site Name",
                    "region": "Region",
                    "alert_count": st.column_config.NumberColumn(
                        "Alerts",
                        format="%d ⚠️"
                    ),
                    "status": st.column_config.TextColumn(
                        "Status",
                        help="Current site status"
                    )
                }
            )
        else:
            st.success("✨ No critical alerts at the moment!")

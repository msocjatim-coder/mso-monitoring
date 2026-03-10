import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class ModernCharts:
    @staticmethod
    def status_distribution(data):
        """Pie chart distribusi status"""
        status_counts = data['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        colors = {'Active': '#10b981', 'Maintenance': '#f59e0b', 'Down': '#ef4444'}
        
        fig = px.pie(
            status_counts, 
            values='count', 
            names='status',
            title='📊 Status Distribution',
            color='status',
            color_discrete_map=colors
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def uptime_by_region(data):
        """Bar chart uptime per region"""
        region_uptime = data.groupby('region')['uptime_percentage'].mean().reset_index()
        
        fig = px.bar(
            region_uptime,
            x='region',
            y='uptime_percentage',
            title='📈 Uptime by Region',
            color='uptime_percentage',
            color_continuous_scale='Viridis',
            text_auto='.1f'
        )
        
        fig.update_traces(
            textposition='outside',
            marker_line_width=0,
            hovertemplate='<b>%{x}</b><br>Uptime: %{y:.1f}%<extra></extra>'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            coloraxis_showscale=False
        )
        
        return fig
    
    @staticmethod
    def bandwidth_usage(data):
        """Scatter plot bandwidth usage"""
        fig = px.scatter(
            data,
            x='site_name',
            y='bandwidth_usage',
            size='alert_count',
            color='status',
            title='🌐 Bandwidth Usage Distribution',
            color_discrete_map={'Active': '#10b981', 'Maintenance': '#f59e0b', 'Down': '#ef4444'},
            hover_data=['region']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', title='Bandwidth Usage (Mbps)'),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @staticmethod
    def alerts_timeline(data):
        """Line chart alerts timeline"""
        # Simulasi timeline data
        if 'created_at' in data.columns:
            data['created_at'] = pd.to_datetime(data['created_at'])
            alerts_over_time = data.groupby(pd.Grouper(key='created_at', freq='D'))['alert_count'].sum().reset_index()
        else:
            # Fallback jika tidak ada created_at
            return go.Figure()
        
        fig = px.line(
            alerts_over_time,
            x='created_at',
            y='alert_count',
            title='📅 Alerts Timeline',
            markers=True
        )
        
        fig.update_traces(
            line=dict(color='#ef4444', width=3),
            marker=dict(size=8, color='#ef4444'),
            hovertemplate='<b>%{x|%d %b}</b><br>Alerts: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, title='Date'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', title='Number of Alerts')
        )
        
        return fig

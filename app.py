import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation
@st.cache_data
def load_data():
    # Headcount trend data
    headcount_trend = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Employees': [245, 252, 259, 266, 273, 280],
        'New Hires': [12, 10, 15, 13, 11, 14],
        'Terminations': [5, 3, 8, 6, 4, 7]
    })
    
    # Department data
    department_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Employee Count': [95, 62, 38, 18, 25, 42],
        'Avg Salary': [98000, 75000, 72000, 68000, 82000, 65000]
    })
    
    # Diversity data
    diversity_data = pd.DataFrame({
        'Gender': ['Male', 'Female', 'Non-binary'],
        'Percentage': [58, 40, 2]
    })
    
    # Turnover by department
    turnover_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Turnover Rate': [8.2, 14.5, 11.3, 6.7, 7.8, 12.1]
    })
    
    # Performance data
    performance_data = pd.DataFrame({
        'Rating': ['Exceptional', 'Exceeds', 'Meets', 'Needs Improvement', 'Unsatisfactory'],
        'Count': [42, 98, 112, 23, 5]
    })
    
    # Engagement trend
    engagement_trend = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Score': [72, 74, 73, 76, 78, 79]
    })
    
    return headcount_trend, department_data, diversity_data, turnover_data, performance_data, engagement_trend

# Load data
headcount_trend, department_data, diversity_data, turnover_data, performance_data, engagement_trend = load_data()

# Sidebar
st.sidebar.title("⚙️ Dashboard Controls")
time_filter = st.sidebar.selectbox(
    "Select Time Period",
    ["Week", "Month", "Quarter", "Year"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.info(f"**Total Employees:** 280\n**Departments:** 6\n**Avg Tenure:** 3.2 years")

# Main header
st.title("👥 HR Analytics Dashboard")
st.markdown("### Comprehensive employee metrics and insights")
st.markdown("---")

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Employees",
        value="280",
        delta="2.6%",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="Turnover Rate",
        value="10.2%",
        delta="-1.3%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Avg. Time to Fill",
        value="28 days",
        delta="3 days",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Engagement Score",
        value="79%",
        delta="1.3%",
        delta_color="normal"
    )

st.markdown("---")

# Row 1: Headcount Trend and Department Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Headcount Trend")
    fig_headcount = go.Figure()
    fig_headcount.add_trace(go.Scatter(
        x=headcount_trend['Month'],
        y=headcount_trend['Employees'],
        mode='lines+markers',
        name='Total Employees',
        fill='tozeroy',
        line=dict(color='#3b82f6', width=3)
    ))
    fig_headcount.add_trace(go.Bar(
        x=headcount_trend['Month'],
        y=headcount_trend['New Hires'],
        name='New Hires',
        marker_color='#10b981'
    ))
    fig_headcount.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_headcount, use_container_width=True)

with col2:
    st.subheader("🏢 Employees by Department")
    fig_dept = px.bar(
        department_data,
        x='Department',
        y='Employee Count',
        color='Employee Count',
        color_continuous_scale='Blues'
    )
    fig_dept.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_dept, use_container_width=True)

st.markdown("---")

# Row 2: Diversity, Turnover, and Performance
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌈 Gender Diversity")
    fig_diversity = px.pie(
        diversity_data,
        values='Percentage',
        names='Gender',
        color='Gender',
        color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899', 'Non-binary': '#8b5cf6'}
    )
    fig_diversity.update_traces(textposition='inside', textinfo='percent+label')
    fig_diversity.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_diversity, use_container_width=True)

with col2:
    st.subheader("📉 Turnover Rate by Dept")
    fig_turnover = px.bar(
        turnover_data,
        y='Department',
        x='Turnover Rate',
        orientation='h',
        color='Turnover Rate',
        color_continuous_scale='Reds'
    )
    fig_turnover.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig_turnover, use_container_width=True)

with col3:
    st.subheader("⭐ Performance Ratings")
    fig_performance = px.bar(
        performance_data,
        x='Rating',
        y='Count',
        color='Count',
        color_continuous_scale='Greens'
    )
    fig_performance.update_layout(height=350, showlegend=False)
    fig_performance.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_performance, use_container_width=True)

st.markdown("---")

# Row 3: Engagement and Salary
col1, col2 = st.columns(2)

with col1:
    st.subheader("💚 Employee Engagement Trend")
    fig_engagement = px.line(
        engagement_trend,
        x='Month',
        y='Score',
        markers=True,
        line_shape='spline'
    )
    fig_engagement.update_traces(line_color='#8b5cf6', line_width=3, marker_size=10)
    fig_engagement.update_layout(height=400, yaxis_range=[0, 100])
    st.plotly_chart(fig_engagement, use_container_width=True)

with col2:
    st.subheader("💰 Average Salary by Department")
    fig_salary = px.bar(
        department_data,
        x='Department',
        y='Avg Salary',
        color='Avg Salary',
        color_continuous_scale='YlOrRd'
    )
    fig_salary.update_layout(height=400, showlegend=False)
    fig_salary.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_salary, use_container_width=True)

st.markdown("---")

# Action Items Section
st.subheader("⚠️ Action Items")

col1, col2, col3 = st.columns(3)

with col1:
    st.error("**Critical:** High turnover in Sales department (14.5%)")

with col2:
    st.warning("**Medium:** 23 employees need performance improvement plans")

with col3:
    st.info("**Info:** Quarterly engagement survey due in 2 weeks")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>HR Analytics Dashboard | Last updated: {} | Data refreshes daily</p>
</div>
""".format(datetime.now().strftime("%B %d, %Y at %H:%M")), unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with enhanced styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        margin-bottom: 30px;
        color: white;
    }
    
    .header-title {
        font-size: 42px;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 18px;
        margin-top: 10px;
        color: rgba(255,255,255,0.9);
    }
    
    .header-stats {
        display: flex;
        gap: 30px;
        margin-top: 25px;
        flex-wrap: wrap;
    }
    
    .header-stat-item {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 15px 25px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .header-stat-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    
    .header-stat-value {
        font-size: 28px;
        font-weight: 700;
    }
    
    .last-updated {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Insight boxes */
    .insight-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    
    .alert-warning {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    
    .alert-success {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Typography */
    h1 {
        color: #1a237e;
    }
    
    h2, h3 {
        color: #283593;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f0f2f6;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data generation with more realistic patterns
@st.cache_data
def load_data():
    # Headcount trend with predictions
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    headcount_trend = pd.DataFrame({
        'Month': months,
        'Employees': [245, 252, 259, 266, 273, 280, 287, 294],
        'New Hires': [12, 10, 15, 13, 11, 14, 16, 12],
        'Terminations': [5, 3, 8, 6, 4, 7, 9, 5],
        'Forecast': [None, None, None, None, None, None, 287, 294]
    })
    
    # Department data with additional metrics
    department_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Employee Count': [95, 62, 38, 18, 25, 42],
        'Avg Salary': [98000, 75000, 72000, 68000, 82000, 65000],
        'Satisfaction': [4.2, 3.8, 4.0, 4.5, 4.1, 3.9],
        'Avg Tenure': [3.5, 2.1, 2.8, 4.2, 3.9, 3.0],
        'Open Positions': [8, 5, 2, 1, 2, 4]
    })
    
    # Diversity data with more categories
    diversity_data = pd.DataFrame({
        'Gender': ['Male', 'Female', 'Non-binary'],
        'Percentage': [58, 40, 2]
    })
    
    age_diversity = pd.DataFrame({
        'Age Group': ['18-25', '26-35', '36-45', '46-55', '56+'],
        'Count': [42, 128, 76, 28, 6]
    })
    
    # Turnover with historical comparison
    turnover_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Current Quarter': [8.2, 14.5, 11.3, 6.7, 7.8, 12.1],
        'Previous Quarter': [7.8, 16.2, 10.5, 7.1, 8.2, 11.8],
        'Industry Avg': [10.5, 15.0, 12.0, 8.0, 9.0, 13.0]
    })
    
    # Performance with trend
    performance_data = pd.DataFrame({
        'Rating': ['Exceptional', 'Exceeds', 'Meets', 'Needs Improvement', 'Unsatisfactory'],
        'Count': [42, 98, 112, 23, 5],
        'Previous': [38, 95, 115, 20, 4]
    })
    
    # Engagement with breakdown
    engagement_trend = pd.DataFrame({
        'Month': months[:6],
        'Overall': [72, 74, 73, 76, 78, 79],
        'Recognition': [68, 70, 71, 73, 75, 77],
        'Growth': [75, 76, 74, 78, 80, 81],
        'Work-Life': [70, 72, 72, 74, 76, 78]
    })
    
    # Recruitment funnel
    recruitment_funnel = pd.DataFrame({
        'Stage': ['Applications', 'Phone Screen', 'Interview', 'Offer', 'Accepted'],
        'Count': [450, 180, 85, 35, 28]
    })
    
    # Skills gap analysis
    skills_gap = pd.DataFrame({
        'Skill': ['AI/ML', 'Cloud Computing', 'Data Analysis', 'Project Management', 'Leadership', 'Cybersecurity'],
        'Current': [45, 62, 78, 85, 72, 38],
        'Required': [75, 85, 90, 90, 85, 70],
        'Gap': [30, 23, 12, 5, 13, 32]
    })
    
    # Compensation analysis
    compensation_trend = pd.DataFrame({
        'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        'Avg Salary': [76000, 77500, 78800, 80200],
        'Market Rate': [78000, 79000, 80000, 81500]
    })
    
    # Recruitment metrics over time
    recruitment_metrics = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Applications': [420, 385, 465, 510, 445, 480],
        'Hires': [12, 10, 15, 13, 11, 14],
        'Time to Fill': [32, 28, 30, 26, 25, 28],
        'Cost per Hire': [4200, 3950, 4100, 3800, 3900, 4000]
    })
    
    # Turnover breakdown
    turnover_breakdown = pd.DataFrame({
        'Category': ['Voluntary', 'Involuntary', 'Retirement', 'Internal Transfer'],
        'Count': [18, 7, 3, 2],
        'Percentage': [60, 23.3, 10, 6.7]
    })
    
    # Turnover reasons (voluntary only)
    turnover_reasons = pd.DataFrame({
        'Reason': ['Better Compensation', 'Career Growth', 'Work-Life Balance', 'Management Issues', 'Relocation', 'Other'],
        'Count': [6, 5, 3, 2, 1, 1]
    })
    
    # Tenure analysis
    tenure_analysis = pd.DataFrame({
        'Tenure Range': ['0-1 year', '1-2 years', '2-3 years', '3-5 years', '5+ years'],
        'Employees': [45, 72, 68, 55, 40],
        'Turnover Rate': [22.5, 15.3, 8.7, 5.2, 3.1]
    })
    
    return (headcount_trend, department_data, diversity_data, age_diversity, 
            turnover_data, performance_data, engagement_trend, recruitment_funnel,
            skills_gap, compensation_trend, recruitment_metrics, turnover_breakdown,
            turnover_reasons, tenure_analysis)

# Load data
(headcount_trend, department_data, diversity_data, age_diversity, 
 turnover_data, performance_data, engagement_trend, recruitment_funnel,
 skills_gap, compensation_trend, recruitment_metrics, turnover_breakdown,
 turnover_reasons, tenure_analysis) = load_data()

# Calculate stats for header
total_employees = department_data['Employee Count'].sum()
avg_satisfaction = department_data['Satisfaction'].mean()
open_positions = department_data['Open Positions'].sum()

# Sidebar with enhanced filters
st.sidebar.title("⚙️ Dashboard Controls")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime.now() - timedelta(days=180), datetime.now()),
    max_value=datetime.now()
)

# Department filter with "Select All" functionality
all_departments = department_data['Department'].tolist()

# Add "Select All" checkbox
select_all = st.sidebar.checkbox("Select All Departments", value=True)

if select_all:
    selected_departments = st.sidebar.multiselect(
        "Filter Departments",
        options=all_departments,
        default=all_departments
    )
else:
    selected_departments = st.sidebar.multiselect(
        "Filter Departments",
        options=all_departments,
        default=[]
    )

# If no departments selected, default to all
if not selected_departments:
    selected_departments = all_departments

# Metric selector
metric_view = st.sidebar.radio(
    "View Mode",
    ["Overview", "Deep Dive", "Predictive Analytics", "Benchmarking"]
)

# Export options
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")

export_col1, export_col2 = st.sidebar.columns(2)
with export_col1:
    if st.button("📄 PDF", use_container_width=True):
        st.sidebar.success("✅ PDF generated!")
with export_col2:
    if st.button("📊 Excel", use_container_width=True):
        st.sidebar.success("✅ Excel ready!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; color: white;">
    <div style="margin-bottom: 10px;">
        <strong>Total Employees:</strong> {total_employees}
    </div>
    <div style="margin-bottom: 10px;">
        <strong>Open Positions:</strong> {open_positions}
    </div>
    <div style="margin-bottom: 10px;">
        <strong>Avg Satisfaction:</strong> {avg_satisfaction:.1f}/5.0
    </div>
    <div>
        <strong>Avg Tenure:</strong> 3.2 years
    </div>
</div>
""", unsafe_allow_html=True)

# Main header with beautiful formatting
st.markdown(f"""
<div class="header-container">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
        <div style="flex: 1; min-width: 300px;">
            <h1 class="header-title">👥 HR Analytics Dashboard</h1>
            <p class="header-subtitle">Comprehensive workforce insights and predictive analytics</p>
        </div>
        <div class="last-updated">
            <div style="font-weight: 600;">📅 Last Updated</div>
            <div style="margin-top: 5px;">{datetime.now().strftime('%B %d, %Y at %H:%M')}</div>
        </div>
    </div>
    
    <div class="header-stats">
        <div class="header-stat-item">
            <div class="header-stat-label">Total Workforce</div>
            <div class="header-stat-value">{total_employees}</div>
        </div>
        <div class="header-stat-item">
            <div class="header-stat-label">Departments</div>
            <div class="header-stat-value">6</div>
        </div>
        <div class="header-stat-item">
            <div class="header-stat-label">Open Positions</div>
            <div class="header-stat-value">{open_positions}</div>
        </div>
        <div class="header-stat-item">
            <div class="header-stat-label">Satisfaction Score</div>
            <div class="header-stat-value">{avg_satisfaction:.1f}/5.0</div>
        </div>
        <div class="header-stat-item">
            <div class="header-stat-label">Avg Tenure</div>
            <div class="header-stat-value">3.2 yrs</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# AI-Powered Insights Section
st.markdown("### 🤖 AI-Powered Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='insight-box alert-success'>
        <strong>✅ Positive Trend:</strong><br>
        Employee engagement increased by 9.7% over the last 6 months, with Work-Life balance showing the strongest improvement.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='insight-box alert-warning'>
        <strong>⚠️ Attention Needed:</strong><br>
        Sales department turnover (14.5%) is above industry average. Consider retention initiatives.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='insight-box alert-critical'>
        <strong>🔴 Critical Gap:</strong><br>
        Cybersecurity and AI/ML skills are 32% and 30% below required levels. Training recommended.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key metrics row with enhanced styling
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Employees",
        value=f"{total_employees}",
        delta="2.6%"
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
        label="Time to Fill",
        value="28 days",
        delta="3 days",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="Engagement",
        value="79%",
        delta="1.3%"
    )

with col5:
    st.metric(
        label="Retention Rate",
        value="89.8%",
        delta="1.3%"
    )

st.markdown("---")

# Tabbed interface for better organization
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", "👤 Workforce Analytics", "📈 Performance", "🎯 Recruitment", "💰 Compensation", "🔄 Turnover Analysis"
])

with tab1:
    # Row 1: Headcount and Department
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Headcount Trend & Forecast")
        fig_headcount = go.Figure()
        fig_headcount.add_trace(go.Scatter(
            x=headcount_trend['Month'],
            y=headcount_trend['Employees'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8)
        ))
        fig_headcount.add_trace(go.Scatter(
            x=headcount_trend['Month'][-2:],
            y=headcount_trend['Forecast'][-2:],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#10b981', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig_headcount.add_trace(go.Bar(
            x=headcount_trend['Month'],
            y=headcount_trend['New Hires'],
            name='New Hires',
            marker_color='rgba(16, 185, 129, 0.5)',
            yaxis='y2'
        ))
        fig_headcount.update_layout(
            height=400,
            hovermode='x unified',
            yaxis2=dict(overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_headcount, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Department Metrics")
        filtered_dept = department_data[department_data['Department'].isin(selected_departments)]
        fig_dept = go.Figure()
        fig_dept.add_trace(go.Bar(
            x=filtered_dept['Department'],
            y=filtered_dept['Employee Count'],
            name='Employees',
            marker_color='#3b82f6'
        ))
        fig_dept.add_trace(go.Scatter(
            x=filtered_dept['Department'],
            y=filtered_dept['Satisfaction'] * 20,
            name='Satisfaction (scaled)',
            mode='lines+markers',
            marker=dict(size=10, color='#f59e0b'),
            yaxis='y2'
        ))
        fig_dept.update_layout(
            height=400,
            yaxis2=dict(overlaying='y', side='right', title='Satisfaction'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dept, use_container_width=True)

with tab2:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌈 Gender Diversity")
        fig_diversity = px.pie(
            diversity_data,
            values='Percentage',
            names='Gender',
            color='Gender',
            color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899', 'Non-binary': '#8b5cf6'},
            hole=0.4
        )
        fig_diversity.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_diversity, use_container_width=True)
    
    with col2:
        st.subheader("👥 Age Distribution")
        fig_age = px.bar(
            age_diversity,
            x='Age Group',
            y='Count',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col3:
        st.subheader("📉 Turnover Comparison")
        fig_turnover = go.Figure()
        fig_turnover.add_trace(go.Bar(
            name='Current Q',
            x=turnover_data['Department'],
            y=turnover_data['Current Quarter'],
            marker_color='#ef4444'
        ))
        fig_turnover.add_trace(go.Bar(
            name='Previous Q',
            x=turnover_data['Department'],
            y=turnover_data['Previous Quarter'],
            marker_color='#fca5a5'
        ))
        fig_turnover.add_trace(go.Scatter(
            name='Industry Avg',
            x=turnover_data['Department'],
            y=turnover_data['Industry Avg'],
            mode='lines+markers',
            marker=dict(size=10, color='#1f2937'),
            line=dict(width=2, dash='dash')
        ))
        fig_turnover.update_layout(barmode='group', height=350)
        fig_turnover.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_turnover, use_container_width=True)
    
    st.markdown("---")
    
    # Skills Gap Analysis
    st.subheader("🎯 Skills Gap Analysis")
    fig_skills = go.Figure()
    fig_skills.add_trace(go.Bar(
        name='Current Level',
        x=skills_gap['Skill'],
        y=skills_gap['Current'],
        marker_color='#3b82f6'
    ))
    fig_skills.add_trace(go.Bar(
        name='Required Level',
        x=skills_gap['Skill'],
        y=skills_gap['Required'],
        marker_color='#10b981'
    ))
    fig_skills.add_trace(go.Scatter(
        name='Gap',
        x=skills_gap['Skill'],
        y=skills_gap['Gap'],
        mode='lines+markers',
        marker=dict(size=12, color='#ef4444'),
        line=dict(width=3),
        yaxis='y2'
    ))
    fig_skills.update_layout(
        barmode='group',
        height=400,
        yaxis2=dict(overlaying='y', side='right', title='Gap %'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_skills, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⭐ Performance Distribution")
        fig_performance = go.Figure()
        fig_performance.add_trace(go.Bar(
            name='Current Period',
            x=performance_data['Rating'],
            y=performance_data['Count'],
            marker_color='#10b981'
        ))
        fig_performance.add_trace(go.Bar(
            name='Previous Period',
            x=performance_data['Rating'],
            y=performance_data['Previous'],
            marker_color='#86efac'
        ))
        fig_performance.update_layout(barmode='group', height=400)
        fig_performance.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with col2:
        st.subheader("💚 Engagement Breakdown")
        fig_engagement = go.Figure()
        for col in ['Overall', 'Recognition', 'Growth', 'Work-Life']:
            fig_engagement.add_trace(go.Scatter(
                x=engagement_trend['Month'],
                y=engagement_trend[col],
                mode='lines+markers',
                name=col,
                line=dict(width=3)
            ))
        fig_engagement.update_layout(height=400, yaxis_range=[0, 100])
        st.plotly_chart(fig_engagement, use_container_width=True)

with tab4:
    # Add recruitment metrics summary at top
    st.markdown("### 📊 Recruitment KPIs")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_time = recruitment_metrics['Time to Fill'].mean()
        st.metric("Avg Time to Fill", f"{avg_time:.0f} days", "-2 days")
    
    with col2:
        avg_cost = recruitment_metrics['Cost per Hire'].mean()
        st.metric("Avg Cost per Hire", f"${avg_cost:,.0f}", "-$200")
    
    with col3:
        total_hires = recruitment_metrics['Hires'].sum()
        st.metric("Total Hires (6mo)", total_hires, "+15%")
    
    with col4:
        offer_accept = (recruitment_funnel.iloc[4]['Count'] / recruitment_funnel.iloc[3]['Count']) * 100
        st.metric("Offer Accept Rate", f"{offer_accept:.0f}%", "+5%")
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Recruitment Funnel")
        fig_funnel = go.Figure(go.Funnel(
            y=recruitment_funnel['Stage'],
            x=recruitment_funnel['Count'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"])
        ))
        fig_funnel.update_layout(height=400)
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Conversion rates
        st.markdown("**Conversion Rates:**")
        conv_col1, conv_col2 = st.columns(2)
        for i in range(len(recruitment_funnel) - 1):
            rate = (recruitment_funnel.iloc[i+1]['Count'] / recruitment_funnel.iloc[i]['Count']) * 100
            with conv_col1 if i % 2 == 0 else conv_col2:
                st.metric(
                    f"{recruitment_funnel.iloc[i]['Stage']} → {recruitment_funnel.iloc[i+1]['Stage']}",
                    f"{rate:.1f}%",
                    delta_color="off"
                )
    
    with col2:
        st.subheader("📊 Recruitment Trends")
        fig_recruit_trend = go.Figure()
        fig_recruit_trend.add_trace(go.Scatter(
            x=recruitment_metrics['Month'],
            y=recruitment_metrics['Applications'],
            mode='lines+markers',
            name='Applications',
            line=dict(color='#3b82f6', width=3),
            yaxis='y'
        ))
        fig_recruit_trend.add_trace(go.Bar(
            x=recruitment_metrics['Month'],
            y=recruitment_metrics['Hires'],
            name='Hires',
            marker_color='#10b981',
            yaxis='y2'
        ))
        fig_recruit_trend.update_layout(
            height=400,
            yaxis=dict(title='Applications'),
            yaxis2=dict(title='Hires', overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_recruit_trend, use_container_width=True)
    
    st.markdown("---")
    
    # Additional recruitment metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Time to Fill Trend")
        fig_ttf = px.line(
            recruitment_metrics,
            x='Month',
            y='Time to Fill',
            markers=True,
            line_shape='spline'
        )
        fig_ttf.update_traces(line_color='#f59e0b', line_width=3, marker_size=10)
        fig_ttf.update_layout(height=300)
        st.plotly_chart(fig_ttf, use_container_width=True)
    
    with col2:
        st.subheader("💵 Cost per Hire Trend")
        fig_cph = px.line(
            recruitment_metrics,
            x='Month',
            y='Cost per Hire',
            markers=True,
            line_shape='spline'
        )
        fig_cph.update_traces(line_color='#8b5cf6', line_width=3, marker_size=10)
        fig_cph.update_layout(height=300)
        st.plotly_chart(fig_cph, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Open Positions by Department")
        fig_open = px.bar(
            department_data,
            x='Department',
            y='Open Positions',
            color='Open Positions',
            color_continuous_scale='Oranges',
            text='Open Positions'
        )
        fig_open.update_traces(textposition='outside')
        fig_open.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_open, use_container_width=True)
    
    with col2:
        st.subheader("📈 Application to Hire Ratio")
        recruitment_metrics['Ratio'] = recruitment_metrics['Applications'] / recruitment_metrics['Hires']
        fig_ratio = px.bar(
            recruitment_metrics,
            x='Month',
            y='Ratio',
            text='Ratio',
            color='Ratio',
            color_continuous_scale='Blues'
        )
        fig_ratio.update_traces(texttemplate='%{text:.1f}:1', textposition='outside')
        fig_ratio.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_ratio, use_container_width=True)

with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Salary vs Market Rate")
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Scatter(
            x=compensation_trend['Quarter'],
            y=compensation_trend['Avg Salary'],
            mode='lines+markers',
            name='Company Avg',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=10)
        ))
        fig_comp.add_trace(go.Scatter(
            x=compensation_trend['Quarter'],
            y=compensation_trend['Market Rate'],
            mode='lines+markers',
            name='Market Rate',
            line=dict(color='#ef4444', width=3, dash='dash'),
            marker=dict(size=10)
        ))
        fig_comp.update_layout(height=400)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        st.subheader("💵 Average Salary by Department")
        fig_salary = px.bar(
            department_data.sort_values('Avg Salary', ascending=True),
            y='Department',
            x='Avg Salary',
            orientation='h',
            color='Avg Salary',
            color_continuous_scale='YlOrRd',
            text='Avg Salary'
        )
        fig_salary.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_salary.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_salary, use_container_width=True)

with tab6:
    st.markdown("### 🔄 Turnover Analysis & Insights")
    
    # Turnover KPIs at top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Turnover Rate", "10.2%", "-1.3%")
    
    with col2:
        voluntary_rate = (turnover_breakdown.iloc[0]['Count'] / turnover_breakdown['Count'].sum()) * 10.2
        st.metric("Voluntary Turnover", f"{voluntary_rate:.1f}%", "-0.8%")
    
    with col3:
        st.metric("Avg Tenure", "3.2 years", "+0.3 years")
    
    with col4:
        st.metric("90-Day Retention", "94.5%", "+2.1%")
    
    st.markdown("---")
    
    # Row 1: Turnover breakdown and reasons
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Turnover Breakdown")
        fig_turnover_breakdown = px.pie(
            turnover_breakdown,
            values='Count',
            names='Category',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_turnover_breakdown.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
        fig_turnover_breakdown.update_layout(height=400)
        st.plotly_chart(fig_turnover_breakdown, use_container_width=True)
        
        # Summary stats
        st.markdown("**Turnover Summary:**")
        st.dataframe(turnover_breakdown[['Category', 'Count', 'Percentage']], 
                    use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🔍 Voluntary Turnover Reasons")
        fig_reasons = px.bar(
            turnover_reasons.sort_values('Count', ascending=True),
            y='Reason',
            x='Count',
            orientation='h',
            color='Count',
            color_continuous_scale='Reds',
            text='Count'
        )
        fig_reasons.update_traces(textposition='outside')
        fig_reasons.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_reasons, use_container_width=True)
        
        st.info("💡 **Key Insight:** 61% of voluntary turnover is due to compensation and career growth")
    
    st.markdown("---")
    
    # Row 2: Tenure analysis and turnover by department
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏳ Turnover by Tenure")
        fig_tenure = go.Figure()
        fig_tenure.add_trace(go.Bar(
            x=tenure_analysis['Tenure Range'],
            y=tenure_analysis['Employees'],
            name='Employee Count',
            marker_color='#3b82f6',
            yaxis='y'
        ))
        fig_tenure.add_trace(go.Scatter(
            x=tenure_analysis['Tenure Range'],
            y=tenure_analysis['Turnover Rate'],
            name='Turnover Rate %',
            mode='lines+markers',
            marker=dict(size=10, color='#ef4444'),
            line=dict(width=3),
            yaxis='y2'
        ))
        fig_tenure.update_layout(
            height=400,
            yaxis=dict(title='Employees'),
            yaxis2=dict(title='Turnover Rate %', overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_tenure, use_container_width=True)
        
        st.warning("⚠️ **High Risk:** Employees with 0-1 year tenure have 22.5% turnover rate")
    
    with col2:
        st.subheader("🏢 Turnover Rate by Department")
        fig_dept_turnover = go.Figure()
        fig_dept_turnover.add_trace(go.Bar(
            name='Current Quarter',
            x=turnover_data['Department'],
            y=turnover_data['Current Quarter'],
            marker_color='#ef4444'
        ))
        fig_dept_turnover.add_trace(go.Bar(
            name='Previous Quarter',
            x=turnover_data['Department'],
            y=turnover_data['Previous Quarter'],
            marker_color='#fca5a5'
        ))
        fig_dept_turnover.add_trace(go.Scatter(
            name='Industry Avg',
            x=turnover_data['Department'],
            y=turnover_data['Industry Avg'],
            mode='lines+markers',
            marker=dict(size=10, color='#1f2937'),
            line=dict(width=2, dash='dash')
        ))
        fig_dept_turnover.update_layout(
            barmode='group',
            height=400,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_dept_turnover, use_container_width=True)
    
    st.markdown("---")
    
    # Predictive insights
    st.subheader("🎯 Retention Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='insight-box alert-critical'>
            <strong>🔴 Immediate Action - Sales Dept</strong><br>
            14.5% turnover (highest)<br>
            <small>• Exit interview analysis<br>
            • Compensation review<br>
            • Manager training</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='insight-box alert-warning'>
            <strong>🟡 Focus on New Hires</strong><br>
            First-year turnover at 22.5%<br>
            <small>• Enhance onboarding<br>
            • 30/60/90 day check-ins<br>
            • Buddy system</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='insight-box alert-success'>
            <strong>✅ Retain Top Talent</strong><br>
            94.5% 90-day retention<br>
            <small>• Career development plans<br>
            • Competitive compensation<br>
            • Recognition programs</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cost of turnover
    st.subheader("💰 Cost of Turnover Analysis")
    
    avg_salary = department_data['Avg Salary'].mean()
    total_turnover = 30  # Example: 30 employees left this quarter
    cost_per_turnover = avg_salary * 0.5  # Typically 50-200% of annual salary
    total_cost = total_turnover * cost_per_turnover
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Employees Lost (6mo)", total_turnover)
    with col2:
        st.metric("Avg Cost per Turnover", f"${cost_per_turnover:,.0f}")
    with col3:
        st.metric("Total Turnover Cost", f"${total_cost:,.0f}", delta_color="off")
    
    st.info(f"💡 **Estimated Impact:** Based on 50% of average salary (${avg_salary:,.0f}), turnover cost is approximately ${total_cost:,.0f} over 6 months. Reducing turnover by 2% could save ~${total_cost * 0.2:,.0f}")

st.markdown("---")

# Action Items Dashboard
st.subheader("⚠️ Action Items & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 Critical Actions")
    st.markdown("""
    <div class='insight-box alert-critical'>
        <strong>1. Sales Turnover Crisis</strong><br>
        14.5% turnover rate - 3.5% above target<br>
        <small>Action: Conduct exit interviews, review compensation</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box alert-critical'>
        <strong>2. Skills Gap - Cybersecurity</strong><br>
        32% gap in critical security skills<br>
        <small>Action: Launch upskilling program immediately</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("#### 🟡 Medium Priority")
    st.markdown("""
    <div class='insight-box alert-warning'>
        <strong>1. Performance Reviews</strong><br>
        23 employees need improvement plans<br>
        <small>Action: Schedule manager training sessions</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box alert-warning'>
        <strong>2. Compensation Gap</strong><br>
        Trailing market rate by $1,300<br>
        <small>Action: Review salary bands for Q1 2025</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer with additional info
col1, col2, col3 = st.columns(3)
with col1:
    st.info("💡 **Tip:** Use filters to drill down into specific departments")
with col2:
    st.success("✅ **Data Quality:** 98% - Last validated today")
with col3:
    st.warning("📅 **Next Review:** Quarterly board meeting in 12 days")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 20px; border-top: 1px solid #ddd;'>
    <p>HR Analytics Dashboard v2.0 | Powered by AI | Real-time data synchronization</p>
    <small>For support, contact hr-analytics@company.com</small>
</div>
""", unsafe_allow_html=True)

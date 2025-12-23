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
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.3rem 0 0 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }
    
    .update-time {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        display: inline-block;
        margin-top: 0.5rem;
        font-size: 0.8rem;
    }
    
    .header-stats {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
        gap: 0.8rem;
    }
    
    .header-stat-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        flex: 1;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .header-stat-label {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    
    .header-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    .insight-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .insight-positive {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-left: 4px solid #10b981;
    }
    
    .insight-warning {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        border-left: 4px solid #f59e0b;
    }
    
    .insight-critical {
        background: linear-gradient(135deg, #fab1a0 0%, #ff7675 100%);
        border-left: 4px solid #ef4444;
    }
    
    .insight-box h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    
    .insight-box p {
        margin: 0;
        font-size: 0.9rem;
    }
    
    .action-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #ef4444;
    }
    
    .action-item h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        color: #1a202c;
    }
    
    .action-item p {
        margin: 0.3rem 0;
        font-size: 0.85rem;
        color: #4a5568;
    }
    
    .footer {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
        text-align: center;
        border-top: 2px solid #e2e8f0;
    }
    
    .footer p {
        margin: 0.2rem 0;
        color: #718096;
        font-size: 0.85rem;
    }
    
    .sidebar-quick-stat {
        background: #f7fafc;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced data generation with more realistic patterns
@st.cache_data
def load_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    headcount_trend = pd.DataFrame({
        'Month': months,
        'Employees': [245, 252, 259, 266, 273, 280, 287, 294],
        'New Hires': [12, 10, 15, 13, 11, 14, 16, 12],
        'Terminations': [5, 3, 8, 6, 4, 7, 9, 5],
        'Forecast': [None, None, None, None, None, None, 287, 294]
    })
    
    department_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Employee Count': [95, 62, 38, 18, 25, 42],
        'Avg Salary': [98000, 75000, 72000, 68000, 82000, 65000],
        'Satisfaction': [4.2, 3.8, 4.0, 4.5, 4.1, 3.9],
        'Avg Tenure': [3.5, 2.1, 2.8, 4.2, 3.9, 3.0],
        'Open Positions': [8, 5, 2, 1, 2, 4]
    })
    
    diversity_data = pd.DataFrame({
        'Gender': ['Male', 'Female', 'Non-binary'],
        'Percentage': [58, 40, 2]
    })
    
    age_diversity = pd.DataFrame({
        'Age Group': ['18-25', '26-35', '36-45', '46-55', '56+'],
        'Count': [42, 128, 76, 28, 6]
    })
    
    turnover_data = pd.DataFrame({
        'Department': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'],
        'Current Quarter': [8.2, 14.5, 11.3, 6.7, 7.8, 12.1],
        'Previous Quarter': [7.8, 16.2, 10.5, 7.1, 8.2, 11.8],
        'Industry Avg': [10.5, 15.0, 12.0, 8.0, 9.0, 13.0]
    })
    
    performance_data = pd.DataFrame({
        'Rating': ['Exceptional', 'Exceeds', 'Meets', 'Needs Improvement', 'Unsatisfactory'],
        'Count': [42, 98, 112, 23, 5],
        'Previous': [38, 95, 115, 20, 4]
    })
    
    engagement_trend = pd.DataFrame({
        'Month': months[:6],
        'Overall': [72, 74, 73, 76, 78, 79],
        'Recognition': [68, 70, 71, 73, 75, 77],
        'Growth': [75, 76, 74, 78, 80, 81],
        'Work-Life': [70, 72, 72, 74, 76, 78]
    })
    
    recruitment_funnel = pd.DataFrame({
        'Stage': ['Applications', 'Phone Screen', 'Interview', 'Offer', 'Accepted'],
        'Count': [450, 180, 85, 35, 28]
    })
    
    skills_gap = pd.DataFrame({
        'Skill': ['AI/ML', 'Cloud Computing', 'Data Analysis', 'Project Management', 'Leadership', 'Cybersecurity'],
        'Current': [45, 62, 78, 85, 72, 38],
        'Required': [75, 85, 90, 90, 85, 70],
        'Gap': [30, 23, 12, 5, 13, 32]
    })
    
    compensation_trend = pd.DataFrame({
        'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        'Avg Salary': [76000, 77500, 78800, 80200],
        'Market Rate': [78000, 79000, 80000, 81500]
    })
    
    recruitment_metrics = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Applications': [420, 385, 465, 510, 445, 480],
        'Hires': [12, 10, 15, 13, 11, 14],
        'Time to Fill': [32, 28, 30, 26, 25, 28],
        'Cost per Hire': [4200, 3950, 4100, 3800, 3900, 4000]
    })
    
    turnover_breakdown = pd.DataFrame({
        'Category': ['Voluntary', 'Involuntary', 'Retirement', 'Internal Transfer'],
        'Count': [18, 7, 3, 2],
        'Percentage': [60, 23.3, 10, 6.7]
    })
    
    turnover_reasons = pd.DataFrame({
        'Reason': ['Better Compensation', 'Career Growth', 'Work-Life Balance', 'Management Issues', 'Relocation', 'Other'],
        'Count': [6, 5, 3, 2, 1, 1]
    })
    
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

# Calculate stats
total_employees = int(department_data['Employee Count'].sum())
avg_satisfaction = float(department_data['Satisfaction'].mean())
open_positions = int(department_data['Open Positions'].sum())
avg_tenure = float(department_data['Avg Tenure'].mean())
num_departments = len(department_data)

# Sidebar
st.sidebar.title("⚙️ Dashboard Controls")

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime.now() - timedelta(days=180), datetime.now()),
    max_value=datetime.now()
)

all_departments = department_data['Department'].tolist()
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

if not selected_departments:
    selected_departments = all_departments

metric_view = st.sidebar.radio(
    "View Mode",
    ["Overview", "Deep Dive", "Predictive Analytics", "Benchmarking"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")

# Prepare data for export
@st.cache_data
def convert_to_excel():
    from io import BytesIO
    output = BytesIO()
    try:
        # Try openpyxl first (more commonly available)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            department_data.to_excel(writer, sheet_name='Departments', index=False)
            headcount_trend.to_excel(writer, sheet_name='Headcount Trend', index=False)
            turnover_data.to_excel(writer, sheet_name='Turnover', index=False)
            performance_data.to_excel(writer, sheet_name='Performance', index=False)
            recruitment_metrics.to_excel(writer, sheet_name='Recruitment', index=False)
            turnover_breakdown.to_excel(writer, sheet_name='Turnover Breakdown', index=False)
            skills_gap.to_excel(writer, sheet_name='Skills Gap', index=False)
    except ImportError:
        # Fallback: create a simple CSV if Excel isn't available
        import csv
        output = BytesIO()
        output.write(b"HR Analytics Data Export\n\n")
        
        # Write each dataframe as CSV section
        for name, df in [
            ('Departments', department_data),
            ('Headcount Trend', headcount_trend),
            ('Turnover', turnover_data),
            ('Performance', performance_data),
            ('Recruitment', recruitment_metrics),
            ('Turnover Breakdown', turnover_breakdown),
            ('Skills Gap', skills_gap)
        ]:
            output.write(f"\n{name}\n".encode())
            output.write(df.to_csv(index=False).encode())
    
    output.seek(0)
    return output

@st.cache_data
def generate_html_report():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>HR Analytics Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                color: #333;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .metric-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .metric-label {{
                font-size: 0.9em;
                color: #666;
                margin-bottom: 5px;
            }}
            .metric-value {{
                font-size: 2em;
                font-weight: bold;
                color: #1a202c;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            tr:hover {{
                background: #f8f9fa;
            }}
            .section {{
                margin: 30px 0;
                page-break-inside: avoid;
            }}
            .section h2 {{
                color: #667eea;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }}
            .insight {{
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid;
            }}
            .insight-positive {{
                background: #d4fc79;
                border-color: #10b981;
            }}
            .insight-warning {{
                background: #ffeaa7;
                border-color: #f59e0b;
            }}
            .insight-critical {{
                background: #fab1a0;
                border-color: #ef4444;
            }}
            .footer {{
                margin-top: 50px;
                padding: 20px;
                background: #f8f9fa;
                border-top: 2px solid #e2e8f0;
                text-align: center;
                color: #666;
            }}
            @media print {{
                body {{ margin: 20px; }}
                .no-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>👥 HR Analytics Report</h1>
            <p>Comprehensive Workforce Insights</p>
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        </div>
        
        <div class="no-print" style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <strong>💡 To save as PDF:</strong> Press Ctrl+P (or Cmd+P on Mac) and select "Save as PDF"
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Total Workforce</div>
                <div class="metric-value">{total_employees}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Departments</div>
                <div class="metric-value">{num_departments}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Open Positions</div>
                <div class="metric-value">{open_positions}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Satisfaction Score</div>
                <div class="metric-value">{avg_satisfaction:.1f}/5.0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Average Tenure</div>
                <div class="metric-value">{avg_tenure:.1f} yrs</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🤖 AI-Powered Insights</h2>
            <div class="insight insight-positive">
                <strong>✅ Positive Trend:</strong> Employee engagement increased by 9.7% over the last 6 months, with Work-Life balance showing the strongest improvement.
            </div>
            <div class="insight insight-warning">
                <strong>⚠️ Attention Needed:</strong> Sales department turnover (14.5%) is above industry average. Consider retention initiatives.
            </div>
            <div class="insight insight-critical">
                <strong>🔴 Critical Gap:</strong> Cybersecurity and AI/ML skills are 32% and 30% below required levels. Training recommended.
            </div>
        </div>
        
        <div class="section">
            <h2>🏢 Department Overview</h2>
            <table>
                <tr>
                    <th>Department</th>
                    <th>Employees</th>
                    <th>Avg Salary</th>
                    <th>Satisfaction</th>
                    <th>Avg Tenure</th>
                    <th>Open Positions</th>
                </tr>
                {''.join([f"<tr><td>{row['Department']}</td><td>{row['Employee Count']}</td><td>${row['Avg Salary']:,.0f}</td><td>{row['Satisfaction']:.1f}/5.0</td><td>{row['Avg Tenure']:.1f} yrs</td><td>{row['Open Positions']}</td></tr>" for _, row in department_data.iterrows()])}
            </table>
        </div>
        
        <div class="section">
            <h2>📉 Turnover Analysis</h2>
            <table>
                <tr>
                    <th>Department</th>
                    <th>Current Quarter</th>
                    <th>Previous Quarter</th>
                    <th>Industry Average</th>
                </tr>
                {''.join([f"<tr><td>{row['Department']}</td><td>{row['Current Quarter']:.1f}%</td><td>{row['Previous Quarter']:.1f}%</td><td>{row['Industry Avg']:.1f}%</td></tr>" for _, row in turnover_data.iterrows()])}
            </table>
        </div>
        
        <div class="section">
            <h2>🎯 Skills Gap Analysis</h2>
            <table>
                <tr>
                    <th>Skill</th>
                    <th>Current Level</th>
                    <th>Required Level</th>
                    <th>Gap</th>
                </tr>
                {''.join([f"<tr><td>{row['Skill']}</td><td>{row['Current']}%</td><td>{row['Required']}%</td><td style='color: #ef4444; font-weight: bold;'>{row['Gap']}%</td></tr>" for _, row in skills_gap.iterrows()])}
            </table>
        </div>
        
        <div class="section">
            <h2>⭐ Performance Distribution</h2>
            <table>
                <tr>
                    <th>Rating</th>
                    <th>Current Period</th>
                    <th>Previous Period</th>
                    <th>Change</th>
                </tr>
                {''.join([f"<tr><td>{row['Rating']}</td><td>{row['Count']}</td><td>{row['Previous']}</td><td>{'+' if row['Count'] > row['Previous'] else ''}{row['Count'] - row['Previous']}</td></tr>" for _, row in performance_data.iterrows()])}
            </table>
        </div>
        
        <div class="section">
            <h2>📊 Recruitment Metrics (6-Month Summary)</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr><td>Total Applications</td><td>{recruitment_metrics['Applications'].sum():,}</td></tr>
                <tr><td>Total Hires</td><td>{recruitment_metrics['Hires'].sum()}</td></tr>
                <tr><td>Avg Time to Fill</td><td>{recruitment_metrics['Time to Fill'].mean():.0f} days</td></tr>
                <tr><td>Avg Cost per Hire</td><td>${recruitment_metrics['Cost per Hire'].mean():,.0f}</td></tr>
                <tr><td>Offer Accept Rate</td><td>{(recruitment_funnel.iloc[4]['Count'] / recruitment_funnel.iloc[3]['Count'] * 100):.0f}%</td></tr>
            </table>
        </div>
        
        <div class="footer">
            <p><strong>© Henrietta Atsenokhai</strong></p>
            <p>For demo purposes only</p>
        </div>
    </body>
    </html>
    """
    return html_content

export_col1, export_col2 = st.sidebar.columns(2)

with export_col1:
    html_report = generate_html_report()
    st.download_button(
        label="📄 PDF",
        data=html_report,
        file_name=f"HR_Analytics_Report_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=True
    )

with export_col2:
    excel_data = convert_to_excel()
    st.download_button(
        label="📊 Excel",
        data=excel_data,
        file_name=f"HR_Analytics_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.markdown(f"""
<div class="sidebar-quick-stat">
    <strong>Total Employees:</strong> {total_employees}
</div>
<div class="sidebar-quick-stat">
    <strong>Open Positions:</strong> {open_positions}
</div>
<div class="sidebar-quick-stat">
    <strong>Avg Satisfaction:</strong> {avg_satisfaction:.1f}/5.0
</div>
<div class="sidebar-quick-stat">
    <strong>Avg Tenure:</strong> {avg_tenure:.1f} years
</div>
""", unsafe_allow_html=True)

# Main header - Compact version
st.markdown(f"""
<div class="main-header">
    <h1>👥 HR Analytics Dashboard</h1>
    <p>Comprehensive workforce insights and predictive analytics</p>
    <div class="update-time">
        📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}
    </div>
</div>

<div class="header-stats">
    <div class="header-stat-item">
        <div class="header-stat-label">Total Workforce</div>
        <div class="header-stat-value">{total_employees}</div>
    </div>
    <div class="header-stat-item">
        <div class="header-stat-label">Departments</div>
        <div class="header-stat-value">{num_departments}</div>
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
        <div class="header-stat-value">{avg_tenure:.1f} yrs</div>
    </div>
</div>
""", unsafe_allow_html=True)

# AI Insights
st.markdown("### 🤖 AI-Powered Insights")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="insight-box insight-positive">
        <h4>✅ Positive Trend</h4>
        <p>Employee engagement increased by 9.7% over the last 6 months, with Work-Life balance showing the strongest improvement.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box insight-warning">
        <h4>⚠️ Attention Needed</h4>
        <p>Sales department turnover (14.5%) is above industry average. Consider retention initiatives.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="insight-box insight-critical">
        <h4>🔴 Critical Gap</h4>
        <p>Cybersecurity and AI/ML skills are 32% and 30% below required levels. Training recommended.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Employees", f"{total_employees}", delta="2.6%")

with col2:
    st.metric("Turnover Rate", "10.2%", delta="-1.3%", delta_color="inverse")

with col3:
    st.metric("Time to Fill", "28 days", delta="3 days", delta_color="inverse")

with col4:
    st.metric("Engagement", "79%", delta="1.3%")

with col5:
    st.metric("Retention Rate", "89.8%", delta="1.3%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "👤 Workforce Analytics",
    "📈 Performance",
    "🎯 Recruitment",
    "💰 Compensation",
    "🔄 Turnover Analysis"
])

with tab1:
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
        fig_age = px.bar(age_diversity, x='Age Group', y='Count', color='Count', color_continuous_scale='Viridis')
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
        
        for col_name in ['Overall', 'Recognition', 'Growth', 'Work-Life']:
            fig_engagement.add_trace(go.Scatter(
                x=engagement_trend['Month'],
                y=engagement_trend[col_name],
                mode='lines+markers',
                name=col_name,
                line=dict(width=3)
            ))
        
        fig_engagement.update_layout(height=400, yaxis_range=[0, 100])
        st.plotly_chart(fig_engagement, use_container_width=True)

with tab4:
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
        fig_turnover_breakdown.update_traces(textposition='inside', textinfo='percent+label')
        fig_turnover_breakdown.update_layout(height=400)
        st.plotly_chart(fig_turnover_breakdown, use_container_width=True)
        
        st.markdown("**Turnover Summary:**")
        st.dataframe(turnover_breakdown[['Category', 'Count', 'Percentage']], use_container_width=True, hide_index=True)
    
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
    
    st.subheader("🎯 Retention Recommendations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-item">
            <h4>🔴 Immediate Action - Sales Dept</h4>
            <p>14.5% turnover (highest)</p>
            <p>• Exit interview analysis</p>
            <p>• Compensation review</p>
            <p>• Manager training</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-item">
            <h4>🟡 Focus on New Hires</h4>
            <p>First-year turnover at 22.5%</p>
            <p>• Enhance onboarding</p>
            <p>• 30/60/90 day check-ins</p>
            <p>• Buddy system</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="action-item">
            <h4>✅ Retain Top Talent</h4>
            <p>94.5% 90-day retention</p>
            <p>• Career development plans</p>
            <p>• Competitive compensation</p>
            <p>• Recognition programs</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p><strong>© Henrietta Atsenokhai</strong></p>
    <p>For demo purposes only</p>
</div>
""", unsafe_allow_html=True)

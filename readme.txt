# HR Analytics Dashboard 👥

A comprehensive, interactive HR analytics dashboard built with Streamlit that provides workforce insights, predictive analytics, and actionable recommendations for human resources management.

## Features

### 📊 Core Analytics
- **Headcount Trends & Forecasting** - Track employee growth with predictive forecasts
- **Department Metrics** - Analyze performance across all organizational units
- **AI-Powered Insights** - Automated identification of trends, risks, and opportunities
- **Real-time KPI Tracking** - Monitor key metrics like turnover, engagement, and satisfaction

### 📈 Six Comprehensive Tabs

1. **Overview** - High-level workforce trends and department comparisons
2. **Workforce Analytics** - Diversity metrics, age distribution, and skills gap analysis
3. **Performance** - Performance ratings and engagement breakdown over time
4. **Recruitment** - Funnel analysis, time-to-fill, cost-per-hire, and hiring trends
5. **Compensation** - Salary benchmarking and market rate comparisons
6. **Turnover Analysis** - Deep dive into attrition patterns with actionable recommendations

### 🎯 Key Capabilities

- **Interactive Filtering** - Filter by department and date range
- **Multiple View Modes** - Overview, Deep Dive, Predictive Analytics, and Benchmarking
- **Visual Analytics** - 20+ interactive charts and visualizations using Plotly
- **Export Options** - PDF and Excel export functionality
- **Responsive Design** - Clean, modern interface with gradient styling
- **Predictive Insights** - AI-generated recommendations and risk alerts

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download the repository:
```bash
git clone <repository-url>
cd hr-analytics-dashboard
```

2. Install required dependencies:
```bash
pip install streamlit pandas plotly numpy
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Requirements.txt
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

## Usage

### Running the Dashboard

1. Navigate to the project directory:
```bash
cd hr-analytics-dashboard
```

2. Launch the Streamlit app:
```bash
streamlit run app.py
```

3. The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Dashboard Navigation

**Sidebar Controls:**
- **Date Range Selector** - Filter data by time period
- **Department Filter** - Select specific departments or view all
- **View Mode** - Switch between different analytical perspectives
- **Export Options** - Generate PDF or Excel reports
- **Quick Stats** - At-a-glance key metrics

**Main Interface:**
- **Header Statistics** - Total workforce, departments, open positions, satisfaction, and tenure
- **AI Insights** - Automated alerts for positive trends, warnings, and critical gaps
- **KPI Metrics** - Key performance indicators with trend indicators
- **Tabbed Navigation** - Six specialized views for different HR functions

## Data Structure

The dashboard uses synthetic data for demonstration purposes. In production, connect to your HRIS system or database by modifying the `load_data()` function.

### Current Data Includes:
- Headcount trends (8 months)
- Department metrics (6 departments)
- Diversity and age demographics
- Turnover and performance data
- Engagement scores
- Recruitment funnel metrics
- Skills gap analysis
- Compensation trends
- Tenure analysis

## Customization

### Adding Your Own Data

Replace the `@st.cache_data` decorated `load_data()` function with your data source:

```python
@st.cache_data
def load_data():
    # Connect to your database
    headcount_trend = pd.read_sql("SELECT * FROM headcount", conn)
    department_data = pd.read_sql("SELECT * FROM departments", conn)
    # ... load other data
    return (headcount_trend, department_data, ...)
```

### Modifying Visualizations

All charts use Plotly for interactivity. Customize colors, layouts, or chart types in the respective tab sections:

```python
fig.update_layout(
    height=400,
    colorway=['#3b82f6', '#10b981'],  # Custom colors
    font=dict(size=12)
)
```

### Styling

The dashboard uses custom CSS in the `st.markdown()` section at the top. Modify the styles in the `<style>` tags to match your brand:

```css
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Your custom gradient */
}
```

## Features by Tab

### 📊 Overview
- Headcount growth trends with forecasting
- Department employee counts and satisfaction scores
- Combined visualization of multiple metrics

### 👤 Workforce Analytics
- Gender diversity pie chart
- Age distribution histogram
- Department turnover comparison
- Skills gap analysis with current vs. required levels

### 📈 Performance
- Performance rating distribution (current vs. previous period)
- Engagement trends across four dimensions (Overall, Recognition, Growth, Work-Life)

### 🎯 Recruitment
- Complete recruitment funnel with conversion rates
- Time-to-fill and cost-per-hire trends
- Application volume tracking
- Offer acceptance rate monitoring

### 💰 Compensation
- Company average salary vs. market rate trends
- Department salary comparisons
- Competitive positioning analysis

### 🔄 Turnover Analysis
- Voluntary vs. involuntary turnover breakdown
- Exit reason analysis
- Tenure-based turnover patterns
- Department-specific turnover rates
- Actionable retention recommendations

## Technical Details

### Performance Optimization
- Data caching with `@st.cache_data` for faster load times
- Efficient data filtering and aggregation
- Optimized chart rendering with Plotly

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Demo Data

This dashboard includes realistic synthetic data for demonstration purposes:
- 280+ employees across 6 departments
- 8 months of historical trends
- Complete recruitment and turnover metrics
- Performance and engagement scores

## Support and Feedback

For questions, issues, or feature requests:
- Create an issue in the repository
- Contact: [Your contact information]

## License

This project is created by **Henrietta Atsenokhai** for demonstration purposes.

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

**Note:** This dashboard uses synthetic data for demonstration purposes. In a production environment, integrate with your organization's HRIS system and ensure proper data security and privacy measures are in place.

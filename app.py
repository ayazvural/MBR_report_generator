import streamlit as st
import pandas as pd
import io # Keep for potential future use or remove if to_csv is deleted
import base64 # For HTML download link

# Import modularized functions
from utils import metrics, charts, filters

def display_metrics_table(df_metrics, target_hours):
    """Displays the formatted monthly metrics table."""
    if df_metrics.empty:
        st.warning("No metrics to display for the selected filters.")
        return

    display_metrics = df_metrics.rename(columns={
        'Year-Month': 'Month',
        'total_tickets_opened': 'Opened',
        'total_tickets_resolved': 'Resolved',
        'percentage_closed': '% Closed',
        'avg_close_time_hours': 'Avg Close Time (hrs)',
        'median_close_time_hours': 'Median Close Time (hrs)',
        f'tickets_closed_within_{target_hours}h': f'Closed < {target_hours}h',
        f'percentage_closed_within_{target_hours}h': f'% Closed < {target_hours}h',
        'tickets_open_over_1_week': 'Open > 1 week',
        'percentage_open_over_1_week': '% Open > 1 week'
    })

    # Format numerical columns 
    formatted_metrics = display_metrics.style.format({
        'Opened': '{:.0f}',
        'Resolved': '{:.0f}',
        '% Closed': '{:.1f}%',
        'Avg Close Time (hrs)': '{:.1f}',
        'Median Close Time (hrs)': '{:.1f}',
        f'Closed < {target_hours}h': '{:.0f}',
        f'% Closed < {target_hours}h': '{:.1f}%',
        'Open > 1 week': '{:.0f}',
        '% Open > 1 week': '{:.1f}%'
    }, na_rep="N/A")
    
    st.dataframe(formatted_metrics, use_container_width=True)

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        layout="wide", 
        page_title="Intercom Support Report",
        page_icon="📊" # Optional: Add a favicon
    )
    
    st.title("📊 Intercom Customer Support Report Generator")

    # --- Info and Download Section --- 
    col_info, col_dl = st.columns([0.8, 0.2]) 
    # Download button placeholder in col_dl will be populated later
    
    # --- File Upload --- 
    uploaded_file = st.sidebar.file_uploader("Upload your Intercom CSV export", type=["csv"])

    if uploaded_file is None:
        st.info("Please upload a CSV file to begin.")
        return

    # --- Load Data --- 
    df_raw = metrics.load_data(uploaded_file)
    if df_raw is None:
        # Error handled in load_data
        return 
    if df_raw.empty:
        st.warning("Uploaded file is empty or contains no valid data.")
        return

    # --- Add Derived Columns --- 
    df_raw = metrics.add_escalation_column(df_raw)

    # --- Sidebar Filters --- 
    filter_selections = filters.display_sidebar_filters(df_raw)

    # --- Apply Filters --- 
    df_filtered = filters.apply_filters(df_raw, filter_selections)

    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
        # Optionally hide the download button placeholder if needed here
        return 

    # --- Calculate Metrics --- 
    close_target = filter_selections['close_time_target']
    monthly_metrics_data = metrics.calculate_metrics(df_filtered, close_target)

    # --- Display Metrics Table --- 
    st.header("Monthly Metrics Summary")
    display_metrics_table(monthly_metrics_data, close_target)

    # --- Main Visualizations (Ticket Health & Close Time) ---
    st.header("Ticket Performance Overview")
    col_viz1, col_viz2 = st.columns(2)
    with col_viz1:
        fig_health = charts.plot_ticket_health(monthly_metrics_data)
        st.plotly_chart(fig_health, use_container_width=True)
    with col_viz2:
        fig_time = charts.plot_close_time(monthly_metrics_data)
        st.plotly_chart(fig_time, use_container_width=True)

    # --- Top Ticket Types --- 
    st.header("Top Ticket Types")
    category_col = 'Category'
    issue_source_col = 'Issue Source'
    col_top1, col_top2 = st.columns(2)
    with col_top1:
        st.markdown("**Top Categories**")
        if category_col in df_filtered.columns:
            top_categories = df_filtered[category_col].value_counts().dropna().head(10)
            if not top_categories.empty:
                st.dataframe(
                    top_categories.rename_axis('Category').reset_index(name='Count'), 
                    use_container_width=True
                )
            else: st.caption("No category data.")
        else: st.caption(f"Column '{category_col}' not found.")
    with col_top2:
        st.markdown("**Top Issue Sources**")
        if issue_source_col in df_filtered.columns:
            top_sources = df_filtered[issue_source_col].value_counts().dropna().head(10)
            if not top_sources.empty:
                st.dataframe(
                    top_sources.rename_axis('Issue Source').reset_index(name='Count'),
                    use_container_width=True
                )
            else: st.caption("No issue source data.")
        else: st.caption(f"Column '{issue_source_col}' not found.")

    # --- Priority & Escalation Distribution --- 
    st.header("Priority & Escalation Distribution")
    col_pie1, col_pie2 = st.columns(2)
    with col_pie1:
        fig_priority = charts.plot_priority_distribution(df_filtered)
        if fig_priority:
            st.plotly_chart(fig_priority, use_container_width=True)
        else:
            st.caption(f"Priority chart could not be generated. Check column '{charts.priority_col}'.")
    with col_pie2:
        fig_escalation = charts.plot_escalation_distribution(df_filtered)
        if fig_escalation:
            st.plotly_chart(fig_escalation, use_container_width=True)
        else:
            # Check if columns were missing vs. just no data
            if 'Escalated' in df_filtered.columns:
                st.caption("No escalation data to display.")
            else:
                 st.caption(f"Escalation chart requires columns '{metrics.assigned_col}' and '{metrics.closed_by_col}'.")

    # --- Top Customers --- 
    fig_customers = charts.plot_top_customers(df_filtered)
    if fig_customers:
        st.header("Top Customers by Ticket Volume")
        st.plotly_chart(fig_customers, use_container_width=True)
    # else: # Optional: Add caption if chart failed
    #     st.caption("Could not generate Top Customers chart.") 

    # --- Agent Closures --- 
    fig_agent_closures = charts.plot_agent_closures(df_filtered)
    if fig_agent_closures:
        st.header("Ticket Closures by Agent")
        st.plotly_chart(fig_agent_closures, use_container_width=True)
    # else: # Optional: Add caption if chart failed
    #     st.caption("Could not generate Agent Closures chart.")

    # --- Removed Sections Placeholder (Download CSV / Raw Data) ---
    # Original code for these sections can be found in previous versions if needed.

if __name__ == "__main__":
    main() 
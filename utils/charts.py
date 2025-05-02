import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_ticket_health(metrics_df):
    """Generates the Ticket Health (Opened/Resolved/ % Closed) chart."""
    if metrics_df.empty:
        return go.Figure() # Return empty figure if no data
        
    fig = px.bar(metrics_df,
                 x='Year-Month',
                 y=['total_tickets_opened', 'total_tickets_resolved'],
                 title='Ticket Health by Year-Month',
                 labels={'value': 'Number of Tickets', 'variable': 'Metric', 'Year-Month': 'Month'},
                 barmode='group',
                 color_discrete_sequence=['#1F77B4', '#A6CEE3']
                 )

    fig.add_trace(go.Scatter(x=metrics_df['Year-Month'],
                    y=metrics_df['percentage_closed'],
                    yaxis='y2',
                    name='% Closed',
                    mode='lines+markers',
                    line=dict(color='#7FC241', width=3)
                    ))

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Tickets',
        yaxis2=dict(
            title='% Closed',
            overlaying='y',
            side='right',
            range=[0, 105]
        ),
        legend_title_text='Metric',
        title_x=0.5
    )
    return fig

def plot_close_time(metrics_df):
    """Generates the Avg/Median Close Time chart (Bar + Line)."""
    if metrics_df.empty:
        return go.Figure()
        
    fig = px.bar(
        metrics_df,
        x='Year-Month',
        y='avg_close_time_hours',
        title='Average and Median Close Time by Year-Month',
        labels={'avg_close_time_hours': 'Avg Close Time (H)', 'Year-Month': 'Month'},
        color_discrete_sequence=['#7FC241']
    )
    
    fig.add_trace(go.Scatter(
        x=metrics_df['Year-Month'],
        y=metrics_df['median_close_time_hours'],
        mode='lines+markers',
        name='Median Close Time (H)',
        line=dict(color='#1F77B4', width=3)
    ))

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Time (Hours)',
        title_x=0.5,
        legend_title_text='Metric Type',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.data[0].name = 'Average Close Time (H)' # Explicitly set bar legend name
    return fig

def plot_priority_distribution(df):
    """Generates the Ticket Priority Distribution pie chart."""
    priority_col = 'Ticket Priority'
    if priority_col not in df.columns or df[priority_col].isnull().all():
        return None # Indicate chart cannot be generated

    priority_counts = df[priority_col].fillna("Unspecified").value_counts()
    if priority_counts.empty:
        return None 
        
    priority_df = priority_counts.rename_axis('Priority').reset_index(name='Count')
    fig = px.pie(
        priority_df, names='Priority', values='Count',
        title='Ticket Priority Distribution', hole=0.4,
        color_discrete_sequence=['#7FC241', '#1F77B4', '#A6CEE3', '#FF7F0E', '#2CA02C', '#D62728'] 
    )
    fig.update_traces(
        marker=dict(line=dict(color='white', width=0)),
        textinfo='percent+label'
    )
    fig.update_layout(title_x=0.5, showlegend=True)
    return fig

def plot_escalation_distribution(df):
    """Generates the Escalation Distribution pie chart."""
    if 'Escalated' not in df.columns:
        return None
        
    escalation_counts = df['Escalated'].map({True: 'Escalated', False: 'Not Escalated'}).value_counts()
    if escalation_counts.empty:
         return None
         
    escalation_df = escalation_counts.rename_axis("Escalation Status").reset_index(name='Count')
    fig = px.pie(
        escalation_df,
        names="Escalation Status",
        values="Count",
        title="Escalation Distribution",
        hole=0.4,
        color_discrete_sequence=['#D62728', '#7FC241'] # Red for escalated, Green for not
    )
    fig.update_traces(
        marker=dict(line=dict(color='white', width=0)),
        textinfo='percent+label'
    )
    fig.update_layout(title_x=0.5, showlegend=True)
    return fig

def plot_top_customers(df):
    """Generates the Top Customers by Ticket Volume bar chart."""
    customer_col = 'Companies (name)' # Ensure this is the correct column name
    if customer_col not in df.columns:
        return None
        
    top_customers = df[customer_col].value_counts().dropna().head(10)
    if top_customers.empty:
        return None

    customer_df = top_customers.rename_axis("Company Name").reset_index(name="Ticket Count")
    customer_df['Company Name'] = customer_df['Company Name'].astype(str)
    
    fig = px.bar(
        customer_df.sort_values("Ticket Count", ascending=True),
        x="Ticket Count",
        y="Company Name",
        orientation="h",
        title="Top 10 Customers by Ticket Volume",
        text="Ticket Count",
        color_discrete_sequence=['#7FC241'] 
    )
    fig.update_layout(title_x=0.5, yaxis_title="Company Name", xaxis_title="Ticket Count")
    return fig

def plot_agent_closures(df):
    """Generates the Ticket Closures by Agent vertical bar chart."""
    closed_by_col = 'Closed by (name)'
    if closed_by_col not in df.columns:
        return None
        
    agent_counts = df[closed_by_col].value_counts().dropna()
    if agent_counts.empty:
        return None

    agent_df = agent_counts.rename_axis("Agent Name").reset_index(name="Tickets Closed")
    
    fig = px.bar(
        agent_df.sort_values("Tickets Closed", ascending=False), 
        x="Agent Name",
        y="Tickets Closed",
        title="Ticket Closures by Agent",
        text="Tickets Closed",
        color_discrete_sequence=['#7FC241'] 
    )
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Agent Name",
        yaxis_title="Tickets Closed",
        xaxis_tickangle=-45,
        height=max(500, len(agent_df) * 20) 
    )
    return fig 
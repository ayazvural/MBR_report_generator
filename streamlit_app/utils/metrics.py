import pandas as pd
import streamlit as st # Needed for error/success messages in load_data

def load_data(uploaded_file):
    """Loads and preprocesses the Intercom CSV data."""
    try:
        df = pd.read_csv(uploaded_file)

        # --- Data Preprocessing --- 
        required_cols = ['Created at', 'Last resolved at']
        for col in required_cols:
            if col not in df.columns:
                 raise KeyError(f"Missing required column: {col}")

        df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')
        df['Last resolved at'] = pd.to_datetime(df['Last resolved at'], errors='coerce')

        # Drop rows where 'Created at' is NaT after conversion
        df.dropna(subset=['Created at'], inplace=True)

        # Create derived columns
        df['Year-Month'] = df['Created at'].dt.strftime('%B %Y')
        df['Hours Open'] = (df['Last resolved at'] - df['Created at']).dt.total_seconds() / 3600
        df.loc[df['Hours Open'] < 0, 'Hours Open'] = pd.NA 
        df['Open More than 1 week'] = df['Hours Open'] > 168
        # --- End Preprocessing ---

        st.success("Data loaded and preprocessed successfully!")
        return df
    except KeyError as e:
        st.error(f"Error processing data: {e}. Please ensure your CSV has the required columns.")
        return None
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        return None

def add_escalation_column(df):
    """Adds an 'Escalated' boolean column based on Assigned vs Closed By."""
    assigned_col = 'Assigned to (name)'
    closed_by_col = 'Closed by (name)'
    
    if assigned_col in df.columns and closed_by_col in df.columns:
        df['Escalated'] = df[assigned_col] != df[closed_by_col]
        # Note: Comparison treats NaN != value as True, NaN != NaN as True.
    else:
        # Handle case where columns might be missing, maybe log a warning
        # For now, the column won't be added if deps are missing
        print(f"Warning: Cannot create 'Escalated' column. Missing '{assigned_col}' or '{closed_by_col}'.")
        pass 
    return df


def calculate_metrics(df, close_time_target_hours=72):
    """Calculates monthly summary metrics from the processed DataFrame."""
    if df.empty or 'Year-Month' not in df.columns:
        return pd.DataFrame() # Return empty DataFrame if input is invalid

    # Ensure 'Year-Month' is treated as a categorical type with a specific order
    year_month_order = sorted(
        df['Year-Month'].unique(), 
        key=lambda ym: pd.to_datetime(ym, format='%B %Y')
    )
    # Use temporary df to avoid SettingWithCopyWarning if df is a slice
    df_calc = df.copy()
    df_calc['Year-Month'] = pd.Categorical(df_calc['Year-Month'], categories=year_month_order, ordered=True)

    monthly_metrics = df_calc.groupby('Year-Month', observed=False).agg(
        total_tickets_opened=('Created at', 'count'),
        total_tickets_resolved=('Last resolved at', 'count'),
        avg_close_time_hours=('Hours Open', 'mean'),
        median_close_time_hours=('Hours Open', 'median'),
        tickets_meeting_target=('Hours Open', lambda x: (x <= close_time_target_hours).sum()),
        tickets_open_over_1_week=('Open More than 1 week', 'sum')
    ).reset_index()

    # Calculate percentages safely
    if 'total_tickets_opened' in monthly_metrics.columns and monthly_metrics['total_tickets_opened'].sum() > 0:
         monthly_metrics['percentage_closed'] = (monthly_metrics['total_tickets_resolved'] / monthly_metrics['total_tickets_opened'] * 100).round(1)
         monthly_metrics['percentage_open_over_1_week'] = (monthly_metrics['tickets_open_over_1_week'] / monthly_metrics['total_tickets_opened'] * 100).round(1)
    else:
         monthly_metrics['percentage_closed'] = 0
         monthly_metrics['percentage_open_over_1_week'] = 0

    if 'total_tickets_resolved' in monthly_metrics.columns and monthly_metrics['total_tickets_resolved'].sum() > 0:
        monthly_metrics['percentage_meeting_target'] = (monthly_metrics['tickets_meeting_target'] / monthly_metrics['total_tickets_resolved'] * 100).round(1)
    else:
        monthly_metrics['percentage_meeting_target'] = 0
        
    monthly_metrics['percentage_meeting_target'] = monthly_metrics['percentage_meeting_target'].fillna(0)

    # Rename columns for clarity
    monthly_metrics.rename(columns={
        'tickets_meeting_target': f'tickets_closed_within_{close_time_target_hours}h',
        'percentage_meeting_target': f'percentage_closed_within_{close_time_target_hours}h'
        }, inplace=True)

    return monthly_metrics 
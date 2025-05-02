import streamlit as st
import pandas as pd

def display_sidebar_filters(df_raw):
    """Displays filter widgets in the sidebar and returns selected values."""
    
    st.sidebar.header("Filters & Settings")
    
    selections = {}

    # --- Close Time Target --- 
    selections['close_time_target'] = st.sidebar.number_input(
        "Close Time Target (Hours)", min_value=1, value=72, step=1
    )

    # --- Year-Month Filter --- 
    if 'Year-Month' in df_raw.columns:
        year_months = sorted(
            df_raw['Year-Month'].unique(), 
            key=lambda ym: pd.to_datetime(ym, format='%B %Y')
        )
        selections['selected_year_months'] = st.sidebar.multiselect(
            "Filter by Year-Month", options=year_months, default=year_months
        )
    else:
         selections['selected_year_months'] = []
         st.sidebar.caption("Year-Month column not found for filtering.")

    # --- Team Filter --- 
    team_col = 'Team assigned to (name)'
    selections['selected_teams'] = []
    if team_col in df_raw.columns:
        teams = sorted(df_raw[team_col].dropna().unique())
        if teams:
            selections['selected_teams'] = st.sidebar.multiselect(
                "Filter by Team Assigned", options=teams, default=teams
            )
        else:
            st.sidebar.caption("No teams found in data.")
    else:
        st.sidebar.caption(f"Column '{team_col}' not found.")

    # --- Priority Filter --- 
    priority_col = 'Ticket Priority'
    selections['selected_priorities'] = []
    if priority_col in df_raw.columns:
        priority_options = sorted(df_raw[priority_col].dropna().unique())
        if priority_options:
            selections['selected_priorities'] = st.sidebar.multiselect(
                "Filter by Ticket Priority", options=priority_options, default=priority_options
            )
        else:
            st.sidebar.caption("No priority values found.")
    else:
        st.sidebar.caption(f"Column '{priority_col}' not found.")

    # --- Escalation Filter --- 
    selections['escalation_filter'] = "All"
    if 'Escalated' in df_raw.columns: # Check if pre-calculated column exists
        selections['escalation_filter'] = st.sidebar.selectbox(
            "Filter by Escalation Status", 
            options=["All", "Escalated Only", "Not Escalated"],
            index=0
        )
    # else: # Optional: Indicate why filter is missing
    #    st.sidebar.caption("Escalation filter unavailable (required columns missing).")

    # --- Agent (Closed By) Filter --- 
    closed_by_col = 'Closed by (name)'
    selections['selected_agents'] = []
    if closed_by_col in df_raw.columns:
        agent_options = sorted(df_raw[closed_by_col].dropna().unique())
        if agent_options:
            selections['selected_agents'] = st.sidebar.multiselect(
                "Filter by Agent (Closed Ticket)", options=agent_options, default=agent_options
            )
        else:
            st.sidebar.caption("No agent names found.")
    else:
        st.sidebar.caption(f"Column '{closed_by_col}' not found.")

    return selections

def apply_filters(df, selections):
    """Applies the selected filters to the DataFrame."""
    df_filtered = df.copy()

    # Year-Month
    if selections.get('selected_year_months') is not None and 'Year-Month' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Year-Month'].isin(selections['selected_year_months'])]
        
    # Team
    team_col = 'Team assigned to (name)' 
    if selections.get('selected_teams') and team_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[team_col].isin(selections['selected_teams'])]

    # Priority
    priority_col = 'Ticket Priority'
    if selections.get('selected_priorities') and priority_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[priority_col].isin(selections['selected_priorities'])]

    # Escalation
    escalation_filter = selections.get('escalation_filter', "All")
    if escalation_filter != "All" and 'Escalated' in df_filtered.columns:
        is_escalated = (escalation_filter == "Escalated Only")
        df_filtered = df_filtered[df_filtered['Escalated'] == is_escalated]

    # Agent (Closed By)
    closed_by_col = 'Closed by (name)'
    if selections.get('selected_agents') and closed_by_col in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[closed_by_col].isin(selections['selected_agents'])]
        
    return df_filtered 
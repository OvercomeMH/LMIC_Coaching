import streamlit as st
import pandas as pd
import numpy as np # For np.nan
from config import ORGANISATION_FIXED_COSTS # Import the R&D budget

def display_overall_comparison_tab(results_data):
    st.header("Programme Comparison: Key Metrics")
    
    if not results_data or not all(isinstance(res, dict) for res in results_data.values()) or \
       not all('Cost per WELLBY' in res for res in results_data.values()):
        st.info('Adjust parameters in the other tabs to see a comparison here.')
        return

    df = pd.DataFrame.from_dict(results_data, orient='index')

    # Rename columns for clarity in the table
    column_renames = {
        'Total Cost (Money Spent)': 'Marginal Programme Cost',
        'Net WELLBYs Generated': 'WELLBYs Generated',
        'Cost per WELLBY': 'Cost per WELLBY',
        'Total Clients Seen': 'Clients Seen',
        'Clients Retained': 'Clients Retained',
        'Net WELLBYs per Retained Client': 'WELLBYs / Ret. Client'
    }
    df = df.rename(columns=column_renames)

    # For reference: calculate cost per "Happiness Year" (making someone 1 point happier for 1 year)
    if 'WELLBYs Generated' in df.columns and 'Marginal Programme Cost' in df.columns:
        # Ensure 'WELLBYs Generated' is not zero for division
        df['Cost per Happiness Year'] = np.where(
            df['WELLBYs Generated'] != 0,
            df['Marginal Programme Cost'] / df['WELLBYs Generated'],
            np.nan
        )
    else:
        df['Cost per Happiness Year'] = np.nan

    # Desired column order for display
    desired_columns_order = [
        'Marginal Programme Cost',
        'WELLBYs Generated',
        'Clients Seen',
        'Clients Retained',
        'WELLBYs / Ret. Client',
        'Cost per WELLBY',
        'Cost per Happiness Year'
    ]
    existing_columns_in_order = [col for col in desired_columns_order if col in df.columns]
    df_display = df[existing_columns_in_order]

    ordered_programmes = ['Bespoke Offering', 'Procrastination', 'Insomnia']
    ordered_programmes_in_results = [p for p in ordered_programmes if p in df_display.index]
    df_display = df_display.reindex(ordered_programmes_in_results)

    # Calculate Summary Row (only for display columns)
    if not df_display.empty:
        summary_data = {}
        if 'Marginal Programme Cost' in df_display.columns: 
            summary_data['Marginal Programme Cost'] = df_display['Marginal Programme Cost'].sum()
        if 'WELLBYs Generated' in df_display.columns: 
            summary_data['WELLBYs Generated'] = df_display['WELLBYs Generated'].sum()
        if 'Clients Seen' in df_display.columns: 
            summary_data['Clients Seen'] = df_display['Clients Seen'].sum()
        if 'Clients Retained' in df_display.columns: 
            summary_data['Clients Retained'] = df_display['Clients Retained'].sum()
        
        # For averages/derived metrics in summary:
        total_direct_cost_sum = summary_data.get('Marginal Programme Cost', 0)
        total_wellbys_sum = summary_data.get('WELLBYs Generated', 0)
        total_clients_retained_sum = summary_data.get('Clients Retained', 0)

        summary_data['WELLBYs / Ret. Client'] = (total_wellbys_sum / total_clients_retained_sum) if total_clients_retained_sum > 0 else np.nan
        summary_data['Cost per WELLBY'] = (total_direct_cost_sum / total_wellbys_sum) if total_wellbys_sum > 0 else np.nan
        summary_data['Cost per Happiness Year'] = (total_direct_cost_sum / total_wellbys_sum) if total_wellbys_sum > 0 else np.nan
        
        summary_df_cols = {k: [v] for k, v in summary_data.items() if k in df_display.columns}
        summary_row = pd.DataFrame(summary_df_cols, index=["Total/Overall Average"])
        df_display = pd.concat([df_display, summary_row])

    # Formatting dictionary
    formats = {
        'Marginal Programme Cost': '${:,.0f}',
        'WELLBYs Generated': '{:,.2f}',
        'Clients Seen': '{:,.0f}',
        'Clients Retained': '{:,.0f}',
        'WELLBYs / Ret. Client': '{:,.3f}',
        'Cost per WELLBY': '${:,.0f}',
        'Cost per Happiness Year': '${:,.0f}'
    }
    valid_formats = {k: v for k, v in formats.items() if k in df_display.columns}
    st.dataframe(df_display.style.format(valid_formats, na_rep="N/A"), height=(df_display.shape[0] + 1) * 35 + 3) 
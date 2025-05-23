import streamlit as st
import pandas as pd
import numpy as np # For np.nan
import plotly.express as px
from config import ORGANISATION_FIXED_COSTS, DEFAULT_COACHES_PER_COHORT, DEFAULT_CLIENTS_PER_COACH # Import the R&D budget and operational defaults

def display_overall_comparison_tab(results_data):
    
    # Add controls for branches and client distribution
    st.subheader("Scale and Distribution")
    
    # Number of branches slider
    num_branches = st.slider(
        "Number of branches", 
        min_value=1, 
        max_value=20, 
        value=3, 
        step=1,
        help="Each branch can serve approximately 2,700 clients per year (225 per month)"
    )
    
    # Calculate total clients capacity based on operational parameters
    # With coaches volunteering for 3 months and training one cohort per month,
    # at steady state we have 3 active cohorts simultaneously
    coaches_per_cohort = DEFAULT_COACHES_PER_COHORT  # 15
    clients_per_coach_total = DEFAULT_CLIENTS_PER_COACH  # 15 over 3 months
    active_cohorts = 3  # Number of cohorts active simultaneously
    
    # Calculate capacity per branch
    active_coaches_per_branch = active_cohorts * coaches_per_cohort  # 3 * 15 = 45
    clients_per_coach_per_month = clients_per_coach_total / 3  # 15 / 3 = 5 per month
    clients_per_branch_per_month = active_coaches_per_branch * clients_per_coach_per_month  # 45 * 5 = 225
    clients_per_branch_per_year = clients_per_branch_per_month * 12  # Annual capacity
    total_clients_capacity = num_branches * clients_per_branch_per_year
    
    # Display capacity metrics
    capacity_col1, capacity_col2, capacity_col3 = st.columns(3)
    
    with capacity_col1:
        st.metric("Monthly Client Capacity", f"{num_branches * clients_per_branch_per_month:,} clients")
    
    with capacity_col2:
        st.metric("Yearly Client Capacity", f"{total_clients_capacity:,} clients")
    
    with capacity_col3:
        st.metric("Clients per Branch (Monthly)", f"{clients_per_branch_per_month:,.0f} clients")
    
    # Client distribution pie chart controls
    st.subheader("Client Distribution")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Adjust the proportion of clients in each programme:**")
        bespoke_pct = st.slider("Bespoke Offering (%)", 0, 100, 60, 5)
        procrastination_pct = st.slider("Procrastination (%)", 0, 100, 20, 5)
        insomnia_pct = st.slider("Insomnia (%)", 0, 100, 20, 5)
        
        # Normalize to 100%
        total_pct = bespoke_pct + procrastination_pct + insomnia_pct
        if total_pct > 0:
            bespoke_norm = bespoke_pct / total_pct
            procrastination_norm = procrastination_pct / total_pct  
            insomnia_norm = insomnia_pct / total_pct
        else:
            bespoke_norm = procrastination_norm = insomnia_norm = 0.33
        
        st.caption(f"Total: {total_pct}% (automatically normalized to 100%)")
    
    with col2:
        # Create pie chart
        pie_data = {
            'Programme': ['Bespoke Offering', 'Procrastination', 'Insomnia'],
            'Percentage': [bespoke_norm * 100, procrastination_norm * 100, insomnia_norm * 100],
            'Clients': [
                int(bespoke_norm * total_clients_capacity),
                int(procrastination_norm * total_clients_capacity), 
                int(insomnia_norm * total_clients_capacity)
            ]
        }
        
        pie_df = pd.DataFrame(pie_data)
        fig = px.pie(pie_df, values='Percentage', names='Programme', 
                    title=f"Client Distribution Across {total_clients_capacity:,} Total Clients")
        st.plotly_chart(fig, use_container_width=True)
    
    # Calculate scaled results
    if not results_data or not all(isinstance(res, dict) for res in results_data.values()) or \
       not all('Cost per WELLBY' in res for res in results_data.values()):
        st.info('Adjust parameters in the other tabs to see a comparison here.')
        return

    # Scale the results based on new client numbers
    scaled_results = {}
    client_distribution = {
        'Bespoke Offering': int(bespoke_norm * total_clients_capacity),
        'Procrastination': int(procrastination_norm * total_clients_capacity),
        'Insomnia': int(insomnia_norm * total_clients_capacity)
    }
    
    for programme, original_data in results_data.items():
        if programme in client_distribution:
            # Get scaling factor
            original_clients = original_data.get('Total Clients Seen', 1)
            new_clients = client_distribution[programme]
            scale_factor = new_clients / original_clients if original_clients > 0 else 0
            
            # Scale the results
            scaled_results[programme] = {
                'Total Cost (Money Spent)': original_data.get('Total Cost (Money Spent)', 0) * scale_factor,
                'Net WELLBYs Generated': original_data.get('Net WELLBYs Generated', 0) * scale_factor,
                'Cost per WELLBY': original_data.get('Cost per WELLBY', 0),  # This stays the same per unit
                'Total Clients Seen': new_clients,
                'Clients Retained': original_data.get('Clients Retained', 0) * scale_factor,
                'Net WELLBYs per Retained Client': original_data.get('Net WELLBYs per Retained Client', 0)  # This stays the same per client
            }

    df = pd.DataFrame.from_dict(scaled_results, orient='index')

    # Rename columns for clarity in the table
    column_renames = {
        'Total Cost (Money Spent)': 'Marginal Programme Cost',
        'Net WELLBYs Generated': 'WELLBYs Generated',
        'Cost per WELLBY': 'Cost per WELLBY',
        'Total Clients Seen': 'Clients Seen',
        'Clients Retained': 'Clients Retained'
    }
    df = df.rename(columns=column_renames)

    # Desired column order for display
    desired_columns_order = [
        'Marginal Programme Cost',
        'WELLBYs Generated',
        'Clients Seen',
        'Clients Retained',
        'Cost per WELLBY'
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

        summary_data['Cost per WELLBY'] = (total_direct_cost_sum / total_wellbys_sum) if total_wellbys_sum > 0 else np.nan
        
        summary_df_cols = {k: [v] for k, v in summary_data.items() if k in df_display.columns}
        summary_row = pd.DataFrame(summary_df_cols, index=["Total/Overall Average"])
        df_display = pd.concat([df_display, summary_row])

    # Formatting dictionary
    formats = {
        'Marginal Programme Cost': '${:,.0f}',
        'WELLBYs Generated': '{:,.2f}',
        'Clients Seen': '{:,.0f}',
        'Clients Retained': '{:,.0f}',
        'Cost per WELLBY': '${:,.0f}'
    }
    valid_formats = {k: v for k, v in formats.items() if k in df_display.columns}
    
    # Display the table
    st.subheader("Scaled Programme Results")
    st.dataframe(df_display.style.format(valid_formats, na_rep="N/A"), height=(df_display.shape[0] + 1) * 35 + 3) 
    
    # Add table with fixed costs included
    st.subheader("Total Cost Analysis (Including Fixed Costs)")
    
    if not df_display.empty:
        # Create a copy of the scaled results for fixed cost calculations
        fixed_cost_df = df_display.copy()
        
        # Remove the summary row temporarily for calculations
        programmes_only_df = fixed_cost_df.drop("Total/Overall Average", errors='ignore')
        
        # Calculate fixed cost allocation based on clients seen
        total_clients = programmes_only_df['Clients Seen'].sum() if 'Clients Seen' in programmes_only_df.columns else 0
        
        if total_clients > 0:
            # Allocate fixed costs proportionally to clients seen
            programmes_only_df['Allocated Fixed Costs'] = programmes_only_df['Clients Seen'] * (ORGANISATION_FIXED_COSTS / total_clients)
            programmes_only_df['Total Cost'] = programmes_only_df['Marginal Programme Cost'] + programmes_only_df['Allocated Fixed Costs']
            programmes_only_df['Total Cost per WELLBY'] = programmes_only_df['Total Cost'] / programmes_only_df['WELLBYs Generated']
            
            # Calculate new summary row
            fixed_summary_data = {
                'Marginal Programme Cost': programmes_only_df['Marginal Programme Cost'].sum(),
                'Allocated Fixed Costs': programmes_only_df['Allocated Fixed Costs'].sum(),
                'Total Cost': programmes_only_df['Total Cost'].sum(),
                'WELLBYs Generated': programmes_only_df['WELLBYs Generated'].sum(),
                'Clients Seen': programmes_only_df['Clients Seen'].sum(),
                'Clients Retained': programmes_only_df['Clients Retained'].sum()
            }
            
            # Calculate overall total cost per WELLBY
            fixed_summary_data['Total Cost per WELLBY'] = (fixed_summary_data['Total Cost'] / 
                                                         fixed_summary_data['WELLBYs Generated']) if fixed_summary_data['WELLBYs Generated'] > 0 else np.nan
            
            # Add summary row
            fixed_summary_row = pd.DataFrame({k: [v] for k, v in fixed_summary_data.items()}, 
                                           index=["Total/Overall Average"])
            fixed_cost_display = pd.concat([programmes_only_df, fixed_summary_row])
            
            # Define column order for fixed cost table
            fixed_cost_columns = [
                'Marginal Programme Cost',
                'Allocated Fixed Costs', 
                'Total Cost',
                'WELLBYs Generated',
                'Clients Seen',
                'Clients Retained',
                'Total Cost per WELLBY'
            ]
            
            # Filter to existing columns
            fixed_cost_display = fixed_cost_display[[col for col in fixed_cost_columns if col in fixed_cost_display.columns]]
            
            # Format the fixed cost table
            fixed_formats = {
                'Marginal Programme Cost': '${:,.0f}',
                'Allocated Fixed Costs': '${:,.0f}',
                'Total Cost': '${:,.0f}',
                'WELLBYs Generated': '{:,.2f}',
                'Clients Seen': '{:,.0f}',
                'Clients Retained': '{:,.0f}',
                'Total Cost per WELLBY': '${:,.0f}'
            }
            fixed_valid_formats = {k: v for k, v in fixed_formats.items() if k in fixed_cost_display.columns}
            
            # Show explanation
            st.markdown(f"""
            **Fixed costs (${ORGANISATION_FIXED_COSTS:,}) are allocated proportionally based on clients seen.**
            
            This gives a more complete picture of the true cost per WELLBY when including R&D and organizational overhead costs.
            """)
            
            # Display the fixed cost table
            st.dataframe(fixed_cost_display.style.format(fixed_valid_formats, na_rep="N/A"), 
                        height=(fixed_cost_display.shape[0] + 1) * 35 + 3) 
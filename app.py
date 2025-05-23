# Save this script as app.py

import streamlit as st
from config import offerings

# Import tab display functions
from tabs.model_params_tab import display_model_parameters_tab
from tabs.assumptions_tab import display_assumptions_tab
from tabs.overall_tab import display_overall_comparison_tab
from tabs.programme_tab import display_programme_tab
from tabs.cost_per_session_tab import display_cost_per_session_tab
from tabs.fixed_costs_tab import display_fixed_costs_tab

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('CEA: Coaching LMIC natives')

# ==========================================================
#                 INSTRUCTIONS
# ==========================================================

# ==========================================================
#                 DEFAULT VALUES FOR EACH TAB
# ==========================================================

# Define default model parameters (these will be overridden by the new tab's inputs)
# but are needed for the app to load initially before tab interactions.
# Keeping them here also serves as a reference for their original default values.

# ==========================================================
#                 TABS FOR EACH OFFERING
# ==========================================================

# Define tab names and create tabs
programme_tab_names = list(offerings.keys())
# New order: Intro, Programmes, Marginal Costs, Fixed Costs, Overall, Assumptions, Model Params
tab_names = ["Intro"] + programme_tab_names + ["Marginal Costs", "Fixed Costs", "Overall", "Assumptions", "Model Parameters"]

all_tabs = st.tabs(tab_names)

# Assign tabs to meaningful variables
intro_tab_ui = all_tabs[0]
programme_st_tabs = all_tabs[1 : 1 + len(programme_tab_names)]
# Calculate the starting index for tabs after programme_st_tabs
next_tab_index = 1 + len(programme_tab_names)
marginal_costs_tab_ui = all_tabs[next_tab_index]
fixed_costs_tab_ui = all_tabs[next_tab_index + 1]
overall_tab_ui = all_tabs[next_tab_index + 2]
assumptions_tab_ui = all_tabs[next_tab_index + 3]
model_params_tab_ui = all_tabs[next_tab_index + 4] # Adjusted index to account for new tab

offering_results = {}

# --- Render Intro Tab ---
with intro_tab_ui:
    st.markdown("""
    **Instructions:**
    - Use the tabs below to switch between different programme offerings.
    - Adjust the sliders to see how cost per WELLBY changes.
    - Email [john@overcome.org.uk](mailto:john@overcome.org.uk) if you have any questions.
    
    **You should know**
    - We'll be continously updating this model to reflect our current best understanding, largely for our own benefit.

    """)

# --- Render Model Parameters Tab ---
with model_params_tab_ui:
    (
        cost_per_session_input,
        avg_sessions_dropouts_input
    ) = display_model_parameters_tab()

# --- Render Programme Tabs ---
for i, tab_name in enumerate(programme_tab_names):
    with programme_st_tabs[i]:
        tab_defaults = offerings[tab_name]
        offering_results[tab_name] = display_programme_tab(
            tab_name, 
            tab_defaults, 
            cost_per_session_input,
            avg_sessions_dropouts_input
        )

# --- Render Marginal Costs Tab ---
with marginal_costs_tab_ui:
    calculated_cost_per_session = display_cost_per_session_tab()

# --- Render Fixed Costs Tab ---
with fixed_costs_tab_ui:
    display_fixed_costs_tab()

# --- Render Assumptions Tab ---
with assumptions_tab_ui:
    display_assumptions_tab()

# --- Render Overall Comparison Tab ---
with overall_tab_ui:
    display_overall_comparison_tab(offering_results)

# All function definitions previously here should have been removed by this edit.
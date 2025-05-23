import streamlit as st
# Import DEFAULT values from the main config file
from config import (
    DEFAULT_COST_PER_SESSION, 
    DEFAULT_AVG_SESSIONS_FOR_DROPOUTS
)

def display_model_parameters_tab():
    st.header("Model Parameters")
    st.markdown("Adjust the global parameters that affect all programme calculations.")
    
    cost_per_session = st.number_input(
        "Cost per Coaching Session ($)", 
        min_value=0.0, 
        value=DEFAULT_COST_PER_SESSION, 
        step=0.50,
        help="The direct financial cost for one coaching session."
    )
    
    avg_sessions_for_dropouts = st.number_input(
        "Average Sessions Completed by Dropouts", 
        min_value=0.0, 
        value=DEFAULT_AVG_SESSIONS_FOR_DROPOUTS, 
        step=0.1,
        help="On average, how many sessions does a participant who drops out complete?"
    )
    
    return (
        cost_per_session,
        avg_sessions_for_dropouts
    ) 
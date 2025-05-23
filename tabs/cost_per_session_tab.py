import streamlit as st
# Import DEFAULT values from the main config file
from config import (
    DEFAULT_COACHES_PER_COHORT,
    DEFAULT_CLIENTS_PER_COACH, 
    DEFAULT_SESSIONS_PER_CLIENT,
    DEFAULT_COUNSELLOR_SALARY,
    DEFAULT_HEAD_OF_TRAINING_SALARY,
    DEFAULT_VA_SALARY,
    DEFAULT_BRANCH_MANAGER_SALARY,
    DEFAULT_HIRING_MANAGER_SALARY,
    DEFAULT_OTHER_SALARY
)

def display_cost_per_session_tab():
    st.header("Marginal Costs Calculator")
    st.markdown("Calculate the marginal costs per coaching session for a single branch based on staffing and operational parameters.")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Operational Parameters")
        
        coaches_per_cohort = st.number_input(
            "Coaches per Cohort", 
            min_value=1, 
            value=DEFAULT_COACHES_PER_COHORT, 
            step=1
        )
        
        clients_per_coach = st.number_input(
            "Clients per Coach", 
            min_value=1, 
            value=DEFAULT_CLIENTS_PER_COACH, 
            step=1
        )
        
        sessions_per_client = st.number_input(
            "Average Sessions per Client", 
            min_value=1, 
            value=DEFAULT_SESSIONS_PER_CLIENT, 
            step=1
        )
        
        # Checkbox for final roleplay assessment
        final_roleplay_assessment = st.checkbox(
            "An Overcome core-team member conducts a final roleplay assessment with every coach before they see clients",
            value=True
        )
        
        st.markdown("""
        **About these parameters:**
        - **Coaches per cohort** reflects our current cohort size
        - **We train one cohort per month**
        - **We think we could handle cohorts of 20 without much issue**
        - **Clients per coach** and **sessions per client** are our current averages
        - While our retention would imply a lower average number of sessions, many clients choose to extend and the coach agrees
        
        **These estimates are conservative because they assume no improvement despite:**
        - **Hiring manager will attract larger applicant pools**, allowing us to be more selective and hire higher-quality coaches
        - **Our hiring process is still being refined** - better selection criteria should reduce training costs and improve coach effectiveness  
        - **Current performance metrics reflect periods of client shortage** - coaches working below capacity may underperform compared to when fully utilized
        - **We're using above-market salaries in our calculations** (except branch manager) - we could potentially hire at lower market rates
        - **No automation improvements assumed** - we see clear opportunities to automate scheduling, admin tasks, and initial assessments
        """)
    
    with col2:
        st.subheader("Monthly Costs (USD)")
        
        counsellor_salary = st.number_input(
            "Counsellor Salary", 
            min_value=0, 
            value=DEFAULT_COUNSELLOR_SALARY, 
            step=50
        )
        
        head_of_training_salary = st.number_input(
            "Head of Training Salary", 
            min_value=0, 
            value=DEFAULT_HEAD_OF_TRAINING_SALARY, 
            step=50
        )
        
        va_salary = st.number_input(
            "Virtual Assistant Salary", 
            min_value=0, 
            value=DEFAULT_VA_SALARY, 
            step=50
        )
        
        branch_manager_salary = st.number_input(
            "Branch Manager Salary", 
            min_value=0, 
            value=DEFAULT_BRANCH_MANAGER_SALARY, 
            step=50
        )
        
        # Checkbox for hiring manager
        hiring_manager_enabled = st.checkbox(
            "Hiring Manager (increases applicant number/quality, iterates on hiring process)",
            value=True
        )
        
        other_salary = st.number_input(
            "Other", 
            min_value=0, 
            value=DEFAULT_OTHER_SALARY, 
            step=50
        )
        
        st.markdown("""
        **About these costs:**
        - **Counsellor** (supervision, client emergencies): Median salary of a counsellor in India
        - **Head of Training** (coordinates training, interviews, workshops): What we paid our head of training before promoting her to executive role
        - **Branch Manager** (client flow, coordination, payroll): What Roshnee would be happy to accept
        - **Virtual Assistant** (books assessments, applicant emails, scheduling): Standard VA rate
        - **Hiring Manager** ($400/month): Average salary for a psychologist with 3 years experience. Increases applicant number/quality, iterates on hiring process
        - **Other**: Mostly insurance, SAAS, and other small recurring expenses
        """)
    
    # Calculations
    st.subheader("Cost Calculations")
    
    # Calculate additional cost for final roleplay assessment
    final_assessment_cost = 7 * coaches_per_cohort if final_roleplay_assessment else 0
    
    # Calculate hiring manager cost
    hiring_manager_cost = DEFAULT_HIRING_MANAGER_SALARY if hiring_manager_enabled else 0
    
    # Calculate total monthly salary costs
    total_monthly_salaries = (
        counsellor_salary + 
        head_of_training_salary + 
        va_salary + 
        branch_manager_salary +
        hiring_manager_cost +
        other_salary +
        final_assessment_cost
    )
    
    # Calculate total clients per cohort
    total_clients_per_cohort = coaches_per_cohort * clients_per_coach
    
    # Calculate total sessions per cohort
    total_sessions_per_cohort = total_clients_per_cohort * sessions_per_client
    
    # Assuming each cohort runs for one month (you might want to make this configurable)
    cost_per_session = total_monthly_salaries / total_sessions_per_cohort if total_sessions_per_cohort > 0 else 0
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Sessions per Cohort", 
            value=f"{total_sessions_per_cohort:,}"
        )
    
    with col2:
        st.metric(
            label="Cost per Session", 
            value=f"${cost_per_session:.2f}"
        )
    
    with col3:
        # Show final assessment cost breakdown if enabled
        if final_roleplay_assessment:
            st.metric(
                label="Final Roleplay Assessment Cost", 
                value=f"${final_assessment_cost}",
                help=f"${7} × {coaches_per_cohort} coaches"
            )
        else:
            st.metric(
                label="Final Roleplay Assessment Cost", 
                value="$0"
            )
    
    # Additional breakdown
    st.subheader("Summary")
    
    # Calculate capacity metrics for a single branch
    monthly_client_capacity = total_clients_per_cohort  # One cohort per month
    yearly_client_capacity = monthly_client_capacity * 12  # 12 cohorts per year
    
    # Create metrics layout
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            label="Monthly Client Capacity", 
            value=f"{monthly_client_capacity:,} clients",
            help="Clients served per month (one cohort per month)"
        )
    
    with summary_col2:
        st.metric(
            label="Yearly Client Capacity", 
            value=f"{yearly_client_capacity:,} clients",
            help="Total clients served per year (12 cohorts)"
        )
    
    with summary_col3:
        st.metric(
            label="Total Sessions per Cohort", 
            value=f"{total_sessions_per_cohort:,}"
        )
    
    with summary_col4:
        st.metric(
            label="Total Monthly Costs", 
            value=f"${total_monthly_salaries:,.2f}"
        )
    
    # Return the calculated cost per session for use in other tabs if needed
    return cost_per_session 
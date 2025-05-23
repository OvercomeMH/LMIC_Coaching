import streamlit as st
import numpy as np
# pandas and altair are not directly used by display_programme_tab itself,
# but by display_decay_visualisation which it calls from utils.py.
# So, they are not strictly needed here if display_decay_visualisation handles its own chart objects.

# Import helper functions from utils.py
from utils import display_decay_visualisation, calculate_total_wellbys_per_ea
# No direct config import needed here as `offerings` (tab_defaults) is passed in.
from config import DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS
from config import programme_introductions, programme_wellbeing_gain_explanations

def display_programme_tab(
    tab_name, 
    tab_defaults, 
    cost_per_session_global,
    avg_sessions_dropouts_global
):
    st.header(f"{tab_name} Programme")
    # Use config-based introduction text
    intro_text = programme_introductions.get(tab_name, "")
    if intro_text:
        st.markdown(intro_text)
    
    st.subheader("Benefit Duration and Decay")
    decay_model_options = ["Exponential Decay", "Linear Decay", "Custom Curve"]
    default_decay_model = tab_defaults.get("default_decay_model", "Exponential Decay")

    # Evidence base text (optional, keep if you want to show it)
    if tab_name == "Bespoke Offering":
        st.markdown("""
        **Evidence Base:** The UK's Improving Access to Psychological Therapies (IAPT) program provides 
        the closest studied model to our general programme. Like IAPT, we use low-intensity, CBT-focused 
        interventions, though we use psychology graduates rather than the nurses or social workers often 
        used in IAPT services.
        
        [Research on IAPT outcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC9790710/) shows significant 
        decay in wellbeing benefits over time, with approximately 50% annual decay in effects being a reasonable estimate.
        """)
    elif tab_name == "Insomnia":
        st.markdown("""
        **Evidence Base:** Meta-analysis of cognitive behavioral therapy for insomnia 
        ([van der Zweerde et al., 2019](https://pubmed.ncbi.nlm.nih.gov/31491656/)) shows that 
        wellbeing effects decline over time. While CBT-I produces clinically significant improvements that last up to a year 
        after therapy, the evidence suggests approximately 60% annual decay in wellbeing effects.
        """)
    elif tab_name == "Procrastination":
        st.markdown("""
        **Evidence Base:** The only paper I could find which looked at how well a procrastination interventions wellbeing improvement held up showed that X% were retained 12 months later, but we're doubtful that finding would replicate. We think a decay curve like this is more realistic.
        """)
    
    decay_model = st.selectbox(
        "Benefit Decay Model", 
        options=decay_model_options, 
        index=decay_model_options.index(default_decay_model),
        key=f"decay_model_{tab_name}",
        help="'Exponential Decay': Benefits reduce by a fixed percentage each period. 'Linear Decay': Benefits reduce by a fixed amount each period until zero. 'Custom Curve': Define your own decay curve by adjusting control points.'"
    )

    timeframe_of_interest_months = DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS
    timeframe_of_interest_weeks = (timeframe_of_interest_months / 12) * 52  # Use 52 weeks for wellbeing calculations

    annual_decay_rate_input = None
    months_to_zero_input = None
    custom_month_sliders = {}

    if decay_model == "Exponential Decay":
        default_decay_rate = tab_defaults.get("default_decay_rate", 25.0)
        annual_decay_rate_input = st.slider(
            'Annual Decay Rate (%)', 0.1, 99.9, default_decay_rate, 0.1, key=f"annual_decay_{tab_name}",
            help="The percentage by which the remaining wellbeing benefit decreases each year. Cannot be 0% or 100%."
        ) / 100.0
        if tab_name == "Insomnia": st.caption("Based on meta-analysis of CBT-I studies (van der Zweerde et al., 2019).")
        elif tab_name == "Bespoke Offering": st.caption("Based on IAPT outcome data for similar CBT-based interventions.")
        else: st.caption("Happier Lives Institute and Founders Pledge cite a decay of ~25% each year for group therapy for depression.")
    elif decay_model == "Linear Decay":
        default_months_to_zero = tab_defaults.get("default_months_to_zero", 12.0)
        months_to_zero_input = st.slider(
            'Months until Effect is Zero', 1.0, 60.0, default_months_to_zero, 0.1, key=f"months_to_zero_{tab_name}",
            help="How many months until the linearly decaying wellbeing effect reaches zero."
        )
        if tab_name == "Procrastination": st.caption("Conservative estimate based on clinical experience, as limited research exists.")
    elif decay_model == "Custom Curve":
        st.markdown("**Define your custom decay curve by adjusting the benefit value at each control point:**")
        col1, col2 = st.columns(2)
        with col1:
            custom_month_sliders['month_3'] = st.slider('Benefit at 3 months (%)', 0.0, 100.0, 75.0, 1.0, key=f"custom_3month_{tab_name}") / 100.0
            custom_month_sliders['month_9'] = st.slider('Benefit at 9 months (%)', 0.0, 100.0, 30.0, 1.0, key=f"custom_9month_{tab_name}") / 100.0
        with col2:
            custom_month_sliders['month_6'] = st.slider('Benefit at 6 months (%)', 0.0, 100.0, 50.0, 1.0, key=f"custom_6month_{tab_name}") / 100.0
            custom_month_sliders['month_12'] = st.slider('Benefit at 12 months (%)', 0.0, 100.0, 15.0, 1.0, key=f"custom_12month_{tab_name}") / 100.0
    
    weekly_points_for_calc = display_decay_visualisation(
        decay_model,
        annual_decay_rate_input=annual_decay_rate_input,
        months_to_zero_input=months_to_zero_input,
        month_3_slider=custom_month_sliders.get('month_3'),
        month_6_slider=custom_month_sliders.get('month_6'),
        month_9_slider=custom_month_sliders.get('month_9'),
        month_12_slider=custom_month_sliders.get('month_12'),
        timeframe_of_interest_weeks=timeframe_of_interest_weeks
    )

    st.subheader("Wellbeing Impact & Participants")
    # Add explanatory sentence about dropouts
    st.markdown("We assume that anyone who dropped out without telling us they were better got zero wellbeing benefit. So, we only need to consider people who've completed the programme.")
    
    baseline_wellbeing = st.slider(
        'Baseline wellbeing score before intervention (0-10 scale)',
        min_value=0.0, max_value=10.0, value=tab_defaults["baseline_wellbeing_score"], step=0.1, key=f"baseline_wellbeing_{tab_name}",
        help="0 = Extremely unhappy, 10 = Extremely happy. Average person scores around 7."
    )
    
    peak_wellbeing = st.slider(
        'Peak wellbeing score when treatment is maximally effective (0-10 scale)',
        min_value=0.0, max_value=10.0, value=tab_defaults["peak_wellbeing_score"], step=0.1, key=f"peak_wellbeing_{tab_name}",
        help="Wellbeing score at peak effectiveness, before any decay begins."
    )
    
    wellbeing_gain = peak_wellbeing - baseline_wellbeing
    # Make the wellbeing gain text larger
    st.markdown(f"<span style='font-size:1.5em'><b>Wellbeing Gain: {wellbeing_gain:.1f} points</b></span>", unsafe_allow_html=True)
    
    # Add section to help user interpret the wellbeing gain (now config-based)
    st.markdown("### How do I know if the wellbeing gain makes sense?")
    wellbeing_explanation = programme_wellbeing_gain_explanations.get(tab_name, "The wellbeing gain estimate is based on the best available evidence and expert judgment for this type of intervention.")
    st.markdown(wellbeing_explanation)
    
    retention_rate = st.slider(
        'Retention Rate (%)', 0.0, 100.0, value=tab_defaults["retention"], step=0.1, key=f"retention_rate_{tab_name}"
    ) / 100
    # Add explanation and 65% statistic next to retention rate for Bespoke Offering
    if tab_name == "Bespoke Offering":
        st.caption("On average, 65% of clients who do one session will go on to do at least six sessions. Retention rate here means the probability that a participant will complete every session in the programme, given that they attended the first session.")
    elif tab_name in ["Insomnia", "Procrastination"]:
        st.caption("Our average retention rate (lower bound) is 40%. Both RCTs retained >80% of clients (and 90% of those from LMICs). We're estimating 50% here.")
    else:
        st.caption("Our average EA completion rate is ~60%. Both RCTs retrained >80% of users. We're estimating for 75%, adjusted upwards because we think the RCT would have retained more users if they had known the results for those who completed, and we'll be advertising those results hard.")
    
    # MOVED TO LAST: Proportion of harm borne by affected individual
    # Create condition-specific text for each tab
    if tab_name == "Bespoke Offering":
        slider_text = "What percentage of the harm from each case of depression / anxiety is bore by the affected person? (%)"
        caption_condition = "depression / anxiety"
    elif tab_name == "Insomnia":
        slider_text = "What percentage of the harm from each case of insomnia is bore by the affected person? (%)"
        caption_condition = "insomnia"
    elif tab_name == "Procrastination":
        slider_text = "What percentage of the harm from each case of procrastination is bore by the affected person? (%)"
        caption_condition = "procrastination"
    else:
        slider_text = "What percentage of the harm from each case of depression / anxiety is bore by the affected person? (%)"
        caption_condition = "depression / anxiety"
    
    # Set default harm proportion based on programme type
    if tab_name == "Procrastination":
        default_harm_proportion = 50  # 50/50 split for procrastination
    else:
        default_harm_proportion = 75  # 75% for other programmes
    
    harm_proportion = st.slider(
        slider_text,
        min_value=1, max_value=100, value=default_harm_proportion, step=1, key=f"harm_proportion_{tab_name}",
        help="Consider the direct impact on the person's wellbeing, work performance, and relationships. This accounts for how much of the total harm (including effects on friends, family, and community) is experienced by the individual themselves."
    ) / 100.0
    st.caption(f"This means {harm_proportion:.0%} of the total harm from {caption_condition} affects the individual directly, while {(1-harm_proportion):.0%} affects their broader network (friends, family, colleagues, community).")
    
    sessions_per_participant = tab_defaults["sessions_per_participant"]
    
    # Use default number of participants for calculations (will be overridden by overall tab)
    num_participants = tab_defaults["num_participants"]
    total_EAs = num_participants
    overall_retention_rate = retention_rate
    total_retained_EAs = total_EAs * overall_retention_rate
    
    # Calculate initial weekly wellbeing gain (in wellbeing points per week)
    initial_weekly_wellbeing_gain_per_ea = wellbeing_gain  # The gain is continuous, not just during work hours

    # This calculates GROSS WELLBYs gained per client over the period, before accounting for time spent on intervention
    gross_wellbys_per_ea_who_completes = calculate_total_wellbys_per_ea(
        initial_weekly_wellbeing_gain_per_ea=initial_weekly_wellbeing_gain_per_ea,
        decay_model=decay_model,
        timeframe_of_interest_weeks=timeframe_of_interest_weeks,
        working_weeks_per_year=52,  # Default value since we removed the parameter
        annual_decay_rate=annual_decay_rate_input,
        months_to_zero=months_to_zero_input,
        custom_weekly_points=weekly_points_for_calc
    )

    # Total gross WELLBYs from all clients who are retained
    gross_wellbys_from_retained = gross_wellbys_per_ea_who_completes * total_retained_EAs
    
    # Simplified calculation - no time opportunity costs or disappointment
    # The main benefit is the wellbeing gain from those who complete the program
    # Divide by harm proportion to account for broader societal benefits beyond the individual
    net_wellbys_gained = gross_wellbys_from_retained / harm_proportion
    
    # Calculate base cost from sessions (This is now the total direct cost for this programme)
    base_sessions_cost = sessions_per_participant * cost_per_session_global * total_EAs
    total_cost = base_sessions_cost # Total cost is now only the direct sessions cost

    cost_per_wellby = total_cost / net_wellbys_gained if net_wellbys_gained > 0 else np.nan

    # Calculate metrics for display
    net_wellbys_per_retained_client = (net_wellbys_gained / total_retained_EAs) if total_retained_EAs > 0 else 0
    gross_wellbys_per_retained_client = (gross_wellbys_from_retained / total_retained_EAs) if total_retained_EAs > 0 else 0
    societal_wellbys_per_retained_client = net_wellbys_per_retained_client - gross_wellbys_per_retained_client

    # Display the breakdown of WELLBYs per retained client
    st.subheader("Programme Outcomes")
    
    # Create three columns for the metrics
    outcome_col1, outcome_col2, outcome_col3 = st.columns(3)
    
    with outcome_col1:
        st.metric(
            label="WELLBYs per Retained Client (Client)",
            value=f"{gross_wellbys_per_retained_client:,.3f}",
            help="Direct wellbeing benefit experienced by each person who completes the programme"
        )
    
    with outcome_col2:
        st.metric(
            label="WELLBYs per Retained Client (Society)",
            value=f"{societal_wellbys_per_retained_client:,.3f}",
            help="Additional wellbeing benefit to family, friends, colleagues, and community per person who completes the programme"
        )
    
    with outcome_col3:
        st.metric(
            label="Total WELLBYs per Retained Client",
            value=f"{net_wellbys_per_retained_client:,.3f}",
            help="Combined wellbeing benefit including both individual and societal impact per person who completes the programme"
        )

    return {
        "Total Cost (Money Spent)": total_cost, # This is the direct cost
        "Net WELLBYs Generated": net_wellbys_gained,
        "Cost per WELLBY": cost_per_wellby,
        "Total Clients Seen": total_EAs,
        "Clients Retained": total_retained_EAs,
        "Net WELLBYs per Retained Client": net_wellbys_per_retained_client
    } 
# Configuration data for the CEA Coaching Streamlit app

offerings = {
    "Bespoke Offering": {
        "retention": 40.0,
        "num_participants": 400,
        "sessions_per_participant": 6,
        "default_effect_duration": 6.0,  # months
        "baseline_wellbeing_score": 6.5,    # 0-10 scale wellbeing before intervention
        "peak_wellbeing_score": 8.0,       # 0-10 scale wellbeing at peak effectiveness
        "default_decay_rate": 50.0,       # percent, for Exponential Decay
        "default_months_to_zero": 12.0,   # months, for Linear Decay
        "default_decay_model": "Exponential Decay"
    },
    "Procrastination": {
        "retention": 50.0,
        "num_participants": 300,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "baseline_wellbeing_score": 5.5,
        "peak_wellbeing_score": 7.0,
        "default_decay_rate": 80.0,       # percent, for Exponential Decay
        "default_months_to_zero": 6.0,
        "default_decay_model": "Exponential Decay"
    },
    "Insomnia": {
        "retention": 70.0,
        "num_participants": 150,
        "sessions_per_participant": 4,
        "default_effect_duration": 4.0,
        "baseline_wellbeing_score": 4.8,
        "peak_wellbeing_score": 6.5,
        "default_decay_rate": 60.0,       # percent, for Exponential Decay
        "default_months_to_zero": 12.0,
        "default_decay_model": "Exponential Decay"
    }
}

DEFAULT_COST_PER_SESSION = 2.36
DEFAULT_AVG_SESSIONS_FOR_DROPOUTS = 2.0

DEFAULT_TIMEFRAME_OF_INTEREST_MONTHS = 12.0

# Constants for overall cost explanation
ORGANISATION_FIXED_COSTS = 93000 # Fixed R&D Budget in USD

# Default values for cost per session calculations
DEFAULT_COACHES_PER_COHORT = 15
DEFAULT_CLIENTS_PER_COACH = 15
DEFAULT_SESSIONS_PER_CLIENT = 5
DEFAULT_COUNSELLOR_SALARY = 500
DEFAULT_HEAD_OF_TRAINING_SALARY = 500
DEFAULT_VA_SALARY = 350
DEFAULT_BRANCH_MANAGER_SALARY = 500
DEFAULT_HIRING_MANAGER_SALARY = 400
DEFAULT_OTHER_SALARY = 300

# Programme-specific introduction text
programme_introductions = {
    "Bespoke Offering": '''
        **About the Bespoke Offering:**
        - This programme covers a wide range of issues, from dietary improvement and habit change to severe depression and anxiety.
        - Our best estimate for the median user is a kenyan schoolteacher seeking help for moderate anxiety
    ''',
    "Insomnia": '''
        **About the Insomnia Programme:**
        - This programme is designed for people struggling with moderate to severe insomnia.
        - The intervention is based on cognitive behavioral therapy for insomnia (CBT-I), the gold standard treatment.
        - Participants typically experience significant wellbeing improvements due to better sleep quality.

    ''',
    "Procrastination": '''
        This four session programme helps people who're in the top 20% of procrastinators relative to the general population.

        
    '''
}

# Programme-specific wellbeing gain explanation text
programme_wellbeing_gain_explanations = {
    "Bespoke Offering": """
after six sessions, our average client gains 2.3 points on a 0-10 scale, going from ~4.5 to 6.8). No doubt, some of this would have happened anyway.
""",
    "Insomnia": """
Almost nobody has ever studied chronic insomnia's affect on wellbeing in LMICs. Your guess is as good as mine.
""",
    "Procrastination": """
Our procrastination RCT had 44 LMIC participants. We retained 90% of them. The difference between the control and intervention group was 1.8 points on Cantril's ladder at post, and that difference held up at the one-month follow up.
"""
}
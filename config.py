# Configuration data for the CEA Coaching EAs Streamlit app

offerings = {
    "Bespoke Offering": {
        "retention": 60.0,
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
        "retention": 70.0,
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
ORGANISATION_FIXED_COSTS = 136000 # Fixed R&D Budget in USD

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
        - Expected wellbeing gain: **1.7 points** on the 0-10 happiness scale.
    ''',
    "Procrastination": '''
        This four session programme helps people who're in the top 20% of procrastinators relative to the general population.

        Very little research exists on the long-term durability of procrastination interventions. We suspect that it will decay sharply without additional intervention. To help prevent relapse, completers will get a free referral link to [GoalsWon, a daily accountability service](https://www.goalswon.com/giving-back) (free for EAs). We think this is likely to dramatically reduce the likelihood of relapse. Their CEO reached out to me asking for more EA clients, so it's a win-win at no cost to you / us / users.
        
        Expected wellbeing gain: **1.5 points** on the 0-10 happiness scale.
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
Chronic procrastination is associated with significant stress, guilt, and reduced life satisfaction. Successful intervention can reduce these negative emotions and increase sense of control and accomplishment.

Given that procrastination interventions address both productivity and emotional wellbeing, our best estimate is a 1.5 point improvement on the happiness scale.
"""
}
import streamlit as st

def display_assumptions_tab():
    st.header("Model Assumptions")
    st.markdown(""" 
    This model relies on several key assumptions that are not directly configurable as numerical inputs. 
    Understanding these is crucial for interpreting the results:

    - **Fixed Timeframe of Interest (12 months):** The model calculates benefits over a standard 12-month 
      period for all programmes. This timeframe is used to sum up the total WELLBYs gained, 
      applying the selected decay model and its parameters.

    - **Market Size & Sign-up Feasibility:** The model calculates outcomes based on the 'Number of Participants' 
      you set for each programme. It does not assess whether it's feasible to attract that many participants 
      at the specified retention rates.

    - **Decay Model Accuracy:** The different decay models (Exponential, Linear) are simplifications 
      of how wellbeing benefits actually diminish over time. The default decay parameters for each programme are based 
      on the best available evidence or conservative estimates where evidence is limited.

    - **Accuracy of User Inputs:** The validity of the outputs heavily depends on the accuracy of your inputs for:
        - Baseline and peak wellbeing scores.
        - Expected effect duration.
        - Retention rates.

    - **Zero Wellbeing Gain for Dropouts:** The model assumes that participants who drop out 
      do not contribute any wellbeing gains. Only those who complete the programme are counted 
      towards the 'WELLBYs Generated'.

    - **Homogeneity of Participants:** The model uses average or median values for participant characteristics 
      and outcomes. It does not capture the full distribution or range of individual experiences or benefits.

    - **Nature of Wellbeing Measurement:** The wellbeing scores are assumed to be measured on a consistent 0-10 scale, 
      where the model treats all points on this scale as having equal value (linear utility). The model assumes 
      decay begins immediately.
    
    - **Marginal Cost Model:** The total cost for each programme is calculated as the marginal cost of 
      providing sessions to participants. This represents the direct cost of delivering the programme 
      without considering fixed organizational overhead.

    - **Harm Proportion and Societal Benefits:** The model uses a "harm proportion" slider to account for 
      broader societal benefits beyond the individual participant. This assumes that when someone recovers 
      from mental health issues, insomnia, or procrastination, the benefits extend to their family, friends, 
      colleagues, and community. The total WELLBYs are calculated by dividing individual benefits by the 
      proportion of harm borne directly by the affected person, scaling up to capture these wider impacts.

    - **Additionality:** The model assumes that any wellbeing gains are purely additional and would not have 
      occurred without the intervention.

    - **No Follow-up Sessions:** The model assumes no additional coaching sessions are provided beyond the initially defined programme length.

    - **No Change in Attitude to Coaching/Therapy:** The intervention is not assumed to change a participant's general attitude towards seeking coaching or therapy in the future, beyond the direct effects modelled.

    - **Single Programme per Participant:** The model assumes each individual will only participate in one of the listed programmes. There are no overlaps or combined effects from multiple programme participations by the same individual.
    """) 
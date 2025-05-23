import streamlit as st

def display_fixed_costs_tab():
    st.header("Fixed Costs: Team & Operations")
    st.markdown("Our fixed costs cover the core team that makes all programmes possible, regardless of client participation.")
    
    # Team Members section
    st.subheader("Core Team")
    
    team_members = [
        {
            "name": "Helen",
            "salary": "$39,000",
            "role": "She handles RCTs and sale of part-time courses while preparing us to scale by writing our policies and liaising with external partners. She led a team of volunteers that designed insomnia RCT, got it through ethics, trained the coaches, and recruited the participants."
        },
        {
            "name": "Angel", 
            "salary": "$36,000",
            "role": "Manages triaging, client-coach pairing, coach experience, safeguarding, leads procrastination RCT, and generally does whatever is needed, from website design to database automation. Literally works 100 hours each week every week."
        },
        {
            "name": "David",
            "salary": "$6,000", 
            "role": "Video editor based in the Philippines. Each other day, he turns one script into a fully edited video, which helps us standardise our training so it can be scaled up with fidelity."
        },
        {
            "name": "Me (Founder)",
            "salary": "$18,000 (optional)",
            "role": "I'm responsible for impact-oriented client demographics (e.g. founders, key people within animal welfare), special projects, organisational strategy, fundraising, B2B sales, hiring, firing, and accounting. I work on this ~70 hours per week ~49 weeks a year. (Happy to keep volunteering if needs be)"
        },
        {
            "name": "Kishah",
            "salary": "$12,000",
            "role": "Native Kenyan psychologist. In charge of developing our training and hiring practices."
        }
    ]
    
    # Display each team member
    for member in team_members:
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{member['name']}**")
                st.markdown(f"**{member['salary']}**")
            
            with col2:
                st.markdown(member['role'])
            
            st.markdown("---")
    
    # Calculate total costs
    st.subheader("Total Fixed Costs")
    
    # Calculate range based on founder salary
    min_total = 39000 + 36000 + 6000 + 0 + 12000  # $93k if founder takes $0
    max_total = 39000 + 36000 + 6000 + 18000 + 12000  # $111k if founder takes $18k
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="If I don't take salary", 
            value=f"${min_total:,}"
        )
    
    with col2:
        st.metric(
            label="If I take salary", 
            value=f"${max_total:,}"
        ) 
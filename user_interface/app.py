import streamlit as st

# Page setup
optimal_credit_length_estimation = st.Page("pages/optimal_credit_length_estimation_page.py", title="Optimal Credit Length Estimation", icon="💳")
dummy = st.Page("pages/dummy_page.py", title="Dummy", icon="🧪")

# Navigation setup
pg = st.navigation({"Finance": [optimal_credit_length_estimation], "Misc": [dummy]})

# Run
pg.run()

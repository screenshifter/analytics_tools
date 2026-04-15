import streamlit as st
from orchestrator import optimal_credit_length_estimation as oc

st.title("Optimal Credit Length Estimation")

with st.sidebar:
    st.header("Parameters")
    credit_amount = st.number_input("Credit amount", value=600000, disabled=True)
    credit_rate = st.number_input("Credit rate (%)", value=8.0, disabled=True)
    inflation = st.number_input("Expected inflation (%)", value=3.0, disabled=True)
    monthly_payment = st.number_input("Acceptable monthly payment", value=6000, disabled=True)
    investment_rate = st.number_input("Investment interest rate (%)", value=5.0, disabled=True)

fig = oc.get_credit_figure()
st.pyplot(fig)

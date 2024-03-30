import streamlit as st
import math
import subprocess

# Install scipy

subprocess.check_call(["pip", "install", "scipy"])
from scipy.stats import norm

def calculate_p_value(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    alpha = {90: 0.1, 95: 0.05, 99: 0.01}[confidence_level]
    z_alpha = norm.ppf(1 - alpha/2)
    p_value = 2 * (1 - norm.cdf(abs((treatment_conversions/treatment_visitors - control_conversions/control_visitors) * math.sqrt((control_visitors + treatment_visitors) / 2)) / math.sqrt(1/(control_visitors) + 1/(treatment_visitors))))
    if p_value <= alpha:
        return "Experiment Group is Better"
    elif p_value >= 1 - alpha:
        return "Control Group is Better"
    else:
        return "Indeterminate"

# Set the app's layout and styling
st.set_page_config(layout="wide")
st.title("A/B Test Hypothesis Testing")
st.subheader("Enter the inputs below")

col1, col2 = st.beta_columns(2)

with col1:
    control_visitors = st.number_input("Control Group Visitors", value=1000)
    control_conversions = st.number_input("Control Group Conversions", value=100)

with col2:
    treatment_visitors = st.number_input("Treatment Group Visitors", value=1000)
    treatment_conversions = st.number_input("Treatment Group Conversions", value=105)

confidence_level = st.selectbox("Confidence Level", (90, 95, 99))

# Perform the hypothesis test
result = calculate_p_value(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)

col1, col2 = st.beta_columns(2)

with col1:
    st.subheader("Results")
    st.write(f'The result of the A/B test is {result}.')

with col2:
    st.button("Clear Inputs")

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

num_groups = st.number_input(label='Number of groups', value=5, step=1)
your_roll = st.number_input(label='Your roll', min_value=1, max_value=20, step=1)

num_simulations = 100_000
# Generate random rolls for the remaining slots in each group
random_rolls = np.random.randint(1, 21, size=(num_simulations, num_groups - 1))

# Create a column of 'your_roll' to prepend to each simulation
your_rolls_column = np.full((num_simulations, 1), your_roll)

# Combine them into a single 2D array
simulations = np.hstack([your_rolls_column, random_rolls])


average = np.average(simulations, axis=1)
minimum = np.min(simulations, axis=1)
maximum = np.max(simulations, axis=1)
summation = np.sum(simulations, axis=1)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label='Minimum', value=f"{np.average(minimum):.2f}")
with col2:
    st.metric(label='Average', value=f"{np.average(average):.2f}")
with col3:
    st.metric(label='Maximum', value=f"{np.average(maximum):.2f}")
with col4:
    st.metric(label='Sum', value=np.average(summation))


metrics = {
    'minimum': minimum,
    'average': average,
    'maximum': maximum,
    'sum': summation
}

choice = st.selectbox('Pick your metric', metrics.keys())

df = pd.DataFrame(metrics)

plot_type = st.radio("Select Plot Type", ["Histogram", "PMF (Probability)", "CDF (Cumulative)"])

if plot_type == "Histogram":
    fig = px.histogram(df, x=choice, title=f"Histogram of {choice}")
elif plot_type == "PMF (Probability)":
    fig = px.histogram(df, x=choice, histnorm='probability', title=f"PMF of {choice}")
else:
    fig = px.histogram(df, x=choice, histnorm='probability', cumulative=True, title=f"CDF of {choice}")

fig

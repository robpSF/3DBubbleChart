import streamlit as st
import pandas as pd
import plotly.express as px

# Input data section
st.title('3D Bubble Chart Viewer')

st.sidebar.header('Input Data')
# Define a simple form to collect data points
data_points = st.sidebar.slider('Number of data points', 5, 100, 10)

# Create an empty DataFrame to hold data
data = {
    'X': [st.sidebar.number_input(f'X[{i}]', value=i) for i in range(data_points)],
    'Y': [st.sidebar.number_input(f'Y[{i}]', value=i*2) for i in range(data_points)],
    'Z': [st.sidebar.number_input(f'Z[{i}]', value=i*3) for i in range(data_points)],
    'Size': [st.sidebar.number_input(f'Size[{i}]', value=10) for i in range(data_points)]
}

df = pd.DataFrame(data)

# Plotting
st.header('3D Bubble Chart')
fig = px.scatter_3d(df, x='X', y='Y', z='Z', size='Size', opacity=0.7)

# Customize the layout for better interaction
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    )
)

st.plotly_chart(fig, use_container_width=True)

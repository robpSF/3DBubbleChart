import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Title and instructions
st.title('Enhanced 3D Bubble Chart Viewer from Excel')
st.write("""
Upload an Excel file with the following columns: **Segment, Realism, Evaluation, Speed, Customisation, Revenue**.
This app will create two interactive 3D bubble charts with enhanced separation for better visibility.
""")

# Sidebar file uploader
st.sidebar.header('Upload Excel File')
uploaded_file = st.sidebar.file_uploader('Upload your Excel file (.xlsx)', type=['xlsx'])

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Strip spaces from column names
    df.columns = df.columns.str.strip()

    # Preview of uploaded data
    st.write('Preview of Uploaded Data:')
    st.dataframe(df)

    # Check if all required columns are present
    required_columns = ['Segment', 'Realism', 'Evaluation', 'Speed', 'Customisation', 'Revenue']
    if all(col in df.columns for col in required_columns):
        
        # Cap all values to a maximum of 6 for specified axes
        capped_columns = ['Realism', 'Evaluation', 'Speed', 'Customisation']
        df[capped_columns] = df[capped_columns].clip(upper=6)

        # Increase bubble size using a nonlinear transformation for better separation
        df['Revenue'] = (df['Revenue'] ** 1.5).clip(upper=30)  # Apply power transformation and cap at 30

        # Add a small jitter to avoid overlaps in the 3D space
        jitter_amount = 0.1
        df['Realism'] = df['Realism'] + np.random.uniform(-jitter_amount, jitter_amount, df.shape[0])
        df['Evaluation'] = df['Evaluation'] + np.random.uniform(-jitter_amount, jitter_amount, df.shape[0])
        df['Speed'] = df['Speed'] + np.random.uniform(-jitter_amount, jitter_amount, df.shape[0])
        df['Customisation'] = df['Customisation'] + np.random.uniform(-jitter_amount, jitter_amount, df.shape[0])

        # Sidebar opacity selection
        opacity = st.sidebar.slider('Select Bubble Opacity', 0.1, 1.0, 0.7)

        # Chart 1: Realism vs Evaluation vs Customisation
        st.header('3D Bubble Chart 1: Realism vs Evaluation vs Customisation')
        fig1 = px.scatter_3d(
            df,
            x='Realism',
            y='Evaluation',
            z='Customisation',
            size='Revenue',
            color='Segment',
            hover_name='Segment',  # Add segment name to the bubble on hover
            opacity=opacity
        )
        fig1.update_layout(
            scene=dict(
                xaxis_title='Realism',
                yaxis_title='Evaluation',
                zaxis_title='Customisation',
                xaxis=dict(range=[0, 6]),
                yaxis=dict(range=[0, 6]),
                zaxis=dict(range=[0, 6])
            )
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Speed vs Customisation vs Realism
        st.header('3D Bubble Chart 2: Speed vs Customisation vs Realism')
        fig2 = px.scatter_3d(
            df,
            x='Speed',
            y='Customisation',
            z='Realism',
            size='Revenue',
            color='Segment',
            hover_name='Segment',  # Add segment name to the bubble on hover
            opacity=opacity
        )
        fig2.update_layout(
            scene=dict(
                xaxis_title='Speed',
                yaxis_title='Customisation',
                zaxis_title='Realism',
                xaxis=dict(range=[0, 6]),
                yaxis=dict(range=[0, 6]),
                zaxis=dict(range=[0, 6])
            )
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.error('The uploaded file must contain the following columns: Segment, Realism, Evaluation, Speed, Customisation, Revenue.')

else:
    st.warning('Please upload an Excel file to proceed.')

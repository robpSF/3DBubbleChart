import streamlit as st
import pandas as pd
import plotly.express as px

# Title and instructions
st.title('3D Bubble Chart Viewer from Excel')
st.write("""
Upload an Excel file with the following columns: **Segment, Realism, Evaluation, Speed, Customisation, Revenue**.
This app will create three interactive 3D bubble charts.
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

        # Slider for adjusting Revenue scaling
        st.sidebar.header('Bubble Size Scaling')
        scaling_factor = st.sidebar.slider('Select Revenue Scaling Factor', 1.0, 10.0, 3.0)

        # Apply scaling factor to Revenue
        df['Scaled Revenue'] = df['Revenue'] * scaling_factor

        # Chart 1: Realism vs Evaluation vs Customisation
        st.header('3D Bubble Chart 1: Realism vs Evaluation vs Customisation')
        fig1 = px.scatter_3d(
            df,
            x='Realism',
            y='Evaluation',
            z='Customisation',
            size='Scaled Revenue',
            color='Segment',
            hover_name='Segment',  # Add segment name to the bubble on hover
            opacity=0.7
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
            size='Scaled Revenue',
            color='Segment',
            hover_name='Segment',  # Add segment name to the bubble on hover
            opacity=0.7
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

        # Chart 3: Evaluation vs Speed vs Realism
        st.header('3D Bubble Chart 3: Evaluation vs Speed vs Realism')
        fig3 = px.scatter_3d(
            df,
            x='Evaluation',
            y='Speed',
            z='Realism',
            size='Scaled Revenue',
            color='Segment',
            hover_name='Segment',  # Add segment name to the bubble on hover
            opacity=0.7
        )
        fig3.update_layout(
            scene=dict(
                xaxis_title='Evaluation',
                yaxis_title='Speed',
                zaxis_title='Realism',
                xaxis=dict(range=[0, 6]),
                yaxis=dict(range=[0, 6]),
                zaxis=dict(range=[0, 6])
            )
        )
        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.error('The uploaded file must contain the following columns: Segment, Realism, Evaluation, Speed, Customisation, Revenue.')

else:
    st.warning('Please upload an Excel file to proceed.')

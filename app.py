import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Sample Data Creation
def create_sample_data():
    data = {
        'Claim ID': [1001, 1002, 1003, 1004, 1005],
        'CPT Code': ['99213', '99214', '99215', '99213', '99214'],
        'Date': ['2023-09-01', '2023-09-02', '2023-09-03', '2023-09-01', '2023-09-04'],
        'Days to Payment': [30, 45, 40, 35, 50],
        'Predicted Payment Date': [
            (datetime.strptime('2023-09-01', '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d'),
            (datetime.strptime('2023-09-02', '%Y-%m-%d') + timedelta(days=45)).strftime('%Y-%m-%d'),
            (datetime.strptime('2023-09-03', '%Y-%m-%d') + timedelta(days=40)).strftime('%Y-%m-%d'),
            (datetime.strptime('2023-09-01', '%Y-%m-%d') + timedelta(days=35)).strftime('%Y-%m-%d'),
            (datetime.strptime('2023-09-04', '%Y-%m-%d') + timedelta(days=50)).strftime('%Y-%m-%d')
        ]
    }
    df = pd.DataFrame(data)
    return df

# Load Data
df = create_sample_data()

# Streamlit app layout
st.title('Time to Payment Prediction Application')

# Filter by CPT Code (default: all)
cpt_codes = df['CPT Code'].unique()
selected_cpt_code = st.selectbox('Filter by CPT Code:', options=['All'] + list(cpt_codes), index=0)

if selected_cpt_code != 'All':
    df = df[df['CPT Code'] == selected_cpt_code]

# Display the data
st.subheader('Claim Data')
st.write(df)

# Group by predicted payment date and calculate total predicted payments
df['Predicted Payment Date'] = pd.to_datetime(df['Predicted Payment Date'])
payment_summary = df.groupby('Predicted Payment Date').size().reset_index(name='Total Payments')

# Plotly Time Series Chart
st.subheader('Total Predicted Payment by Date')
fig = px.line(payment_summary, x='Predicted Payment Date', y='Total Payments', title='Total Predicted Payments Over Time')

st.plotly_chart(fig)

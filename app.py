import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Function to create sample data
def create_sample_data():
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = start_date + timedelta(days=180)
    
    claim_ids = []
    cpt_codes = []
    dates = []
    days_to_payment = []
    predicted_payment_dates = []
    allowed_amounts = []

    # Generate at least 10 claims per day for a 6-month period
    while start_date <= end_date:
        num_claims = random.randint(10, 15)  # Random between 10 and 15 claims per day
        for _ in range(num_claims):
            claim_ids.append(random.randint(1000, 9999))
            cpt_codes.append(random.choice(['99213', '99214', '99215']))
            dates.append(start_date.strftime('%Y-%m-%d'))
            payment_days = random.randint(30, 60)  # Random days to payment
            days_to_payment.append(payment_days)
            predicted_payment_date = start_date + timedelta(days=payment_days)
            predicted_payment_dates.append(predicted_payment_date.strftime('%Y-%m-%d'))
            allowed_amounts.append(round(random.uniform(100, 500), 2))  # Random allowed amount between 100 and 500
        
        start_date += timedelta(days=1)
    
    data = {
        'Claim ID': claim_ids,
        'CPT Code': cpt_codes,
        'Date': dates,
        'Days to Payment': days_to_payment,
        'Predicted Payment Date': predicted_payment_dates,
        'Allowed Amount': allowed_amounts
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

# Convert 'Predicted Payment Date' to datetime format for easier manipulation
df['Predicted Payment Date'] = pd.to_datetime(df['Predicted Payment Date'])

# Group by predicted payment date and calculate the total allowed amount
payment_summary = df.groupby('Predicted Payment Date')['Allowed Amount'].sum().reset_index()

# Plotly Time Series Chart: Total Allowed Amount by Predicted Payment Date
st.subheader('Total Allowed Amount by Predicted Payment Date')
fig = px.line(payment_summary, x='Predicted Payment Date', y='Allowed Amount', title='Total Allowed Amount Over Time')

st.plotly_chart(fig)

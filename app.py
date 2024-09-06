import streamlit as st
import pandas as pd
import random

# Function to generate random data
def generate_data(num_rows):
    claim_ids = [random.randint(1000, 9999) for _ in range(num_rows)]
    cpt_codes = random.choices(['99213', '80050', '99214', '99381', '99215', '85025', '93000'], k=num_rows)
    diagnoses = random.choices(['Hypertension', 'Diabetes', 'Asthma'], k=num_rows)
    days_to_payment = [random.randint(1, 90) for _ in range(num_rows)]  # Generate random days between 1 and 90
    
    data = {
        'Claim ID': claim_ids,
        'CPT Code': cpt_codes,
        'Diagnosis': diagnoses,
        'Days to Payment': days_to_payment
    }
    
    return pd.DataFrame(data)

# Generate 50 rows of data
df = generate_data(50)

# Title of the app
st.title('Claim Days to Payment Table')

# Display the filter controls
st.sidebar.header('Filter by Days to Payment')

# Slider to filter by days
min_days, max_days = st.sidebar.slider(
    'Select the range of Days to Payment',
    min_value=int(df['Days to Payment'].min()), 
    max_value=int(df['Days to Payment'].max()), 
    value=(int(df['Days to Payment'].min()), int(df['Days to Payment'].max()))
)

# Filter the DataFrame based on the selected range
filtered_df = df[(df['Days to Payment'] >= min_days) & (df['Days to Payment'] <= max_days)]

# Sort the filtered DataFrame by "Days to Payment" (ascending order)
df_sorted = filtered_df.sort_values(by='Days to Payment', ascending=True)

# Display the filtered and sorted DataFrame
st.write(f'Displaying claims with Days to Payment between {min_days} and {max_days}:')
st.dataframe(df_sorted)

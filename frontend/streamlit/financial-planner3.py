import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import boto3

# Database connection
dynamodb = boto3.resource('dynamodb')
input_table = dynamodb.Table('input_data')
output_table = dynamodb.Table('output_data')

# Page layout
col1, col2 = st.columns(2)

# Home tab 
def home():
    with col1:
        st.header('Home')
        st.write('Welcome to the financial planner!')

    with col2:
        st.header('Monthly Budget')
        income = st.number_input('Monthly income', min_value=0, value=5000)
        expenses = st.number_input('Monthly expenses', min_value=0, value=4000)
        input_table.put_item(Item={'income': income, 'expenses': expenses})

        budget_df = pd.DataFrame({'Category': ['Income', 'Expenses'], 
                                  'Amount': [income, expenses]})

        fig, ax = plt.subplots()
        ax.pie(budget_df['Amount'], labels=budget_df['Category'], autopct='%1.1f%%')
        st.pyplot(fig)

# Cars tab
def cars():
    with col1:
        st.header('Cars')
        st.write('Add and view your cars here')

    with col2:
        st.header('Car Payments')
        car_loan = st.number_input('Monthly car payment', min_value=0, value=500)
        input_table.put_item(Item={'car_loan': car_loan})

        st.write('You are paying $%d per month for your car loans' % car_loan)

# Loans tab
def loans():
   with col1:
        st.header('Loans')
        st.write('Add and view your loans here')

   with col2:
        st.header('Loan Payments')
        student_loan = st.number_input('Monthly student loan payment', min_value=0, value=200)
        mortgage = st.number_input('Monthly mortgage payment', min_value=0, value=1500)
        input_table.put_item(Item={'student_loan': student_loan, 'mortgage': mortgage})

        total_loans = student_loan + mortgage
        st.write('You are paying $%d per month for your total loans' % total_loans)

# Investments tab
def investments():
    with col1:
        st.header('Investments')
        st.write('Add and view your investments here')

    with col2:
        st.header('Investment Income')
        investment_income = st.number_input('Monthly investment income', min_value=0, value=100)
        input_table.put_item(Item={'investment_income': investment_income})

        st.write('You are earning $%d per month from your investments' % investment_income)

# Navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go To', ['Home', 'Cars', 'Loans', 'Investments'])

if page == 'Home':
    home()
elif page == 'Cars':
    cars()
elif page == 'Loans':
    loans()  
else:
    investments()

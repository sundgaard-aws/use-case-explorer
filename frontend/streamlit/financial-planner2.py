import streamlit as st
import pandas as pd 
import plotly.express as px

st.title('Financial Planner')

income = st.number_input('Monthly income', value=5000)
expenses = st.number_input('Monthly expenses', value=3000)

loan_amount = st.number_input('Total loan amount', value=100000) 
loan_interest = st.number_input('Yearly interest rate', value=5.0)
loan_years = st.number_input('Number of years', value=30)

investment_amount = st.number_input('Investment amount', value=1000)
investment_interest = st.number_input('Yearly interest rate', value=7.0)
investment_years = st.number_input('Number of years', value=10) 

monthly_savings = income - expenses

loan_payments = loan_amount * (loan_interest/100) * (1 + loan_interest/100)**loan_years / ((1 + loan_interest/100)**loan_years - 1) 

investment_gains = investment_amount * (1 + investment_interest/100)**investment_years

fig = px.pie(values=[expenses, loan_payments, investment_gains], 
             names=['Expenses', 'Loan Payments', 'Investment Gains'])

st.plotly_chart(fig)

st.write('Monthly savings:', monthly_savings)
st.write('Monthly loan payment:', loan_payments) 
st.write('Investment gains:', investment_gains)
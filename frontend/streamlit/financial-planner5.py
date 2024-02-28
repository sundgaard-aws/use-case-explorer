import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import ClientError

# Create DynamoDB client 
dynamodb = boto3.client('dynamodb')

# Create tables if they don't exist
try:
    dynamodb.create_table(
        TableName='input_data',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5,'WriteCapacityUnits': 5}
    )
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceInUseException':
        raise
        
try:
    dynamodb.create_table(
        TableName='output_data',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5,'WriteCapacityUnits': 5}
    )
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceInUseException':
        raise
        
# Page layout
st.set_page_config(page_title='Financial Planner')

st.title('Financial Planner')

# Input column
with st.container():
    st.header('Inputs')
    
    income = st.number_input('Monthly Income', min_value=0.0, value=5000.0, step=100.0)
    
    housing = st.number_input('Housing', min_value=0.0, value=1000.0, step=100.0)
    utilities = st.number_input('Utilities', min_value=0.0, value=150.0, step=10.0)
    household = st.number_input('Household', min_value=0.0, value=650.0, step=50.0)  
    transport = st.number_input('Transport', min_value=0.0, value=650.0, step=50.0)
    food = st.number_input('Food', min_value=0.0, value=650.0, step=50.0)
    healthcare = st.number_input('Healthcare', min_value=0.0, value=325.0, step=25.0)
    personal = st.number_input('Personal', min_value=0.0, value=200.0, step=10.0)
    entertainment = st.number_input('Entertainment', min_value=0.0, value=200.0, step=10.0)
    other = st.number_input('Other', min_value=0.0, value=100.0, step=10.0)
    
    # Save inputs to DynamoDB
    try:
        dynamodb.put_item(
            TableName='input_data',
            Item={'id': {'S': '1'}, 
                  'income': {'N': str(income)},
                  'housing': {'N': str(housing)},
                  'utilities': {'N': str(utilities)},
                  'household': {'N': str(household)},
                  'transport': {'N': str(transport)},
                  'food': {'N': str(food)},
                  'healthcare': {'N': str(healthcare)},
                  'personal': {'N': str(personal)},
                  'entertainment': {'N': str(entertainment)},
                  'other': {'N': str(other)}}
        )
    except ClientError as e:
        st.error(e.response['Error']['Message'])
        raise

# Output column 
with st.container():
    st.header('Outputs')
    
    expenses = housing + utilities + household + transport + food + healthcare + personal + entertainment + other
    savings = income - expenses
    
    c1, c2 = st.columns(2)
    
    # Expenses pie chart 
    fig, ax = plt.subplots()
    labels = ['Housing', 'Utilities', 'Household', 'Transport', 'Food', 'Healthcare', 
              'Personal', 'Entertainment', 'Other']
    values = [housing, utilities, household, transport, food, healthcare, personal, 
              entertainment, other]
    ax.pie(values, labels=labels, autopct='%1.1f%%')
    c1.pyplot(fig)
    
    # Savings stack chart
    fig, ax = plt.subplots()
    labels = ['Expenses', 'Savings']
    values = [expenses, savings]
    ax.bar(labels, values)
    ax.set_title('Monthly Budget')
    c2.pyplot(fig)
    
    c3, c4 = st.columns(2)
    
    c3.metric('Total Expenses', f'{expenses:,.2f}')
    c4.metric('Total Savings', f'{savings:,.2f}')
    
    # Save outputs to DynamoDB
    try:
        dynamodb.put_item(
            TableName='output_data',
            Item={'id': {'S': '1'}, 
                  'expenses': {'N': str(expenses)},
                  'savings': {'N': str(savings)}}
        ) 
    except ClientError as e:
        st.error(e.response['Error']['Message'])
        raise
        
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Cars", "Loans", "Investments"])

with tab1:
   st.header('Home')
   # Home content here
   
with tab2:
   st.header('Cars')
   # Car content here
   
with tab3:
   st.header('Loans')
   # Loan content here
   
with tab4:
   st.header('Investments')
   # Investment content here

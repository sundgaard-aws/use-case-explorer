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
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    dynamodb.create_table(
        TableName='output_data',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
except ClientError as e:
    if e.response['Error']['Code'] != 'ResourceInUseException':
        raise
        
# Layout  
col1, col2 = st.columns(2)

with col1:
    st.title("Financial Planner")

with col2:
    st.text("")
    
st.markdown("""---""")
    
# Homes tab
st.header("Homes")

home_purchase_price = st.number_input("Home Purchase Price") 
home_down_payment_percent = st.slider("Down Payment Percent", 0, 100, 10)
home_down_payment = home_purchase_price * (home_down_payment_percent/100)

st.write("Down Payment:", home_down_payment)

# Plot pie chart 
labels = 'Down Payment', 'Remaining Mortgage'
sizes = [home_down_payment, home_purchase_price-home_down_payment]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
st.pyplot(fig1)

# Save home data
home_data = {'purchase_price': home_purchase_price, 
             'down_payment': home_down_payment}

dynamodb.put_item(TableName='input_data', Item={'id': {'S': 'home'}, 'data': {'M': home_data}})

# Cars tab  
st.header("Cars")

car_purchase_price = st.number_input("Car Purchase Price")
car_down_payment_percent = st.slider("Down Payment Percent", 0, 100, 20)  
car_down_payment = car_purchase_price * (car_down_payment_percent/100)

st.write("Down Payment:", car_down_payment)

# Plot pie chart
labels = 'Down Payment', 'Remaining Loan'  
sizes = [car_down_payment, car_purchase_price-car_down_payment]

fig2, ax2 = plt.subplots()
ax2.pie(sizes, labels=labels, autopct='%1.1f%%')
st.pyplot(fig2)

# Save car data
car_data = {'purchase_price': car_purchase_price,
            'down_payment': car_down_payment}

dynamodb.put_item(TableName='input_data', Item={'id': {'S': 'car'}, 'data': {'M': car_data}})

# Loans tab
st.header("Loans")

loan_amount = st.number_input("Loan Amount")
interest_rate = st.number_input("Interest Rate") 
loan_months = st.number_input("Number of Months")

monthly_payment = loan_amount * (interest_rate/100) * (1 + interest_rate/100)**loan_months / ((1 + interest_rate/100)**loan_months - 1)

st.write("Monthly Payment:", monthly_payment)

# Save loan data
loan_data = {'amount': loan_amount,
             'interest_rate': interest_rate,
             'months': loan_months,
             'monthly_payment': monthly_payment}

dynamodb.put_item(TableName='input_data', Item={'id': {'S': 'loan'}, 'data': {'M': loan_data}})

# Investments tab
st.header("Investments")

investment_amount = st.number_input("Investment Amount")
expected_return = st.number_input("Expected Annual Return")
investment_years = st.number_input("Number of Years")

accrued_value = investment_amount * (1 + expected_return/100) ** investment_years

st.write("Accrued Value:", accrued_value) 

# Plot bar chart
fig3, ax3 = plt.subplots()
ax3.bar(['Investment','Return'], [investment_amount, accrued_value-investment_amount])
st.pyplot(fig3)

# Save investment data
investment_data = {'amount': investment_amount,
                   'return': expected_return,
                   'years': investment_years,
                   'accrued_value': accrued_value}
                   
dynamodb.put_item(TableName='input_data', Item={'id': {'S': 'investment'}, 'data': {'M': investment_data}})

# Output summary
st.header("Summary")

home_data = dynamodb.get_item(TableName='input_data', Key={'id': {'S': 'home'}})['Item']['data']['M']
car_data = dynamodb.get_item(TableName='input_data', Key={'id': {'S': 'car'}})['Item']['data']['M'] 
loan_data = dynamodb.get_item(TableName='input_data', Key={'id': {'S': 'loan'}})['Item']['data']['M']
investment_data = dynamodb.get_item(TableName='input_data', Key={'id': {'S': 'investment'}})['Item']['data']['M']

total_down_payment = float(home_data['down_payment']) + float(car_data['down_payment'])
total_monthly_payments = float(loan_data['monthly_payment'])
total_investment = float(investment_data['amount'])
total_return = float(investment_data['accrued_value']) - float(investment_data['amount'])

summary_data = {'total_down_payment': total_down_payment,
                'total_monthly_payments': total_monthly_payments,
                'total_investment': total_investment,
                'total_return': total_return}
                
dynamodb.put_item(TableName='output_data', Item={'id': {'S': 'summary'}, 'data': {'M': summary_data}})

st.write("Total Down Payment:", total_down_payment)
st.write("Total Monthly Payments:", total_monthly_payments) 
st.write("Total Investment:", total_investment)
st.write("Total Return:", total_return)
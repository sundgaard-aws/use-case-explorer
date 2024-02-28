import streamlit as st
import pandas as pd

st.title("Financial Planner")

starting_balance = st.number_input("Starting Balance", min_value=0, value=10000)
monthly_contribution = st.number_input("Monthly Contribution", min_value=0, value=500)  
years = st.number_input("Years", min_value=0, value=5)
interest_rate = st.number_input("Interest Rate (%%)", min_value=0.0, value=5.0) / 100

df = pd.DataFrame()
df["Year"] = list(range(0, years+1))
df["Starting Balance"] = starting_balance
df["Monthly Contribution"] = monthly_contribution

for i in range(1, years+1):
  prev_balance = df.loc[i-1, "Starting Balance"]
  contribution = monthly_contribution
  interest = prev_balance * interest_rate
  end_balance = prev_balance + contribution + interest
  df.loc[i, "Starting Balance"] = end_balance

st.dataframe(df)

end_balance = df["Starting Balance"].iloc[-1]
st.write("Ending balance: ${:,.2f}".format(end_balance))
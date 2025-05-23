import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ This MUST be the first Streamlit command
st.set_page_config(page_title="💸 Expense Tracker", layout="centered")

st.title("💸 Expense Tracker")

# Sample DataFrame to start with
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Form to input new expense
with st.form("expense_form"):
    date = st.date_input("Date", value=datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = pd.DataFrame({
            "Date": [pd.to_datetime(date)],
            "Category": [category],
            "Amount": [amount],
            "Description": [description]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_expense], ignore_index=True)
        st.success("Expense added!")

# Filter section
st.subheader("📅 Filter Expenses")

# Safely get min date
if not st.session_state.df.empty:
    safe_min_date = st.session_state.df["Date"].min()
else:
    safe_min_date = datetime.today()

start_date = st.date_input("Start Date", value=safe_min_date)
end_date = st.date_input("End Date", value=datetime.today())

# Filter the DataFrame based on dates
filtered_df = st.session_state.df[
    (st.session_state.df["Date"] >= pd.to_datetime(start_date)) &
    (st.session_state.df["Date"] <= pd.to_datetime(end_date))
]

# Display filtered results
st.subheader("📊 Expense Summary")
st.dataframe(filtered_df)

# Show total expenses
total = filtered_df["Amount"].sum()
st.metric(label="Total Expenses", value=f"₹ {total:,.2f}")

import streamlit as st
import pandas as pd
import os

FILENAME = "expenses.csv"

st.set_page_config(page_title="Expense Analyzer", layout="centered")

st.title("📊 Personal Expense Analyzer")
st.write("Track and analyze your spending easily!")

# --- FORM TO ADD EXPENSES ---
st.header("➕ Add New Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount (₪)", min_value=0.0, step=1.0, format="%.2f")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Rent", "Other"])
    
    description = st.text_input("Description")
    submitted = st.form_submit_button("Save Expense")

if submitted:
    if amount > 0:
        file_exists = os.path.exists(FILENAME)
        df_new = pd.DataFrame([{"Amount (ILS)": amount, "Category": category, "Description": description}])
        
        # Save to CSV
        df_new.to_csv(FILENAME, mode="a", header=not file_exists, index=False)
        st.success(f"Added ₪{amount:.2f} under {category}!")
        st.rerun()
    else:
        st.warning("Please enter an amount greater than 0.")

# --- DISPLAY EXPENSES & SUMMARY ---
st.divider()
st.header("📈 Spending Summary")

if os.path.exists(FILENAME):
    df = pd.read_csv(FILENAME)
    
    # Filter out empty or corrupted rows if any exist
    df["Amount (ILS)"] = pd.to_numeric(df["Amount (ILS)"], errors="coerce")
    df = df.dropna(subset=["Amount (ILS)"])

    if not df.empty:
        total_spent = df["Amount (ILS)"].sum()
        st.metric(label="Total Amount Spent", value=f"₪{total_spent:,.2f}")

        # Show Table
        st.subheader("Recent Expenses")
        st.dataframe(df, use_container_width=True)

        # Show Chart
        st.subheader("Spending by Category")
        category_totals = df.groupby("Category")["Amount (ILS)"].sum()
        st.bar_chart(category_totals)
    else:
        st.info("No valid expenses recorded yet.")
else:
    st.info("No expenses added yet. Fill out the form above!")
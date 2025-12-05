import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CONFIGURATION ---
DATA_FILE = "trade_journal.csv"

# --- SETUP PAGE ---
st.set_page_config(page_title="My Trade Journal", layout="centered")
st.title("📈 Trader's Diary")

# --- LOAD DATA ---
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date", "Segment", "Instrument", "Type", 
            "Expiry", "Strike", "Action", "Qty", "Price", "Notes"
        ])

df = load_data()

# --- INPUT FORM (Mobile Friendly) ---
with st.expander("📝 Add New Trade", expanded=True):
    with st.form("trade_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trade_date = st.date_input("Date", date.today())
            segment = st.selectbox("Market", ["NIFTY OPT", "NIFTY FUT", "STOCK OPT", "STOCK FUT", "MCX FUT"])
            instrument = st.text_input("Instrument", "NIFTY").upper()
            
        with col2:
            action = st.radio("Action", ["BUY", "SELL"], horizontal=True)
            trade_type = st.selectbox("Type", ["CE", "PE", "FUT"])
            price = st.number_input("Price", min_value=0.0, step=0.05, format="%.2f")
            
        qty = st.number_input("Quantity (Total shares/units)", min_value=1, step=1)
        
        # Only show Strike and Expiry if not Futures (Logic handled in UI via simplifications)
        strike = st.number_input("Strike Price (0 for Fut)", min_value=0, step=50)
        expiry = st.date_input("Expiry Date")
        notes = st.text_area("Reason for Trade")
        
        submitted = st.form_submit_button("💾 Save Trade")
        
        if submitted:
            new_trade = {
                "Date": trade_date,
                "Segment": segment,
                "Instrument": instrument,
                "Type": trade_type,
                "Expiry": expiry,
                "Strike": strike,
                "Action": action,
                "Qty": qty,
                "Price": price,
                "Notes": notes
            }
            
            # Append and Save
            df = pd.concat([df, pd.DataFrame([new_trade])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Trade Saved!")

# --- DASHBOARD (Your Analysis) ---
st.divider()
st.subheader("📊 Recent Activity")

if not df.empty:
    # Quick Summary Logic
    df['Value'] = df['Price'] * df['Qty']
    
    # Show last 5 trades (Reverse order)
    st.dataframe(df.tail(5).iloc[::-1], use_container_width=True)
    
    # Simple Metrics
    total_trades = len(df)
    st.metric("Total Trades Recorded", total_trades)
else:
    st.info("No trades recorded yet. Enter your first trade above.")
import logging 
logging.basicConfig(level=logging.INFO)

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass

from src.utils.accounts import get_account_details, get_account_transactions_details
from src.utils.visualization import generate_info_card, generate_metric_card

from src.constants.theme import PRIMARY_COLOR, SECONDARY_BACKGROUND_COLOR, TEXT_COLOR

@dataclass
class ProfileContext:
    accounts_details_df: pd.DataFrame
    transactions_df: pd.DataFrame
    account_id: str

class ProfileAnalysis:
    def __init__(self, profile_context: ProfileContext):
        self.account_id = profile_context.account_id
        self.account_details_df = profile_context.accounts_details_df
        self.original_transactions_df = profile_context.transactions_df
        self.filtered_transactions_df = self._filter_transactions()
        
    def _filter_transactions(self) -> pd.DataFrame:
        return self.original_transactions_df.query("sender == @self.account_id or receiver == @self.account_id").copy()
    
    def generate_profile_overview(self):
        acc_details = get_account_details(self.account_details_df, self.account_id)
        generate_info_card("Name", acc_details["name"])
        st.text('')
        generate_info_card("Email", acc_details["email"])
        st.text('')
        generate_info_card("Mobile number", acc_details["mobile"])
        st.text('')
        generate_info_card("Location", acc_details["location"])
        st.text('')
        generate_info_card("Registration", acc_details["registration_date"])

    def generate_metrics(self):
        transaction_details = get_account_transactions_details(self.filtered_transactions_df, self.account_id)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            generate_metric_card("Total amount sent", f'${transaction_details["amount_sent"]}')
        with col2:
            generate_metric_card("Total amount received", f'${transaction_details["amount_received"]}')
        with col3:
            generate_metric_card("Transactions count", transaction_details["transactions_count"])
        with col4:
            generate_metric_card("Laundering probability (AI prediction)", "65%")

    def generate_transactions_timeline_chart(self):
        transactions_timeline_df = self.filtered_transactions_df.copy()
        transactions_timeline_df["date"] = pd.to_datetime(transactions_timeline_df["timestamp"]).dt.date
        received_transactions = transactions_timeline_df.query("receiver == @self.account_id").groupby('date', as_index=False)['amount_paid'].sum()
        sent_transactions = transactions_timeline_df.query("sender == @self.account_id").groupby('date', as_index=False)['amount_paid'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=received_transactions.date, y=received_transactions.amount_paid, name='Received amount', line=dict(color=PRIMARY_COLOR)))
        fig.add_trace(go.Scatter(x=sent_transactions.date, y=sent_transactions.amount_paid, name='Sent amount', line=dict(color='#fd7e14')))
        fig.update_layout(
            title=dict(text='Transactions timeline'),
            plot_bgcolor=SECONDARY_BACKGROUND_COLOR,
            paper_bgcolor=SECONDARY_BACKGROUND_COLOR,
            font=dict(color=TEXT_COLOR),
            xaxis=dict(showgrid=False, gridcolor="lightgrey"),
            yaxis=dict(showgrid=True, gridcolor="lightgrey"),
            hovermode="x unified",
            title_x=0.45
        )
        st.plotly_chart(fig, use_container_width=True)
        logging.info("Transaction timeline graph generated successfully.")

    def generate_payment_method_pie_chart(self):
        payment_type_df = self.filtered_transactions_df.copy()
        payment_type_df = payment_type_df.groupby("payment_format", as_index=False).amount_paid.sum()
        custom_colors = {
            "Cheque": PRIMARY_COLOR,
            "Credit Card": "#fd7e14",
            "ACH": "#dc3545",
            "Cash": "#66b3ff",
            "Wire": "#28a745",
            "Bitcoin": "#D4A157"
        }
        fig = px.pie(
            payment_type_df, 
            names="payment_format", 
            values="amount_paid", 
            title="Payment Method Distribution",
            hole=0.4,
            color="payment_format",
            color_discrete_map=custom_colors
        )
        fig.update_layout(
            plot_bgcolor=SECONDARY_BACKGROUND_COLOR,
            paper_bgcolor=SECONDARY_BACKGROUND_COLOR,
            title_x=0.30
        )
        st.plotly_chart(fig, use_container_width=True)

    def generate_transactions_distribuition(self):
        fig = px.histogram(
            self.filtered_transactions_df,
            x="amount_paid",
            title="Transaction Value Distribution",
            labels={"amount_paid": "Transaction Amount"},
            color_discrete_sequence=[PRIMARY_COLOR]
        )
        fig.update_layout(
            xaxis_title="Transaction Amount (USD)",
            yaxis_title="Frequency",
            bargap=0.1,
            plot_bgcolor=SECONDARY_BACKGROUND_COLOR,
            paper_bgcolor=SECONDARY_BACKGROUND_COLOR,
            title_x=0.30,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    def generate_dataframe_overview(self):
        st.dataframe(self.filtered_transactions_df.style.applymap(lambda x: 'background-color : white'),
            hide_index=True,
            height=400,
            use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from tokenwise import TokenWise
from dotenv import load_dotenv
import os
from datetime import datetime
import io

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Solana Token Analytics",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    /* Main page background */
    .stApp {
        background: #ffffff;
    }
    
    /* Container styling */
    .stButton {
        text-align: center;
        margin: 0 auto;
        display: flex;
        justify-content: center;
        padding-top: 1rem;
    }
    
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 8px;
        padding: 15px 32px;
        font-size: 18px;
        font-weight: 500;
        border: none;
        width: 250px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        background-color: #333333;
    }
    
    .title {
        font-size: 52px;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin: 0.5rem 0 1rem 0;
        padding: 0;
        letter-spacing: -1px;
    }

    .session-selector {
        max-width: 300px;
        margin: 1rem auto;
        padding: 0.5rem;
    }
    
    /* Net direction styling */
    .net-direction {
        font-size: 28px;
        font-weight: 600;
        text-align: center;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        background-color: #f8f9fa;
    }

    .net-direction-buy {
        color: #28a745;
    }

    .net-direction-sell {
        color: #dc3545;
    }

    .direction-note {
        font-size: 16px;
        color: #666;
        text-align: center;
        margin-top: 10px;
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stDataFrame table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }
    
    .stDataFrame th {
        background-color: #f8f9fa;
        color: #000000;
        padding: 12px;
        font-weight: 600;
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
        color: #000000;
    }
    
    /* Error message styling */
    .stAlert {
        background-color: #fff5f5;
        border-left: 5px solid #ff0000;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }

    /* Subheader styling */
    .stSubheader {
        color: #000000;
        font-weight: 600;
        margin: 1.5rem 0;
    }

    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        color: #000000;
        border: 1px solid #eaeaea;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #000000;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Simple title
st.markdown('<p class="title">Solana Token Analytics Dashboard</p>', unsafe_allow_html=True)

# Initialize TokenWise instance
token_wise = TokenWise()

# Center column for start button
col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("Start New Session"):
        with st.spinner('Starting new session...'):
            try:
                transactions = token_wise.start_session()
                st.success('New session started successfully!')
                st.rerun()
            except Exception as e:
                st.error(f'Error starting session: {str(e)}')

# Get available session dates
session_dates = token_wise.get_session_dates()

# Session date selector
if session_dates:
    st.markdown('<div class="session-selector">', unsafe_allow_html=True)
    selected_date = st.selectbox(
        "Select Session Date",
        options=session_dates,
        format_func=lambda x: x.strftime("%Y-%m-%d %H:%M:%S"),
        index=len(session_dates)-1  # Select the most recent date by default
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Get data for selected session
    with st.spinner('Loading session data...'):
        try:
            # Get holders and transactions for the selected session
            holders = token_wise.get_token_holders(selected_date)
            transactions = token_wise.get_transactions(selected_date)

            # Display basic stats
            st.markdown("### Session Overview")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Holders", len(holders))
            with col2:
                st.metric("Total Transactions", len(transactions))

            # Add download buttons in a row
            col1, col2 = st.columns(2)
            with col1:
                # Get transaction report
                tx_report = token_wise.get_transaction_report(selected_date)
                # Excel download button
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    tx_report.to_excel(writer, sheet_name='Transactions', index=False)
                    # Get the workbook and the worksheet
                    workbook = writer.book
                    worksheet = writer.sheets['Transactions']
                    
                    # Auto-adjust columns width
                    for idx, col in enumerate(tx_report.columns):
                        series = tx_report[col]
                        max_len = max(
                            series.astype(str).map(len).max(),  # len of largest item
                            len(str(series.name))  # len of column name/header
                        ) + 1  # adding a little extra space
                        worksheet.set_column(idx, idx, max_len)  # set column width
                
                st.download_button(
                    label="📥 Download Transaction Report (Excel)",
                    data=buffer.getvalue(),
                    file_name=f'transactions_{selected_date.strftime("%Y%m%d_%H%M%S")}.xlsx',
                    mime='application/vnd.ms-excel'
                )
            
            with col2:
                # CSV download button
                csv = tx_report.to_csv(index=False)
                st.download_button(
                    label="📥 Download Transaction Report (CSV)",
                    data=csv,
                    file_name=f'transactions_{selected_date.strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv'
                )

            # Create distribution charts
            if transactions:
                # Count protocol occurrences
                protocol_counts = {}
                direction_counts = {'buy': 0, 'sell': 0}
                for tx in transactions:
                    # Protocol counting
                    protocol = tx.token_transfers.protocol
                    protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
                    
                    # Direction counting
                    direction = tx.direction.lower()
                    direction_counts[direction] = direction_counts.get(direction, 0) + 1

                # Calculate net direction
                total_transactions = direction_counts['buy'] + direction_counts['sell']
                if total_transactions > 0:
                    buy_percentage = (direction_counts['buy'] / total_transactions) * 100
                    sell_percentage = (direction_counts['sell'] / total_transactions) * 100
                    
                    # Determine if buy-heavy or sell-heavy
                    is_buy_heavy = direction_counts['buy'] > direction_counts['sell']
                    direction_class = "net-direction-buy" if is_buy_heavy else "net-direction-sell"
                    direction_text = "BUY-HEAVY" if is_buy_heavy else "SELL-HEAVY"
                    
                    # Display net direction
                    st.markdown(f"""
                        <div class="net-direction">
                            <div class="{direction_class}">Net Direction: {direction_text}</div>
                            <div class="direction-note">
                                Buy: {buy_percentage:.1f}% ({direction_counts['buy']} transactions)<br>
                                Sell: {sell_percentage:.1f}% ({direction_counts['sell']} transactions)
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                # Create DataFrames for plotting
                protocol_df = pd.DataFrame([
                    {"Protocol": protocol, "Count": count}
                    for protocol, count in protocol_counts.items()
                ]).sort_values("Count", ascending=False)

                direction_df = pd.DataFrame([
                    {"Direction": direction.upper(), "Count": count}
                    for direction, count in direction_counts.items()
                ]).sort_values("Count", ascending=False)

                # Create tabs for visualizations
                tab1, tab2 = st.tabs(["Protocol Distribution", "Direction Distribution"])
                
                with tab1:
                    # Protocol distribution chart
                    fig_protocol = px.bar(
                        protocol_df,
                        x="Protocol",
                        y="Count",
                        title="Transaction Distribution by Protocol",
                        color="Protocol",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    fig_protocol.update_layout(
                        showlegend=False,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        title_x=0.5,
                        title_font_size=20,
                        xaxis_title="Protocol",
                        yaxis_title="Number of Transactions",
                        xaxis=dict(tickangle=45),
                        bargap=0.2,
                        height=400,
                        margin=dict(t=50, b=100)
                    )
                    
                    st.plotly_chart(fig_protocol, use_container_width=True)
                
                with tab2:
                    # Direction distribution chart
                    fig_direction = px.bar(
                        direction_df,
                        x="Direction",
                        y="Count",
                        title="Transaction Distribution by Direction",
                        color="Direction",
                        color_discrete_sequence=['#FF9B9B', '#9BFF9D']  # Red for sell, Green for buy
                    )
                    
                    fig_direction.update_layout(
                        showlegend=False,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        title_x=0.5,
                        title_font_size=20,
                        xaxis_title="Direction",
                        yaxis_title="Number of Transactions",
                        bargap=0.2,
                        height=400,
                        margin=dict(t=50, b=100)
                    )
                    
                    st.plotly_chart(fig_direction, use_container_width=True)

            # Display token holders in a data table
            if holders:
                st.markdown("### Token Holders")
                holders_df = pd.DataFrame([
                    {
                        "Rank": idx + 1,
                        "Wallet Address": holder.address,
                        "Token Amount": f"{holder.amount:,.2f}"
                    } for idx, holder in enumerate(holders)
                ])
                
                st.dataframe(
                    holders_df,
                    column_config={
                        "Rank": st.column_config.NumberColumn(
                            "Rank",
                            help="Position in top holders list",
                            format="%d"
                        ),
                        "Wallet Address": st.column_config.TextColumn(
                            "Wallet Address",
                            help="Solana wallet address",
                            width="large"
                        ),
                        "Token Amount": st.column_config.TextColumn(
                            "Token Amount",
                            help="Number of tokens held",
                            width="medium"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # Add CSV download button
                csv = holders_df.to_csv(index=False)
                st.download_button(
                    label="Download Token Holders Data",
                    data=csv,
                    file_name=f'token_holders_{selected_date.strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                )

        except Exception as e:
            st.error(f'Error loading session data: {str(e)}')
else:
    st.info('No sessions available. Click "Start New Session" to begin analysis.') 

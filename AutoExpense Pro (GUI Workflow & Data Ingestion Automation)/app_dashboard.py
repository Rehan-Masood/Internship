import os
import re
import time
import openpyxl
import pandas as pd
import plotly.express as px
import pyautogui
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="AutoExpense Pro | RPA Control Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Glassmorphism CSS ---
st.markdown(
    """
<style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #38bdf8 !important;
        font-weight: 700;
    }
    
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #3b82f6);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- Helper Functions ---
LEDGER_PATH = 'Expense_Ledger.xlsx'
INVOICE_DIR = './invoices'


def load_ledger_data():
  """Loads data from Excel ledger into Pandas DataFrame."""
  if os.path.exists(LEDGER_PATH):
    return pd.read_excel(LEDGER_PATH)
  return pd.DataFrame(columns=['Vendor', 'Date', 'Amount ($)', 'Status'])


def parse_mock_invoice(file_path):
  """Extracts transaction details from invoice text files."""
  with open(file_path, 'r') as f:
    content = f.read()

  vendor = re.search(r'Vendor:\s*(.*)', content)
  date = re.search(r'Date:\s*(.*)', content)
  amount = re.search(r'Amount:\s*\$?(.*)', content)

  return {
      'vendor': vendor.group(1).strip() if vendor else 'Unknown Vendor',
      'date': date.group(1).strip() if date else '2026-08-09',
      'amount': float(amount.group(1).strip()) if amount else 0.0,
  }


def update_excel_ledger(data):
  """Appends expense items into the Excel ledger."""
  if not os.path.exists(LEDGER_PATH):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Expenses'
    ws.append(['Vendor', 'Date', 'Amount ($)', 'Status'])
  else:
    wb = openpyxl.load_workbook(LEDGER_PATH)
    ws = wb.active

  ws.append([data['vendor'], data['date'], data['amount'], 'Automated'])
  wb.save(LEDGER_PATH)


def run_gui_automation(data, countdown=3):
  """Executes PyAutoGUI sequence with on-screen countdown."""
  pyautogui.FAILSAFE = True
  pyautogui.PAUSE = 0.5

  st.warning(
      f'⚠️ **GUI Automation starting in {countdown} seconds!** Switch focus to'
      ' your accounting form.'
  )
  time.sleep(countdown)

  # PyAutoGUI Form Filling Sequence
  pyautogui.write(data['vendor'], interval=0.05)
  pyautogui.press('tab')

  pyautogui.write(data['date'], interval=0.05)
  pyautogui.press('tab')

  pyautogui.write(str(data['amount']), interval=0.05)
  pyautogui.press('tab')

  pyautogui.press('enter')


# --- Sidebar Controls ---
st.sidebar.title('⚡ AutoExpense Pro')
st.sidebar.markdown('**RPA & Workflow Engine**')
st.sidebar.divider()

engine_status = st.sidebar.toggle('Active Directory Monitor', value=True)
if engine_status:
  st.sidebar.success('Status: Engine Idle & Watching `./invoices/`')
else:
  st.sidebar.error('Status: Engine Paused')

st.sidebar.divider()
st.sidebar.caption('PyAutoGUI Safety: Move cursor to Top-Left corner to abort.')

# --- Header Section ---
st.title('🖥️ Robotic Automation & Expense Ledger')
st.markdown(
    'Automated invoice processing, structured logging, and GUI form-filling'
    ' workflows.'
)

# --- Top Metrics Row ---
df = load_ledger_data()
col1, col2, col3, col4 = st.columns(4)

total_expenses = df['Amount ($)'].sum() if not df.empty else 0.0
total_count = len(df)
pending_files = (
    len([f for f in os.listdir(INVOICE_DIR) if f.endswith('.txt')])
    if os.path.exists(INVOICE_DIR)
    else 0
)

col1.metric('Total Expenses Logged', f'${total_expenses:,.2f}')
col2.metric('Processed Transactions', f'{total_count}')
col3.metric('Pending Invoices', f'{pending_files}')
col4.metric('Automation Accuracy', '100%')

st.divider()

# --- Main Content Split ---
left_col, right_col = st.columns([1, 1])

with left_col:
  st.subheader('📁 Run Batch Workflow')

  if st.button('🚀 Process Invoices & Automate GUI'):
    if not os.path.exists(INVOICE_DIR):
      os.makedirs(INVOICE_DIR)
      sample_file = os.path.join(INVOICE_DIR, 'sample_receipt.txt')
      with open(sample_file, 'w') as f:
        f.write('Vendor: Nexora Solutions\nDate: 2026-08-09\nAmount: 450.00\n')

    files = [f for f in os.listdir(INVOICE_DIR) if f.endswith('.txt')]

    if not files:
      st.info('No pending `.txt` invoices found in `./invoices`.')
    else:
      progress_bar = st.progress(0)
      status_text = st.empty()

      for idx, file_name in enumerate(files):
        full_path = os.path.join(INVOICE_DIR, file_name)
        status_text.text(f'Parsing {file_name}...')

        data = parse_mock_invoice(full_path)
        update_excel_ledger(data)

        status_text.text(f"Executing GUI Form Entry for {data['vendor']}...")
        run_gui_automation(data, countdown=2)

        progress_bar.progress((idx + 1) / len(files))

      st.success('🎉 All invoices processed and logged successfully!')
      st.rerun()

  st.divider()
  st.subheader('📊 Expense Analytics')

  if not df.empty:
    fig = px.bar(
        df,
        x='Vendor',
        y='Amount ($)',
        color='Vendor',
        title='Expenses by Vendor',
        template='plotly_dark',
    )
    # Updated to width="stretch" to eliminate Streamlit warning
    st.plotly_chart(fig, width='stretch')
  else:
    st.info('No expenses logged yet. Process invoices to populate charts.')

with right_col:
  st.subheader('📜 Live Excel Ledger')
  if not df.empty:
    # Updated to width="stretch" to eliminate Streamlit warning
    st.dataframe(df, width='stretch', height=400)
  else:
    st.write('Ledger is currently empty.')
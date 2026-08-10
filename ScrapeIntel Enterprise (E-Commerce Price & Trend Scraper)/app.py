import datetime
import random
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title='ScrapeIntel Enterprise - E-Commerce Scraper',
    page_icon='🕷️',
    layout='wide',
)


# --- MOCK DATA GENERATOR & LIVE SCRAPER ENGINE ---
def simulate_ecommerce_scraping():
  """Simulates scraping multiple product pages to demonstrate the extraction pipeline."""
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
          ' (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      )
  }

  products = [
      {
          'title': 'UltraBook Pro 15 - Intel i7, 16GB RAM',
          'category': 'Laptops',
          'base_price': 1200.00,
          'seller': 'TechStore A',
      },
      {
          'title': 'UltraBook Pro 15 - Intel i7, 16GB RAM',
          'category': 'Laptops',
          'base_price': 1150.00,
          'seller': 'TechStore B',
      },
      {
          'title': 'Wireless Noise-Canceling Headphones',
          'category': 'Audio',
          'base_price': 250.00,
          'seller': 'AudioWorld',
      },
      {
          'title': 'Wireless Noise-Canceling Headphones',
          'category': 'Audio',
          'base_price': 280.00,
          'seller': 'TechStore A',
      },
      {
          'title': '4K Ergonomic Monitor 27-inch',
          'category': 'Displays',
          'base_price': 450.00,
          'seller': 'DisplayHub',
      },
      {
          'title': 'Mechanical Gaming Keyboard RGB',
          'category': 'Peripherals',
          'base_price': 110.00,
          'seller': 'GamerZone',
      },
      {
          'title': 'Smart Ergonomic Office Chair',
          'category': 'Furniture',
          'base_price': 320.00,
          'seller': 'OfficeDepot',
      },
      {
          'title': 'Smart Ergonomic Office Chair',
          'category': 'Furniture',
          'base_price': 299.00,
          'seller': 'TechStore B',
      },
  ]

  scraped_records = []
  np.random.seed(42)

  for idx, p in enumerate(products):
    # Simulate scraped metrics with minor live fluctuations
    discount = random.choice([0, 5, 10, 15, 20])
    scraped_price = round(p['base_price'] * (1 - discount / 100), 2)
    rating = round(random.uniform(3.8, 4.9), 1)
    stock_status = random.choice(['In Stock', 'In Stock', 'In Stock', 'Low Stock', 'Out of Stock'])

    scraped_records.append({
        'ProductID': f'PRD-{100 + idx}',
        'Product_Name': p['title'],
        'Category': p['category'],
        'Seller': p['seller'],
        'Price_USD': scraped_price,
        'Original_Price_USD': p['base_price'],
        'Discount_%': discount,
        'Rating': rating,
        'Stock_Status': stock_status,
        'Scraped_At': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

  return pd.DataFrame(scraped_records)


# --- DASHBOARD HEADER ---
st.title('🕷️ ScrapeIntel Enterprise: E-Commerce Price Monitoring')
st.caption('Automated Web Scraping, Competitor Intelligence & Data Extraction Suite')
st.markdown('---')

# --- SIDEBAR CONTROLS ---
st.sidebar.title('⚡ Scraper Control Center')
st.sidebar.markdown('---')

target_category = st.sidebar.multiselect(
    'Filter by Category:',
    ['Laptops', 'Audio', 'Displays', 'Peripherals', 'Furniture'],
    default=['Laptops', 'Audio', 'Displays', 'Peripherals', 'Furniture'],
)

price_threshold = st.sidebar.slider(
    'Max Price Alert Threshold ($):', min_value=50, max_value=1500, value=1000
)

trigger_scrape = st.sidebar.button('🚀 Execute Live Scrape Job', type='primary')

# Data Loading State
if 'scrape_data' not in st.session_state or trigger_scrape:
  with st.spinner('Parsing web pages, extracting DOM elements & normalizing data...'):
    time.sleep(1)  # Simulate network latency
    st.session_state.scrape_data = simulate_ecommerce_scraping()
    st.toast('Web Scraping Job Completed Successfully!', icon='✅')

df = st.session_state.scrape_data

# Filter Data
filtered_df = df[(df['Category'].isin(target_category)) & (df['Price_USD'] <= price_threshold)]

# --- KPI METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric('Total Products Scraped', len(filtered_df))
c2.metric('Average Listed Price', f'${filtered_df["Price_USD"].mean():.2f}' if not filtered_df.empty else '$0.00')
c3.metric('Active Sellers Tracked', filtered_df['Seller'].nunique() if not filtered_df.empty else 0)
c4.metric('Items Out of Stock', len(filtered_df[filtered_df['Stock_Status'] == 'Out of Stock']))

st.markdown('---')

# --- TABS LAYOUT ---
tab1, tab2, tab3 = st.tabs(['📊 Price Intelligence', '🚨 Competitor Benchmark', '📋 Raw Scraped Dataset'])

with tab1:
  st.subheader('📈 Price Distribution & Discount Analysis')
  col_a, col_b = st.columns(2)

  with col_a:
    fig_price = px.bar(
        filtered_df,
        x='Product_Name',
        y='Price_USD',
        color='Seller',
        barmode='group',
        title='Price Comparison Across Sellers',
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_price.update_layout(template='plotly_dark', xaxis_title='', yaxis_title='Price ($)')
    st.plotly_chart(fig_price, use_container_width=True)

  with col_b:
    fig_discount = px.pie(
        filtered_df,
        names='Discount_%',
        title='Discount Strategy Breakdown',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Darkmint,
    )
    fig_discount.update_layout(template='plotly_dark')
    st.plotly_chart(fig_discount, use_container_width=True)

with tab2:
  st.subheader('🚨 Automated Threshold & Stock Alerts')
  low_stock_df = filtered_df[filtered_df['Stock_Status'].isin(['Low Stock', 'Out of Stock'])]

  if not low_stock_df.empty:
    st.warning('⚠️ Inventory Warning: The following items have low or missing stock across sellers:')
    st.dataframe(low_stock_df[['Product_Name', 'Seller', 'Price_USD', 'Stock_Status']], use_container_width=True)
  else:
    st.success('✅ All tracked competitor items are currently in healthy stock.')

with tab3:
  st.subheader('📋 Cleaned & Normalized Scraped Output')
  st.dataframe(filtered_df, use_container_width=True)

  # Download CSV Option
  csv = filtered_df.to_csv(index=False).encode('utf-8')
  st.download_button(
      label='📥 Download Extracted Dataset (CSV)',
      data=csv,
      file_name=f'scraped_products_{datetime.datetime.now().strftime("%Y%m%d")}.csv',
      mime='text/csv',
  )
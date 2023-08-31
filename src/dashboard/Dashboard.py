import duckdb
import streamlit as st
import pandas as pd
import altair as alt

# connect to db
dwh = duckdb.connect("/data/transformed/dwh.duckdb", read_only=True)
# load data
spending_by_customer = dwh.query("SELECT * FROM spending_per_customer").df()
customer_seg = dwh.query("SELECT * FROM CustomerSegmentation").df()
inv_lvl = dwh.query("SELECT * FROM InventoryLevel").df()
clv = dwh.query("SELECT  * FROM CustomerLifetimeValue").df()
prod_review = dwh.query("SELECT * FROM ProductRevenue").df()
freq_customer = dwh.query("SELECT * FROM FrequentCustomers ORDER BY order_count").df()

# Create app
st.set_page_config(page_title = "This is a Multipage WebApp")
st.markdown("<h1 style='text-align: center; color: white;'>Portable Data App</h1>", unsafe_allow_html=True)

# st.title("Portable Data App")
st.sidebar.image("imgs/meme1.jpg")
st.sidebar.image("imgs/meme3.png")
st.sidebar.image("imgs/meme2.png")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart = alt.Chart(freq_customer).mark_bar(size=25).encode(
                x= alt.X('customer_id:O', sort=alt.SortField(field="order_count", order='descending')),
                y='order_count',
            ).interactive().properties(
                title={
                    "text": 'Orders per Customer',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
    with col2:
        chart = alt.Chart(spending_by_customer).mark_bar(size=25).encode(
                x= alt.X('customer_id:O', sort=alt.SortField(field="total_spent", order='descending')),
                y='total_spent',
            ).interactive().properties(
                title={
                    "text": 'Spending per Customer',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
        
    with col3:
        chart = alt.Chart(clv).mark_bar(size=25).encode(
                x= alt.X('customer_id:O', sort=alt.SortField(field="clv", order='descending')),
                y='clv',
            ).interactive().properties(
                title={
                    "text": 'Customer Lifetime Value',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart = alt.Chart(customer_seg).mark_bar(size=25).encode(
                x= alt.X('customer_id:O', sort=alt.SortField(field="spending_category", order='descending')),
                y='spending_category',
            ).interactive().properties(
                title={
                    "text": 'Customer Segmentation',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
    with col2:
        chart = alt.Chart(inv_lvl).mark_bar(size=25).encode(
                x= alt.X('product:O', sort=alt.SortField(field="inventory_level", order='descending')),
                y='inventory_level',
            ).interactive().properties(
                title={
                    "text": 'Inventory Levels',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
        
    with col3:
        chart = alt.Chart(prod_review).mark_bar(size=25).encode(
                x= alt.X('product:O', sort=alt.SortField(field="revenue", order='descending')),
                y='revenue',
            ).interactive().properties(
                title={
                    "text": 'Product Revenue',
                    "anchor": 'middle'
                }
            )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)
with st.container():
    data = customer_seg
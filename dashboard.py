import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
import methodology as m
import numpy as np
import altair as alt
#reading a csv file
df = pd.read_csv("Afficionado Coffee Roasters.csv")

#calculate the revenue and total revenue
df["revenue"] = df["transaction_qty"]* df["unit_price"]
total_revenue = df["revenue"].sum()
#title of the dashboard
st.markdown(
"""
<h1 style='background-color:#1D4E89; 
           color:white; 
           padding:10px; 
           border-radius:8px; 
           text-align:center;'>
☕ Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters
</h1>
""",
unsafe_allow_html=True
)

# Change background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f5dc;
    }
    [data-testid="stSidebar"] {
    background-color: #d2b48c;
}
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.image(
"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
use_container_width=True
)
# Copy dataframe
filtered_df = df.copy()

# Sidebar title
st.sidebar.header("Filters")

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    df["product_category"].unique()
)

# Product type filter
product_type_filter = st.sidebar.multiselect(
    "Select Product Type",
    df["product_type"].unique()
)

# Store location filter
location_filter = st.sidebar.selectbox(
    "Select Store Location",
    df["store_location"].unique()
)

# Apply category filter
if category_filter:
    filtered_df = filtered_df[filtered_df["product_category"].isin(category_filter)]

# Apply product type filter
if product_type_filter:
    filtered_df = filtered_df[filtered_df["product_type"].isin(product_type_filter)]

# Apply location filter
filtered_df = filtered_df[filtered_df["store_location"] == location_filter]

top_n = st.sidebar.slider(
    "Select Top N Products",
    5, 20, 10
)
top_products = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

#st.bar_chart(top_products)

#key performance indicator

#Product Revenue Contribution (%)Share of total revenu
Total_revenue = filtered_df["revenue"].sum().round(2)


# Product Sales Volume	Popularity indicator

popular_product = filtered_df.groupby("product_detail")["transaction_qty"].sum().sort_values(ascending=False)

total_units = filtered_df["transaction_qty"].sum()

#Category Revenue Share	Business dependency
category_revenue= filtered_df.groupby("product_category")["revenue"].sum()
category_share =(category_revenue / total_revenue)*100
category_share.sort_values(ascending=False)
top_category_name = category_share.idxmax()
top1_category = category_share .max()

 #Revenue Concentration Ratio	Menu risk exposure
product_revenue = filtered_df.groupby("product_detail")["revenue"].sum()
total_revenue = product_revenue.sum()
product_contribution = (product_revenue / total_revenue.sum()) * 100
product_contribution = product_contribution.sort_values(ascending=False)
top3_share = product_contribution.head(3).sum().round(2)





 # Product Efficiency Score (Revenue per SKU)

total_revenue = filtered_df["revenue"].sum()
total_skus = filtered_df["product_detail"].nunique()
revenue_per_sku = total_revenue / total_skus


st.set_page_config(layout="wide")
st.subheader("Key Business Metrics")
col1, col2, col3, col4,col5 = st.columns(5)
with col1:
 with st.container(border=True):
  st.metric("Total revenue", f"{total_revenue:.2f}%")
 
with col2:
 with st.container(border=True):
  st.metric("Total unit sold",total_units )
with col3:
 with st.container(border=True):
  st.metric("Top category share%",top_category_name,f"{top1_category:.2f}%") 
with col4:
 with st.container(border=True):
  st.metric("Top3 revenue share %", f"{top3_share:.2f}%")
with col5:
 with st.container(border=True):
   st.metric("Revenue per SKU",revenue_per_sku)

st.subheader("Volume vs Revenue")

# Aggregate using filtered data
product_ranking = filtered_df.groupby("product_detail").agg(
    volume=("transaction_qty", "sum"),
    revenue=("revenue", "sum")
).reset_index()

# Ranking
product_ranking["volume_rank"] = product_ranking["volume"].rank(ascending=False, method="dense")
product_ranking["revenue_rank"] = product_ranking["revenue"].rank(ascending=False, method="dense")

# Sort
sorted_df = product_ranking.sort_values(by="revenue", ascending=False)
sorted_df = sorted_df.head(top_n)


chart = alt.Chart(sorted_df).mark_bar().encode(
    x=alt.X("revenue:Q", title="Total Revenue"),
    y=alt.Y("product_detail:N", sort="-x", title="Product"),
     color=alt.Color(
       "product_detail:N",
        scale=alt.Scale(range=[
"#0D3B66",
"#1D4E89",
"#3A86FF",
"#4EA8DE",
"#90DBF4",
"#CAF0F8"
])), 
tooltip=[
        alt.Tooltip("product_detail:N", title="Product"),
        alt.Tooltip("volume:Q", title="Quantity Sold"),
        alt.Tooltip("revenue:Q", title="Revenue"),
        alt.Tooltip("revenue_rank:Q", title="Revenue Rank"),
        alt.Tooltip("volume_rank:Q", title="Volume Rank")
    ]
).interactive()

st.altair_chart(chart, use_container_width=True)




st.subheader("Category revenue distribution")
# Compute total revenue
total_revenue = df["revenue"].sum()

# Group by category (already grouped in this case)
category_revenue = filtered_df.groupby("product_category")["revenue"].sum().reset_index()

category_revenue["share"] = (category_revenue["revenue"] / total_revenue) * 100

# Check dtypes
st.write(category_revenue)

# Altair donut chart
chart = alt.Chart(category_revenue).mark_arc(innerRadius=70).encode(
    theta=alt.Theta("revenue:Q"),           # numeric column
    color=alt.Color(
       "product_category:N",
        scale=alt.Scale(range=["#6F4E37", "#C4A484", "#A67B5B", "#8B5A2B", "#D2B48C"])),  # categorical
    tooltip=[
        alt.Tooltip("product_category:N", title="Category"),
        alt.Tooltip("revenue:Q", title="Revenue"),
        alt.Tooltip("share:Q", title="Revenue Share (%)", format=".2f")
    ]
)

st.altair_chart(chart, use_container_width=True)


product_data = filtered_df.groupby("product_detail").agg(
    popularity=("transaction_qty","sum"),
    revenue=("revenue","sum")
).reset_index()
sorted_df = product_data.sort_values(by="revenue", ascending=False)
sorted_df = sorted_df.head(top_n)
st.subheader("Popularity vs Revenue")

scatter = alt.Chart(sorted_df).mark_circle(size=120).encode(
    x=alt.X(
        "popularity:Q",
        title="Popularity (Units Sold)",
        scale=alt.Scale(domain=[100, 2000])   # adjust range
    ),
    y=alt.Y(
        "revenue:Q",
        title="Revenue",
        scale=alt.Scale(domain=[1000, 9000])
    ),
    color=alt.Color("revenue:Q", scale=alt.Scale(scheme="blues")),
    tooltip=[
        alt.Tooltip("product_detail:N", title="Product"),
        alt.Tooltip("popularity:Q", title="Units Sold"),
        alt.Tooltip("revenue:Q", title="Revenue")
    ]
)

st.altair_chart(scatter, use_container_width=True)

product_table = filtered_df.groupby("product_detail").agg(
    Units_Sold=("transaction_qty","sum"),
    Revenue=("revenue","sum")
).reset_index()

product_table["Avg_Price"] = product_table["Revenue"] / product_table["Units_Sold"]

total_revenue = product_table["Revenue"].sum()

product_table["Rank"] = product_table["Revenue"].rank(ascending=False)

product_table["Revenue_%"] = (product_table["Revenue"] / total_revenue) * 100

sorted_df = product_table.sort_values(by="Rank").head(top_n)

st.subheader("Product Performance Table")

st.dataframe(sorted_df, use_container_width=True)





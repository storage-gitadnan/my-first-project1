import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv("Afficionado Coffee Roasters.csv")
print(df)
#EDA section Data Ingestion & Validation
print(df.shape)
print(df.columns) 
print(df.info())
print(df.dtypes)
df["transaction_time"] = pd.to_datetime(df["transaction_time"],format ="%H:%M:%S")
print(df.isnull().sum())
print(df.duplicated().sum())
print(df[df["transaction_qty"]<=0])
print(df[df["unit_price"] <=0])

#Revenue Computation
df["revenue"]= df["transaction_qty"]*df["unit_price"] # it create a new columns of revenue
print(df["revenue"])
print(df.columns) #checking the revenue column is created are not

Total_revenue= df["revenue"].sum()# calculate total revenue
print(Total_revenue)
product_revenue = df.groupby("product_detail")["revenue"].sum() #product wise revenue calculate
print(product_revenue.sort_values(ascending=False))

product_category_revenue = df.groupby("product_category")["revenue"].sum()#category wise revenue
print(product_category_revenue.sort_values(ascending=False))
revenue_product_type =df.groupby("product_type")["revenue"].sum() #product type revenue 
print(revenue_product_type.sort_values(ascending=False))

print(df.columns)
print(df.groupby("product_detail")["product_detail"].value_counts()) # count of the product that it contain


#Product Popularity Analysis
Total_unit_sold=df.groupby("product_detail")["transaction_qty"].sum()#total unit sold by product type
print(Total_unit_sold.sort_values(ascending=False))

rank_quantity = df.groupby("product_detail")["transaction_qty"].sum() 
ranking_product = rank_quantity.rank(ascending=False)
print(ranking_product.sort_values(ascending=False))

top_product_detail =df.groupby("product_detail")["transaction_qty"].sum().sort_values(ascending=False).head(5)
print(top_product_detail)  # top three product_detail
bottom_sale_product =df.groupby("product_detail")["transaction_qty"].sum().sort_values().head(5)
print(bottom_sale_product)#bottom product detail


#Revenue Contribution Analysis

Total_revenue_contribution = (product_revenue / Total_revenue) *100
print(Total_revenue_contribution .sort_values(ascending=False))
#• Total revenue per product
product_revenue = df.groupby("product_detail")["revenue"].sum()
print(len(product_revenue))
pd.set_option('display.max_rows', None)#length of the product_detail of distinct
print(product_revenue.sort_values(ascending=False)) 

# Comparison between volume rank and revenue rank

volume = df.groupby("product_detail")["transaction_qty"].sum()
print(volume)
revenue = df.groupby("product_detail")["revenue"].sum()
pd.set_option('display.max_rows',None)#This line show the total rows in the product_type distinct 
print(revenue)

volume_rank = volume.rank(ascending=False)
revenue_rank= revenue.rank(ascending=False)
compresion =pd.DataFrame({"volume":volume,"volume_rank":volume_rank,"revenue":revenue,"revenue_rank":revenue_rank})
compresion = compresion.sort_values(by="revenue_rank", ascending=True)
print(compresion)


# Revenue share by category (Coffee, Tea, Chocolate)
category_revenue = df.groupby("product_category")["revenue"].sum()
print(category_revenue.sort_values(ascending=False))
category_revenue_share = (category_revenue / Total_revenue)*100
print(category_revenue_share.sort_values(ascending=False))

# Product-type contribution within each category
product_type1 = df.groupby(["product_category","product_type"])["revenue"].sum()
category_product1= df.groupby("product_category")["revenue"].sum()
category_in_product_share = (product_type1 / category_product1  )*100
print(category_in_product_share) 

#dependancy category share
dependancy_category = (category_revenue /Total_revenue) *100
print(dependancy_category.sort_values(ascending=False))

print(df.groupby("product_category")["product_category"].value_counts())

print(df.groupby("product_type")["product_category"].value_counts().sort_values(ascending=False))

#Revenue Concentration & Menu Balance

product_revenue= df.groupby("product_detail")["revenue"].sum().sort_values(ascending=False)
pareto= product_revenue.cumsum()/product_revenue.sum()*100
print(pareto)

#anchors product top product
product_detail_dependancy = df.groupby("product_detail")["revenue"].sum()
dependancy_product= (product_detail_dependancy/product_detail_dependancy.sum())*100
print(dependancy_product .sort_values(ascending=False).head(10))

print(dependancy_product.count())
#tail product low performance
product_detail_dependancy = df.groupby("product_detail")["revenue"].sum()
dependancy_product= (product_detail_dependancy/product_detail_dependancy.sum())*100
print(dependancy_product .sort_values(ascending=False).tail(5))

print(dependancy_product.count())




volume = df.groupby("product_detail")["transaction_qty"].sum()
print(volume)
revenue = df.groupby("product_detail")["revenue"].sum()
pd.set_option('display.max_rows',None)#This line show the total rows in the product_type distinct 
print(revenue)



product_menu = df.groupby("product_detail")["revenue"].sum().sort_values(ascending=False)

result = product_menu.reset_index()
result.columns = ["Product Name", "Revenue"]

result["Contribution (%)"] = (result["Revenue"] / result["Revenue"].sum()) * 100
result["Cumulative %"] = result["Contribution (%)"].cumsum()

print(result)



print(df.info())


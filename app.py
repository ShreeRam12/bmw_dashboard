import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset
df = pd.read_csv("bmw_sales.csv")

# Normalize column names to avoid case/space issues in CSV headers.
df.columns = df.columns.str.strip().str.lower()

# Map expected dashboard fields to the available dataset columns.
year_col = "year"
model_col = "model"
region_col = "fueltype" if "fueltype" in df.columns else None
sales_col = "price" if "price" in df.columns else None

# Validate required columns.
required = [year_col, model_col, sales_col]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"Missing required columns in CSV: {', '.join(missing)}")
    st.stop()

# Title
st.title("BMW Car Sales Dashboard")

# Sidebar filters
years = st.sidebar.multiselect("Select Year", sorted(df[year_col].unique()))
models = st.sidebar.multiselect("Select Model", sorted(df[model_col].unique()))
if region_col:
    regions = st.sidebar.multiselect("Select Fuel Type", sorted(df[region_col].unique()))
else:
    regions = []

# Apply filters
filtered_df = df.copy()
if years:
    filtered_df = filtered_df[filtered_df[year_col].isin(years)]
if models:
    filtered_df = filtered_df[filtered_df[model_col].isin(models)]
if regions and region_col:
    filtered_df = filtered_df[filtered_df[region_col].isin(regions)]

# Charts
fig = px.line(
    filtered_df,
    x=year_col,
    y=sales_col,
    color=model_col,
    title="Price Trend by Model",
)
st.plotly_chart(fig)

top_models = filtered_df.groupby(model_col)[sales_col].sum().reset_index()
fig2 = px.bar(top_models, x=model_col, y=sales_col, title="Top Models by Total Price")
st.plotly_chart(fig2)

if region_col:
    region_sales = filtered_df.groupby(region_col)[sales_col].sum().reset_index()
    fig3 = px.pie(
        region_sales,
        names=region_col,
        values=sales_col,
        title="Fuel Type Share by Total Price",
    )
    st.plotly_chart(fig3)

# KPIs
st.metric("Total Price", int(filtered_df[sales_col].sum()))

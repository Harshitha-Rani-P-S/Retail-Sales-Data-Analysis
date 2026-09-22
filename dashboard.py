
import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Retail Sales Interactive Dashboard")
st.write("Superstore Sales Analysis using Python, Pandas, Plotly and Streamlit")

# Load dataset
df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Convert date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Create additional columns
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month_name()
df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)


# Sidebar Filters

st.sidebar.header("Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# KPI Section


total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    total_orders
)

col4.metric(
    "Total Customers",
    total_customers
)

st.divider()


# Sales by Category


category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)


# Sales by Region


region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Sales Distribution by Region"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# Monthly Sales Trend


monthly_sales = (
    filtered_df.groupby("Year-Month")["Sales"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Year-Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# Top Products


top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales"
)

fig_products.update_layout(
    yaxis={"categoryorder": "total ascending"}
)


# Top Customers


top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    title="Top 10 Customers by Sales"
)

fig_customers.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )


# Profit by Sub-Category

subcategory_profit = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit")
)

fig_profit = px.bar(
    subcategory_profit,
    x="Sub-Category",
    y="Profit",
    title="Profit by Sub-Category"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# Discount vs Profit


fig_discount = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    size="Sales",
    color="Category",
    title="Discount vs Profit"
)

st.plotly_chart(
    fig_discount,
    use_container_width=True
)


# Data Preview


st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# Business Insights


st.subheader("Business Insights")

if len(filtered_df) > 0:

    best_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    top_customer = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .idxmax()
    )

    top_product = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    st.write(f"**Best Performing Region:** {best_region}")
    st.write(f"**Highest Sales Category:** {best_category}")
    st.write(f"**Top Customer:** {top_customer}")
    st.write(f"**Top Product:** {top_product}")

else:

    st.warning(
        "No records match the selected filters."
    )

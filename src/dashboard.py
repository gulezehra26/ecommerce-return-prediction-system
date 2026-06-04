import streamlit as st
import plotly.express as px

def show_dashboard(df):

    # This factor converts dataset price scale into estimated PKR display values
    PKR_FACTOR = 312.5

    st.title("KPI Dashboard")

    # Calculate key business numbers
    total_orders = len(df)
    total_sales_pkr = df["reported_order_total"].sum() * PKR_FACTOR
    average_order_value_pkr = df["reported_order_total"].mean() * PKR_FACTOR
    return_rate = df["return_flag"].mean() * 100

    # Show KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Total Sales", f"PKR {total_sales_pkr:,.0f}")
    col3.metric("Average Order Value", f"PKR {average_order_value_pkr:,.0f}")
    col4.metric("Return Rate", f"{return_rate:.1f}%")

    st.divider()

    # Sales by category in PKR
    category_sales = df.groupby("category")["reported_order_total"].sum().reset_index()
    category_sales["sales_pkr"] = category_sales["reported_order_total"] * PKR_FACTOR

    fig1 = px.bar(
        category_sales,
        x="category",
        y="sales_pkr",
        title="Sales by Product Category",
        labels={
            "category": "Product Category",
            "sales_pkr": "Total Sales (PKR)"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Return rate by category
    category_returns = df.groupby("category")["return_flag"].mean().reset_index()
    category_returns["return_rate"] = category_returns["return_flag"] * 100

    fig2 = px.bar(
        category_returns,
        x="category",
        y="return_rate",
        title="Return Rate by Product Category",
        labels={
            "category": "Product Category",
            "return_rate": "Return Rate (%)"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Return rates are relatively similar across product categories. "
        "This suggests that returns may depend on multiple combined factors, not category alone."
    )
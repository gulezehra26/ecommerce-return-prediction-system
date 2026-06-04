import streamlit as st
import pandas as pd
import numpy as np


def show_prediction(df, model, feature_columns):

    # These factors convert PKR input into the scale used during model training
    PRICE_FACTOR = 312.5
    SHIPPING_FACTOR = 50
    THRESHOLD = 0.30

    st.title("Prediction Center")

    st.write(
        "Enter order details below."
    )

    # Clean display names
    def clean_payment(value):
        value = str(value).lower().strip()

        if value in ["cc", "credit card", "creditcard"]:
            return "Credit Card"

        if value in ["cod", "cash on delivery", "cash"]:
            return "Cash on Delivery"

        return value.title()

    def clean_sales_channel(value):
        value = str(value).lower().strip()

        if value in ["mobile app", "mobile-app", "mobile_app", "app"]:
            return "Mobile App"

        if value in ["mkt place", "marketplace", "market place"]:
            return "Marketplace"

        if value in ["web", "website"]:
            return "Website"

        return value.title()

    def clean_loyalty(value):
        return str(value).title()

    # Create dropdown maps
    # Display value

    payment_map = {}

    for value in df["payment_method"].dropna().unique():

        if "paypal" in str(value).lower():
           continue

        payment_map[clean_payment(value)] = value

    sales_channel_map = {}
    for value in df["sales_channel"].dropna().unique():
        sales_channel_map[clean_sales_channel(value)] = value

    loyalty_map = {}
    for value in df["loyalty_tier"].dropna().unique():
        loyalty_map[clean_loyalty(value)] = value

    category_options = sorted(df["category"].dropna().unique())

    # Input form
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Customer Age",
            min_value=10,
            max_value=100,
            value=30,
            help="Enter customer age in years."
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            max_value=20,
            value=1,
            help="Enter number of items purchased."
        )

        product_price_pkr = st.number_input(
            "Product Price (PKR)",
            min_value=100.0,
            max_value=500000.0,
            value=7000.0,
            help="Enter product price."
        )

        discount_pct = st.number_input(
            "Discount Percentage",

            min_value=0.0,
            max_value=100.0,
            value=10.0,
            help="Enter discount percentage applied to the order."
        )

        shipping_cost_pkr = st.number_input(
            "Shipping Cost (PKR)",
            min_value=0.0,
            max_value=10000.0,
            value=300.0,
            help="Enter shipping cost."
        )

    with col2:
        delivery_time_days = st.number_input(
            "Delivery Time Days",
            min_value=0,
            max_value=60,
            value=5,
            help="Enter number of days between order and delivery."
        )

        category = st.selectbox(
            "Product Category",
            category_options,
            help="Select product category."
        )

        payment_display = st.selectbox(
            "Payment Method",
            sorted(payment_map.keys()),
            help="Select payment method."
        )

        sales_channel_display = st.selectbox(
            "Sales Channel",
            sorted(sales_channel_map.keys()),
            help="Select sales channel."
        )

        loyalty_display = st.selectbox(
            "Loyalty Tier",
            sorted(loyalty_map.keys()),
            help="Select customer loyalty tier."
        )

    # Prediction button
    
    if st.button("Predict Return Risk", use_container_width=True):

        # Convert PKR input values into model training scale
        unit_price = product_price_pkr / PRICE_FACTOR
        shipping_cost = shipping_cost_pkr / SHIPPING_FACTOR

        # Convert clean dropdown labels back to original dataset values
        payment_method = payment_map[payment_display]
        sales_channel = sales_channel_map[sales_channel_display]
        loyalty_tier = loyalty_map[loyalty_display]

        # Create engineered features
        discount_value = unit_price * quantity * discount_pct / 100
        final_order_value = (unit_price * quantity) - discount_value
        avg_item_cost = final_order_value / quantity

        if final_order_value > 0:
            shipping_ratio = shipping_cost / final_order_value
        else:
            shipping_ratio = 0

        delayed_delivery_flag = 1 if delivery_time_days > 7 else 0
        high_value_order = 1 if final_order_value > df["reported_order_total"].median() else 0

        # Review score is removed from the form, so we use median as a neutral value
        if "review_score" in df.columns:
            review_score = df["review_score"].median()
        else:
            review_score = 3

        low_review_flag = 1 if review_score <= 2 else 0

        # Supplier country is removed from the form, so Pakistan is used as default
        supplier_country = "pakistan"

        # Create one-row input data
        input_data = pd.DataFrame({
            "age": [age],
            "quantity": [quantity],
            "unit_price": [unit_price],
            "discount_pct": [discount_pct],
            "shipping_cost": [shipping_cost],
            "review_score": [review_score],
            "reported_order_total": [final_order_value],
            "delivery_time_days": [delivery_time_days],
            "order_month": [6],
            "order_weekday": [2],
            "customer_tenure_days": [0],
            "delayed_delivery_flag": [delayed_delivery_flag],
            "discount_value": [discount_value],
            "final_order_value": [final_order_value],
            "avg_item_cost": [avg_item_cost],
            "high_value_order": [high_value_order],
            "low_review_flag": [low_review_flag],
            "shipping_ratio": [shipping_ratio],
            "category": [category],
            "payment_method": [payment_method],
            "sales_channel": [sales_channel],
            "loyalty_tier": [loyalty_tier],
            "supplier_country": [supplier_country]
        })

        # Convert categorical columns into numeric columns
        input_encoded = pd.get_dummies(input_data)

        # Match the same columns used during model training
        input_encoded = input_encoded.reindex(
            columns=feature_columns,
            fill_value=0
        )

        # Clean invalid values
        input_encoded = input_encoded.replace([np.inf, -np.inf], 0)
        input_encoded = input_encoded.fillna(0)

        # Predict return probability
        probability = model.predict_proba(input_encoded)[0][1]
        probability_percent = probability * 100

        # Assign risk level
        if probability >= 0.60:
            risk_level = "High Return Risk"
            recommendation = "Consider proactive customer support and order verification."
        elif probability >= THRESHOLD:
            risk_level = "Moderate Return Risk"
            recommendation = "Monitor this order and ensure timely delivery communication."
        else:
            risk_level = "Low Return Risk"
            recommendation = "This order shows a lower estimated return risk."

        # Show result
    
        st.divider()
        st.subheader("Prediction Result")

        col_a, col_b = st.columns(2)

        col_a.metric("Return Probability", f"{probability_percent:.2f}%")
        col_b.metric("Risk Level", risk_level)

        st.write("Order Summary")
        st.write(f"Product Price: PKR {product_price_pkr:,.0f}")
        st.write(f"Shipping Cost: PKR {shipping_cost_pkr:,.0f}")
        st.write(f"Discount: {discount_pct:.1f}%")

        if probability >= THRESHOLD:
            st.warning(recommendation)
        else:
            st.success(recommendation)
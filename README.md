⁕⁕ E-Commerce Return Prediction System

Project Overview

An e-commerce analytics platform that helps businesses track sales performance, understand customer behavior, and assess the likelihood of product returns.



⁕⁕Features

• Interactive KPI Dashboard
• Sales Performance Analysis
• Return Rate Analysis
• Product Category Insights
• Return Risk Prediction
• User-Friendly Streamlit Interface
• Business-Oriented Visualizations


⁕⁕Dataset Summary

• Total Orders: 7,687
• Return Rate: 27.6%
• Multiple customer, product, and order related features
• Cleaned and processed for predictive modeling


⁕⁕Data Preparation

The dataset was prepared through several preprocessing steps:

• Missing value treatment
• Duplicate removal
• Data validation
•Feature engineering
• Outlier inspection
•Categorical encoding

Additional details are available in the reports/data_cleaning_report.pdf file.


⁕⁕ Machine Learning Models Evaluated

The following algorithms were evaluated:

• Logistic Regression
• Decision Tree
• Random Forest
• XGBoost

Random Forest was selected as the final deployment model due to its strong overall performance and ability to handle complex relationships within the data.



⁕⁕ Dashboard KPIs

The dashboard provides:

• Total Orders
• Total Sales
• Average Order Value
• Return Rate
• Sales by Product Category
• Return Rate by Category


⁕⁕ Prediction Module

Users can enter:

• Customer Age
• Quantity
• Product Price
• Discount Percentage
• Shipping Cost
• Delivery Time
• Product Category
• Payment Method
• Sales Channel
•Loyalty Tier

The system estimates the probability of product return and classifies the order into:

• Low Return Risk
• Moderate Return Risk
• High Return Risk



⁕⁕ Project Structure

ecommerce-return-prediction/
    •app.py
    •requirements.txt
    •README.md

assets/
    •home_page.png
    •dashboard.png
    •prediction_form.png
    •prediction_result.png

reports/
    •data_cleaning_report.pdf

data/
    •cleaned_data.csv

models/
    •model.pkl
    •feature_columns.pkl

src/
    •dashboard.py
    •prediction.py
    •utils.py



Technologies Used

• Python
• Pandas
• NumPy
• Scikit-Learn
• Streamlit
• Plotly
• Joblib



Future Improvements

• Advanced model tuning
• Additional business KPIs
• Real time prediction API
• User authentication
• Cloud deployment


Author

Developed as a portfolio project demonstrating data cleaning, exploratory data analysis, machine learning, dashboard development, and business analytics workflows.

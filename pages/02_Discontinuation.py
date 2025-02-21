import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import pickle

# Streamlit app
st.title("👩‍💻Cosmetic Product Discontinuation Prediction")

# Step 1: Load the dataset
data = pd.read_csv(r'clean_data.csv')

st.subheader("Step 8: Predict Discontinuation for a Product")
st.subheader("⏮️Data Preview")
st.markdown("""Showing the first 50 rows of the dataset""")
# Display the first 50 rows of the updated dataset without encoded values
if st.button("Show First 50 Rows"):

    st.write(data.loc[:, ['ProductName', 'BrandName','SubCategory','ChemicalName', 'ChemicalCount','Discontinued']].head(50))
    
label_encoders = {}
for col in ['ProductName', 'BrandName','SubCategory','ChemicalName', 'ChemicalCount']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le 


features = data[['ProductName', 'BrandName','SubCategory','ChemicalName', 'ChemicalCount']]
target = data['Discontinued']


X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42,stratify=target)

model = RandomForestClassifier(
    n_estimators=100,       # Reduce number of trees  
    max_depth=12,          # Limit tree depth  
    min_samples_split=10,   # Require more samples per split  
    min_samples_leaf=4, # Require at least 3 samples in leaf nodes
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)




    
st.markdown("""
Enter a ['ProductName', 'BrandName','SubCategory','ChemicalName', 'ChemicalCount'] to get know the product is discountinued or not.
""")
product_name = st.text_input("Product Name")
brand_name = st.text_input("Brand Name")
SubCategory = st.text_input("SubCategory")
ChemicalName=st.text_input("ChemicalName")
chemical_count = st.number_input("Chemical Count", min_value=0)

if st.button("Predict"):
    # Create DataFrame for user input
    input_data = pd.DataFrame({
        'ProductName': [product_name],
        'BrandName': [brand_name],
        'SubCategory': [SubCategory],
        'ChemicalName': [ChemicalName],
        'ChemicalCount': [chemical_count]
    })

    # Encode user input
    for column, le in label_encoders.items():
        if column in input_data.columns:
            input_data[column] = input_data[column].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

    # Make prediction
    prediction = model.predict(input_data)

    if prediction[0] == 1:
          st.write(f"The product '{product_name}' is likely to be discontinued.")
    else:
        st.write(f"The product '{product_name}' is likely to remain in production.")       
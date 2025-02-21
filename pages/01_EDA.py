import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    # Replace 'your_dataset.csv' with the actual file name
    return pd.read_csv('clean_data.csv')

df = load_data()



# Title and Introduction
st.title("EDA for Chemcials in Cosmetics ")
st.markdown("""
### Overview
Explore the relationships between products, chemicals, brands, and companies. Visualize trends and draw insights through statistical testing to enhance decision-making.
""")


# Horizontal divider
st.markdown("---")


# Section 1: Total Counts
st.header("Key Statistics")
st.markdown("#### Total Counts for Key Entities")
total_products = df['ProductName'].nunique()
total_chemicals = df['ChemicalName'].nunique()
total_companies = df['CompanyName'].nunique()
total_brands = df['BrandName'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", total_products)
col2.metric("Total Chemicals", total_chemicals)
col3.metric("Total Companies", total_companies)
col4.metric("Total Brands", total_brands)

# Horizontal divider
st.markdown("---")

# Section 2: Product with Most Chemicals
st.header("Product with Most Chemicals")

# Find the product with the most chemicals
product_with_most_chemicals = df['ProductName'].value_counts().idxmax()

# Get the count of occurrences for that product
count_occurrences = df[df['ProductName'] == product_with_most_chemicals].shape[0]

# Display the product name and total number of chemicals
st.markdown(f"**Product with most chemicals**: {product_with_most_chemicals}")
st.markdown(f"**Count of occurrences**: {count_occurrences}")

# Horizontal divider
st.markdown("---")

# Section 3: Products with 5 or More Toxic Chemicals
st.header("Products with 5 or More Toxic Chemicals")

# Display the insight and implication as markdown text
st.markdown("""
### Insight: 
A limited number of products contain 5 or more toxic chemicals. Most products use fewer chemicals, but those with 5 or more could pose greater health risks due to the higher chemical load.

### Implication:
Products with 5 or more toxic chemicals may require further investigation for regulatory compliance and safety concerns.
""")

toxic_chemicals_count = df.groupby('ProductName')['ChemicalName'].nunique()
products_with_5_or_more_chemicals = toxic_chemicals_count[toxic_chemicals_count >= 5]
#st.write(products_with_5_or_more_chemicals)

st.markdown("#### Visualization")
plt.figure(figsize=(12, 6))
products_with_5_or_more_chemicals.sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top Products with 5 or More Toxic Chemicals', fontsize=14)
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Number of Toxic Chemicals', fontsize=12)
plt.xticks(rotation=45, ha='right')
st.pyplot(plt)

# Horizontal divider
st.markdown("---")

# Section 4: Top 10 Reported Chemicals
st.header("Top 10 Most Reported Chemicals")

# Display Insight and Implication for the top 10 chemicals
st.markdown("""
### Insight: 
The top 10 most frequently reported chemicals, such as Titanium Dioxide or Coal Tar Distillates, are widely used across multiple products. These chemicals are commonly found in many formulations.

### Implication: 
Commonly used chemicals, especially toxic ones, should be closely monitored. Brands using these ingredients may face consumer pressure or regulatory challenges.
""")


top_chemicals = df['ChemicalName'].value_counts().head(10)

st.markdown("#### Visualization")
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))
top_chemicals.plot(kind='barh', color='skyblue', edgecolor='black')
plt.title('Top 10 Most Reported Chemicals', fontsize=16, weight='bold')
plt.xlabel('Number of Occurrences', fontsize=14, weight='bold')
plt.ylabel('Chemical Name', fontsize=14, weight='bold')
st.pyplot(plt)

# Horizontal divider
st.markdown("---")

# Section 5: Top 7 Brands by Chemical Usage
st.header("Top 7 Brands by Chemical Usage")

# Display Insight and Implication for the top 10 chemicals
st.markdown("""
### Insight: 
Brands like SEPHORA and Charlotte Tilbury could benefit from investing in research and development for safer alternatives or cleaner formulations, especially as consumer demand for such products increases.
### Implication: 
Commonly used chemicals, especially toxic ones, should be closely monitored. Brands using these ingredients may face consumer pressure or regulatory challenges.
""")

top_brands = df.groupby('BrandName')['ChemicalCount'].sum().sort_values(ascending=False).head(7)

plt.figure(figsize=(12, 6))
top_brands.plot(kind='bar', color='purple')
plt.title('Top 7 Brands by Chemical Usage')
plt.xlabel('Brand Name')
plt.ylabel('Chemical Count')
plt.xticks(rotation=45)
st.pyplot(plt)



# Horizontal divider
st.markdown("---")

# Section 6: Top 7 Companies by Chemical Usage
st.header("Top 13 Discontinued Products by Category")

# Display Insight and Implication for the top 10 chemicals
st.markdown("""
### Insight: 
The makeup products category shows a significantly high number of discontinued products, indicating rapid changes in trends, customer preferences, and potential product failures.Sun-related products have a moderate level of discontinued products, indicating their seasonal nature.
### Implication: 
Baby Products and Tattoos highlight the importance of strict safety standards.Businesses should focus on chemical-free alternatives, regulatory compliance, and transparency to address safety concerns, build consumer trust, and reduce product recalls.""")


# Convert 'DiscontinuedDate' to a binary 'Discontinued' column (1 for discontinued, 0 for not)
df['Discontinued'] = df['DiscontinuedDate'].notnull().astype(int)

# Group by 'PrimaryCategory' and sum the discontinued products in each category
category_discontinued_count = df.groupby('PrimaryCategory')['Discontinued'].sum().reset_index()

# Sort the categories by the count of discontinued products in descending order
category_discontinued_count = category_discontinued_count.sort_values(by='Discontinued', ascending=False)

# Create a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Discontinued', y='PrimaryCategory', data=category_discontinued_count, palette='viridis')

# Add labels and title
plt.title('Top Categories with Most Discontinued Products')
plt.xlabel('Number of Discontinued Products')
plt.ylabel('Primary Category')

# Show the plot on Streamlit
st.pyplot(plt)


# Horizontal divider
st.markdown("---")

# Section 7: Year with Most Product Discontinuations
st.header("Year with Most Product Discontinuations")

st.markdown("""
### Insight: 
The highest number of product discontinuations occurred in 2016 (2137), with a noticeable peak between 2009 and 2016, followed by a sharp decline in recent years.
### Implication: 
The peak in discontinuations might show that companies were adjusting to new rules or trends, and the later drop could mean products became better or there were fewer competitors.""")

df['DiscontinuedDate'] = pd.to_datetime(df['DiscontinuedDate'], errors='coerce')
discontinued_year = df['DiscontinuedDate'].dt.year.value_counts().sort_index()

plt.figure(figsize=(10, 6))
discontinued_year.plot(kind='bar', color='red')
plt.title('Year with Most Product Discontinuations')
plt.xlabel('Year')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)
st.pyplot(plt)



st.markdown("#### Discontinuation Trend Over Time")
discontinued_trend = df.groupby(df['DiscontinuedDate'].dt.year).size()

plt.figure(figsize=(10, 6))
discontinued_trend.plot(kind='line', marker='o', color='blue')
plt.title('Discontinued Products Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Discontinued Products')
plt.grid()
st.pyplot(plt)


# Horizontal divider
st.markdown("---")

import streamlit as st

# Assuming `marginal_prob_titanium` is already calculated
marginal_prob_titanium = 0.8154577572294675

# Subheading for Marginal Probability
st.markdown("## Marginal Probability")

# Display the probability
st.markdown("### Probability of a Product Containing Titanium Dioxide")
st.metric(label="Titanium Dioxide Probability", value=f"{marginal_prob_titanium:.2%}")

# Add insights
st.markdown("#### Insights")
st.write(
    """
    - **Prevalence**: Approximately 81.55% of products contain Titanium Dioxide, making it a commonly used ingredient.
    - **Reason for Use**: Likely due to its properties such as providing opacity or UV protection.
    - **Potential Concerns**: However, its prevalence also raises concerns about potential health impacts, making it a key chemical for regulatory and consumer focus.
    """
)

# Horizontal divider
st.markdown("---")

import streamlit as st
import scipy.stats as stats
import pandas as pd

# Sample DataFrame (replace with your actual data)
# df = your_dataframe

# Grouping the data by 'PrimaryCategory' and getting the chemical count
grouped = df.groupby('PrimaryCategory')['ChemicalCount']

# ANOVA test
f_statistic, p_value = stats.f_oneway(*[group for name, group in grouped])

# Display the test results on the Streamlit page
st.markdown("## ANOVA Test on Chemical Count Across Product Categories")
st.markdown("### Objective")
st.write(
    """
    The goal is to determine whether the number of chemicals used in products 
    varies significantly across different product categories.
    """
)

st.markdown("### Hypothesis")
st.write(
    """
    - **Null Hypothesis (H₀):** Chemical count does not differ significantly across product categories.
    - **Alternative Hypothesis (H₁):** Chemical count differs significantly across product categories.
    """
)

# Display ANOVA results
st.markdown("### Results")
st.write(f"**F-statistic:** {f_statistic:.2f}")
st.write(f"**P-value:** {p_value:.5f}")

# Decision based on p-value
if p_value < 0.05:
    st.success(
        "Reject the null hypothesis: Chemical count differs significantly across product categories."
    )
else:
    st.info(
        "Fail to reject the null hypothesis: No significant difference in chemical count across product categories."
    )

# Interpretation
st.markdown("### Interpretation")
st.write(
    """
    - The p-value is less than 0.05, providing strong evidence to reject the null hypothesis.
    - This indicates a statistically significant difference in the chemical count between product categories.
    """
)

# Horizontal divider
st.markdown("---")


import streamlit as st
import scipy.stats as stats
import pandas as pd

# Sample DataFrame (replace with your actual data)
# df = your_dataframe

# Filter data for Makeup Products and Skin Care Products
makeup_data = df[df['PrimaryCategory'] == 'Makeup Products (non-permanent)']['ChemicalCount']
skincare_data = df[df['PrimaryCategory'] == 'Skin Care Products ']['ChemicalCount']

# Perform a two-sample t-test
t_stat, p_value = stats.ttest_ind(makeup_data, skincare_data, equal_var=False)  # Assuming unequal variances

# Display the results on the Streamlit page
st.markdown("## Hypothesis Testing on Chemical Count in Makeup vs. Skincare Products")
st.markdown("### Objective")
st.write(
    """
    We aimed to test whether the number of chemicals in makeup products differs significantly from those in skincare products.
    """
)

st.markdown("### Hypothesis")
st.write(
    """
    - **Null Hypothesis (H₀):** There is no significant difference in the number of chemicals between makeup and skincare products.
    - **Alternative Hypothesis (H₁):** The number of chemicals in makeup products is significantly different from skincare products.
    """
)

# Display test results
st.markdown("### Results")
st.write(f"**T-statistic:** {t_stat:.2f}")
st.write(f"**P-value:** {p_value:.2e}")

# Decision based on p-value
if p_value < 0.05:
    st.success(
        "Reject the null hypothesis: The number of chemicals in makeup products differs significantly from those in skincare products."
    )
else:
    st.info(
        "Fail to reject the null hypothesis: The number of chemicals in makeup products does not differ significantly from those in skincare products."
    )

# Interpretation
st.markdown("### Interpretation")
st.write(
    """
    - The p-value is extremely small (much less than 0.05), indicating a highly significant result.
    - This means that the number of chemicals in makeup products does differ significantly from those in skincare products.
    """
)

# Business Insights
st.markdown("### Business Insights")
st.write(
    """
    **The significant difference suggests that the chemical compositions of makeup and skincare products are not the same.**
    - **Skincare products** may require more active ingredients or a more complex formulation for skin benefits.
    - **Makeup products** may need different chemicals for color, texture, and durability.

    **Implications for the Business:**
    - Product developers must understand that makeup and skincare products require distinct approaches in terms of chemical formulations.
    - Regulatory requirements and industry standards may differ between these categories.
    """
)
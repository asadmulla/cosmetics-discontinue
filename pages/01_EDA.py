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


st.markdown("---")



# Section 1: Top 10 Reported Chemicals
st.header("Top 10 Most Reported Chemicals")

# Display Insight and Implication for the top 10 chemicals
st.markdown("""
### Insight: 
The top 10 most frequently reported chemicals, such as Titanium Dioxide or Coal Tar Distillates, are widely used across multiple products. These chemicals are commonly found in many formulations.

### Implication: 
Commonly used chemicals, especially toxic ones, should be closely monitored. Brands using these ingredients may face consumer pressure or regulatory challenges.
""")


top_chemicals = df['ChemicalName'].value_counts().head(10).sort_values(ascending=True) 

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

# Section 2: Products with 5 or More Toxic Chemicals
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

# Section 3: Top 7 Brands by Chemical Usage
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
top_brands.plot(kind='bar', color='skyblue')
plt.title('Top 7 Brands by Chemical Usage')
plt.xlabel('Brand Name')
plt.ylabel('Chemical Count')
plt.xticks(rotation=45)
st.pyplot(plt)




st.markdown("---")

# Section 4: Top 10  by Category by Discontinued Products by
st.header("Top 10 Category by Discontinued Products")

# Display Insight and Implication for the top 10 chemicals
st.markdown("""
### Insight: 
The makeup products category shows a significantly high number of discontinued products, indicating rapid changes in trends, customer preferences, and potential product failures.Sun-related products have a moderate level of discontinued products, indicating their seasonal nature.
### Implication: 
Baby Products and Tattoos highlight the importance of strict safety standards.Businesses should focus on chemical-free alternatives, regulatory compliance, and transparency to address safety concerns, build consumer trust, and reduce product recalls.""")


category_counts = df['PrimaryCategory'].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_counts.values, y=category_counts.index, color='skyblue')
plt.xlabel('Number of Discontinued Products')
plt.ylabel('Primary Category')
plt.title('Top 10 Discontinued Product Categories')
plt.grid(True,axis='x', linestyle='--', alpha=0.7)
# Show the plot in Streamlit
st.pyplot(plt)



st.markdown("---")

# Section 5: Year with Most Product Discontinuations
st.header("Trend of Discontinued Products Over Time")

st.markdown("""
### Insight: 
The highest number of product discontinuations occurred in 2016 (2137), with a noticeable peak between 2009 and 2016, followed by a sharp decline in recent years.
### Implication: 
The peak in discontinuations might show that companies were adjusting to new rules or trends, and the later drop could mean products became better or there were fewer competitors.""")

df['DiscontinuedDate'] = pd.to_datetime(df['DiscontinuedDate'], errors='coerce')

st.markdown("#### Discontinuation Trend Over Time")
discontinued_trend = df.groupby(df['DiscontinuedDate'].dt.year).size()

plt.figure(figsize=(10, 6))
discontinued_trend.plot(kind='line', marker='o', color='skyblue')
plt.title('Discontinued Products Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Discontinued Products')
plt.xticks(discontinued_trend.index, discontinued_trend.index.astype(int), rotation=45)
plt.grid()
st.pyplot(plt)



st.markdown("---")

import streamlit as st

df['ChemicalName'] = df['ChemicalName'].str.lower()

# Count products containing 'titanium dioxide'
titanium_count = df['ChemicalName'].str.contains('titanium dioxide', na=False).sum()
total_products = len(df)
probability_titanium = titanium_count / total_products
marginal_prob_titanium = probability_titanium*100

st.markdown("## Marginal Probability")

# Display the probability
st.markdown("### Probability of a Product Containing Titanium Dioxide")
st.metric(label="Titanium Dioxide Probability", value=f"{probability_titanium:.2%}")

# Add insights
st.markdown("#### Insights")
st.write(
    """
    - **Prevalence**: Approximately 81.68% of products contain Titanium Dioxide, making it a commonly used ingredient.
    - **Reason for Use**: Likely due to its properties such as providing opacity or UV protection.
    - **Potential Concerns**: However, its prevalence also raises concerns about potential health impacts, making it a key chemical for regulatory and consumer focus.
    """
)
st.markdown("---")
st.header("Target distribution")
discontinued_counts = df['Discontinued'].value_counts()

# Create Pie Chart
plt.figure(figsize=(4, 4))
plt.pie(discontinued_counts, labels=["Active", "Discontinued"], autopct='%1.1f%%', colors=["#3498DB", "#F39C12"])
plt.title("Percentage of Discontinued Products")
st.pyplot(plt)


st.markdown("---")

import streamlit as st
import scipy.stats as stats
import pandas as pd


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


st.markdown("---")


import streamlit as st
import scipy.stats as stats
import pandas as pd


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


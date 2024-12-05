# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Load datasets
# Assuming the two datasets are already available as ozempic_data and ozempic_reviews_data
ozempic_data_path = 'Ozempic_openFDA_Data.csv'
ozempic_reviews_data_path = 'Ozempic_Reviews_Drugs.csv'

ozempic_data = pd.read_csv(ozempic_data_path)
ozempic_reviews_data = pd.read_csv(ozempic_reviews_data_path)

####
# Preprocess the dataset: Filter age to a realistic range
ozempic_data['patient_age'] = pd.to_numeric(ozempic_data['patient_age'], errors='coerce')  # Ensure numeric
ozempic_data = ozempic_data[(ozempic_data['patient_age'] >= 0) & (ozempic_data['patient_age'] <= 120)]
####


###################################################

from textblob import TextBlob

# Generate sentiment labels
def classify_sentiment(text):
    if pd.isna(text):
        return "neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# Apply sentiment classification
ozempic_reviews_data["sentiment"] = ozempic_reviews_data["review_text"].apply(classify_sentiment)




###################################################

# Streamlit App
def main():
    # App title
    st.title("openFDA Ozempic Data Explorer")
    st.write("""
    This app allows users to explore adverse event data and user sentiment analysis for Ozempic.
    Use the filters and tabs to interact with the datasets and generate insights.
    """)
    
    # Sidebar filters (Unified for All Tabs)
    st.sidebar.header("Global Filters")
    age_range = st.sidebar.slider("Age Range", int(ozempic_data["patient_age"].min()),
                                   int(ozempic_data["patient_age"].max()), (30, 80))
    gender_filter = st.sidebar.multiselect("Gender", options=["Male", "Female"], default=["Male", "Female"])
    severity_filter = st.sidebar.selectbox("Event Severity", options=["All", "Serious", "Non-Serious"])
    
    # Data filtering
    filtered_data = ozempic_data[
        (ozempic_data["patient_age"] >= age_range[0]) &
        (ozempic_data["patient_age"] <= age_range[1])
    ]
    if "Male" in gender_filter and "Female" not in gender_filter:
        filtered_data = filtered_data[filtered_data["patient_sex"] == 1]
    elif "Female" in gender_filter and "Male" not in gender_filter:
        filtered_data = filtered_data[filtered_data["patient_sex"] == 2]
    if severity_filter == "Serious":
        filtered_data = filtered_data[filtered_data["serious"] == 1]
    elif severity_filter == "Non-Serious":
        filtered_data = filtered_data[filtered_data["serious"] == 0]
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Overview", "Data Explorer", "Visualizations"])
    
    
    with tab1:
        # Overview Tab
        st.subheader("Welcome to my openFDA Ozempic Data Explorer")
        st.write("""
        This Streamlit app provides an interactive platform for exploring data about Ozempic, a medication widely used 
        for diabetes management and weight loss. Combining clinical adverse event reports from the openFDA dataset 
        with patient reviews from Drugs.com, the app allows users to delve into the real-world effects and user experiences of Ozempic.
        """)
        
        st.subheader("What You Can Do with This App")
        st.write("""
        - **Visualize Trends**:
            - Explore the most frequently reported side effects and their severity.
            - Understand demographic distribution of adverse events.
            - Analyze patient sentiment (positive, neutral, negative) from Drugs.com reviews.
        - **Filter and Customize**:
            - Use sidebar filters to narrow the data by age range, gender, event severity, or keywords. (Some graphs are not affected by the sidebar filters)
            - Dynamically adjust visualizations to focus on specific subsets of the data.
        - **Download and Explore Data**:
            - Download filtered datasets (openFDA Ozempic data and Drugs.com reviews) for offline analysis or custom insights.
        """)
        
        st.subheader("How to Use This App")
        st.write("""
        1. **Explore Clinical Data**:
            - Head to the **Data Explorer** tab to view the raw datasets, apply filters, and download the data for personal analysis.
        2. **Interact with Visualizations**:
            - In the **Visualizations** tab, use the interactive charts to:
                - Identify the top side effects reported.
                - Compare the proportion of serious vs. non-serious adverse events.
                - Examine patient sentiment across reviews, including specific keywords like "weight loss" or "nausea."
        """)

        st.subheader("My Hope For This App")
        st.write("""
        Whether you’re a researcher, healthcare professional, or simply curious about Ozempic’s effects, I truly hope my Streamlit app inspires you 
        to find new way to explore data in a user-friendly and interactive way. Secondly, I hope it also helps you gain valuable insights into how Ozempic impacts 
        patients both clinically and emotionally.
        """)

    
    # Data Explorer Tab
    with tab2:
        st.subheader("Data Explorer")
        st.write("openFDA Ozempic Dataset:")
        st.dataframe(filtered_data)
        st.download_button(
            label="Download openFDA Dataset",
            data=filtered_data.to_csv(index=False).encode('utf-8'),
            file_name='filtered_ozempic_data.csv',
            mime='text/csv',
        )
        
        
        # Drugs.com Reviews Dataset
        st.write("Drugs.com Reviews Dataset:")
        st.dataframe(ozempic_reviews_data)
        st.download_button(
            label="Download Drugs.com Reviews Data",
            data=ozempic_reviews_data.to_csv(index=False).encode('utf-8'),
            file_name='ozempic_reviews_data.csv',
            mime='text/csv',
        )
    
    # Visualization Tab
    with tab3:
        
        st.subheader("Top 10 Most Reported Side Effects")
        
        # Use only gender and age filters for this chart
        side_effects_data = ozempic_data[
            (ozempic_data["patient_age"] >= age_range[0]) &
            (ozempic_data["patient_age"] <= age_range[1])
        ]
        if "Male" in gender_filter and "Female" not in gender_filter:
            side_effects_data = side_effects_data[side_effects_data["patient_sex"] == 1]
        elif "Female" in gender_filter and "Male" not in gender_filter:
            side_effects_data = side_effects_data[side_effects_data["patient_sex"] == 2]
        
        # Calculate Top 10 Side Effects
        top_side_effects = side_effects_data["reaction_meddra"].value_counts().head(10)

        # Plot the bar chart
        fig, ax = plt.subplots()
        top_side_effects.plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")
        ax.set_title("Top 10 Most Reported Side Effects")
        ax.set_xlabel("Side Effects")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
        
        

        st.subheader("Serious vs. Non-Serious Adverse Events")

        # Apply gender and age filters
        severity_data = ozempic_data[
            (ozempic_data["patient_age"] >= age_range[0]) &
            (ozempic_data["patient_age"] <= age_range[1])
        ]
        if "Male" in gender_filter and "Female" not in gender_filter:
            severity_data = severity_data[severity_data["patient_sex"] == 1]
        elif "Female" in gender_filter and "Male" not in gender_filter:
            severity_data = severity_data[severity_data["patient_sex"] == 2]
        
        # Debugging: Check the filtered data
        st.write("Filtered Data for Severity Chart:")
        st.write(severity_data.head())  # Verify the data used for the chart

        # Calculate serious vs. non-serious counts
        severity_counts = severity_data["serious"].value_counts()

        # Handle cases where data might be empty
        if not severity_counts.empty:
            labels = ["Serious" if idx == 1 else "Non-Serious" for idx in severity_counts.index]
            sizes = [severity_counts.get(1, 0), severity_counts.get(2, 0)]  # Proper mapping of 1 and 2
        else:
            labels = ["No Data"]
            sizes = [1]

        # Plotting the pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=["orange", "skyblue"])
        ax.set_title("Severity Distribution of Adverse Events")
        st.pyplot(fig)


        # Sentiment Distribution Bar Chart
        st.subheader("Sentiment Distribution in Reviews")

        # Filter by keywords
        keyword_filter = st.text_input("Filter Reviews by Keyword:", "")
        
        # Filter by sentiment
        sentiment_filter = st.selectbox(
            "Filter by Sentiment:",
            options=["All", "Positive", "Neutral", "Negative"],
            index=0
        )
        
        # Apply keyword filter first
        sentiment_data = ozempic_reviews_data.copy()
        if keyword_filter:
            sentiment_data = sentiment_data[
                sentiment_data["review_text"].str.contains(keyword_filter, case=False, na=False)
            ]
        
        # Check if the keyword filter resulted in an empty DataFrame
        if sentiment_data.empty:
            st.error("That word was not found in the Reviews.")
        else:
            # Apply sentiment filter (only after keyword filter)
            if sentiment_filter != "All":
                sentiment_map = {"Positive": "positive", "Neutral": "neutral", "Negative": "negative"}
                sentiment_data = sentiment_data[
                    sentiment_data["sentiment"] == sentiment_map[sentiment_filter]
                ]

            # Count sentiment categories based on filtered data
            sentiment_counts = sentiment_data["sentiment"].value_counts()

            # Assign default colors for "All" view
            color_map = {"positive": "green", "neutral": "gray", "negative": "red"}
            if sentiment_filter == "All":
                colors = [color_map.get(sent, "blue") for sent in sentiment_counts.index]
            else:
                # Assign single color for filtered sentiment
                colors = [color_map[sentiment_map[sentiment_filter]]]

            # Plot the bar chart
            fig3, ax = plt.subplots()
            sentiment_counts.plot(kind="bar", ax=ax, color=colors, edgecolor="black")
            ax.set_title(f"Sentiment Distribution in Reviews (Filtered by '{keyword_filter}' and {sentiment_filter})")
            ax.set_xlabel("Sentiment")
            ax.set_ylabel("Number of Reviews")
            st.pyplot(fig3)

            
        
        
        
        
        


# Run the app
if __name__ == "__main__":
    main()

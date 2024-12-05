# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
# Assuming the two datasets are already available as ozempic_data and ozempic_reviews_data
ozempic_data_path = 'Ozempic_openFDA_Data.csv'
ozempic_reviews_data_path = '/mnt/data/Ozempic_Reviews_Drugs.csv'

ozempic_data = pd.read_csv(ozempic_data_path)
ozempic_reviews_data = pd.read_csv(ozempic_reviews_data_path)

# Streamlit App
def main():
    # App title
    st.title("openFDA Ozempic Data Explorer")
    st.write("""
    This app allows users to explore adverse event data and user sentiment analysis for Ozempic.
    Use the filters and tabs to interact with the datasets and generate insights.
    """)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    age_range = st.sidebar.slider("Age Range", int(ozempic_data["patient_age"].min()),
                                   int(ozempic_data["patient_age"].max()), (30, 60))
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
    
    # Overview Tab
    with tab1:
        st.subheader("Overview")
        st.write("""Explore the datasets, filter the data, and view dynamic visualizations.""")
    
    # Data Explorer Tab
    with tab2:
        st.subheader("Data Explorer")
        st.write("Filtered Dataset:")
        st.dataframe(filtered_data)
        st.download_button(
            label="Download Filtered Data",
            data=filtered_data.to_csv(index=False).encode('utf-8'),
            file_name='filtered_ozempic_data.csv',
            mime='text/csv',
        )
    
    # Visualization Tab
    with tab3:
        st.subheader("Visualizations")
        st.write("Top 10 Most Reported Side Effects")
        top_side_effects = filtered_data["reaction_meddra"].value_counts().head(10)
        
        # Bar chart for Top 10 Side Effects
        fig, ax = plt.subplots()
        top_side_effects.plot(kind='bar', ax=ax)
        ax.set_title("Top 10 Most Reported Side Effects")
        ax.set_xlabel("Side Effects")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def top_names_plot(df, year=2000, n=10, width=800, height=600, variable='count'):
    year_data = df[df['year'] == year].copy()
    year_data['overall_rank'] = year_data[variable].rank(method='min', ascending=False).astype(int)

    male_names = year_data[year_data['sex'] == 'M']
    top_male = male_names.sort_values(variable, ascending=False).head(n)
    top_male['sex_rank'] = range(1, n + 1)  # Rank within male names

    female_names = year_data[year_data['sex'] == 'F']
    top_female = female_names.sort_values(variable, ascending=False).head(n)
    top_female['sex_rank'] = range(1, n + 1)  # Rank within female names

    df = pd.concat([top_male, top_female])
    df.sort_values(variable, ascending=False, inplace=True)

    fig = px.bar(df, x='name', y=variable, color='sex',
                category_orders={"name": df['name'].tolist()},
                hover_data={'sex_rank': True, 'overall_rank': True, 'sex': False, 'name': False})  # Add custom hover data

    fig.update_layout(title=f'Top {n} by sex names in {year}',
                    width=width, height=height)  
    return fig  


def name_frequencies_plot(df, year=200, width=800, height=600):
    year_data = df[df['year'] == year].copy()
    name_counts = year_data.groupby(['name', 'sex'])['count'].sum().reset_index()
    color_map = {"M": "#636EFA", "F": "#EF553B"}

    fig = px.histogram(
        name_counts, 
        x='count', 
        color='sex',  
        nbins=30, 
        title=f"Distribution of Name Frequencies by Sex in {year}",
        facet_col='sex',
        category_orders={'sex': ['M', 'F']},
        color_discrete_map=color_map 
    )

    fig.update_yaxes(type="log", matches="y")
    fig.update_xaxes(title_text="Number of Occurrences of Each Name", matches="x")

    fig.update_layout(
        xaxis_title="Number of Occurrences of Each Name",
        yaxis_title="Frequency (Log Scale)",
        yaxis_type="log",  # Set y-axis to log scale
        width=width, height=height
    )
    return fig

def name_trend_plot(df, name='John', width=800, height=600):
    name_data = df[df['name'] == name].copy()
    color_map = {"M": "#636EFA", "F": "#EF553B"}

    if name_data.empty:
        print("Name not found in the dataset.")
    else:
        # Group by Year and Sex, and calculate total counts
        #sex_counts = name_data.groupby(['year', 'sex'])['count'].sum().reset_index()

        # Calculate total count per year and male-to-female ratio
        yearly_counts = name_data.groupby(['year', 'sex']).sum()['count'].unstack(fill_value=0)
        yearly_counts['Total'] = yearly_counts['M'] + yearly_counts['F']
        yearly_counts['Male_Ratio'] = yearly_counts['M'] / yearly_counts['Total']
        yearly_counts['Female_Ratio'] = yearly_counts['F'] / yearly_counts['Total']
        yearly_counts = yearly_counts.reset_index()

        # Create subplots with shared x-axis
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("Total Count Over Time", "Sex Balance Ratio Over Time")
        )

        # Add total count plot
        fig.add_trace(
            go.Scatter(x=yearly_counts['year'], y=yearly_counts['M'], mode='lines', name='Male', line=dict(color=color_map['M'])),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(x=yearly_counts['year'], y=yearly_counts['F'], mode='lines', name='Female', line=dict(color=color_map['F'])),
            row=1, col=1
        )

        # Add male and female ratio plot
        fig.add_trace(
            go.Scatter(x=yearly_counts['year'], y=yearly_counts['Male_Ratio'], mode='lines', showlegend=False,  line=dict(color=color_map['M'])),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=yearly_counts['year'], y=yearly_counts['Female_Ratio'], mode='lines', showlegend=False, line=dict(color=color_map['F'])),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            title=f"Name Trend and Sex Distribution for '{name}'",
            xaxis_title="Year",
            yaxis_title="Total Count",
            yaxis2_title="Ratio",
            height=height,
            width=width
        )

        return fig

def name_sex_balance_plot(df, name='John'):
    name_data = df[df['name'] == name].copy()
    color_map = {"M": "#636EFA", "F": "#EF553B"}

    if name_data.empty:
        print("Name not found in the dataset.")
    else:
        sex_counts = name_data.groupby('sex').sum()['count']
        male_count = sex_counts.get('M', 0)
        female_count = sex_counts.get('F', 0)
        total_count = male_count + female_count
        if total_count > 0:
            male_ratio = male_count / total_count
            female_ratio = female_count / total_count

            fig, ax = plt.subplots(figsize=(10, 2))

            # Create a stacked bar representing male and female ratios
            ax.barh(0, male_ratio, color=color_map['M'], label='Male')
            ax.barh(0, female_ratio, left=male_ratio, color=color_map['F'], label='Female')

            # Customize the chart
            ax.set_xlim(0, 1)
            ax.set_xticks([0, 0.5, 1])
            ax.set_xticklabels(['0%', '50%', '100%'])
            ax.set_yticks([])  # Hide y-axis ticks

            # Add labels to display the ratios
            ax.text(male_ratio / 2, 0, f"{male_ratio * 100:.1f}%", va='center', 
                    ha='center', color='white', 
                    fontweight='bold',
                    fontsize=20)
            ax.text(male_ratio / 2, -.25, "male", va='center', 
                    ha='center', color='white', 
                    fontweight='bold',
                    fontsize=20)
            ax.text(male_ratio + female_ratio / 2, 0, f"{female_ratio * 100:.1f}%", va='center', 
                    ha='center', color='white', 
                    fontweight='bold',
                    fontsize=20)
            ax.text(male_ratio + female_ratio / 2, -.25, "female", va='center', 
                    ha='center', color='white', 
                    fontweight='bold',
                    fontsize=20)
            plt.title(f"Sex Balance of the '{name}'")
            return fig


        else:
            print("Insufficient data for gender dominance calculation.")

def unique_names_summary(df, year=1977):
    year_data = df[df['year'] == year].copy()
    total_names_per_sex = year_data.groupby('sex')['count'].sum()
    unique_names_per_sex = year_data.groupby('sex')['name'].nunique()
    percent_unique_names_per_sex = (unique_names_per_sex / total_names_per_sex) * 100

    output = pd.DataFrame({
        "Total Names": total_names_per_sex,
        "Unique Names": unique_names_per_sex,
        "Percent Unique": percent_unique_names_per_sex})
    
    return output

def one_hit_wonders(ohw_data, year=1977):
    
    ohw_year = ohw_data[ohw_data['year']==year]

    if ohw_year.empty:
        print(f"No one-hit wonders found in {year}")
    else:
        one_hit_wonder_counts = ohw_year['sex'].value_counts()
        common_one_hit_wonders = ohw_year.groupby(['name', 'sex'])['count'].sum().reset_index()

        try: 
            most_common_female = common_one_hit_wonders[common_one_hit_wonders['sex'] == 'F'].sort_values(by='count', ascending=False).iloc[0]
            most_common_male = common_one_hit_wonders[common_one_hit_wonders['sex'] == 'M'].sort_values(by='count', ascending=False).iloc[0]

            print(f"Summary of One-Hit Wonders in {year}:")
            print(f"Number of female one-hit wonders: {one_hit_wonder_counts.get('F', 0)}")
            print(f"Number of male one-hit wonders: {one_hit_wonder_counts.get('M', 0)}")

            print(f"Most common female one-hit wonder: {most_common_female['name']} with {most_common_female['count']} occurrences")
            print(f"Most common male one-hit wonder: {most_common_male['name']} with {most_common_male['count']} occurrences")
        except:
            print(f"Not enough data to calculate one-hit wonders by sex in {year}")



#################################################



# Sidebar
st.sidebar.title("BYU Life")
st.sidebar.write("Navigate your BYU journey!")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/BYUlogo.svg/1200px-BYUlogo.svg.png", use_container_width=True)
st.sidebar.write("Explore credit load, study hour balance, and a small list of things to do!")

# Tabs
tab1, tab2, tab3 = st.tabs(["Dashboard", "Study Habits", "Campus Fun"])

# Tab 1: Dashboard Content
with tab1:
    st.title("Welcome to BYU Life Tracker")
    st.write("Track your academic progress, study habits, and involvement on campus!")

    # Input Widgets
    st.header("Customize Your Tracker")
    credit_hours = st.number_input("How many credit hours are you taking?", value=15, step=1)
    study_hours = st.slider("How many hours do you study per week?", min_value=0, max_value=50, value=15)
    major = st.selectbox("Do you feel overwhelmed with your current schedule?", options=["Yes", "Somewhat", "No"])
    involvement = st.radio("Have you sought on campus learning assistance?", options=["Yes", "No", "What's that?"])

    # Graph that shoudl update based on study_hours
    st.subheader("Study Hours Overview")
    x = np.arange(6)  # Days of the week (Monday to Saturday)
    y = [study_hours / 6] * 6  # Distribute study hours across six days (excluding Sunday)
    fig, ax = plt.subplots()
    ax.bar(x, y, tick_label=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], color="#002E5D")  # Exclude Sunday
    ax.set_ylabel("Hours Studied")
    ax.set_title("Study Hours Per Day")
    st.pyplot(fig)


    # Dynamic Text
    st.write("🏆 Academic Insights:")
    st.write(f"You're taking **{credit_hours} credit hours** and studying **{study_hours} hours per week**. "
            f"This suggests you're dedicating about **{study_hours / credit_hours:.1f} hours per credit hour**—")

    # My feedback based on user's study hours per credit hour
    study_per_credit = study_hours / credit_hours if credit_hours > 0 else 0

    if study_per_credit < 2:
        st.warning("You're dedicating less than 2 hours per credit hour. Make sure your understanding the class material.")
    elif 2 <= study_per_credit <= 3:
        st.success("Great! You're within the recommended study range of 2-3 hours per credit hour. Keep up the good work!")
    else:
        st.error("You're studying more than 3 hours per credit hour. This might indicate that you're struggling to understand the material. "
                "Consider seeking support such as attending TA sessions, teacher office hours, or group tutoring to improve your efficiency and understanding.")


    # Table
    st.write("📅 Suggested Weekly Breakdown:")
    schedule = pd.DataFrame({
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "Hours to Study": [study_hours / 6] * 6
    })
    st.table(schedule)

# Tab 2: Study Habits
with tab2:
    st.title("Study Habits Analysis")

    # 1. User selects number of study days
    study_days = st.multiselect(
        "Select which days you study:",
        options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        default=["Monday", "Wednesday", "Friday"]
    )

    # 2. They input specific hours for each day
    study_hours = {}
    for day in study_days:
        study_hours[day] = st.number_input(f"How many hours do you study on {day}?", min_value=0.0, max_value=24.0, value=2.0, step=0.5)

    # User populates hours for days not selected
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in all_days:
        if day not in study_hours:
            study_hours[day] = 0.0

    # This bar chart updates dynamically
    st.write("Your Weekly Study Schedule:")
    x = np.arange(7)  # Days of the week
    y = [study_hours[day] for day in all_days]  # Hours per day
    fig, ax = plt.subplots()
    ax.bar(x, y, tick_label=all_days, color="#002E5D")
    ax.set_ylabel("Hours Studied")
    ax.set_title("Study Hours Per Day")
    st.pyplot(fig)

    # Compare input to national average
    national_average = [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5]  # Example national average for each day

    st.write("Comparison with National Average:")
    fig2, ax2 = plt.subplots()
    width = 0.35  # Width of bars

    # User data bars
    ax2.bar(x - width / 2, y, width=width, label="Your Hours", color="#002E5D")

    # National average bars
    ax2.bar(x + width / 2, national_average, width=width, label="National Average", color="#A5A7AA")

    ax2.set_xticks(x)
    ax2.set_xticklabels(all_days)
    ax2.set_ylabel("Hours Studied")
    ax2.set_title("Study Hours vs National Average")
    ax2.legend()
    st.pyplot(fig2)

    # Summary Text
    total_study_hours = sum(y)
    national_avg_total = sum(national_average)
    st.write(f"**Your Total Weekly Study Hours:** {total_study_hours} hours")
    st.write(f"**National Average Weekly Study Hours:** {national_avg_total} hours")
    if total_study_hours > national_avg_total:
        st.success("You're studying more than the national average. Don't push yourself more than you can bear!")
    elif total_study_hours == national_avg_total:
        st.info("You're matching the national average. Keep it up!")
    else:
        st.warning("You're studying less than the national average. Consider increasing your credit load!")

# Tab 3: Campus Fun
with tab3:
    st.title("Campus Fun and Events")
    st.write("Here's some fun activities and events you can do at BYU!")

    
    st.container()
    with st.container():
        st.subheader("Weekly Activity Ideas")
        st.write("- **Monday**: FHE at the Wilkinson Center.")
        st.write("- **Tuesday**: Devotional at the Marriott Center and on-campus club nights.")
        st.write("- **Wednesday**: BYUSA Club Activities.")
        st.write("- **Thursday**: Study night with friends at the library.")
        st.write("- **Friday**: Cheer the Cougars at the game!")
        st.write("- **Saturday**: Hike the Y, play volleyvall, or have a date night!")
        st.write("- **Sunday**: Worship, reflect, and recharge.")


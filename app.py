import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

##
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)

##
st.sidebar.markdown("# Olympics 🏅 Analysis")
st.sidebar.markdown("An interactive dashboard to explore historical Olympics data.")
st.sidebar.image('https://assets.editorial.aetnd.com/uploads/2010/01/gettyimages-466313493-2.jpg?width=1920&height=960&crop=1920%3A960%2Csmart&quality=75')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Basic Stats','Analysis Over Time','Total Medals By Each Country','Total Medals In Each Years','Medals Filter By Country And Year','Trend Analysis for a Country',
     'Trend Analysis In Every Sport for a Country','Top Atheletes for a Country','Age Distribution','Men and Women Participation Over the Years')
)



if user_menu == 'Total Medals By Each Country':
    st.sidebar.header("Medal Table For Countries")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)

    medal_tally = helper.fetch_medal_tally_region(df,selected_year)
    if selected_year == 'Overall':
        st.title("Medals In All Years")
    if selected_year != 'Overall':
        st.title("Medals in " + str(selected_year) + " Olympics")
    st.table(medal_tally)



if user_menu == 'Total Medals In Each Years':
    st.sidebar.header("Medal Table For Years")
    years,country = helper.country_year_list(df)

    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally_year(df,selected_country)
    if selected_country == 'Overall':
        st.title("Medals By All Countries")
    if selected_country != 'Overall':
        st.title("Medals By " + str(selected_country))
    st.table(medal_tally)


if user_menu == 'Medals Filter By Country And Year':
    st.sidebar.header("Medal Table for a country in a year")
    years,country = helper.country_year_list(df)
    years = years[1:]
    country=country[1:]
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally_year_country(df, selected_year, selected_country)

    st.title(str(selected_country) + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Basic Stats':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)


if user_menu == 'Analysis Over Time':
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y='Count of ' + 'region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    nations_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(nations_over_time, x="Year", y='Count of ' + 'Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    nations_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(nations_over_time, x="Year", y='Count of ' + 'Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)




if user_menu == 'Trend Analysis for a Country':
    st.sidebar.header("Select a Country for time series trend")
    years,country = helper.country_year_list(df)
    years = years[1:]
    country = country[1:]
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_trend_for_country(df,selected_country)
    st.title("Trend Analysis for " + str(selected_country))
    fig = px.line(medal_tally, x="Year", y='Medal')
    st.plotly_chart(fig)
    #st.table(medal_tally)


if user_menu == 'Trend Analysis In Every Sport for a Country':
    st.sidebar.header("Select a Country for time series trend")
    years,country = helper.country_year_list(df)
    years = years[1:]
    country = country[1:]
    selected_country = st.sidebar.selectbox("Select Country", country)

    st.title("Medals Over Time In Every Sport")

    # Remove NaN values in 'Medal' column
    temp_df = df.dropna(subset=['Medal'])

    # Remove duplicates and assign the result back to temp_df
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # Filter by the selected country
    new_df = temp_df[temp_df['region'] == selected_country]

    # Create a pivot table
    pivot_table = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(
        'int')

    # Check if the pivot_table is empty
    if not pivot_table.empty:
        # Plot the heatmap
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pivot_table, annot=True, ax=ax)
        st.pyplot(fig)
    else:
        st.write("No data available for the selected country.")

if user_menu == 'Top Atheletes for a Country':
    st.sidebar.header("Select a Country To get Top Athletes")
    years,country = helper.country_year_list(df)
    years = years[1:]
    country = country[1:]
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_top_atheletes(df,selected_country)
    st.title("Top Athletes for " + str(selected_country))
    st.table(medal_tally)



if user_menu == 'Age Distribution':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt Medal Type")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Gymnastics',
                      'Weightlifting', 'Wrestling',
                      'Hockey', 'Rowing',
                     'Shooting', 'Boxing',  'Cycling', 'Diving',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Table Tennis', 'Baseball',
                     'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age of Gold Medalist wrt Sports")
    st.plotly_chart(fig)


if user_menu== "Men and Women Participation Over the Years":
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    st.title("Men Vs Women Participation Over the Years")
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

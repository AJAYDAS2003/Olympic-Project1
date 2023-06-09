import Preprocessor,helper
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=Preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://peacepalacelibrary.nl/sites/default/files/styles/featured_image/public/2019-10/Other-Research-guide-Olympic-games.jpg?itok=PHrPGsDF")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Countrywise Analysis','Athlete wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    metal_Tally=helper.fetch_metal_tally(df,selected_year,selected_country)
    if selected_year=='overall' and selected_country=='overall':
        st.title('Overall Tally')
    if selected_year!='overall' and selected_country=='overall':
        st.title('Medal Tally in '+ str(selected_year) +" Olympics")
    if selected_year=='overall' and selected_country!='overall':
        st.title(selected_country+" Overall Performence.")
    if selected_year!='overall' and selected_country!='overall':
        st.title(selected_country+" performence in "+str(selected_year))
    st.table(metal_Tally)
if user_menu=='Overall Analysis':
    editions = df['Year'].nunique()-1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    event = df['Event'].nunique()
    nations = df['region'].nunique()
    athletes = df['Name'].nunique()
    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
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
        st.header("Countries")
        st.title(nations)
    with col2:
        st.header("Events")
        st.title(event)
    with col3:
        st.header("Athletes")
        st.title(athletes)


    nations_over_time=helper.participating_nation_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating nations over years:")
    st.plotly_chart(fig)
    data_over_time = helper.participating_nation_over_time(df,'Event')
    fig = px.line(data_over_time, x="Year", y="Event")
    st.title("Events organised over years:")
    st.plotly_chart(fig)
    athlete_over_time = helper.participating_nation_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="Name")
    st.title("Athletes over years:")
    st.plotly_chart(fig)

    st.title("No. of events over time(Every Sport):")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int32'),annot=True)
    st.pyplot(fig)

    st.title("Most Sucessful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_sucessful(df,selected_sport)
    st.table(x)
if user_menu == 'Countrywise Analysis':

    st.sidebar.title("Countrywise Analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a country",country_list)
    country_df=helper.Year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country +" Medal Tally over years:")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports:")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes in "+selected_country)
    top10_df=helper.most_sucessful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,height=600,width=1000)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    Name = []
    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                    'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo',
                    'Hockey', 'Rowing', 'Fencing', 'Equestrianism', 'Shooting', 'Boxing',
                    'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Modern Pentathlon',
                    'Golf', 'Softball', 'Archery', 'Volleyball',
                    'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Trampolining', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo', 'Cricket',
                    'Ice Hockey']
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        Name.append(sport)

    fig = ff.create_distplot(x,Name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, height=600, width=1000)
    st.title("Distribution of Age wrt sports(Gold Medalist")
    st.plotly_chart(fig)

    st.title("Weight vs Height")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women participation over the Years")
    temp_df=helper.men_vs_female(df)
    fig = px.line(temp_df, x="Year", y=['Male', 'Female'])
    fig.update_layout(autosize=False, height=600, width=1000)
    st.plotly_chart(fig)
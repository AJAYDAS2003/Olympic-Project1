import numpy as np
def medal_tally(df):
    medal_Tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    medal_Tally=medal_Tally.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold', ascending=False).reset_index()
    medal_Tally['Total'] = medal_Tally['Gold'] + medal_Tally['Bronze'] + medal_Tally['Silver']
    return medal_Tally
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years,country

def fetch_metal_tally(df,year,country):
    flag=0
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    if year == 'overall' and country =='overall':
        temp_df=medal_df
    if year == 'overall' and country !='overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year !='overall' and country=='overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='overall' and country!='overall':
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]
    if flag==0:
        x=temp_df.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
    else:
        x=temp_df.groupby('Year').sum()[['Bronze','Gold','Silver']].sort_values('Year').reset_index()
    x['Total']=x['Gold']+x['Bronze']+x['Silver']
    return x
def participating_nation_over_time(df,col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns={'index': 'Year', 'Year': col}, inplace=True)
    return nation_over_time

def most_sucessful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

def Year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby("Year").count()['Medal'].reset_index()
    return final_df
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return pt

def most_sucessful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df=temp_df[temp_df['region']==country]
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x
def weight_v_height(df,sport):
    temp_df = df.drop_duplicates(subset=['Name', 'region'])
    temp_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    return temp_df
def men_vs_female(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    final['Female'] = final['Female'].astype('int')
    return final
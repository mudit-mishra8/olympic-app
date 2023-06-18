import numpy as np

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally_region(df, year):
    # Remove duplicates
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # If year or country is 'Overall', use 'year_overall' or 'country_overall'
    year_column = 'year_overall' if year == 'Overall' else 'Year'

    # Filter the data
    temp_df = medal_df[(medal_df[year_column] == year)]

    # Group and sum the medals
    x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()


    # Compute total medals
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Convert medal counts to integers
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def fetch_medal_tally_year(df, country):
    # Remove duplicates
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    # If year or country is 'Overall', use 'year_overall' or 'country_overall'
    country_column = 'country_overall' if country == 'Overall' else 'region'

    # Filter the data
    temp_df = medal_df[ (medal_df[country_column] == country)]

    # Group and sum the medals

    x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    # Compute total medals
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Convert medal counts to integers
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def fetch_medal_tally_year_country(df, year, country):
    # Remove duplicates
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Filter the data
    temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    # Group and sum the medals

    x = temp_df[['Gold', 'Silver', 'Bronze']].sum().to_frame().T


    # Compute total medals
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # Convert medal counts to integers
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('count')
    nations_over_time.rename(columns={'count': 'Count of '+col}, inplace=True)
    return nations_over_time


def fetch_trend_for_country(df,country):

    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def fetch_top_atheletes(df,country):

    temp_df = df.dropna(subset=['Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Name').count()['Medal'].reset_index().merge(new_df, on='Name', how='inner')[[ 'Name', 'Medal_x', 'Sport']]
    final_df=final_df.drop_duplicates(subset=['Name','Medal_x'])
    sorted_df = final_df.sort_values(by='Medal_x', ascending=False)

    sorted_df['rank'] = sorted_df['Medal_x'].rank(method='min', ascending=False)

    # Filter out the top 10 (including ties)
    top_10_with_ties = sorted_df[sorted_df['rank'] <= sorted_df.loc[sorted_df['rank'] <= 10, 'rank'].max()]

    return top_10_with_ties.drop(columns=['rank'])

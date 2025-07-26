import time
import pandas as pd
import numpy as np

#Sets all CSV equal to one constant
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

#Start of user interatction prompts asking city, months and day filters
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Which city would you like to analyze? (chicago, new york city, washington), or type "quit" to exit: ').lower()
        if city == "quit":
            print("Exiting program.")
            return None, None, None
        elif city in CITY_DATA:
            break
        else:
            print('Invalid city. Please try again.')

    while True:
        month = input('Which month would you like to analyze? (all, january, february, march, april, may, june), or type "quit" to exit: ').lower()
        if month == "quit":
            print("Exiting program.")
            return None, None, None
        elif month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month. Please try again.')

    while True:
        day = input('Which day of the week would you like to analyze? (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday), or type "quit" to exit: ').lower()
        if day == "quit":
            print("Exiting program.")
            return None, None, None
        elif day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day. Please try again.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # filter by month if applicable
    if month != 'all':
        month_map = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        df = df[df['Start Time'].dt.month == month_map[month]]

    # filter by day if applicable
    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode().values[0]
    print(f'The most common month is {popular_month}')

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day_of_week = df['day_of_week'].mode().values[0]
    print(f'The most common day of the week is {popular_day_of_week}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode().values[0]
    print(f'The most common start hour is {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode().values[0]
    print(f'The most commonly used start station is {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode().values[0]
    print(f'The most commonly used end station is {popular_end_station}')

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode().values[0]
    print(f'The most frequent combination of start station and end station trip is {popular_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert 'End Time' column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    df['Trip Duration'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time is {total_travel_time}')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The mean travel time is {mean_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'The counts of user types are:\n{user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'The counts of gender are:\n{gender_counts}')
    else:
        print('No gender data available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode().values

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#quit function allowing user to quit at any time during input prompts 
def main():
    while True:
        city, month, day = get_filters()
        if city is None and month is None and day is None:
            break
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
#Function to ask user if they would like to display the raw data and to ask if they would like the next 5 lines of data after displayed data. 
        start_index = 0
        while True:
            view_data = input('\nWould you like to view the next 5 lines of raw data? Enter yes or no.\n')
            if view_data.lower() == 'yes':
                if start_index < len(df):
                    print(df.iloc[start_index:start_index+5])
                    start_index += 5
                else:
                    print('No more data')
                    break
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Exiting program.")
            break


if __name__ == "__main__":
    main()
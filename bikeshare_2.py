import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the city name to query: ")
    city = city.lower()
    while city not in CITY_DATA.keys():
        city = input("that city name not in database, try again: ")
        city = city.lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Enter all or the month you would like to query: ")
    month = month.lower()
    while month not in valid_months:
        month = input("Not a valid input month, try again: ")
        month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("Enter all or the day you would like to query: ")
    day = day.lower()
    while day not in valid_days:
        day = input("Not a valid input day, try again: ")
        day = day.lower()


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
    df['End Time'] = pd.to_datetime(df['End Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_start = df['Start Station'].mode()[0] 
    print('the most commonly used Start Station for the selected period is: ', station_start)

    # display most commonly used end station
    station_end = df['End Station'].mode()[0]
    print('the most common End Station for the selected period is: ', station_end)


    # display most frequent combination of start station and end station trip
    df['combined Start End'] = df['Start Station'] + ' to ' + df['End Station']
    combo_start_end = df['combined Start End'].mode()[0] 
    print('the most frequent combination of Start Station and End Station for the selected period is: ', combo_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['travel_time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['travel_time'].sum()
    print('the total time traveled for the selected period is: ', total_travel_time)

    # display mean travel time
    avg_travel_time = df['travel_time'].mean()
    print('the average travel time for the selected period is: ', avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user = df['User Type'].nunique()
    print('the counts of the user types for the selected period is: ', count_user)

    # Display counts of gender
    if 'Gender' in df:
        count_gender = df['Gender'].nunique()
        print('the counts of the user genders for the selected period is: ', count_gender)
    else:
        


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        mode_birth_year = df['Birth Year'].mode()[0]
        print('the earliest Birth Year for the selected period is: ', min_birth_year)
        print('the most recent Birth Year for the selected period is: ', max_birth_year)
        print('the most common Birth Year for the selected period is: ', mode_birth_year)
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, location=0):
    """Displays the raw data in 5 line increments."""

    n = 0
    if location + 5 > len(df):
        print('End of the data')
        return
    while n < 5:
        print(df.iloc[location,:], "\n")
        n += 1
        location += 1

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        valid_reponse = ['yes', 'no']
        display = 'yes'
        location = 0
        while display.lower() != 'no':
            display = input('\nWould you like to display the data? Enter yes or no.\n')
            while display.lower() not in valid_reponse:
                display = input('\nSorry, try again. Would you like to display some data? Enter yes or no.\n')

            if display.lower() == 'yes': 
                display_data(df, location)
                location += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in valid_reponse:
            restart = input('\nSorry, try again. Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

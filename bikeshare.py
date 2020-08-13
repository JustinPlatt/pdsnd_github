import time                     #for timers
import pandas as pd
import numpy as np

city_files = {'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv'}

def get_filters():
    """    Asks user to specify a city, month, and day to analyze.

    Returns:
    (str) city - abbreviated name of the city to analyze --  ['c', 'n', 'w']
    (str) month - month to filter by (1-6), or 'all' to not apply the filter
    (str) day - day of week to filter by (0-6), or 'all' to not apply the filter
    """

    month, day = ('all', 'all')     #set default month and day

    print('Hello! Let\'s explore some US bikeshare data!')

    city = input('Analyze data for [C]hicago, [N]ew York City, or [W]ashington? ').lower()
    while city not in ['c', 'n', 'w']:
        print('\nInvalid choice!')
        city = input('Analyze data for [C]hicago, [N]ew York City, or [W]ashington? ').lower()

    filter_input = input('Filter data by [M]onth, [D]ay of week, [B]oth, or [N]one? ').lower()
    while filter_input not in ['m', 'd', 'b', 'n']:
        print('\nInvalid choice!')
        filter_input = input('Filter data by [M]onth, [D]ay of week, [B]oth, or [N]one? ').lower()

    f = filter_input
    if f != 'n':
        if f in ['m', 'b']:
            month = input('Which month?  Input as an integer between 1 (Jan) and 6 (Jun) ')
            while month not in ('1', '2', '3', '4', '5', '6'):
                print('\nInvalid choice!')
                month = input('Which month?  Input as an integer between 1 (Jan) and 6 (Jun) ')
        if f in ['d', 'b']:
            day = input('Which day of the week?  Input as an integer between 0 (Monday) and 6 (Sunday) ')
            while day not in ('0', '1', '2', '3', '4', '5', '6'):
                print('\nInvalid choice!')
                day = input('Which day of the week?  Input as an integer between 0 (Monday) and 6 (Sunday) ')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv('./' + city_files[city])
    df['Start Time'] = pd.to_datetime(df['Start Time']) # convert 'Start Time' column values to datetime
    df['Month'] =  df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Start and End Station'] = df['Start Station'] + ' to ' + df['End Station']
    if month != 'all':
        df = df[df['Start Time'].dt.month == int(month)]
    if day != 'all':
        df = df[df['Start Time'].dt.weekday == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common month: ' + df['Month'].mode()[0])
    print('Most common day of week: ' + df['Day of Week'].mode()[0])
    print('Most common start hour: ' + str(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_counts = df['Start Station'].value_counts()
    top_start = start_counts.index[0] #Name of most frequent trip
    top_start_ct = start_counts.values[0] #Count of most frequent trip
    print('Most commonly used start station: {} ({} times)'.format(top_start,str(top_start_ct)))


    end_counts = df['End Station'].value_counts()
    top_end = end_counts.index[0] #Name of most frequent trip
    top_end_ct = end_counts.values[0] #Count of most frequent trip
    print('Most commonly used end station: {} ({} times)'.format(top_end,str(top_end_ct)))


    trip_counts = df['Start and End Station'].value_counts()
    top_trip = trip_counts.index[0]
    top_trip_ct = trip_counts.values[0]
    print('Most commonly used start station: {} ({} trips)'.format(top_trip,str(top_trip_ct)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total travel time (seconds): ' + str(df['Trip Duration'].sum()))
    print('Mean travel time (seconds): ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('\nUsers by Type:')
    print(df['User Type'].value_counts().to_frame()) #convert series back to df for cleaner look

    if 'Gender' in df.columns:
        print('\nUsers by Gender:')
        print(df['Gender'].value_counts().to_frame())
    else:
        print('\n No gender data exists.  Skipping...')

    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth:')
        print(int(df['Birth Year'].min()))
        print('\nMost recent year of birth:')
        print(int(df['Birth Year'].max()))
        print('\nMost common birth year:')
        print(int(df['Birth Year'].mode()[0])) #int removes the decimal
    else:
        print('\n No birth year data exists.  Skipping...')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """Displays five lines of data at a time."""
    print('\nFirst five rows of data:')
    start_row = 0
    end_row = 5
    view_more = 'y'
    while view_more == 'y':
        print()
        print(df.iloc[start_row:end_row])
        start_row += 5
        end_row +=5
        view_prompt = '\nWould you like to view five more rows? Enter [Y]es or [N]o.\n'
        view_more = input(view_prompt).lower()
        while view_more not in ('n', 'y'):
            print('\nInvalid choice!')
            view_more = input(view_prompt).lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart_prompt = '\nWould you like to restart? Enter [Y]es or [N]o.\n'
        restart = input(restart_prompt).lower()
        while restart not in ('n', 'y'):
            print('\nInvalid choice!')
            restart = input(restart_prompt)

        if restart == 'n': #quit if restart = n, otherwise restart
            print('\nSee you next time!')
            break


if __name__ == "__main__":
	main()

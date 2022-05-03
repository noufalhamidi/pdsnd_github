import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './Data/chicago.csv',
              'new york city': './Data/new_york_city.csv',
              'washington': './Data/washington.csv' }

month_names = {  'january':'1',
                 'february':'2',
                 'march':'3',
                 'april':'4',
                 'may':'5',
                 'june':'6',
                 'july':'7',
                 'august':'8',
                 'september':'9',
                 'october':'10',
                 'november':'11',
                 'december':'12',
                 'all':'all'  }

day_names = { 'sunday':'1',
              'monday':'2',
              'tuesday':'3',
              'wednesday':'4',
              'thursday':'5',
              'friday':'6',
              'saturday':'7',
              'all':'all'}

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
    city=str(input('Please enter the name of the city to analyze ("chicago","new york city","washington"):  ')).lower()

    while city not in CITY_DATA:
        city=str(input('\nInvalid input, please enter a valid city name:  ')).lower()
    # get user input for month (all, january, february, ... , june)
    month=str(input('Please enter the name of the month to filter by, or "all" to apply no month filter:  ')).lower()

    while month not in month_names:
        month=str(input('\nInvalid input, please enter a valid month or enter "all":  ')).lower()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=str(input('Please enter the name of the day of the week to filter by, or "all" to apply no month filter:  ')).lower()

    while day not in day_names:
        day=str(input('\nInvalid input, please enter a valid day name or enter "all":  ')).lower()


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
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Start_Hour']=df['Start Time'].dt.hour
    df['Start_Day']=df['Start Time'].dt.weekday
    df['Start_Month']=df['Start Time'].dt.month

    month=month_names[month]
    day=day_names[day]

    if month != 'all':
        month=int(month)
        df=df[df.Start_Month==month]

    if day != 'all':
        day=int(day)
        df=df[df.Start_Day==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['Start_Month'].mode()[0]
    print('\nThe most popular month is:',common_month)
    # display the most common day of week
    common_day=df['Start_Day'].mode()[0]
    print('\nThe most popular day of the week is:',common_day)
    # display the most common start hour
    common_hour=df['Start_Hour'].mode()[0]
    print('\nThe most popular hour is:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start=df['Start Station'].mode()[0]
    print('\nThe most popular start station is:',start)

    # display most commonly used end station
    end=df['End Station'].mode()[0]
    print('\nThe most popular end station is:',end)

    # display most frequent combination of start station and end station trip
    df['Trip']='from '+df['Start Station']+' to '+df['End Station']

    trip=df['Trip'].mode()[0]
    print('\nThe most popular trip is:',trip)

    print("\nThis took %s seconds." % (time.time() - start_time))



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total=df['Trip Duration'].sum()
    print('\nTotal travel time in seconds is:',total)

    # display mean travel time
    mean=df['Trip Duration'].mean()
    print('\nMean travel time in seconds is:',mean)

    print("\nThis took %s seconds." % (time.time() - start_time))



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of each user type:\n')
    typecount=df['User Type'].value_counts()
    print(typecount)

    # Display counts of gender
    if city !='washington':
        print('\nCounts of each gender:\n')
        gendercount=df['Gender'].value_counts()
        print(gendercount)

    # Display earliest, most recent, and most common year of birth
    if city !='washington':
        min_yob=int(df['Birth Year'].min())
        max_yob=int(df['Birth Year'].max())
        mode_yob=int(df['Birth Year'].mode()[0])

        print('\nThe earliest year of birth:',min_yob,'\nThe most recent year of birht:',max_yob,'\nThe most common year of birth:',mode_yob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    

def display_data(df):
    display_data=str(input('\nDo you want to see the first 5 rows of data? enter yes or no.  ')).lower()
    if display_data=='yes':
        print('\nBelow is the first 5 rows of data:\n')
        next5='yes'
        start_row=0
        end_row=5
        while next5=='yes':
            sample=df[:][start_row:end_row]
            print(sample)
            start_row+=5
            end_row+=5
            print('\nDo you want to see the next 5 rows?')
            next5=str(input('\nEnter "yes" or "no":   ')).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Bye bye!')
            break


if __name__ == "__main__":
	main()

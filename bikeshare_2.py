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
    while True:
        city=input("Enter the city name:").lower()
        if city not in CITY_DATA:
            print("Re-enter the city name:")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month=input("Enter the month: ").lower()
        if month in ["all", "january", "february","march", "april", "may" , "june"]:
            break
        else:
            print("Re-enter the month:  ")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("Enter the day: ").lower()
        if day in ["all", "monday", "tuesday","Wednesday","thursday" ,"friday","saturday"]:
            break
        else:
            print("Re-enter the day: ")

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
    """ reading the data of city"""
    df=pd.read_csv(CITY_DATA[city])

    """convert strat time from string to date time to extract month, week, day, hour"""
    df["Start Time"]=pd.to_datetime(df["Start Time"])

    """ extract month and day_of_week and start_hour from Start Time to create new columns"""

    df["month"]=df["Start Time"].dt.month
    df["day_of_week"]= df["Start Time"].dt.day_name()
    df["start_hour"]=df["Start Time"].dt.hour

    """ filter the dataframe by month """
    if month!= "all":
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        """finding the  corresponding int of month"""
        month=months.index(month)+1
        df=df[df["month"]==month]

    """ filter by day of week to create the new dataframe"""
    if day!= "all":
        df=df[df["day_of_week"]==day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print ("the most common month:", df["month"].mode()[0])

    # display the most common day of week
    print("the most common day: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    frequent_hour=df["start_hour"].mode()[0]
    print("the most common hour: ", frequent_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df["Start Station"].mode()[0]
    print("the most common start station: ", common_start_station)


    # display most commonly used end station

    print("the most common end station: ", df["End Station"].mode()[0])


    # display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=True).tail(1)
    print("the most frequent start and end station: ", start_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    """ using sum function  for trip duration to calculate the total travel time"""
    tot_travel_time=df["Trip Duration"].sum()
    """divide tot_travel_time by 3600(s) to convert seconds into hours"""
    print( "The total travel time (hour): ", tot_travel_time/3600)


    # display mean travel time
    """ using mean function for the trip duration to calculate the avergae travel time"""
    avg_travel_time=df["Trip Duration"].mean()
    """divide avg_travel_time by 3600(s) to convert seconds into hours"""
    print( "The average travel time (hour): ",avg_travel_time/3600)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count=df["User Type"].value_counts()
    print( "the counts of user types: ", user_type_count)


    # Display counts of gender
    """ We used for loap to select the cities,  we use try function to handle the error 
    incase the city of user input was Washington where Washington city has no Gender nor birth year columns,
    then we use value_counts function to count the gender 
    if the cities of user input were New York City or Chicago """

    for city in CITY_DATA.items():
        try:
            gender_count=df["Gender"].value_counts()
            print( "\nThe counts of gender: ", gender_count)
        except KeyError:
            print("\nGender Types:\nNo data available for this city.")

            # Display earliest, most recent, and most common year of birth
            """ use min function to calculate the earliest year of birth , use max function to determine
            the most recenet year of birth, use mode function to determine the the most common year for birth,
            This is applied to the cities of user input of New York City or Chicago. 
            However, Washington has no data for Birth year so we used try-except function to handle the error incase of
            userinput was Washington"""

        try:
            earliest_yb=df["Birth Year"].min()
            recent_yb=df["Birth Year"].max()
            common_yb=df["Birth Year"].mode()[0]

            print("\nThe earliest year of birth is ",earliest_yb)
            print("The most recent year of birth is ",recent_yb)
            print("The most common year of birth is ",common_yb)

            
        except KeyError:
            print("\nBirth Year:\nNo data available for this city.")
        break

    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    """Display that data 5 lines by 5 lines based on the user input, while loap continues to iterate
    the prompts and display the next 5 lines of the raw data at each iteration until the user input becomes
     no or there is no more data to display """

    raws=0
    show_data=input("\nWould you like to show 5 rows of the raw data? Please Enter yes or no.\n").lower()
    while show_data!="no":
        print (df.iloc[raws:raws+5])
        raws += 5
        show_data=input("Do you want to view  more 5 rows? Enter yes or no\n").lower()
            
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print(" !!Thank you for using Bike Share DATA exploring!!")
            break


if __name__ == "__main__":
	main()

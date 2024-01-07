import time
import pandas as pd
import seaborn as sns
import matplotlib as plt



CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }
def get_filters():
    """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input ('To view the available bikeshare data, kindly type:\n (ch) for Chicago\n (ny) for New York City\n (w) for Washington\n ').lower ()
    while city not in {'ch', 'ny', 'w'}:
        print('That\'s invalid input.')
        city = input ('To view the available bikeshare data, kindly type:\n (ch) for Chicago\n (ny) for New York City\n (w) for Washington\n ').lower ()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('\n\nTo filter {}\'s data by a particular month, please type the month name or all for not filtering by month: \n - January\n - February\n - March\n - April\n - May\n - June\n - All\n\n: '.format(city.title())).lower()

    while month not in months:
        print('That\'s invalid input.')
        month = input('\n\nTo filter {}\'s data by particular month, please type the month or all for not filtering by month:\n-January \n-Feburary\n-March\n-April\n-May\n-June\\n-All\n\n:'.format(
                city.title())).lower()
    days = ['monday', 'tuesday', 'wednesday', 'Thursday', 'friday', 'saturday','sunday', 'all']
    day = input ('\n\nTo filter{}\'s data by a particular month, please type the month or all for not filtering by day:\n-Saturday\n-Sunday\n-Monday\n-Tuesday\n-Wednesday\n-Thursday\n-Friday\\n - All\n\n:'.format(city.title())).lower()
    while day not in days:
        print ('That\'s not a valid choice')
        day = input ('\n\nTo filter {}\'s data by a particular day, please type the day name or all for not filtering by day:\n-Saturday\n-Sunday\n-Monday\n-Tuesday\n-Wednesday\n-Thursday\n-Friday\\n-All\n\n:'.format(city.title())).lower()

    print('-' * 40)
    return city, month, day
city, month, day = get_filters()
print (city, month, day)

def load_data(city,month,day):
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 #change from January, Feburary, March (1,2,3) to match the excel sheet

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
df = load_data(city, month, day)
print (df.head())

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df ['month'].mode()[0]
    print ('Th most common month is:', most_common_month)

    # display the most common day of week
    most_common_day= df ['day_of_week'].mode()[0]
    print('The most common day of the week:', most_common_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df ['hour'].mode()[0]
    print('The most common start hour:', most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

time_stats(df,month, day)


def station_stats(df, station=None):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Most_Common_start_station = df['Start Station'].mode(0)
    print ('The most common Start Station:', Most_Common_start_station )

    # display most commonly used end station
    Most_Common_end_station = df['End Station'].mode(0)
    print ('The most common end station:', Most_Common_end_station)


    # display most frequent combination of start station and end station trip
    df["route"] = df["Start Station"] + "-" + df["End Station"]
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


station_stats(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    Start_Time = time.time()


    # display total travel time
    Total_travel_time = df ['Total Travel Time']=df['Trip Duration'].sum()
    print('Total Average Time:', Total_travel_time)

    # display mean travel time
    Total_average_time= df ['Average Travel Time']=df['Trip Duration'].mean()
    print('Total Average Travel Time:', Total_average_time)


    print("\nThis took %s seconds." % (time.time() - Start_Time))
    print('-'*40)


trip_duration_stats(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('\nUser types:\n', user_count)
    try:
        # Display counts of gender
        Gender_Count = df['Gender'].value_counts()
        print('\nBike riders gender split: \n', Gender_Count)

        # Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int (df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('\n Earliest birth year :  ', earliest_birth)
        print('\n Most recent birth year :  ', most_recent_birth)
        print('\n Most common birth year :  ', most_common_birth)
    # dealing with Washington
    except KeyError:
        print('This data is not available for Washington')

    # Display earliest, most recent, and most common year of birth #use max and min


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

user_stats(df)

def display_raw_data(df):
    """The fuction takes the name of the city produced by the get_filters fuction as input and returns the raw data of that city as 5 rows based upon user input.
    """

    print('\nRaw data is available to check... \n')

    # setting counter for the rows
    start_loc = 0

    # collecting user input
    display_rows = input('To View the available raw data in 5 rows: Yes \n').lower()

    # action based on yes
    while display_rows == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        display_rows = input('Do you want to display 5 more rows? yes or no: ').lower()

    # action based on no
    if display_rows == 'no':
        print('\nNo problem')

    # Validating user input
    while display_rows not in ['yes', 'no']:
        print('That\'s invalid choice, pleas type yes or no')
        display_rows = input('To View the available raw data in 5 rows: Yes \n').lower()

display_raw_data(df)

def main():
    while True:
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank You')
            break
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, day, month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)



if __name__ == "__main__":
    main()


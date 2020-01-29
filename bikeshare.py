import time
import datetime
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
        (str) month - number (as a string) of the month to filter by, or "all" to apply no month filter
        (str) day - number (as a string) of the day of week to filter by, or "all" to apply no day filter (days start with Monday as '0')
    """
    #List of possible cities
    cities = ('chicago', 'new york city', 'washington')
    
    #A dictionary mapping months to their corresponding number, or keeping all as all.
    #We are mapping to numbers (as strings) because when sorting the data, we will get the months as numbers
    months = {'all': 'all', 
              'january': '1',
              'february': '2',
              'march': '3',
              'april': '4',
              'may': '5',
              'june': '6'}
    
    #A dictionary mapping days of the week to a corresponding number, which represents the output when the 
    # weekday() method is called on a date in our data
    days = {'all': 'all',
            'sunday': '6',
            'monday': '0',
            'tuesday': '1',
            'wednesday': '2',
            'thursday': '3',
            'friday': '4',
            'saturday': '5'}
    
    print('Hello! Let\'s explore some US bikeshare data!')
   
    #Getting user input for which city's data to pull 
    done = False
    while not done:
        user_city = input('What city would you like to search for? ').lower()
		#Checking to see if input can be mapped to our dictionary
        if user_city in cities:
            city = user_city
            done = True
        #The input could not be mapped, so giving the user a message on appropriate inputs and looping back to get the input again
		else:
            print('I am sorry, I do not recognize that city. \nYour choices are Chicago, New York City, or Washington.')
    
    #Getting user input for which month to filter by (or no filter with the "all" choice)
    done = False
    while not done:
        user_month = input('What month would you like to look at?  You may choose "all". ').lower()
		#Checking to see if input can be mapped to our dictionary
        if user_month in months:
            month = months[user_month]
            done = True
		#Checking to see if the user input an appropriate number corresponding to a month
        elif user_month in months.values(): 
            month = user_month
            done = True
		#The input could not be mapped, so giving the user a message on appropriate inputs and looping back to get the input again
        else:
            print('I am sorry, I do not recognize that month. \nYou can choose a month between January and June by its name or its number, or you may choose "all".')
    
    #Getting user input for which day of the week to filter the day on (0 for Monday...) or "all" for no filter
    done = False
    while not done:
        user_day = input('What day would you like to look at?  You may choose "all". ').lower()
        #Checking to see if input can be mapped to our dictionary
		if user_day in days:
            day = days[user_day]
            done = True
		#Checking to see if the user input an appropriate number corresponding to a day
        elif user_day in days.values():
            day = user_day
            done = True
		#The input could not be mapped, so giving the user a message on appropriate inputs and looping back to get the input again
        else:
            print('I am sorry, I do not recognize that day. \nYou can choose any day of the week or its number (Monday is 0), or you may choose "all".')
    
    #Formatting a division on the screen after calling this function
    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Reading the chosen city's data into a dataframe to be filtered
    initial_df = pd.read_csv(CITY_DATA[city], parse_dates=[1,2])
    
    #Don't filter if the user has chosen "all", otherwise, filter for the chosen month
    if month == 'all':
        df = initial_df
    else:
    #The value of month is a string, but will look like an integer since the "all" choice has been accounted for in the if statement
        df = initial_df[initial_df['Start Time'].dt.month == int(month)]
    
    #Filtering data for the day of the week
    if day != 'all':
        df = df[df['Start Time'].dt.weekday == int(day)]
    
    return df


def time_stats(df, city, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (dataframe) df - filtered dataframe
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - number of the day of week to filter by, or "all" to apply no day filter 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #Using a list of the days of the week to convert the day provided from a number (passed in as a string) to the day's name
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    #Finding the most common month for trips, using the mode method.
    #If the month is filtered, the message changes as the most common month would be the one filtered on
    if month == 'all':
        df['Month'] = df['Start Time'].dt.month
        common_month_num = df['Month'].mode()[0]
        common_month = datetime.date(1900, common_month_num, 1).strftime('%B')
        print('The most popular month to use the bikeshare in {} is {}.'.format(city.title(), common_month))
        #Dropping the column we added to preserve the raw data
        df.drop(columns='Month', inplace=True)
    else:
        common_month = datetime.date(1900, int(month), 1).strftime('%B')
        print('You chose to look at rides in the month of {} in {}.'.format(common_month, city.title()))
        
    #Finding the most common day of the week for trips, using the mode method.
    #If the day is filtered, the message changes as the most common day would be the one filtered on
    if day == 'all':
        df['Day'] = df['Start Time'].dt.weekday
        common_day_num = df['Day'].mode()[0]
        common_day = days[common_day_num]
        print('The most popular day to use the bikeshare in {} is {}.'.format(city.title(), common_day))
        #Dropping the column we added to preserve the raw data
        df.drop(columns='Day', inplace=True)    
    else:
        common_day = days[int(day)]
        print('You chose to look at rides on the day of {} in {}.'.format(common_day, city.title()))
        
    #Finding the most common hour for trips, using the mode method.
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    #The hour is in 24 hour time, so converting to 12 hour time
    if common_hour > 12:
        print('The most popular start hour is at {} pm.'.format(common_hour-12))
    elif common_hour == 12:
        print('The most popular start hour is at {} pm.'.format(common_hour))
    else:
        print('The most popular start hour is at {} am.'.format(common_hour))
    #Dropping the column we added to preserve the raw data
    df.drop(columns='Hour', inplace=True)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    #Formatting a division on the screen after calling this function
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) df - filtered dataframe
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

	start_station_message = 'The most common station to start a trip is the {} station.'
	end_station_message = 'The most common station to end a trip is the {} station.'
	trip_message = 'The most common trip started at {} and ended at {}.'
	
    #Finding the most common start station
    common_start_station = df['Start Station'].mode()[0]
    print(start_station_message.format(common_start_station))

    #Finding the most common end station
    common_end_station = df['End Station'].mode()[0]
    print(end_station_message.format(common_end_station))

    #Finding the most common trip combination of stations
    #Adding a column to the dataframe that concatenates the start and end station
    df['Trip Stations'] = df['Start Station'] + '-----' + df['End Station']
    #Separating the start and end station with the 5 dashes used in the concatenation
    common_trip = df['Trip Stations'].mode()[0].split('-----')
    
	print(trip_message.format(common_trip[0], common_trip[1]))
    #Dropping the column we added to preserve the raw data
    df.drop(columns='Trip Stations', inplace=True)
    
	#Giving calculation time
	print("\nThis took %s seconds." % (time.time() - start_time))
    #Formatting a division on the screen after calling this function
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on how long the bikes were in use and their average trip length.
    Args:
        (dataframe) df - filtered dataframe
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Getting total travel time (in seconds)
    total_trip_seconds = df['Trip Duration'].sum(axis=0)
    total_trip_days = total_trip_seconds / 86400
    #Formatting to display commas and rounded to 2 decimal places
    print('A total of {:,.2f} seconds of trips were taken.'.format(total_trip_seconds))
    print('This is a total of {:,.2f} days of trips!'.format(total_trip_days))
    
    #Getting the average travel time
    average_trip_seconds = df['Trip Duration'].mean(axis=0)
    print('The average trip took {} seconds, or over {} minutes.'.format(average_trip_seconds, int(average_trip_seconds/60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (dataframe) df - filtered dataframe
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    #Getting the total rows of the dataframe to be able to count any blank entries
    total_trips = df.shape[0]
    #Replacing blank entries with NaN
    df.replace('', np.nan, inplace=True)
    
    #Getting the number of user types that took a bikeshare trip.
    
    #Initializing trip_count variable
    trip_count = 0
    #Getting the unique list of user types
    user_types = set(df['User Type'].dropna())
    #Creating a dictionary that counts the number of rows a user type appears in the dataframe
    user_types_count = {user: df[df['User Type'] == user].shape[0] for user in user_types}
    #Printing out the counts for different users
    for user_type in user_types_count:
        print('There were {} trip(s) by a {}.'.format(user_types_count[user_type], user_type))
        trip_count += user_types_count[user_type]
    #Checking for and printing out the number of trips missing information
    if total_trips == trip_count:
        print('All trips had user type information.')
    else:
        print('{} trips were missing user type information.'.format(total_trips-trip_count))
    #Printing a break to the next set of information
    print('-'*40)
    time_stamp_1 = time.time()
    input('Press enter to continue:\n')
    time_stamp_2 = time.time()
    
    #Getting the number of trips taken by different genders
    
    #Reinitializing trip_count variable
    trip_count = 0
    #Using try/except in case Gender column is missing from dataframe
    try:
        genders = set(df['Gender'].dropna())
        gender_count = {gender: df[df['Gender'] == gender].shape[0] for gender in genders}
        for gender in gender_count:
            print('There were {} trips taken by a {}.'.format(gender_count[gender], gender))
            trip_count += gender_count[gender]
        if total_trips == trip_count:
            print('All trips had information about the gender of the user.')
        else:
            print('{} trips were missing gender information.'.format(total_trips-trip_count))
    except:
        print('There is no information for genders for this city.')
    #Printing a break to the next set of information
    print('-'*40)
    time_stamp_3 = time.time()
    input('Press enter to continue:\n')
    time_stamp_4 = time.time()
    
    #Getting the earliest, most recent, and most common birth years from bikeshare trips
    
    #Using try/except in case Birth Year column is missing from dataframe
    try:
        common_year = int(df['Birth Year'].mode()[0])
        early_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        print('The oldest user we have information on was born in {}, while the youngest was born in {}.'.format(early_year, recent_year))
        print('The most common year of birth among users was {}.'.format(common_year))
              
    except:
        print('There is no information for years of birth for this city.')
    total_calc_time = (time.time()-time_stamp_4) + (time_stamp_3 - time_stamp_2) + (time_stamp_1 - start_time)
    print("\nThe calculations took %s seconds." % (total_calc_time))
    print('-'*40)

def raw_data(df):
    """Displays the raw data upon request, 5 rows at a time.
    Args:
        (dataframe) df - filtered dataframe
    """    
    #Getting the total rows of dataframe
    total_rows = df.shape[0]
    #Initializing a row count variable to keep track of which rows to print out
    row_place = 0
    #Changing display settings to be able to see all the columns
    pd.set_option('display.width',100)
    pd.set_option('display.max_columns',15)
    #Looping through rows and printing them out 5 at a time
    while row_place < total_rows:
        print(df[row_place:min(row_place+5, total_rows)])
        row_place += 5
        proceed = input('Press enter to see the next 5 rows or type "quit" to stop: ')
        if proceed == 'quit':
            break
    
    
def main():
    while True:
        #Getting user input and filtering the data appropriately
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        #Outputting desired statistics about time, station, duration, and users
        time_stats(df, city, month, day)
        
        #Pausing to get user input so the screen does not scroll by.
        #Also allows for users to quit if desired
        proceed = input('Press enter to continue, or quit to stop the program.')
        if proceed == 'quit':
            break
        
        #Outputting desired statistics about starting stations, ending stations, and trip combinations
        station_stats(df)
        
        proceed = input('Press enter to continue, or quit to stop the program.')
        if proceed == 'quit':
            break
        
        #Outputting desired statistics about how long trips take
        trip_duration_stats(df)
        
        proceed = input('Press enter to continue, or quit to stop the program.')
        if proceed == 'quit':
            break
        
        #Outputting desired statistics about the user population
        user_stats(df)
        
        #Asking user if they would like to see the raw data they have filtered for
        see_raw_data = input('Would you like to see the raw data [y/n]?')
        if see_raw_data != 'y':
            break
        #Outputting the raw data 5 lines at a time
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

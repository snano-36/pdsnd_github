import time
import pandas as pd
import numpy as np

ny= 'new_york_city.csv'
ch= 'chicago.csv'
wa= 'washington.csv'

#defining variables for reading the csv documents

df_ny = pd.read_csv(ny)
df_ch = pd.read_csv(ch)
df_wa = pd.read_csv(wa)

month_name=['january','february','march','april','may','june', 'July']
month_short_name=['jan', 'feb', 'mar','apr', 'may', 'jun']
day_name = ['monday', 'tuesday', 'wednesday' , 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():


    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city=input("Which City are you interested in? You can coose between New York City, Washington or Chicago!")

    city=city.lower()
    cities = ['ny', 'new york city', 'chicago', 'washington']
    while city in cities:
        print('Great! Let"s take a look at ', city, ' data.')
        break

    else:
        print('Sorry, there is no data available for your selection')
        city = input("Are you interested in another city? - ").lower()



    #_____________month___________

    month=input("Please Select a month by using the full name! Otherwise please type no which means that no specific month will be shown. Hint: Only month January to June are available!-")

    month=month.lower()
    while month in month_name or month == 'no' or month in month_short_name:
        print('You chose:', month)
        break


    else:
        print('Sorry, there is no data available for your selection')
        month = input("Are you interested in another month? Otherwise please type no. - ")

    #____________weekday______________
    day=input("Please Select a day by using the full name! - ")

    day=day.lower()
    while day in day_name or day=='no':
        print('You chose:', day)
        break

    else:
        print('Sorry, there is no data available for your selection')
        day = input("Are you interested in another day? Otherwise please type no.")

    print('-'*40)

    return city, month, day


def load_data(city, month, day):


    if city == 'ny'or city== 'new york city':
        df=pd.DataFrame(df_ny)

    elif city == 'chicago':
        df=pd.DataFrame(df_ch)

    elif city=='washington':
        df=pd.DataFrame(df_wa)


    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    df['Start Hour'] = df['Start Time'].dt.hour

    #For the user it could be quit intereszing to get an impression of how the data set looks like. Therefore he/she will be able to choose the number of rows he/she would like to see

    row_count = 0
    answer ='yes'

    while  (answer =='yes'):
        while (row_count < 100) & (answer=='yes'):


            row_count = int(input('Please type in the number of rows you wish to see from the data set: '))
            print(df.head(row_count))

            if (month in month_name) & (day in day_name) & (row_count < 100):
                df = df.loc[(df['Month'] == month_name.index(month))&(df['Weekday'] == day_name.index(day))]
                answer = input('Would you like see more of the rows in the data set? - yes/no --->').lower()


            elif (month in month_name) & (row_count < 100):
                df = df.loc[df['Month'] == month_name.index(month)]
                answer = input('Would you like see more of the rows in the data set? - yes/no --->').lower()

            elif (day in day_name) & (row_count < 100):

                df = df.loc[df['Weekday'] == day_name.index(day)]
                answer = input('Would you like see more of the rows in the data set? - yes/no --->').lower()

            elif (month not in month_name) & (day not in day_name) & (row_count < 100):
                df.head(row_count)

                answer = input('Would you like see more of the rows in the data set? - yes/no --->').lower()


            else:
                print('Sorry, we ware not able to display more than 100 rows. Let"s continue the statistics.')
                answer = 'no'


    print('Okay, let"s move on with statistics!')


    return (df)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # ---------------- most common month------------------------

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]


    #----------------- most common day of week-------------------

    df['day'] = df['Start Time'].dt.weekday
    popular_day = df['day'].mode()[0]


    # -----------------most common start hour----------------------

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('The most popular month is ', month_name[popular_month])
    print('The most common day of the week ist ', day_name[popular_day])
    print('The most popular hour is ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]


    # most commonly used end station
    popular_end_station=df['End Station'].mode()[0]

    # most frequent combination of start station and end station trip

    df['combined_stations']= df['Start Station']+ ' & ' + df['End Station']
    most_popular_combined_station = df['combined_stations'].mode()[0]

    # print the results
    print('The most popular start station is ', popular_start_station)
    print('The most popular end station is ', popular_end_station)
    print('The most popular trip is', most_popular_combined_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #give a time format to Trip Duration, in this case hours
    df['Trip Duration'] = df['Start Time'].dt.hour


    # caculate the total travel time
    sum_traveltime = df['Trip Duration'].sum()

    # calculate the mean travel time
    mean_traveltime = df['Trip Duration'].mean()

    # print the results
    print('The sum of travel time in hours is :', sum_traveltime)
    print('The mean traveltime in hours is:', mean_traveltime)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    """ForWashington, the user data is limited compared to the one of New York City or Chicago. In case that a user chose Washington, we have to avoid an error of the python programm"""


    try:

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # counts of user types
        count_user_type = df['User Type'].value_counts()
        print('The counts of user types are: \n', count_user_type)

        # counts of gender
        count_gender = df['Gender'].value_counts()
        print('The counts of gender are:\n', count_gender)

        # earliest & most recent year of birth

        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        print('The earliest birth year of all customers is:', earliest_birth_year)
        print('The most recent birth year of all customers is:', recent_birth_year)

        #most common birth year
        most_common_byear = df['Birth Year'].mode()[0]
        print('The most commen birth year of customers is:', most_common_byear)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    #for handeling errors if f.e. no data is available as it is for the column birth year in csv Washington
    except:
        print('Since the data base is limited for this city we cannot show all statistics as we would do for New York City or Chicago!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np
import csv
from collections import Counter
from datetime import datetime

# Initialize lists and counters to store data fields and occurrences for analysis
trip_duration_list, start_station_list, end_station_list = [], [], []
gender_list, user_list, birthyear_list = [], [], []
month_counter, day_counter, hour_counter = Counter(), Counter(), Counter()

# Track the number of raw data entries processed.
raw_data_count = 0

def load_data(city, month_filter, day_filter):
    """
    Load and filter the data for a given city and apply month and day filters.

    Args:
    city (str): The city to analyze (options are 'CHICAGO', 'NEW YORK', 'WASHINGTON').
    month_filter (str): The month to filter by, or 'All' to apply no month filter.
    day_filter (str): The day to filter by, or 'All' to apply no day filter.

    Returns:
    list: A list of filtered data rows based on the given filters.
    """
    CITY_DATA = {'CHICAGO': 'chicago.csv',
                 'NEW YORK': 'new_york_city.csv',
                 'WASHINGTON': 'washington.csv'}

    file_path = CITY_DATA[city]

    # Open and read the CSV file.
    with open(file_path, 'r') as data:
        csv_reader = csv.reader(data)

        # Skip the header row.
        next(csv_reader)

        # Create a list to store filtered data.
        filtered_data = []

        # Loop through each row in the CSV file.
        for line in csv_reader:
            # Extract start time data (at index 1).
            start_time = line[1]

            # Convert the time data string to a datetime object.
            date_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

            # Extract month, day, and hour from the datetime object.
            month = date_time_obj.strftime('%B')
            day = date_time_obj.strftime('%A')
            hour = date_time_obj.strftime('%H')

            # Apply month and day filters.
            if (month_filter == month or month_filter == 'All') and (day_filter == day or day_filter == 'All'):
                # If both filters match (or are not applied), add the row to filtered_data.
                filtered_data.append(line)

    return filtered_data

def calculations(filtered_data):
    """
    Perform calculations and generate statistics based on the filtered data.

    Args:
    filtered_data (list): A list of data points (rows) filtered by month and day.

    Returns:
    None
    """
    if city_filter == 'CHICAGO' or city_filter == 'NEW YORK':
        # For cities with full data available.
        start_time = time.time()  # Start the timer for performance measurement.

        for data_point in filtered_data:
            # Process each data point in the filtered dataset.

            # First index to gather start time data
            filtered_start_time = data_point[1]

            # Third index to gather trip duration data
            float_trip_duration = float(data_point[3])
            trip_duration_list.append(float_trip_duration)

            # Fourth and Fifth index to gather station data
            start_station_list.append(data_point[4])
            end_station_list.append(data_point[5])

            # Sixth index to gather user data
            user_list.append(data_point[6])

            # Seventh index to gather gender data (Only available for these two cities)
            gender_list.append(data_point[7])

            # Eighth index to gather birthyear data (Only available for these two cities)
            birthyear_list.append((data_point[8]))


            # Convert the start time to a datetime object.
            date_time_obj = datetime.strptime(filtered_start_time, '%Y-%m-%d %H:%M:%S')

            # Extract and count occurrences of month, day, and hour.
            filtered_month_point = date_time_obj.strftime('%B')
            filtered_day_point = date_time_obj.strftime('%A')
            filtered_hour_point = date_time_obj.strftime('%H')

            # Update counters with the extracted month, day, and hour.
            month_counter[filtered_month_point] += 1
            day_counter[filtered_day_point] += 1
            hour_counter[filtered_hour_point] += 1

        # Retrieve the most common month, day, and hour from the counters.
        most_common_month = month_counter.most_common(1)[0]
        most_common_day = day_counter.most_common(1)[0]
        most_common_hour = hour_counter.most_common(1)[0]

        end_time = time.time()  # End the timer for performance measurement.

        # Display the most common times and the time taken to compute them.
        print(f"Most Popular Start Month: {most_common_month[0]}, Count: {most_common_month[1]}")
        print(f"Most Popular Start Day: {most_common_day[0]}, Count: {most_common_day[1]}")
        print(f"Most Popular Start Hour: {most_common_hour[0]}, Count: {most_common_hour[1]}")
        print(f"Time to process Data: {end_time-start_time:.4f} seconds\n")

        # Perform calculations for trip duration statistics.
        start_time = time.time()
        sum_trip_duration = sum(trip_duration_list)
        average_trip = np.mean(trip_duration_list)
        end_time = time.time()
        print(f'Total Trip Duration: {sum_trip_duration}, Count {len(trip_duration_list)}')
        print(f'Average Trip Duration {average_trip}')
        print(f"Time to process Trip Data: {end_time-start_time:.4f} seconds\n")

        # Calculate the most popular start and end stations using Pandas.
        start_time = time.time()
        start_station_series = pd.Series(start_station_list)
        start_value_counts = start_station_series.value_counts()
        popular_start_station = start_value_counts.index[0]
        start_occurrences = start_value_counts.iloc[0]

        end_station_series = pd.Series(end_station_list)
        end_value_counts = end_station_series.value_counts()
        popular_end_station = end_value_counts.index[0]
        end_occurrences = end_value_counts.iloc[0]

        # Create a DataFrame with both start and end stations to find the most common combinations.
        stations_df = pd.DataFrame({'start_station': start_station_list, 'end_station': end_station_list})
        station_combinations = stations_df.value_counts().reset_index(name='count')

        # Extract the most common start and end station combination.
        most_common_combination = station_combinations.iloc[0]
        most_common_start_station = most_common_combination['start_station']
        most_common_end_station = most_common_combination['end_station']
        combination_occurrences = most_common_combination['count']
        end_time = time.time()

        print(f'The Most Popular Trip combination begins at: {most_common_start_station}, and ends at: {most_common_end_station}, Count: {combination_occurrences}')
        print(f'Most Popular Start Station: {popular_start_station}, Count: {start_occurrences}')
        print(f'Most Popular End Station: {popular_end_station}, Count: {end_occurrences}')
        print(f'Time to process Station Data: {end_time - start_time:.4f} seconds\n')

        # Calculate gender statistics using Pandas.
        start_time = time.time()
        gender_series = pd.Series(gender_list)
        gender_value_counts = gender_series.value_counts()
        male_occurrences = gender_value_counts.get("Male", 0)
        female_occurrences = gender_value_counts.get("Female", 0)
        end_time = time.time()

        print(f'Gender statistics: \nMale: {male_occurrences} \nFemale: {female_occurrences}')
        print(f'Time to process Gender Data: {end_time - start_time:.4f} seconds\n')

        # Calculate user type statistics using Pandas.
        start_time = time.time()
        user_series = pd.Series(user_list)
        user_value_counts = user_series.value_counts()
        user_occurrences_1 = user_value_counts.get("Subscriber", 0)
        user_occurrences_2 = user_value_counts.get("Customer", 0)
        user_occurrences_3 = user_value_counts.get("Dependent", 0)
        end_time = time.time()

        print(f'User statistics: \nSubscriber: {user_occurrences_1} \nCustomer: {user_occurrences_2} \nDependent: {user_occurrences_3}')
        print(f'Time to process User Data: {end_time - start_time:.4f} seconds\n')

        # Process birth year data and compute statistics.
        start_time = time.time()
        birthyear_series = pd.Series(birthyear_list)
        birthyear_series = pd.to_numeric(birthyear_series, errors='coerce')
        birthyear_value_counts = birthyear_series.value_counts(dropna=True)
        earliest_birthday = birthyear_series.min()
        latest_birthday = birthyear_series.max()
        end_time = time.time()

        print(f'Earliest birthday: {earliest_birthday}, Latest Birthday: {latest_birthday}')

        # Check for the most common birth year, handling NaN values appropriately.
        if len(birthyear_value_counts) == 0:
            print("No valid birth years available.")
        else:
            most_common_birthyear = birthyear_value_counts.index[0]
            birthyear_occurrences = birthyear_value_counts.iloc[0]
            print(f'Most Common Birthyear: {most_common_birthyear}, Count: {birthyear_occurrences}')
            print(f'Time to process Birthyear Data: {end_time - start_time:.4f} seconds\n')

    else:
        # Handle the case for Washington where certain data is not available.
        start_time = time.time()

        for data_point in filtered_data:
            # Process each data point for Washington dataset.

            # First index to gather start time data
            filtered_start_time = data_point[1]

            # Third index to gather trip duration data
            float_trip_duration = float(data_point[3])
            trip_duration_list.append(float_trip_duration)

            # Fourth and Fifth index to gather station data
            start_station_list.append(data_point[4])
            end_station_list.append(data_point[5])

            # Sixth index to gather user data
            user_list.append(data_point[6])

            # Convert start time to datetime object and extract month, day, and hour.
            date_time_obj = datetime.strptime(filtered_start_time, '%Y-%m-%d %H:%M:%S')

            filtered_month_point = date_time_obj.strftime('%B')
            filtered_day_point = date_time_obj.strftime('%A')
            filtered_hour_point = date_time_obj.strftime('%H')

            # Update counters with extracted month, day, and hour.
            month_counter[filtered_month_point] += 1
            day_counter[filtered_day_point] += 1
            hour_counter[filtered_hour_point] += 1

        # Retrieve the most common month, day, and hour from counters.
        most_common_month = month_counter.most_common(1)[0]
        most_common_day = day_counter.most_common(1)[0]
        most_common_hour = hour_counter.most_common(1)[0]

        end_time = time.time()

        # Display the most common times and the time taken to compute them.
        print(f"Most Popular Start Month: {most_common_month[0]}, Count: {most_common_month[1]}")
        print(f"Most Popular Start Day: {most_common_day[0]}, Count: {most_common_day[1]}")
        print(f"Most Popular Start Hour: {most_common_hour[0]}, Count: {most_common_hour[1]}")
        print(f"Time to process Data: {end_time-start_time:.4f} seconds\n")

        # Perform calculations for trip duration statistics.
        start_time = time.time()
        sum_trip_duration = sum(trip_duration_list)
        average_trip = np.mean(trip_duration_list)
        end_time = time.time()
        print(f'Total Trip Duration: {sum_trip_duration}, Count {len(trip_duration_list)}')
        print(f'Average Trip Duration {average_trip}')
        print(f"Time to process Trip Data: {end_time-start_time:.4f} seconds\n")

        # Calculate the most popular start and end stations using Pandas.
        start_time = time.time()
        start_station_series = pd.Series(start_station_list)
        start_value_counts = start_station_series.value_counts()
        popular_start_station = start_value_counts.index[0]
        start_occurrences = start_value_counts.iloc[0]

        end_station_series = pd.Series(end_station_list)
        end_value_counts = end_station_series.value_counts()
        popular_end_station = end_value_counts.index[0]
        end_occurrences = end_value_counts.iloc[0]

        # Create a DataFrame with both start and end stations to find the most common combinations.
        stations_df = pd.DataFrame({'start_station': start_station_list, 'end_station': end_station_list})
        station_combinations = stations_df.value_counts().reset_index(name='count')

        # Extract the most common start and end station combination.
        most_common_combination = station_combinations.iloc[0]
        most_common_start_station = most_common_combination['start_station']
        most_common_end_station = most_common_combination['end_station']
        combination_occurrences = most_common_combination['count']
        end_time = time.time()

        print(f'The Most Popular Trip combination begins at: {most_common_start_station}, and ends at: {most_common_end_station}, Count: {combination_occurrences}')
        print(f'Most Popular Start Station: {popular_start_station}, Count: {start_occurrences}')
        print(f'Most Popular End Station: {popular_end_station}, Count: {end_occurrences}')
        print(f'Time to process Station Data: {end_time - start_time:.4f} seconds\n')

        # Calculate user type statistics using Pandas.
        start_time = time.time()
        user_series = pd.Series(user_list)
        user_value_counts = user_series.value_counts()
        user_occurrences_1 = user_value_counts.get("Subscriber", 0)
        user_occurrences_2 = user_value_counts.get("Customer", 0)
        user_occurrences_3 = user_value_counts.get("Dependent", 0)
        end_time = time.time()

        print(f'User statistics: \nSubscriber: {user_occurrences_1} \nCustomer: {user_occurrences_2} \nDependent: {user_occurrences_3}')
        print(f'Time to process User Data: {end_time - start_time:.4f} seconds\n')


def get_filter():
    """
    Prompt the user to select a city and apply filters for month, day, both, or none.

    Returns:
    tuple: A tuple containing the selected city, month_filter, and day_filter.
    """

    # List of available cities to choose from.
    cities = ["CHICAGO", "NEW YORK", "WASHINGTON"]

    while True:
        # Ask the user to input the city they are interested in.
        city = input("Would you like to see data for Chicago, New York, or Washington?").strip().upper()

        if not city:
            print("Input cannot be empty. Please try again.")
            continue

        if city in cities:
            print(f"Ok, we will explore the data for: {city.capitalize()}")
            break
        else:
            print("Invalid city. Please choose from Chicago, New York, or Washington.")

    # Lists of available months and days for filtering data.
    month_list = ['January', 'February', 'March', 'April', 'May', 'June']
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    while True:
        # Prompt user to decide on applying a filter for time (month, day, both, or none).
        main_filter = input(
            "Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter: ").strip().capitalize()

        if not main_filter:
            print("Input cannot be empty. Please try again.")
            continue

        if main_filter == 'Month':
            day_filter = 'All'  # If filtering by month only, set day_filter to 'All'.

            while True:
                # Prompt user for the specific month.
                month_filter = input(
                    "Which month? January, February, March, April, May, or June: ").strip().capitalize()
                if not month_filter:
                    print("Input cannot be empty. Please try again.")
                elif month_filter in month_list:
                    print(f'Ok, we will explore the data for {month_filter}')
                    print('Calculating the statistics...\n')
                    return city, month_filter, day_filter
                else:
                    print("Invalid month. Please choose a valid month.")

        elif main_filter == 'Day':
            month_filter = 'All'  # If filtering by day only, set month_filter to 'All'.

            while True:
                # Prompt user for the specific day of the week.
                day_input = input("Which day? Please type your response as an integer (e.g., 1=Sunday). ")

                if not day_input:
                    print("Input cannot be empty. Please try again.")
                    continue

                try:
                    # Convert the user's input into an integer.
                    day_number = int(day_input)
                except ValueError:
                    print("Invalid input. Please enter an integer value (1-7).")
                    continue

                if 1 <= day_number <= 7:
                    day_filter = days_of_week[day_number - 1]
                    print(f'Ok, we will filter data by {day_filter}s')
                    print('Calculating the statistics...\n')
                    return city, month_filter, day_filter
                else:
                    print("Invalid day. Please choose a valid day.")

        elif main_filter == 'Both':
            while True:
                # Prompt user for both month and day for filtering.
                month_filter = input(
                    "Which month? January, February, March, April, May, or June: ").strip().capitalize()
                if not month_filter:
                    print("Input cannot be empty. Please try again.")
                elif month_filter in month_list:
                    break
                else:
                    print("Invalid month. Please choose a valid month.")

            while True:
                # Prompt user for the specific day when both filters are applied.
                day_input = input("Which day? Please type your response as an integer (e.g., 1=Sunday). ")

                if not day_input:
                    print("Input cannot be empty. Please try again.")
                    continue

                try:
                    # Convert the user's input into an integer.
                    day_number = int(day_input)
                except ValueError:
                    print("Invalid input. Please enter an integer value (1-7).")
                    continue

                if 1 <= day_number <= 7:
                    day_filter = days_of_week[day_number - 1]
                    print(f'Ok, we will filter data by {month_filter} and {day_filter}s')
                    print('Calculating the statistics...\n')
                    return city, month_filter, day_filter
                else:
                    print("Invalid day. Please choose a valid day.")

        elif main_filter == 'None':
            # No filters applied; set both filters to 'All'.
            day_filter = 'All'
            month_filter = 'All'
            print("No time filter will be applied.")
            print('Calculating the statistics...\n')
            return city, month_filter, day_filter

        else:
            print("Invalid filter. Please choose month, day, both, or none.")


def disp_raw_data(filtered_data, raw_data_count, batch_size=5):
    """
    Display raw data in batches of 5 based on user request.

    Args:
    filtered_data (list): List of filtered data based on user input.
    raw_data_count (int): The current count of displayed raw data batches.
    batch_size (int): The number of data points to display in each batch. Default is 5

    Returns:
    int: Updated raw_data_count after displaying a batch of raw data.
    """
    CITY_DATA = {'CHICAGO': 'chicago.csv',
                 'NEW YORK': 'new_york_city.csv',
                 'WASHINGTON': 'washington.csv'}

    file_path = CITY_DATA[city_filter]

    # Open and read the CSV file
    with open(file_path, 'r') as data:
        csv_reader = csv.reader(data)

        # Convert the csv_reader to a list
        data_list = list(csv_reader)

        # Now you can access specific rows using indexing
        print(data_list[0])  # Print the first row (header)

        # Calculate the start and end index for the current batch
        start_index = raw_data_count * batch_size
        end_index = start_index + batch_size


        # Display data in the current batch
        display_batch(filtered_data, start_index, end_index)

        # Increment count for next batch
        raw_data_count += 1
        return raw_data_count

def display_batch(filtered_data,start_index, end_index):
    """
        Helper function to display a batch of data.

        Args:
            filtered_data (list): List of filtered data based on user input.
            start_index (int): The starting index of the batch.
            end_index (int): The ending index of the batch.
        """

    for i in range(start_index, min(end_index, len(filtered_data))):
        print(filtered_data[i])



def main():
    """
    Main function to run the interactive bikeshare data analysis program.
    """
    while True:
        global city_filter, month_filter, day_filter, raw_data_count

        # Get filters from the user
        city_filter, month_filter, day_filter = get_filter()

        # Load data based on filters
        filtered_data = load_data(city_filter, month_filter, day_filter)

        # Perform calculations on the filtered data
        calculations(filtered_data)

        # Ask the user if they want to view individual trip data
        while True:
            raw_data_input = input('Would you like to view individual trip data? Enter yes or no. ').upper().strip()
            if raw_data_input == 'YES':
                raw_data_count = disp_raw_data(filtered_data, raw_data_count)  # Update raw_data_count
            elif raw_data_input == 'NO':
                break
            else:
                print("Invalid input. Please choose yes or no.")

        # Ask the user if they want to restart the analysis
        while True:
            restart = input("Would you like to restart? Enter yes or no. ").capitalize().strip()
            if restart == 'Yes':
                break
            elif restart == 'No':
                return
            else:
                print('Invalid input. Please choose yes or no. ')



if __name__ == "__main__":
    main()
import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    # Pivot the DataFrame to create a matrix with id_1 as index, id_2 as columns, and car as values
    df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0 (for cells where id_1 and id_2 don't match)
    df = df.fillna(0)

    # Set diagonal values to 0
    for i in df.index:
        df.at[i, i] = 0
    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Define the conditions for car_type
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]

    # Define the corresponding car_type values
    car_types = ['low', 'medium', 'high']

    # Add a new 'car_type' column based on the conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=car_types, right=False)

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys

    return dict(sorted(type_counts.items()))



def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()
    return bus_indexes

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Calculate the average of 'truck' values for each unique 'route'
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()
    return selected_routes



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
     # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Apply the specified logic to modify values
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)
    return matrix

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Combine 'startDay' and 'startTime' to create a 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    # Extract day of the week and hour for start and end timestamps
    df['start_day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['start_hour'] = df['start_timestamp'].dt.hour
    df['end_day_of_week'] = df['end_timestamp'].dt.dayofweek
    df['end_hour'] = df['end_timestamp'].dt.hour

    # Create a boolean column for incorrect timestamps
    incorrect_start_timestamps = ~((df['start_day_of_week'].between(0, 6)) & (df['start_hour'].between(0, 23)))
    incorrect_end_timestamps = ~((df['end_day_of_week'].between(0, 6)) & (df['end_hour'].between(0, 23)))

    # Group by (id, id_2) and check if any start or end timestamp is incorrect for each group
    result_series = df.groupby(['id', 'id_2']).apply(
        lambda x: (incorrect_start_timestamps.loc[x.index] | incorrect_end_timestamps.loc[x.index]).any()
    ).astype(bool)

    return result_series



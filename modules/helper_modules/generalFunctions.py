import numpy as np


def shorten_strings(strings):
    """
    Shortens a list of strings by creating a dictionary of each string mapped to its shortened version.

    Args:
        strings (list): A list of strings.

    Returns:
        dict: A dictionary mapping each string to its shortened version.

    """
    if len(strings) < 2:
        # A single string in list
        the_only_string = strings[0]
        first_character = the_only_string[0]
        return {the_only_string: first_character}

    else:
        shortest_string_length = min([len(string) for string in strings])

        for length in range(1, shortest_string_length):
            short_strings = [string[:length] for string in strings]
            all_unique = len(set(short_strings)) == len(strings)
            if all_unique:
                return {string: short_string for string, short_string in zip(strings, short_strings)}

    # If the method hasn't returned yet, then the minimum length is longer than the shortest string
    # Returning a dictionary of the strings to themselves

    return {string: string for string in strings}


def city_name_to_file_name(city_name):
    """
    Converts a city name to a valid file name by removing special characters and converting to lowercase.

    Args:
        city_name (str): The name of the city.

    Returns:
        str: The city name converted to a valid file name.

    """
    # Remove special characters
    chars_to_remove = '-_ ./|'
    for char in chars_to_remove:
        city_name = city_name.replace(char, '')

    # Convert to lowercase
    city_name = city_name.lower()

    return city_name


def add_intermediate_values(arr, n):
    """
    Adds intermediate values to an array by expanding each element and interpolating in between.

    Args:
        arr (numpy.ndarray): The input array.
        n (int): The number of intermediate values to add between each pair of elements.

    Returns:
        numpy.ndarray: The expanded array with intermediate values.

    """
    # Calculate the number of elements in the expanded array
    expanded_length = (n + 1) * arr.size - n

    # Create an array with the expanded length
    expanded_arr = np.empty(expanded_length)

    # Copy the original values to the expanded array
    expanded_arr[::n + 1] = arr

    # Calculate the intermediate values using linear interpolation
    for i in range(arr.size - 1):
        start = (n + 1) * i
        end = (n + 1) * (i + 1)
        expanded_arr[start + 1:end] = np.linspace(arr[i], arr[i + 1], n + 1, endpoint=False)[1:]

    return expanded_arr

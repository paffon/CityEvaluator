import pandas as pd


def find_closest_string(input_string, string_list):
    """
    Find the closest string to the input string from a given list.

    Args:
        input_string (str): The input string.
        string_list (list): A list of strings to compare against.

    Returns:
        str: The closest string to the input string from the list.
    """
    min_distance = float('inf')
    closest_string = None

    for string in string_list:
        if len(string) != len(input_string):
            # Check if the target string is a substring of the candidate string
            if input_string in string:
                return string
            continue

        distance = sum(ch1 != ch2 for ch1, ch2 in zip(input_string, string))

        if distance < min_distance:
            min_distance = distance
            closest_string = string

    return closest_string


def calc_expenses_in_city(city_costs, expenses_structure, luxury_level, constants):
    """
    Calculate the expenses in a city based on the cost structure and luxury level.

    Args:
        city_costs (dict): The cost data for the city.
        expenses_structure (dict): The structure of expenses.
        luxury_level (str): The luxury level.
        constants (dict): Constants used in the calculation.

    Returns:
        dict: The calculated expenses in the city.
    """
    total_category_name = constants['categorical values']['total category']

    columns_names = constants['columns names']
    low_range_name = columns_names['low cost estimation']
    expected_cost_name = columns_names['normal cost estimation']
    high_range_name = columns_names['high cost estimation']

    categorical_values = constants['categorical values']
    low_luxury_level = categorical_values['low luxury']
    med_luxury_level = categorical_values['medium luxury']
    high_luxury_level = categorical_values['high luxury']

    result = {total_category_name: {expected_cost_name: 0, low_range_name: 0, high_range_name: 0}}

    for category, elements in expenses_structure.items():
        result[category] = {expected_cost_name: 0, low_range_name: 0, high_range_name: 0}
        for element, qty_range in elements.items():
            qty = {
                low_luxury_level: min(qty_range),
                med_luxury_level: sum(qty_range) / len(qty_range),
                high_luxury_level: max(qty_range),
            }[luxury_level]
            closest_match = find_closest_string(element, list(city_costs[category].keys()))

            element_data = city_costs[category][closest_match]

            cost = round(element_data[expected_cost_name])
            if element_data.get(low_range_name, cost) is not None:
                low_range = round(element_data.get(low_range_name, cost))
            else:
                low_range = cost
            if element_data.get(high_range_name, cost) is not None:
                high_range = round(element_data.get(high_range_name, cost))
            else:
                high_range = cost

            result[category][low_range_name] += low_range * qty
            result[category][expected_cost_name] += cost * qty
            result[category][high_range_name] += high_range * qty

            result[total_category_name][low_range_name] += low_range * qty
            result[total_category_name][expected_cost_name] += cost * qty
            result[total_category_name][high_range_name] += high_range * qty

    return result


def generate_expenses_data_frame(countries_data, expenses_structure, cities_costs, constants):
    """
    Generate an expenses data frame based on the given data.

    Args:
        countries_data (dict): Data for different countries.
        expenses_structure (dict): The structure of expenses.
        cities_costs (dict): Costs data for different cities.
        constants (dict): Constants used in the calculation.

    Returns:
        pandas.DataFrame: The generated expenses data frame.
    """
    columns_names = constants['columns names']
    low_range_name = columns_names['low cost estimation']
    expected_cost_name = columns_names['normal cost estimation']
    high_range_name = columns_names['high cost estimation']
    country_column = columns_names['country']
    city_column = columns_names['city']
    expense_category_column = columns_names['expense category']
    luxury_level_column = columns_names['luxury']

    categorical_values = constants['categorical values']
    low_luxury_level = categorical_values['low luxury']
    med_luxury_level = categorical_values['medium luxury']
    high_luxury_level = categorical_values['high luxury']

    rows = []

    for country, country_data in countries_data.items():
        for city in country_data['cities']:
            city_costs = cities_costs[city]

            for luxury_level in [low_luxury_level, med_luxury_level, high_luxury_level]:

                cost_of_living = calc_expenses_in_city(city_costs, expenses_structure, luxury_level, constants)
                for expense_category, expense_data_per_category in cost_of_living.items():
                    new_row = [country, city, expense_category, luxury_level,
                               expense_data_per_category[low_range_name],
                               expense_data_per_category[expected_cost_name],
                               expense_data_per_category[high_range_name]]
                    rows.append(new_row)

    header = [
        country_column,
        city_column,
        expense_category_column,
        luxury_level_column,
        low_range_name,
        expected_cost_name,
        high_range_name
    ]

    df = pd.DataFrame(data=rows, columns=header)

    return df

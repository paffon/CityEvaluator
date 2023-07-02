import os

from modules.helper_modules import generalFunctions as gF
from modules.helper_modules import fileService as fS


def generate_replacement_dict():
    """
    Generate a dictionary of replacement characters.

    Returns:
        dict: A dictionary mapping characters to their replacement values.
    """
    replacements = {'â': '€',  # Replace â with €
                    '¬': ' '}  # Replace ¬ with space

    for i in range(10, 1, -1):
        replacements[' ' * i] = ' '  # Replace multiple spaces with a single space

    replacements['\t\t'] = '\t'  # Replace multiple tabs with a single tab

    return replacements


def clean_txt_file(content):
    """
    Clean the content of a text file by replacing characters according to the replacement dictionary.

    Args:
        content (str): The content of the text file.

    Returns:
        str: The cleaned content of the text file.
    """
    replacements = generate_replacement_dict()

    for k, v in replacements.items():
        content = content.replace(k, v)

    return content


def extract_city_data(file_path):
    """
    Extract city data from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of lists representing the extracted city data.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    content = clean_txt_file(content)

    lines = content.split('\n')

    stripped_lines = [line.strip() for line in lines]

    split_lines = [line.split('\t') for line in stripped_lines if line.split('\t') != ['']]

    return split_lines


def split_lines_to_raw_dict(lines, constants):
    """
    Convert the extracted city data lines into a dictionary.

    Args:
        lines (list): The extracted city data lines.
        constants (dict): A dictionary containing constant values and column names.

    Returns:
        dict: A dictionary representing the city data.
    """
    normal_estimation_name = constants['columns names']['normal cost estimation']
    range_name = constants['categorical values']['range']

    items_dict = {}
    current_category = ''

    for line in lines:
        if 'Edit' in line:
            current_category = line[0]
            items_dict[current_category] = {}
        else:
            name = line[0]
            cost = line[1]
            cost_range = line[2] if len(line) == 3 else None
            items_dict[current_category][name] = {normal_estimation_name: cost, range_name: cost_range}

    return items_dict


def cost_str_to_float(cost):
    """
    Convert a cost string to a float.

    Args:
        cost (str): The cost string.

    Returns:
        float: The converted cost as a float.
    """
    new_cost = cost.replace(' €‚ ', '').replace(',', '').replace(' €‚', '')
    if new_cost == '?':
        return 0
    return float(new_cost)


def get_low_high_range(range_str):
    """
    Extract the low and high range values from a range string.

    Args:
        range_str (str): The range string.

    Returns:
        tuple: A tuple containing the low and high range values.
    """
    if range_str:
        split_range = range_str.split('-')
        low_range_str = split_range[0].replace(',', '')
        high_range_str = split_range[1].replace(',', '')

        return float(low_range_str), float(high_range_str)
    else:
        return None, None


def parse_txt_file(file_path, constants):
    """
    Parse a text file containing city data.

    Args:
        file_path (str): The path to the text file.
        constants (dict): A dictionary containing constant values and column names.

    Returns:
        dict: A dictionary representing the processed city data.
    """
    columns_names = constants['columns names']
    low_estimation_name = columns_names['low cost estimation']
    normal_estimation_name = columns_names['normal cost estimation']
    high_estimation_name = columns_names['high cost estimation']
    range_name = constants['categorical values']['range']

    lines = extract_city_data(file_path)

    raw_data_dict = split_lines_to_raw_dict(lines, constants)

    processed_data_dict = {}

    for category, products in raw_data_dict.items():
        processed_products = {}

        for product, product_data in products.items():
            cost_float = cost_str_to_float(product_data[normal_estimation_name]) if normal_estimation_name in product_data else 0.0
            low_range, high_range = get_low_high_range(product_data[range_name])

            product_data[low_estimation_name] = low_range
            product_data[normal_estimation_name] = cost_float
            product_data[high_estimation_name] = high_range

            product_data.pop(range_name)

            processed_products[product] = product_data

        processed_data_dict[category] = processed_products

    return processed_data_dict


def get_cities_costs(data_folder, countries_data, constants):
    """
    Get the costs of cities in various countries.

    Args:
        data_folder (str): The folder containing the city data.
        countries_data (dict): A dictionary containing country data.
        constants (dict): A dictionary containing constant values and column names.

    Returns:
        dict: A dictionary representing the costs of cities in various countries.
    """
    cities_costs = {}

    for country, country_data in countries_data.items():
        cities_in_country = country_data['cities']

        dict_city_name_to_file_name = {city: gF.city_name_to_file_name(city) + '.txt' for city in cities_in_country}
        files_that_should_be_in_folder = set(dict_city_name_to_file_name.values())

        cities_folder_in_country = os.path.join(data_folder, country.lower(), 'cities')
        files_actually_in_folder = set(fS.get_files_in_folder(cities_folder_in_country, extension='.txt'))

        # Check if there are any missing files
        missing_files = files_that_should_be_in_folder - files_actually_in_folder
        if missing_files:
            printable_missing_files = '\n\t'.join(list(missing_files))
            raise LookupError(f'The following files are missing for {country}:\n\t{printable_missing_files}')

        # Check if there are any extra files
        extra_files = files_actually_in_folder - files_that_should_be_in_folder
        if extra_files:
            printable_extra_files = '\n\t'.join(list(extra_files))
            print(f'The following extra files were found for {country}:\n\t{printable_extra_files}')

        for city, file_name in dict_city_name_to_file_name.items():
            file_path = os.path.join(cities_folder_in_country, file_name)
            city_costs = parse_txt_file(file_path, constants)
            cities_costs[city] = city_costs

    return cities_costs

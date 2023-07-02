import os

from modules.helper_modules import fileService as fS
from modules.core_modules import netSalaries as nS
from modules.core_modules import citiesData as cD
from modules.core_modules import calcExpenses as cE
from modules.core_modules import visuals


def get_director(ancestor):
    """
    Retrieves the director information from a JSON file and determines the paths to associated folders.

    Args:
        ancestor (str): The name of the ancestor directory to start the search from.

    Returns:
        dict: A dictionary containing the director information and associated folder paths.

    Example:
        ancestor_name = "my_ancestor"
        director_info = get_director(ancestor_name)
        print(director_info)

    """
    path_to_director = fS.determine_path(ancestor, "director.json", "file")
    director = fS.read_json_file(path_to_director)

    folders = director['folders']

    for folder_type, folder_name in folders.items():
        folders[folder_type] = fS.determine_path(ancestor, folder_name, 'folder')

    return director


def main():
    project_name = "CityEvaluator"

    director = get_director(project_name)

    # save folders names in variables
    folders = director['folders']
    constants = director['constants']
    data_folder = folders['data']
    results_folder = folders['results']

    # Save column names in variables
    columns_names = constants['columns names']
    net_salary_column = columns_names['net salary']
    country_column = columns_names['country']
    code_column = columns_names['country code']
    city_column = columns_names['city']
    location_column = columns_names['location']
    luxury_column_name = columns_names['luxury']
    expense_category_column = columns_names['expense category']
    low_range_name = columns_names['low cost estimation']
    expected_cost_name = columns_names['normal cost estimation']
    high_range_name = columns_names['high cost estimation']

    # Save calculation options in variables
    costs_or_left = director['options']['what to calculate']
    remaining = director['options']['remaining']
    costs = director['options']['costs']

    ##########################
    # PROCESSING STARTS HERE #
    ##########################

    # Read countries data and user data
    countries = fS.read_json_file(os.path.join(data_folder, 'countries_income_tax_data.json'))
    user_data = fS.read_json_file(os.path.join(data_folder, 'user_data.json'))

    # Get cities costs data
    cities_costs = cD.get_cities_costs(data_folder, countries, constants)

    # Generate expenses per city DataFrame
    expenses_structure = user_data['expenses']
    expenses_df = cE.generate_expenses_data_frame(countries, expenses_structure, cities_costs, constants)

    # Calculate net salaries for each country
    net_salaries = nS.get_net_salaries(countries, user_data)

    # Add net salary column to DataFrame
    expenses_df[net_salary_column] = expenses_df[country_column].apply(
        lambda country: net_salaries[country])

    # Add a location column to DataFrame
    expenses_df[code_column] = expenses_df[country_column].apply(lambda country: countries[country][code_column])
    expenses_df[location_column] = expenses_df[city_column] + ', ' + expenses_df[code_column]

    if costs_or_left == costs:  # Visualize costs, nothing needs to be done
        pass
    elif costs_or_left == remaining:  # Visualize money remaining after costs
        numerical_columns = [low_range_name, expected_cost_name, high_range_name]
        # Subtract net_salary from each column in numerical_columns
        expenses_df[numerical_columns] = -expenses_df[numerical_columns].sub(expenses_df.net_salary, axis=0)
    else:
        raise ValueError(f'Unknown value for costs/remaining: {costs_or_left}')

    expenses_df = expenses_df.drop(
        columns=[country_column, city_column, code_column, net_salary_column])

    # kind can be 'errors' or 'special'
    visuals.visualize('errors',
                      df=expenses_df,
                      costs_or_left=costs_or_left,
                      category='Total',
                      director=director,
                      hue=luxury_column_name)


if __name__ == "__main__":
    main()

def calculate_net_salary(brackets, percentages, gross_salary):
    """
    Calculates the net salary based on tax brackets and the gross salary.
    Args:
        brackets (list): A list of tax brackets representing the upper limits of income ranges.
        percentages (list): A list of corresponding tax percentages for each bracket.
        gross_salary (float): The gross salary amount.
    Returns:
        float: The net salary after deducting taxes.
    Example:
        brackets = [1000, 2000, 3000]
        percentages = [0.1, 0.2, 0.3] <- meaning 10%, 20%, 30% tax
        gross_salary = 2500
        net_salary = calculate_net_salary(brackets, percentages, gross_salary)
        print(net_salary)
    """
    tax_brackets = list(zip(brackets, percentages))
    tax_brackets.sort(key=lambda x: x[0])
    net_salary = gross_salary

    for i in range(len(tax_brackets)):
        bracket, percentage = tax_brackets[i]
        upper_limit = tax_brackets[i + 1][0] if i + 1 < len(tax_brackets) else float('inf')

        if gross_salary > bracket:
            taxable_amount = min(gross_salary - bracket, upper_limit - bracket)
            tax_amount = taxable_amount * percentage
            net_salary -= tax_amount

    return net_salary


def get_net_salaries(countries_data, user_data):
    """
    Calculates the net salaries for different countries based on user and tax bracket data.
    Args:
        countries_data (dict): A dictionary containing the tax bracket data for different countries.
        user_data (dict): A dictionary containing the user's data, including gross salary.
    Returns:
        dict: A dictionary mapping countries to their respective net salaries.
    Example:
        countries_data = {
            'Country A': {
                'tax brackets': {
                    'amount brackets': [1000, 2000],
                    'percentage brackets': [0.1, 0.2] <- meaning 10%, 20% tax
                }
            },
        }
        user_data = {'gross monthly salary [eur]': 2500}
        net_salaries = get_net_salaries(countries_data, user_data)
        print(net_salaries)
    """
    gross_salary = user_data['gross monthly salary [eur]']

    net_salaries = {}

    for country, country_data in countries_data.items():
        country_brackets_yearly = country_data['tax brackets']['amount brackets']
        country_brackets_monthly = [bracket / 12 for bracket in country_brackets_yearly]
        country_percentage = country_data['tax brackets']['percentage brackets']
        net_salary_in_country = calculate_net_salary(country_brackets_monthly, country_percentage, gross_salary)
        net_salaries[country] = net_salary_in_country

    return net_salaries

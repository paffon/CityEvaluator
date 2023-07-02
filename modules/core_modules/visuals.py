import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from modules.helper_modules import generalFunctions as gF

def visualize(kind, **kwargs):
    """
    Create a visualization based on the specified kind.

    Args:
        kind (str): Specifies the type of visualization to create.
        **kwargs: Additional keyword arguments for the specific visualization.

    Raises:
        ValueError: If an unknown visualization kind is specified.
    """
    df = kwargs.get('df')  # DataFrame containing the data
    costs_or_left = kwargs.get('costs_or_left')  # Specifies whether to visualize 'costs' or 'left' values
    category = kwargs.get('category')  # Category to filter the dataframe
    director = kwargs.get('director')  # Dictionary containing constant values and column names
    hue = kwargs.get('hue')  # Column to determine the hue of the visualization

    if kind == 'errors':
        # Create a visualization with error bars
        visualize_errors(df, costs_or_left, director)

    elif kind == 'special':
        # Create a special visualization with bars and different categories/colors
        visualize_special(df, costs_or_left, category, director, hue)

    else:
        raise ValueError("Unknown visualization kind: {kind}.")


def visualize_errors(df, costs_or_left, director, category=None, luxury_level=None):
    """
    Create a visualization with error bars.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        costs_or_left (str): Specifies whether to visualize 'costs' or 'left' values.
        director (dict): Dictionary containing constant values and column names.
        category (str, optional): Category to filter the dataframe. Defaults to None.
        luxury_level (str, optional): Luxury level to filter the dataframe. Defaults to None.
    """
    constants = director['constants']
    columns_names = constants['columns names']
    expense_category_column = columns_names['expense category']
    location_column = columns_names['location']
    low_range_name = columns_names['low cost estimation']
    expected_cost_name = columns_names['normal cost estimation']
    high_range_name = columns_names['high cost estimation']
    luxury_column = columns_names['luxury']
    total_category_name = constants['categorical values']['total category']
    medium_luxury_level = constants['categorical values']['medium luxury']

    costs = director['options']['costs']

    category = total_category_name if category is None else category
    luxury_level = medium_luxury_level if luxury_level is None else luxury_level

    # Filter the dataframe based on category and luxury_level
    filtered_df = df[(df[expense_category_column] == category) & (df[luxury_column] == luxury_level)]
    # Sort the dataframe based on the 'normal' column, ascending or descending based on costs_or_left
    sorted_df = filtered_df.sort_values(by=expected_cost_name, ascending=costs_or_left == costs)

    # Extract relevant data for plotting
    locations = sorted_df[location_column]
    low_estimations = sorted_df[low_range_name]
    normal_estimations = sorted_df[expected_cost_name]
    high_estimations = sorted_df[high_range_name]

    x_pos = range(len(locations))

    # Create the figure and axes objects
    fig, ax = plt.subplots()

    # Determine the direction of error bars based on costs_or_left
    invert = 1 if costs_or_left == costs else -1

    # Plot the error bars
    ax.errorbar(x_pos, normal_estimations,
                yerr=[invert * (normal_estimations - low_estimations),
                      invert * (high_estimations - normal_estimations)], fmt='o', capsize=4)

    # Set the x-axis tick positions and labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(locations, rotation=45)

    # Set the plot title based on costs_or_left, category, and luxury_level
    ax.set_title(f'{costs_or_left}\n{expense_category_column}: {category}\n{luxury_column}: {luxury_level}')

    # Set the y-axis ticks
    y_ticks = ax.get_yticks()
    y_ticks = gF.add_intermediate_values(y_ticks, 1)
    ax.set_yticks(y_ticks)

    # Enable the grid
    ax.grid(True)

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


def visualize_special(df_original, costs_or_left, category, director, column_for_hue):
    """
    Create a special visualization with bars and different categories/colors.

    Args:
        df_original (pd.DataFrame): DataFrame containing the data.
        costs_or_left (str): Specifies whether to visualize 'costs' or 'left' values.
        category (str): Category to filter the dataframe.
        director (dict): Dictionary containing constant values and column names.
        column_for_hue (str): Column to determine the hue of the visualization.
    """
    constants = director['constants']
    columns_names = constants['columns names']
    expense_category_column = columns_names['expense category']
    location_column = columns_names['location']
    low_range_name = columns_names['low cost estimation']
    expected_cost_name = columns_names['normal cost estimation']
    high_range_name = columns_names['high cost estimation']
    luxury_column = columns_names['luxury']

    medium_luxury_level = constants['categorical values']['medium luxury']

    costs = director['options']['costs']

    # Filter the dataframe based on the expense category
    df_filtered = df_original.loc[df_original[expense_category_column] == category]
    df_filtered = df_filtered.drop(columns=expense_category_column)

    # Melt the dataframe to combine the three cost estimation columns into a single column
    df_melted = pd.melt(df_filtered,
                        id_vars=[location_column, luxury_column],
                        value_vars=[low_range_name,
                                    expected_cost_name,
                                    high_range_name],
                        var_name=expense_category_column,
                        value_name=costs_or_left)

    # Check if the user wants the hue to be lined to the luxury level or to the costs estimation level
    if column_for_hue is None or column_for_hue == luxury_column:
        column_for_hue = luxury_column
        other_category = expense_category_column
    else:
        column_for_hue = expense_category_column
        other_category = luxury_column

    # Define colors based on the column_for_hue
    colors = {
        luxury_column: ['#CD7F32', '#C0C0C0', '#FFD700'],
        expense_category_column: ['#88d669', '#5882f5', '#f03737']
    }[column_for_hue]

    # Sort the dataframe based on specified columns
    df_mediums = df_melted.loc[
        (df_melted[luxury_column] == medium_luxury_level) &
        (df_melted[expense_category_column] == expected_cost_name)
    ].drop(columns=[luxury_column, expense_category_column])
    df_mediums = df_mediums.sort_values(by=costs_or_left, ascending=costs_or_left == costs)
    order = list(df_mediums[location_column])

    # Create the bar plot using seaborn's catplot
    bar = sns.catplot(x=location_column, y=costs_or_left,
                      hue=column_for_hue,
                      data=df_melted, kind="bar", palette=sns.color_palette(colors),
                      legend=False,
                      order=order
                      )
    bar.set(title=f'{costs_or_left}\nError bars: {other_category}')
    bar.set(xlabel=None)
    bar.set(ylabel=None)
    bar.set()

    # Add a dense grid
    bar.ax.set_xticklabels(bar.ax.get_xticklabels(), rotation=45, ha='center', fontsize=8)
    bar.ax.set_yticklabels(bar.ax.get_yticklabels(), fontsize=8)
    bar.ax.xaxis.grid(True, linestyle='-', linewidth=0.5)
    bar.ax.yaxis.grid(True, linestyle='-', linewidth=0.5)

    plt.legend(loc='upper left' if costs_or_left == costs else 'upper right', title=column_for_hue)

    # Display the plot
    plt.show()

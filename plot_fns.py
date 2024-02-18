import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('dark_background')

def plot_top_n(df, n, x_col, y_col, x_label=None, y_label=None, title=None):
    """Plot the top n items in a dataframe as a bar chart.
    
    Args:
    - df: the dataframe to plot
    - n: the number of items to plot
    - x_col: the column to plot on the x-axis
    - y_col: the column to plot on the y-axis
    - x_label: the label for the x-axis
    - y_label: the label for the y-axis
    """
    plt.bar(df[x_col][:n], df[y_col][:n])

    if y_label:
        plt.ylabel(y_label)
    else:
        plt.ylabel(y_col.replace('_', ' ').title())

    if not x_label:
        x_label = x_col.replace('_', ' ').title()

    if title:
        plt.title(title)
    else:
        plt.title(f'Top {n} {x_label}s')

    plt.show()

def plot_time_series(df, x_col, y_col, x_label=None, y_label=None, title=None, rotate_x_labels=False):
    """Plot a time series from a dataframe.
    
    Args:
    - df: the dataframe to plot
    - x_col: the column to plot on the x-axis
    - y_col: the column to plot on the y-axis
    - x_label: the label for the x-axis
    - y_label: the label for the y-axis
    """
    plt.plot(df[x_col], df[y_col])


    if not y_label:
        y_label = y_col.replace('_', ' ').title()
    
    plt.ylabel(y_label)
    
    if rotate_x_labels:
        plt.xticks(rotation=90)

    if title:
        plt.title(title)
    else:
        plt.title(f'{y_label} Over Time')

    plt.show()
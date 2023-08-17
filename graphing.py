'''graphing.py
Takes in a Stats object and performs the required graphs
Dominic Bellido
Climate Media Research
Summer 2023
'''

#import statements
import numpy as np
import data
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

class Graphing:
    def __init__(self, stats_object):

        self.stats = stats_object
        self.df = self.stats.get_data()
        # Make plot font sizes legible
        plt.rcParams.update({'font.size': 15})

    def set_stats(self, new_stats):
        '''Method that re-assigns the instance variable `stats` with the parameter.
        Convenience method to change the stats_object used in an analysis without having to create a new
        Stats object.

        Parameters:
        -----------
        new_stats: Stats object. Contains all data samples and variables in a dataset.
        '''
        self.stats = new_stats
        self.df = self.stats.get_data() # update the dataframe

    def show(self):
        '''Simple wrapper function for matplotlib's show function.

        (Does not require modification)
        '''
        plt.show()

    def over_time(self, ax, col_list, instance=None, num=False, xlabel=None, ylabel=None, title=None, color='blue', dotsize=13):
        # takes in the desired column list, desired instance variable (AKA Yes or No, White or Black, etc.)

        years = list(map(int, self.df['Year'].unique())) # get an unordered list of years
        years.sort() # sort them in ascending order

        var_list = []
        for year in years: # go through each year, get the number of variable instances per year
            holding = []

            for col in col_list:
                if num==False: # dealing with categorical data
                    holding.append((self.df.loc[(self.df['Year'] == str(year)) & (self.df[col] == instance)]).shape[0])
                else: # dealing with numerical data
                    self.stats.clean_numbers([col])
                    self.df = self.stats.get_data()
                    holding.append((self.df.loc[(self.df['Year'] == str(year)) & (self.df[col].astype(float) > 0)]).shape[0])

            var_list.append(sum(holding))

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.scatter(years, var_list, s=dotsize, color=color) # get the points
        ax.plot(years, var_list, color=color, label=instance) # get the connecting line

    def scatter(self, ax, col, xlabel=None, ylabel=None, title=None, color='blue', dotsize='10'):

        self.stats.clean_numbers([col])
        
        self.df = self.stats.get_data()
        y = self.df[col].astype(int).tolist()
        x = np.linspace(0, self.df[col].shape[0], self.df[col].shape[0])

        ax.scatter(x, y, color=color)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

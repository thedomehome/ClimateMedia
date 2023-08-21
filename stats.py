'''stats.py
Reads CSV files into dictionaries, arranges all data into pandas dataframe for stats tabluation
Dominic Bellido
Climate Media Research
Summer 2023
'''

#import statements
import scipy
import numpy as np
import data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


class Stats:
    def __init__(self, list_of_csvfiles=None, film_names = None):
        
        self.filelist = list_of_csvfiles
        self.film_names = film_names
        self.headers = []
        self.headers2col = {}
        self.df = None

        self.dict_list = self.file_convert(self.filelist) # convert all of the input csv files into a list of dictionaries
        self.df = self.read_dicts()

        self.nominal = ['Year', 'Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q17', 'Q18','Q28', 'Q29', 'Q35', 'Q35', 'Q36', 'Q37', 'Q38', 'Q40', 'Q41', 'Q42', 'Q43', 'Q44', 'Q45', 'Q46', 'Q47', 'Q48', 'Q49', 'Q50', 'Q51', 'Q52', 'Q53', 'Q54', 'Q55', 'Q56', 'Q57', 'Q58', 'Q59', 'Q60', 'Q61', 'Q62', 'Q63', 'Q64', 'Q65', 'Q66', 'Q67', 'Q68', 'Q69', 'Q70', 'Q71', 'Q72', 'Q73', 'Q74', 'Q75', 'Q76', 'Q77', 'Q78', 'Q79' ,'Q80', 'Q81', 'Q82', 'Q83', 'Q84', 'Q85', 'Q86', 'Q87', 'Q88', 'Q89', 'Q90', 'Q91', 'Q92', 'Q93', 'Q94', 'Q95', 'Q96', 'Q97', 'Q98', 'Q99', 'Q100', 'Q101', 'Q102', 'Q103', 'Q104', 'First Director Name', 'First Director Gender', 'Second Director Name', 'Second Director Gender', 'First Writer Name', 'First Writer Gender', 'Second Writer Name', 'Second Writer Gender', 'Third Writer Name', 'Third Writer Gender', 'Fourth Writer Name', 'Fourth Writer Gender', 'Fith Writer Name', 'Fifth Writer Gender', 'Sixth Writer Name', 'Sixth Writer Gender', 'Stars', 'Director', 'Certificate', 'Genre','Superhero', 'Marvel or DC', 'Theatrical Distributor', 'Maximum Theaters', 'Theatrical Engagements', 'Category' ]
        self.continuous = ['Q13', 'Q14', 'Q15', 'Q16','Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q30', 'Q31' ,'Q32', 'Q33', 'Q34', 'First Director Age When the Film Was Released', 'Second Director Age When the Film Was Released', 'First Writer Age When the Film Was Released', 'Second Writer Age When the Film Was Released', 'Third Writer Age When the Film Was Released', 'Fourth Writer Age When the Film Was Released', 'FIfth Writer Age When the Film Was Released', 'Sixth Writer Age When Film Was Released', 'Worldwide BO Gross', 'Number of votes', 'Runtime (minutes)', 'Gross Domestic Box Office (USD)', 'Budget (USD)', 'Rating', 'Number of SAG Nominations', 'Number of SAG Wins', 'Number of Oscar Nominations', 'Number of Oscar Wins', 'Combined Number of SAG & Oscar Nominations']

        pass

    def file_convert(self, file_list):
        #spits out a list containing all of the dictionaries from the input csv files
        
        holding_list = []
        count = 0
    
        for file in file_list:

            leftovers = self.film_names.copy()
            file_dict = {}

            csv_data = data.Data(file) # turn into data object
            head = csv_data.get_headers() # get headers, to form new headers list and dict

            if 'Title' in self.headers: #weed out the movie title columns
                head.remove('Title')
                for i in range(len(head)):
                    self.headers.append(head[i])
                    self.headers2col[head[i]] = count
                    count+=1
            else:
                for i in range(len(head)):
                    self.headers.append(head[i])
                    self.headers2col[head[i]] = count
                    count += 1
            
            data_mat = csv_data.get_all_data() #get the entire data matrix array

            for i in range(data_mat.shape[0]): # firsst pass at transfering data from csv to dicts
                index_film = data_mat[i,0]

                if (index_film in self.film_names) and (index_film not in file_dict):
                    leftovers.remove(index_film)
                    file_dict[index_film] = data_mat[i, 1:].tolist()
            
            if len(leftovers) != 0:
                print(file, ' leftovers: ',leftovers)
                for film in leftovers:
                    file_dict[film] = np.zeros(data_mat.shape[1]-1).tolist()

            holding_list.append(file_dict)
        
        return holding_list # list of dictionaries
    

    def read_dicts(self):
        # husks each dictionary and orders it into a final array, result is a pandas dataframe
        df1 = pd.DataFrame.from_records(self.dict_list)

        titles = list(df1.columns)# save the movie names as its own column
        
        df1 = df1.explode(titles).T #explode the lists to fill up the pandas dataframe

        df1.columns = self.get_headers()

        return df1

    # getter functions
    def get_data(self):
        # returns a copy of the pandas dataframe
        return self.df.copy()
    

    def get_headers(self): # gets the headers of the data frame
        if 'Title' in self.headers:
            self.headers.remove('Title') # in case this pesky string slipped through, only for pandas implementation
        return self.headers


    def get_col_index(self, header):
        return self.headers2col.get(header)-1
    

    def get_dict_list(self):
        return self.dict_list # get the list of csv dictionaries created
    
    
    def replace(self, df, col, to_be_replaced, replacement):
        # takes a single column and replaces whatever with the desired replacement
        df[col].replace(to_be_replaced, replacement, regex=True, inplace=True)


    def clean_numbers(self, df, col_list):
        for col in col_list:
            self.replace(df, col, ',', '')
            self.replace(df, col, '', 0)

    
    def percent_pass(self, total_col_list, pass_col=None, total_instance=None, pass_instance=None):
            # gets a dataframe of requested columns using the prefered instance variable (Yes, No, Black, White, etc)
            # calculates percentage of films from the total col list that pass the pass_col
      
        data_toBeCombined = []

        for col in total_col_list: # for each question , gather the data to be combined
            if col in self.nominal:                 
                df1 = self.df.loc[(self.df[col] == total_instance)] # get the sliced dataframe
            elif col in self.continuous:
                self.clean_numbers(self.df, [col])
                self.df[col].fillna(0)

                if total_instance=='No':
                    df1 = self.df.loc[(self.df[col].astype(int) == 0)]
                elif total_instance=='Yes':
                    df1 = self.df.loc[(self.df[col].astype(int) > 0)]
                else: # will default to passing a metric question (numbers are greater than 0)
                    df1 = self.df.loc[(self.df[col].astype(int) > 0)]
                
            data_toBeCombined.append(df1)
        
        total_data = pd.concat(data_toBeCombined) #combine the dataframes
        total_data = total_data.drop_duplicates(keep='first')


        if (pass_col is None) and (pass_instance is None): #only answer the total column
            count = total_data.shape[0]
            return f'{count} / {self.df.shape[0]}, {(count/self.df.shape[0])*100:.3f}%'


        if pass_col in self.nominal:
            count = total_data.loc[total_data[pass_col] == pass_instance].shape[0] # count how many films pass 

        elif pass_col in self.continuous:
            total_data[pass_col].replace('', 0, inplace=True)
            self.clean_numbers(total_data, [pass_col])

            if pass_instance=='No':
                count = total_data.loc[(total_data[pass_col].astype(int) == 0)].shape[0]
            elif pass_instance=='Yes':
                count = total_data.loc[(total_data[pass_col].astype(int) > 0)].shape[0]
            else: # will default to passing a metric question (numbers are greater than 0)
                count = total_data.loc[(total_data[pass_col].astype(int) > 0)].shape[0]
            
        if count == 0:
            return(f'0 out of {total_data.shape[0]} films')
    
        return f'{count} / {total_data.shape[0]}, {(count/total_data.shape[0])*100:.3f}%'
    
    
    def min(self, col):
        self.clean_numbers([col])
        return self.df[col].astype(float).min()
    
    def max(self, col):
        self.clean_numbers([col])
        return self.df[col].astype(float).max()
    
    def range(self, col):
        self.clean_numbers([col])
        return self.max(col) - self.min(col)


    def select_columns(self, col_start, col_end):
        # returns a dataframe starting from one colum and ending at another, inclusive
        return self.df.loc[:,col_start, col_end]
    

    def select_rows(self, row_start, row_end):
        # returns a dataframe starting from one row and enfinga at another, inclusive? need to check
        return self.df.loc[row_start:row_end:,]

    
    def remove_letters(self, list_cols):
        #takes in a list of column names to remove the letters from
        for col in list_cols:
            self.df[col] = self.df[col].replace('\D', '', regex=True)


    def count_totals(self, col, num=False):
        # will return a dict with each coding answer, along with their fraction and percentage from total
        result = {}

        if num == False: #dealing with categorical data
        
            var_list = self.df[col].unique().tolist()
            count_list = [*self.df[col].value_counts(),] # for holding height of each variable

            total = sum(count_list)
            for i in range(len(var_list)):
                result[var_list[i]] = []
                
                frac_str = f'{count_list[i]}/{total}'  #get the fraction out of the total as a string
                result[var_list[i]].append(frac_str)

                percent = (count_list[i]/total)*100
                perc_str = f'{percent:.3f}%'
                result[var_list[i]].append(perc_str)

        else: # dealing with numerical data, get the total sums for each column

            result[col] = self.yearly_num_total(col)

        return result


    def totals_to_csv(self, col_list, file_name, num=False):
        # outputs a csv with the total percentages of the questions requested
        with open(file_name, 'w') as f:
            for col in col_list:
                result_dict = self.count_totals(col, num=num)

                if num==False: # dealing with categorical data
                    f.write(col + '\n')

                    for key in result_dict.keys():
                        f.write(f'{key},{result_dict[key][0]},{result_dict[key][1]}\n')
                
                else: # dealing with numerical data
                    for key in result_dict.keys():
                        f.write(f'{key},{result_dict[key]}\n')


    def yearly_num_total(self, col, year=None):
        # returns the total sum of a numerical question for a specific year. if year is None, then returns for all years
       
        self.df[col] = self.df[col].replace('', 0) # weed out any of the blank spaces

        if year==None: # return answer for all years
            total = self.df[col].astype(int).sum()
        else: #return for the specified year    
            yearly_data = self.df.loc[(self.df['Year'] == str(year))] # get the slice of that specific year's data
            total = yearly_data[col].astype(int).sum() #return the total number of characters/scenes/whatever from that year

        return total
    

    def combine_columns(self, col1, col2, new_colName):
        self.df[new_colName] = self.df[col1].astype(float) + self.df[col2].astype(float)


    def check_strings(self, total_col, pass_col, string, pass_instance=None):
        #returns a dataframe with the rows that contain the string in the specified column
      
        total_data = self.df.loc[self.df[total_col].str.contains(string, case=False)]
        total_data = total_data.drop_duplicates(keep='first')
        
        if pass_col in self.nominal:
            count = total_data.loc[total_data[pass_col] == pass_instance].shape[0] # count how many films pass 
        elif pass_col in self.continuous: 
            total_data[pass_col] = total_data[pass_col].replace('', 0)
            count = total_data.loc[total_data[pass_col].astype(int)>0].shape[0] # count how many films have a number greater than 0
        
        if count == 0:
            return(f'0 out of {total_data.shape[0]} films')

        return f'{count} / {total_data.shape[0]}, {(count/total_data.shape[0])*100:.3f}%'
    
    # def special_check_strings(self, total_col, pass_col, string, pass_instance=None, pass_num=False):
    #     #returns a dataframe with the rows that contain the string in the specified column
      
    #     total_data = self.df.loc[self.df[total_col].str.contains(string, case=False)]

    #     pres_drop = total_data.loc[total_data[total_col].str.contains('Present', case=False)]
    #     future_drop = total_data.loc[total_data[total_col].str.contains('Future', case=False)]

    #     total_data = total_data.drop(pres_drop.index.values)

    #     future_drop = future_drop.drop(['Spider-Man: Into the Spider-Verse', 'Eternals', 'Avengers: Endgame', 'Kimi no na wa (Your Name)'])
    #     #print(pres_drop.index.values)
    #     total_data = total_data.drop(future_drop.index.values)

        
        # if pass_num==False:
        #     count = total_data.loc[total_data[pass_col] == pass_instance].shape[0] # count how many films pass 
        # else: 
        #     total_data[pass_col] = total_data[pass_col].replace('', 0)
        #     count = total_data.loc[total_data[pass_col].astype(int)>0].shape[0] # count how many films have a number greater than 0
        
        # if count == 0:
        #     return(f'0 bruh out of {total_data.shape[0]} films')

        # return f'{count} / {total_data.shape[0]}, {(count/total_data.shape[0])*100:.3f}%'


    def ranged_percent_pass(self, total_col_list, pass_col, min=0, max=None, total_instance=None, pass_instance=None):
        # gets a dataframe of requested columns using the prefered instance variable (Yes, No, Black, White, etc)
        # calculates percentage of films from the total col list that pass the pass_col

        data_toBeCombined = []

        for col in total_col_list: # for each question , gather the data to be combined
            if col in self.nominal:
                df1 = self.df.loc[(self.df[col] == total_instance)] # get the sliced dataframe
            elif col in self.continuous:
                self.clean_numbers(self.df, [col])
                df1 = self.df.loc[(self.df[col].astype(float) <= max)]
                if min == 0:
                    drop = self.df.loc[self.df[col].astype(float) < min]
                else:
                    drop = self.df.loc[self.df[col].astype(float) <= min]

            df1 = df1.drop(drop.index.values)
            data_toBeCombined.append(df1)
      
        total_data = pd.concat(data_toBeCombined) #combine the dataframes
        total_data = total_data.drop_duplicates(keep='first')


        if (pass_col is None) and (pass_instance is None): #only answer the total column
            count = total_data.shape[0]
            return f'{count} / {self.df.shape[0]}, {(count/self.df.shape[0])*100:.3f}%'


        if pass_col in self.nominal:
            count = total_data.loc[total_data[pass_col] == pass_instance].shape[0] # count how many films pass 
        elif pass_col in self.continuous:
            total_data[pass_col] = total_data[pass_col].replace('', 0)
            count = total_data.loc[total_data[pass_col].astype(int)>0].shape[0] # count how many films have a number greater than 0
        
        if count == 0:
            return(f'0 / {total_data.shape[0]} :( ')
    
        return f'{count} / {total_data.shape[0]}, {(count/total_data.shape[0])*100:.3f}%'
    

    def pointbi_test(self, dicht_var, cont_var):
        #runs a pointbiserial correlation test on a column of dichotmous variables and a column of continuous variables
        # returns test score and two-tailed p value

        #need to turn the x array into a array of 0s and 1s
        x = self.df[dicht_var]

        if dicht_var in self.nominal:
            var1, var2 = x.value_counts()
            x.replace(var1, 0, inplace=True)
            x.replace(var2, 1, inplace=True)

        elif dicht_var in self.continuous:
            x.replace('', 0, inplace=True)
            x = x.astype(float).astype(bool).astype(int)

        # clean y array
        y = self.df[cont_var]
        y.replace('\D', '', regex=True, inplace=True)    

        r, p_val = scipy.stats.pointbiserialr(x, y.astype(float))
        return r, p_val
    
    def pearson_test(self, x_arr, y_arr):
        # runs a pearson correlation test on two columns of continuous variables

        x = self.df[x_arr]
        x.replace('', 0, inplace=True)
        x.replace('\D', '', regex=True, inplace=True)  

        y = self.df[y_arr]
        y.replace('', 0, inplace=True)
        y.replace('\D', '', regex=True, inplace=True)   

        r, p_val= scipy.stats.pearsonr(x.astype(float),y.astype(float))
        return r, p_val




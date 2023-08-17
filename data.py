'''data.py
Reads CSV files, stores data, access/filter data by variable name
Dominic Bellido
Climate Media Research
Summer 2023
'''

#import statements
import numpy as np
import scipy
import math
import csv

class Data:
    def __init__(self, filepath=None, headers=None, header2col=None):

        self.filepath = filepath
        self.headers = headers
        self.header2col = header2col
        
        self.metric_data = None

        self.read(self.filepath)

        pass

    def read(self, filepath):
        
        self.filepath = filepath
        self.header2col = dict()
        self.headers = []
        self.data = []

        # open the file
        source = open(filepath, "r")

        reader = csv.reader(source)
        headlist = next(reader)
        headlist = [head.strip() for head in headlist]

        index = 0
        for i in range(len(headlist)):
            self.header2col[headlist[i]] = index
            index += 1
        
        for key, value in self.header2col.items():
            self.headers.append(key)

        for row in reader:
            new = []
            if index == 1:
                new.append(row)
            else:
                for i in range(index):
                    new.append(row[i])

            self.data.append(new)
        
        self.data = np.array(self.data, dtype = str)
        self.headers = self.headers

    def get_headers(self):
        return self.headers

    def head(self):
        return self.data[:5]
    
    def tail(self):
        return self.data[-5:]

    def get_all_data(self):
        return self.data.copy()
    
    def get_num_dims(self):
        '''Get method for number of dimensions in each data sample

        Returns:
        -----------
        int. Number of dimensions in each data sample. Same thing as number of variables.
        '''
        return self.data.shape[1]

    def get_num_samples(self):
        '''Get method for number of data points (samples) in the dataset

        Returns:
        -----------
        int. Number of data samples in dataset.
        '''
        return self.data.shape[0]
    
    def get_col_index(self):
        return self.header2col

# we need a method that will what? 
# we need a method that will clean up the data, so, we go through each column and if there is nothing there, add a 

  
    def make_metric_data(self):
        #remember, always do one column more, since its not-inclusive bracketing

        one = self.data[:, 26:30]
        two = self.data[:, 32:41]
        three = self.data[:, 43:48]

        first_half = np.concatenate([one, two], axis=1)
        metric_data = np.concatenate([first_half, three], axis=1)
        
        metric_data[metric_data == ''] = 0
        self.metric_data = metric_data.astype(np.float64)
        
        return self.metric_data


    def calculate_metric_data(self, pvalue=False):
        mat = self.make_metric_data()
        index_dict = {}
        coeff_dict = {}
        
        for i in range(self.data.shape[0]):
            ind_list = []
            movie_name = self.data[i,1]

            if movie_name not in index_dict:
                ind_list.append(i)
                index_dict[movie_name] = ind_list

            elif movie_name in index_dict:
                index_dict[movie_name].append(i)

        for key in index_dict:
            indices = index_dict[key]
            if len(indices) > 1:
                x = mat[indices[0]]
                y = mat[indices[1]]

                (s, p_value) = scipy.stats.pearsonr(x, y)

                if pvalue == True:
                    coeff_dict[key] = p_value
                else:
                    coeff_dict[key] = s
                
        return coeff_dict
 

def main():
    test_filename = 'data/updated_test.csv'
    test_data = Data(test_filename)

    result = test_data.get_all_data()
    result = result[:,1:]
    print(result)
    print(result.shape)
    

if __name__ == "__main__":
    main()
    



        
        
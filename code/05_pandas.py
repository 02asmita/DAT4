'''
CLASS: Pandas for Data Exploration, Analysis, and Visualization

MovieLens 100k data:
    main page: http://grouplens.org/datasets/movielens/
    data dictionary: http://files.grouplens.org/datasets/movielens/ml-100k-README.txt
    files: u.user, u.data, u.item

WHO alcohol consumption data:
    article: http://fivethirtyeight.com/datalab/dear-mona-followup-where-do-people-drink-the-most-beer-wine-and-spirits/    
    original data: https://github.com/fivethirtyeight/data/tree/master/alcohol-consumption
    files: drinks.csv (with additional 'continent' column)
'''

# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
Reading Files, Summarizing, Selecting, Filtering, Sorting, Detecting Duplicates
'''

# can read a file directly from a URL
pd.read_table('https://raw.githubusercontent.com/justmarkham/DAT4/master/data/u.user')

# read 'u.user' into 'users'
u_cols = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
users = pd.read_table('../data/u.user', header=None, sep='|', names=u_cols, index_col='user_id', dtype={'zip_code':str})

# examine the users data
users                   # print the first 30 and last 30 rows
type(users)             # DataFrame
users.head()            # print the first 5 rows
users.tail()            # print the last 5 rows
users.describe()        # summarize all numeric columns
users.index             # "the index" (aka "the labels")
users.columns           # column names (which is "an index")
users.dtypes            # data types of each column
users.values            # underlying numpy array
users.info()            # concise summary

# select a column
users['gender']         # select one column
type(users['gender'])   # Series
users.gender            # select one column using the DataFrame attribute

# summarize a single column
users.gender.describe()         # describe the gender Series (non-numeric)
users.gender.value_counts()     # for each gender, count number of occurrences

# select multiple columns
users[['age', 'gender']]        # select two columns
my_cols = ['age', 'gender']     # or, create a list...
users[my_cols]                  # ...and use that list to select columns
type(users[my_cols])            # DataFrame

# simple logical filtering
users[users.age < 20]               # only show users with age < 20
young_bool = users.age < 20         # or, create a Series of booleans...
users[young_bool]                   # ...and use that Series to filter rows
users[users.age < 20].occupation    # select one column from the filtered results

# advanced logical filtering
users[users.age < 20][['age', 'occupation']]        # select multiple columns
users[(users.age < 20) & (users.gender=='M')]       # use multiple conditions
users[users.occupation.isin(['doctor', 'lawyer'])]  # filter specific values

# sorting
users.age.order()                           # only works for a Series
users.sort_index()                          # sort rows by label
users.sort_index(by='age')                  # sort rows by a specific column
users.sort_index(by='age', ascending=False) # use descending order instead
users.sort_index(by=['occupation', 'age'])  # sort by multiple columns

# detecting duplicate rows
users.duplicated()                  # Series of booleans
users.duplicated().sum()            # count of duplicates
users[users.duplicated()]           # only show duplicates
users[users.duplicated()==False]    # only show unique rows
users.duplicated(['age', 'gender', 'zip_code']).sum()   # specify columns for finding duplicates


'''
EXERCISE: Working with drinks data
'''

# Read drinks.csv into a DataFrame called 'drinks' (use the default index)
drinks = pd.read_table('../data/drinks.csv', sep=',')
drinks = pd.read_csv('../data/drinks.csv')              # equivalent

# Print the first 10 rows
drinks.head(10)

# Examine the data types of all columns
drinks.dtypes
drinks.info()

# Print the 'beer_servings' Series
drinks.beer_servings
drinks['beer_servings']

# Calculate the average 'beer_servings' for the entire dataset
drinks.describe()                   # summarize all numeric columns
drinks.beer_servings.describe()     # summarize only the 'beer_servings' Series
drinks.beer_servings.mean()         # only calculate the mean

# Print all columns, but only show rows where the country is in Europe
drinks[drinks.continent=='EU']

# Calculate the average 'beer_servings' for all of Europe
drinks[drinks.continent=='EU'].beer_servings.mean()

# Only show European countries with 'wine_servings' greater than 300
drinks[(drinks.continent=='EU') & (drinks.wine_servings > 300)]

# Determine which 10 countries have the highest 'total_litres_of_pure_alcohol'
drinks.sort_index(by='total_litres_of_pure_alcohol').tail(10)

# Determine which country has the highest value for 'beer_servings'
drinks[drinks.beer_servings==drinks.beer_servings.max()].country

# Count the number of occurrences of each 'continent' value and see if it looks correct
drinks.continent.value_counts()


'''
Handling Missing Values
'''

# turn off the missing value filter
pd.read_csv('../data/drinks.csv', na_filter=False)

# keep the missing values (for demonstration purposes)
drinks = pd.read_csv('../data/drinks.csv')

# set more values to NaN (for demonstration purposes)
drinks.loc[192, 'beer_servings':'wine_servings'] = np.nan

# missing values are often just excluded
drinks.describe()                           # excludes missing values
drinks.continent.value_counts()             # excludes missing values
drinks.continent.value_counts(dropna=False) # includes missing values (new in pandas 0.14.1)

# find missing values in a Series
drinks.continent.isnull()           # True if NaN, False otherwise
drinks.continent.notnull()          # False if NaN, True otherwise
drinks[drinks.continent.notnull()]  # only show rows where continent is not NaN
drinks.continent.isnull().sum()     # count the missing values

# find missing values in a DataFrame
drinks.isnull()             # DataFrame of booleans
drinks.isnull().sum()       # calculate the sum of each column

# drop missing values
drinks.dropna()             # drop a row if ANY values are missing
drinks.dropna(how='all')    # drop a row only if ALL values are missing

# fill in missing values
drinks.continent.fillna(value='NA')                 # does not modify 'drinks'
drinks.continent.fillna(value='NA', inplace=True)   # modifies 'drinks' in-place
drinks.fillna(drinks.mean())                        # fill in missing values using mean


'''
More File Reading and File Writing
'''

# read drinks.csv into a list of lists
import csv
with open('../data/drinks.csv', 'rU') as f:
    header = csv.reader(f).next()
    data = [row for row in csv.reader(f)]

# convert into a DataFrame
drinks = pd.DataFrame(data, columns=header)
drinks.isnull().sum()   # no automatic handling of missing values
drinks.dtypes           # type is 'object' because list elements were strings

# fix data types of numeric columns
num_cols = drinks.columns[1:5]                      # create list of numeric columns
drinks[num_cols] = drinks[num_cols].astype(float)   # convert them to type 'float'

# write a DataFrame out to a CSV
drinks.to_csv('../data/drinks_updated.csv')                 # index is used as first column
drinks.to_csv('../data/drinks_updated.csv', index=False)    # ignore index


'''
Adding, Renaming, and Removing Columns
'''

# reset the DataFrame
drinks = pd.read_csv('../data/drinks.csv', na_filter=False)

# add a new column as a function of existing columns
# note: can't assign to an attribute such as 'drinks.total_servings'
drinks['total_servings'] = drinks.beer_servings + drinks.spirit_servings + drinks.wine_servings
drinks.head()

# alternative method: default is column sums, 'axis=1' does row sums instead
drinks['total_servings'] = drinks.loc[:, 'beer_servings':'wine_servings'].sum(axis=1)

# rename a column
drinks.rename(columns={'total_litres_of_pure_alcohol':'pure_alcohol'}, inplace=True)

# hide a column (temporarily)
drinks.drop(['total_servings'], axis=1)     # use 'axis=0' to drop rows instead
drinks[drinks.columns[:-1]]                 # slice 'columns' attribute like a list

# delete a column (permanently)
del drinks['total_litres_of_pure_alcohol']


'''
Split-Apply-Combine
'''

# for each continent, calculate mean beer servings
drinks.groupby('continent').beer_servings.mean()

# for each continent, calculate mean of all numeric columns
drinks.groupby('continent').mean()

# for each continent, count number of occurrences
drinks.groupby('continent').continent.count()
drinks.continent.value_counts()


'''
Plotting
'''

# bar plot of number of countries in each continent
drinks.continent.value_counts().plot(kind='bar', title='Countries per Continent')
plt.xlabel('Continent')
plt.ylabel('Count')
plt.show()

# bar plot of average number of beer servings (per adult per year) by continent
drinks.groupby('continent').beer_servings.mean().plot(kind='bar')
plt.ylabel('Average Number of Beer Servings Per Year')

# histogram of beer servings (shows the distribution of a numeric column)
drinks.beer_servings.hist(bins=20)
plt.xlabel('Beer Servings')
plt.ylabel('Frequency')

# density plot of beer servings (smooth version of a histogram)
drinks.beer_servings.plot(kind='density', xlim=(0,500))
plt.xlabel('Beer Servings')

# grouped histogram of beer servings (shows the distribution for each group)
drinks.beer_servings.hist(by=drinks.continent)
drinks.beer_servings.hist(by=drinks.continent, sharex=True)
drinks.beer_servings.hist(by=drinks.continent, sharex=True, sharey=True)

# boxplot of beer servings by continent (shows five-number summary and outliers)
drinks.boxplot(column='beer_servings', by='continent')

# scatterplot of beer servings versus wine servings
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', alpha=0.3)

# same scatterplot, except all European countries are colored red
colors = np.where(drinks.continent=='EU', 'r', 'b')
drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', c=colors)


'''
Advanced Filtering (of rows) and Selecting (of columns)
'''

# loc: filter rows by LABEL, and select columns by LABEL
users.loc[1]                        # row with label 1
users.loc[1:3]                      # rows with labels 1 through 3
users.loc[1:3, 'age':'occupation']  # rows 1-3, columns 'age' through 'occupation'
users.loc[:, 'age':'occupation']    # all rows, columns 'age' through 'occupation'
users.loc[[1,3], ['age','gender']]  # rows 1 and 3, columns 'age' and 'gender'

# iloc: filter rows by POSITION, and select columns by POSITION
users.iloc[0]                       # row with 0th position (first row)
users.iloc[0:3]                     # rows with positions 0 through 2 (not 3)
users.iloc[0:3, 0:3]                # rows and columns with positions 0 through 2
users.iloc[:, 0:3]                  # all rows, columns with positions 0 through 2
users.iloc[[0,2], [0,1]]            # 1st and 3rd row, 1st and 2nd column

# mixing: select columns by LABEL, then filter rows by POSITION
users.age[0:3]
users[['age', 'gender', 'occupation']][0:3]


'''
Joining Data
'''

# read 'u.item' into 'movies'
m_cols = ['movie_id', 'title']
movies = pd.read_table('../data/u.item', header=None, names=m_cols, sep='|', usecols=[0, 1])
movies.head()

# read 'u.data' into 'ratings'
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_table('../data/u.data', header=None, names=r_cols, sep='\t')
ratings.head()

# merge 'movies' and 'ratings' (inner join on 'movie_id')
movie_ratings = pd.merge(movies, ratings)
movie_ratings.head()


'''
Further Exploration of MovieLens Data
'''

# for each occupation, calculate mean age and age range
users.groupby('occupation').age.mean()
users.groupby('occupation').age.apply(lambda x: x.max() - x.min())

# for each occupation/gender combination, calculate mean age
users.groupby(['occupation', 'gender']).age.mean()
users.groupby(['gender', 'occupation']).age.mean()

# for each movie, count number of ratings
movie_ratings.title.value_counts()

# for each movie, calculate mean rating
movie_ratings.groupby('title').rating.mean().order(ascending=False)

# for each movie, count number of ratings and calculate mean rating
movie_ratings.groupby('title').rating.count()
movie_ratings.groupby('title').rating.mean()
movie_stats = movie_ratings.groupby('title').agg({'rating': [np.size, np.mean]})
movie_stats.head()  # hierarchical index

# limit results to movies with more than 100 ratings
movie_stats[movie_stats.rating.size > 100].sort_index(by=('rating', 'mean'))


'''
Other Useful Features
'''

# change the maximum number of rows and columns printed ('None' means unlimited)
pd.set_option('max_rows', None)     # default is 60 rows
pd.set_option('max_columns', None)  # default is 20 columns
print drinks

# reset options to defaults
pd.reset_option('max_rows')
pd.reset_option('max_columns')

# change the options temporarily (settings are restored when you exit the 'with' block)
with pd.option_context('max_rows', None, 'max_columns', None):
    print drinks

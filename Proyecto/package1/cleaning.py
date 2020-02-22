# The first step in data cleaning is to import all libraries needed:
import re
import pandas as pd
import numpy as np
import datetime
import acquisition
# This next library is used so that warnings of changed DataFrame don't appear on screen:
import warnings
warnings.filterwarnings('ignore')


def drop_cols(df, lst):
    for i in lst:
        df.drop(i, axis=1, inplace=True)
    return df

def clean_numcols_from_text(df, dic):
    for k, v in dic.items():
        df[k] = df[k].str.replace(v, '')
    return df

def column_title(df, lst):
    for i in lst:
        df.update(df[i].str.title())
    return df

def change_china_billionaires_names(df):
    # Since names from china were wrong, their first name was in the last_name column and their last name was in the first_name column
    count = -1
    df['change_name'] = np.nan
    for i in df['country']:
        count += 1
        if i == 'China':
            df['change_name'][count] = df['last_name'][count]
            df['last_name'][count] = df['first_name'][count]
            df['first_name'][count] = df['change_name'][count]
        else:
            pass

# The function change_types receives a list of columns of the df as an argument and will convert its type
# to float, so it's possible to operate with them.
def change_to_float_type(df, lst):
    for i in lst:
        df[i] = df[i].astype(float)
    return df

# To complete our data I had to get this file:
def complete_data(df):
    path = '../data/raw/forbes_2018.csv'
    forbes = pd.read_csv(path)
    forbes.dropna(subset=['position'], inplace=True)
    df['gender'] = df['position'].map(forbes.set_index('position')['gender'])
    df['country'] = df['position'].map(forbes.set_index('position')['country'])
    return df

def save_csv_file(df, file):
    return df.to_csv(file, index=False)

def cleaning(file):
    df = acquisition.reading_csv('df')
    df[['work_field', 'company']] = df['Source'].str.split(' ==> ', expand=True)

    clean_text = {'worth': ' BUSD', 'worthChange': ' millions USD', 'age': ' years old'}
    clean_numcols_from_text(df, clean_text)

    ls_cols = ['name', 'lastName', 'company']
    column_title(df, ls_cols)

    df = df.rename(columns={'name': 'first_name', 'lastName': 'last_name', 'realTimePosition': 'real_time_position', 'worth': 'worth(BUSD)', 'worthChange': 'worth(millions_USD)'})

    # Since we had the first and last name in the column name, with the following code we have only the first
    # name in the column name and the last name in the column lastName
    df['first_name'] = [a.replace(b, '').strip() for a, b in zip(df['first_name'], df['last_name'])]

    change_china_billionaires_names(df)

    # Transform all ages to correct numbers:
    df.age.fillna(str(-2019), inplace=True)
    current_year = datetime.datetime.today().year
    age = []
    for i in df['age']:
        if len(str(i)) == 4:
            age.append(str(current_year - int(i)))
        else:
            age.append(i)
    df['age'] = age

    change_to_float_type(df, ['worth(BUSD)', 'worth(millions_USD)'])

    complete_data(df)
    cols_to_drop = ['Unnamed: 0', 'id', 'Unnamed: 0_x', 'realTimeWorth', 'Unnamed: 0_y', 'Unnamed: 0.1', 'Source', 'change_name', 'position']
    drop_cols(df, cols_to_drop)

    # The column 'name' is going to be used for wikipedia web scraping and the column education is going to be updated
    # by the scraped data.
    df['name'] = df['first_name'] + '_' + df['last_name']
    df['education'] = 'None'
    df = df[['first_name', 'last_name', 'age', 'gender', 'country', 'education', 'real_time_position', 'worth(BUSD)', 'worth(millions_USD)', 'work_field', 'company', 'image', 'name']]

    return save_csv_file(df, file)

cleaning('df')


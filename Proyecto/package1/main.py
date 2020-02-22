import pandas as pd
from acquisition import acquisition
from cleaning import cleaning
from webscraping import webscraping
import analysis
from time import sleep
from sending import sending_email
import converting
import argparse

def main(type_of_analysis):
    if type_of_analysis == 1:
        sleep(1)
        print('Preparing your graphic to see which country has more billionaires...')
        analysis.num_billionaires_per_country(df)
    elif type_of_analysis == 2:
        sleep(1)
        print('Getting the most profitable work fields')
        analysis.profitable_work_field(df)
    elif type_of_analysis == 3:
        sleep(1)
        print('Getting top 15 countries which holds more billions of dollars by its billionaires')
        analysis.more_even_country(df)
    elif type_of_analysis == 4:
        sleep(1)
        print('Getting the gender ratio')
        analysis.male_female_ratio(df)
    elif type_of_analysis == 5:
        sleep(1)
        print("It's interesting to check if education is important to get richer, good choice!")
        analysis.education_ratio(df)
    elif type_of_analysis == 6:
        print('Joining all data to provide you the best graphics possible to learn more about this billionaires!')
        analysis.num_billionaires_per_country(df)
        analysis.male_female_ratio(df)
        analysis.more_even_country(df)
        analysis.profitable_work_field(df)
        analysis.education_ratio(df)
    else:
        print('Not a valid number, try again with a choice from 1 to 6!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare yourself for an analysis of the billionaires of 2018:')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-a', '--analysis', dest='type_of_analysis', default=None, choices=[1, 2, 3, 4, 5, 6], type=int, help="""1 - To know which country has maximum numbers of billionaires;
    2 - To get the male to female ratio based on the total of dollars;
    3 - To know which country has the greatest share in terms of total money held by its billionaires;
    4 - To get the top 15 most profitable fields of work;
    5 - To get the percentage of billionaires with studies;
    6 - To get all the above""", required=True)
    requiredNamed.add_argument('-e', '--email', dest='want_results', default=None, required=True, choices=['y', 'n'], type=str, help="""y - To receive an email with your results; 
    n - Otherwise""")
    args = parser.parse_args()

    print('Prepare yourself for an analysis of the billionaires of 2018!')

    acquisition('df')
    cleaning('df')
    webscraping('df')
    df = pd.read_csv('df')
    main(args.type_of_analysis)
    converting.extra_analysis()
    converting.add_pdf(args.type_of_analysis)
    sending_email(args.want_results)
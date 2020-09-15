import argparse
import logging
import pandas as pd
import numpy as np
import re


def get_year(x):
    '''
    This function takes item description column as input and return the year/years from that
    '''
    years = []
    tokens = re.findall(r'[0-9]+', x)
    for token in tokens:
        if token[0].isdigit() and token[-1].isdigit():
            years.append(token)

    years = [y for y in years if len(y) == 4 and int(y) > 1900 and int(y) < 2025]
    if len(years) == 0:
        return np.NaN
    return ", ".join(years)


def get_season(x):
    '''
    This function takes item description column as input and return the seasons
    Spring / Summer, Fall / Winter, Resort, and Pre - Fall
    '''


    keywords = keywords = ["spring", "summer", "fall", "winter", "fw", "ss", "pre-fall", "pre-spring", "autumn", "resort"]
    x = x.lower()
    seasons = [token for token in x.split() if token in keywords]
    tokens = re.findall(r'[a-z]+', x)
    seasons += [token for token in tokens if token in keywords]

    if len(seasons) == 0:
        return np.NaN

    seasons = ", ".join(list(set(seasons)))
    return seasons


def main(args):
    data = pd.read_csv(args.inputfile)

    data["Year"] = data.item_description.apply(lambda x: get_year(str(x)))
    data["Specific_season"] = data.item_description.apply(lambda x: get_season(str(x)))

    data.to_csv(args.outputfile, index=False)      # writing to csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--inputfile", type=str, default='data/ProductInfo.csv', help='name of the csv file')
    parser.add_argument("--outputfile", type=str, default='output/translated_ProductInfo.csv', help='name of the output csv file')
    parser.add_argument("--logfile", type=str, default='output/products_info.log', help='log file name')
    args = parser.parse_args()

    logging.basicConfig(filename=args.logfile, format='%(asctime)s %(message)s', level=logging.INFO)
    main(args)

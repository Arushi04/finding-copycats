import argparse
import pandas as pd
import numpy as np
import re


def get_retail_price(x):
    x = str(x).lower()
    retail_index = x.find("retail")

    if retail_index == -1:
        return np.NaN

    x = x[retail_index:]

    tokens = re.findall('[$€£]*\s*[0-9]+[.,]*[0-9]+\w*\s*[$€£]*', x)
    # tokens += re.findall('[0-9]+\s+(\s*euro|sek|usd|gbp|pound)', x)

    tokens += re.findall('[0-9]+\s+euro', x)
    tokens += re.findall('[0-9]+\s+sek', x)
    tokens += re.findall('[0-9]+\s+usd', x)
    tokens += re.findall('[0-9]+\s+gbp', x)
    tokens += re.findall('[0-9]+\s+pound', x)

    tokens = [token.strip() for token in tokens]
    single_nos = [token for token in tokens if ' ' not in token]
    multiple_nos = [token for token in tokens if ' ' in token]
    for token in tokens:
        token = token.split()
        if len(token) > 1:
            if token[0] in single_nos:
                single_nos.remove(token[0])

    tokens = multiple_nos + single_nos
    if len(tokens) > 0:
        return tokens[0]
    return tokens


def get_year(x):
    years = []
    tokens = re.findall(r'[0-9]+', x)
    for token in tokens:
        if token[0].isdigit() and token[-1].isdigit():
            years.append(token)

    years = [y for y in years if len(y) == 4 and int(y) > 1990 and int(y) < 2025]
    if len(years) == 0:
        return np.NaN
    return ", ".join(set(years))



def get_season(x):
    ##Spring / Summer, Fall / Winter, Resort, and Pre - Fall
    keywords = ["spring", "summer", "fall", "winter", "fw", "ss", "pre-fall", "pre-spring", "autumn", "resort",
                "s/s", "w/s", "f/w", "spring/summer"]

    x = x.lower()

    seasons = [token for token in x.split() if token in keywords]
    tokens = re.findall(r'[a-z]+/*[a-z]+', x)
    seasons += [token for token in tokens if token in keywords]

    if len(seasons) == 0:
        return np.NaN

    seasons = ", ".join(list(set(seasons)))
    return seasons


def main(args):
    data = pd.read_csv(args.inputfile)

    data["year"] = data.item_desc_tr.apply(lambda x: get_year(str(x)))
    data["specific_season"] = data.item_desc_tr.apply(lambda x: get_season(str(x)))
    data["retail"] = data.item_desc_tr.apply(lambda x: get_retail_price(str(x)))

    data['specific_season'] = data['specific_season'].replace(['fw'], 'fall/winter')
    data['specific_season'] = data['specific_season'].replace(['ss', 's/s'], 'summer/spring')

    data.to_csv(args.outputfile, index=False)      # writing to csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--inputfile", type=str, default='output/translated_ProductInfo.csv', help='name of the csv file')
    parser.add_argument("--outputfile", type=str, default='output/ProductInfo_year_season.csv', help='name of the output csv file')
    args = parser.parse_args()

    main(args)

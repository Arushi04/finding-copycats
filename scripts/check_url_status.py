import argparse
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


'''
Steps to Run:
python check_url_status.py --inputfile "valid_urls.xlsx" --outputfile "out_valid_urls.xlsx"
'''

def get_sel_response(url):
    '''
    This function take a url as an input, uses selenium to dynamically scrape the webpage and return
    beautiful soup object. This also takes care of the page load timeout.
    '''

    options = Options()
    options.add_argument('--headless')  # to make firefox instances run in the background

    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(15)  # setting timeout to load the page
    try:
        driver.get(url)     # opens the url in firefox
        source = driver.page_source    # gets the source code of the page
        driver.quit()  # to auto close the browser
        soup = BeautifulSoup(source, "html.parser")
        return soup
    except:
        return "Timeout error"


def check_wishlist_fav(url):
    '''
    This function takes url as an input and returns True if there is any item in wishlist or favorites of the user.
    '''

    wishlist_soup = get_sel_response(url + '#wishlist')
    if wishlist_soup == "Timeout error":
        print(url, "Wishlist Page not loaded")
        return 3, None

    fav_soup = get_sel_response(url + '#fav')
    if fav_soup == "Timeout error":
        print(url, "Favorite Page not loaded")
        return 3, None

    wishlist, fav = False, False

    if wishlist_soup.find('div', {'class': 'wishlist'}):
        wishlist = True

    if fav_soup.find('div', {'id': 'favs'}):
        fav = True

    return (wishlist or fav), wishlist_soup


def check_followers_count(soup):
    '''
    This function takes beautiful soup object as input and returns True if follower and following count
    exceeds the stated threshold
    '''

    div = soup.findAll("span", {"class": "quantity vc-text-l"})
    fol_count = []
    for count in div:
        fol_count.append(count.text)

    follower = int(fol_count[0])
    following = int(fol_count[1])
    print(f"follower : {follower} following :  {following} ")
    if follower > 3 or following > 8:
        return True
    else:
        return False


def check_status(url):
    '''
    This function takes url as an input and returns status after checking
    wishlist, favorites and follower/following count
    '''

    wishlist_fav_status, soup = check_wishlist_fav(url)
    if wishlist_fav_status == True:
        follower_status = check_followers_count(url, soup)
        if follower_status == True:
            status = 1
        else:
            status = 0
    elif wishlist_fav_status == False:
        status = 0
    else:
        status = 3

    return status


def main(args):
    # check if outputfile exists. If yes, resume the status
    if os.path.isfile(args.outputfile):
        df = pd.read_excel(args.outputfile)
        col_names = list(df.columns)
        print("Col names : ", col_names)
    else:
        if os.path.isfile(args.inputfile):   # Else read from the main input file
            df = pd.read_excel(args.inputfile)
            col_names = list(df.columns)
            print("Col names : ", col_names)

    # Create a column 'Status' if it does not exist in the file, and initialize it with None
    if 'Status' not in col_names:
        df['Status'] = None

    rows = df.shape[0]  # checks total no of urls present in the input file
    start_from = df['Status'].last_valid_index()  # finds the last updated row

    if start_from is None:
        start_from = 0
    else:
        start_from += 1

    print("starting from index : ", start_from)

    # Loop through the index of the file, check the status and update it
    for idx in range(start_from, rows+1):
        url = df.iloc[idx].URLs     # gets the url
        print(url)
        status = check_status(url)     # gets the status
        time.sleep(1)
        print(status)
        df.iloc[idx, df.columns.get_loc('Status')] = status   # updates the status to dataframe

        # write the status to excel
        df.to_excel(args.outputfile, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--inputfile", type=str, default='valid_urls.xlsx', help='name of the excel file')
    parser.add_argument("--outputfile", type=str, default='out_valid_urls.xlsx', help='name of the excel file')
    args = parser.parse_args()
    main(args)

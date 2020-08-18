import argparse
import random
import requests
import csv

'''
Steps to Run:
python collect_urls.py --start 1 --stop 10339999 --max_urls 10000 --filename urls.csv

'''


def save_to_csv(urls, filename):
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(["URLs"])
            for url in urls:
                writer.writerow([url])
    except IOError:
        print("I/O error")


def generate_url(start, stop):
    #  generate a random number between start and stop
    num = random.randrange(start, stop)

    #  Append the number to the url
    url = 'https://us.vestiairecollective.com/members/profile-' + str(num) + '.shtml'
    return url


def main(args):
    #  creating session to check validity of url
    session = requests.Session()
    url_set = set()  # set to store url to avoid duplication
    random.seed(args.seed)      # setting seed so that each time program gives same result

    while len(url_set) < args.max_urls:
        url = generate_url(args.start, args.stop)
        if url not in url_set:
            status_code = session.get(url, headers={'User-Agent': 'Mozilla/5.0'}).status_code
            if status_code == 200:  # check if url is valid
                print(url)
                url_set.add(url)

    print(f"Writing {len(url_set)} urls to csv {args.filename}")
    save_to_csv(url_set, args.filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--start", type=int, default=1, help='number starts generating from this number')
    parser.add_argument("--stop", type=int, default=10339999, help='number generates upto this number')
    parser.add_argument("--max_urls", type=int, default=10000, help='total no of urls we want to create')
    parser.add_argument("--filename", type=str, default='valid_urls.csv', help='name of the csv file')
    parser.add_argument("--seed", type=str, default=4, help='to ensure random number is always generated in same sequence')
    args = parser.parse_args()
    main(args)

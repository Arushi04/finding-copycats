# Web scraping and Automation scripts


### Scripts (all the scripts under scripts folder) :

**1. [collect_urls.py](scripts/collect_urls.py) :** This script creates unique url, checks whether the url is valid and if valid stores it in an excel file.

__Command to run :__       
python collect_urls.py \
--start 1 \
--stop 10339999 \
--max_urls 10000 \
--filename urls.csv


**2. [check_url_status.py](scripts/check_url_status.py)  :** This script checks if the user has anything in their wishlist and favorites. If yes, it checks if the user has followers and following than default and writes it to an excel file.

__Command to run :__        
python check_url_status.py \
--inputfile "valid_urls.xlsx" \
--outputfile "out_valid_urls.xlsx"


**3. [translate_itemdescription.py](scripts/translate_itemdescription.py)  :** This script translates the item description to English and extracts year and season from that.

__Command to run :__        
python translate_itemdescription.py \
--inputfile ProductInfo.csv 
--outputfile modified_productInfo.csv 
--logfile product_info.log


**4. [scrape_designer_details.ipynb](/scrape_designer_details.ipynb)  :** This script takes the root url and scrapes Name, website, contact and location for each designer using Beautiful Soup.


**5. [scrape_product_details.ipynb](/scrape_product_details.ipynb)  :** This script takes the website url of the designer as input, scrapes the website and save the product details like Designer Name, Product name, Year of designing, total images associated with it and product description. It also downloads all the product images in respective folders. This scripts uses Selenium and Beautiful Soup for the crawling.

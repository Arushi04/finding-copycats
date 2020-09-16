# Web scraping and Automation scripts


### Scripts :

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


**3. [translate_itemdescription.py](scripts/translate_itemdescription.py):** This script takes a csv file as an input, cleans the text by removing emojis, detects the language of each item description and translates them accordingly using IBM Watson translation API. 

__Command to run :__         
python translate_itemdescription.py \
--inputfile ProductInfo.csv \
--outputfile translated_productInfo.csv \
--logfile product_info.log 

__Requirements and Installation Steps:__   
1. Install language detection API : conda install -c conda-forge langdetect
1. Install Watson API using command: pip install --upgrade "ibm-watson>=4.6.0"    
2. Create an account at https://cloud.ibm.com/  
3. Use the API key generated for the script authentication.     
__Ref__ : https://cloud.ibm.com/apidocs/language-translator?code=python


**4. [extract_product_details.py](scripts/extract_product_details.py)  :** This script reads the output csv file of the translated csv (producet by script at no 3.) and extracts year, seasons and retail price from the translated item description.

__Command to run :__         
python extract_product_details.py \
--inputfile translated_productInfo.csv \
--outputfile product_details.csv


**5. [scrape_designer_details.ipynb](/scrape_designer_details.ipynb)  :** This script takes the root url and scrapes Name, website, contact and location for each designer using Beautiful Soup.


**6. [scrape_product_details.ipynb](/scrape_product_details.ipynb)  :** This script takes the website url of the designer as input, scrapes the website and save the product details like Designer Name, Product name, Year of designing, total images associated with it and product description. It also downloads all the product images in respective folders. This scripts uses Selenium and Beautiful Soup for the crawling.






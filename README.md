# Web scraping and Automation scripts


### Scripts (all the scripts under scripts folder) :

**1. collect_urls.py  :** This script creates unique url, checks whether the url is valid and if valid stores it in an excel file.

__Command to run :__       
python collect_urls.py \
--start 1 \
--stop 10339999 \
--max_urls 10000 \
--filename urls.csv


**2. check_url_status.py  :** This script checks if the user has anything in their wishlist and favorites. If yes, it checks if the user has followers and following than default and writes it to an excel file.

__Command to run :__        
python check_url_status.py \
--inputfile "valid_urls.xlsx" \
--outputfile "out_valid_urls.xlsx"


**3. translate_itemdescription.py  :** This script translates the item description to English and extracts year and season from that.

__Command to run :__        
python translate_itemdescription.py \
--inputfile ProductInfo.csv 
--outputfile modified_productInfo.csv 
--logfile product_info.log

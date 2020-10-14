# Web scraping of Designer and Product details


**1. [scrape_designer_details.ipynb](/scrape_designer_details.ipynb)  :** This script takes the root url and scrapes Name, website, contact and location for each designer using Beautiful Soup.


**2. [scrape_product_details_static.ipynb](/scrape_product_details_static.ipynb)  :** This script takes the website url of the designer as input, scrapes the website and save the product details like Designer Name, Product name, Year of designing, total images associated with it and product description. It also downloads all the product images in respective folders. This scripts Beautiful Soup for the crawling.


**3. [scrape_product_details_dynamic_using_selenium.ipynb](/scrape_product_details_dynamic_using_selenium.ipynb)  :** This script takes the website url of the designer as input, scrapes the website and save the product details like Designer Name, Product name, Year of designing, total images associated with it and product description. It also downloads all the product images in respective folders. This scripts uses Selenium and Beautiful Soup for crawling dynamically rendering webpages.


#### Installation Requirement:

1. beautifulsoup4==4.9.1
2. selenium==3.141.0
3. requests-html==0.10.0
4. urllib3



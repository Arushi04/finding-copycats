import argparse
import logging
import pandas as pd
import re

from langdetect import detect
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# connecting to IBM cloud services for translation

authenticator = IAMAuthenticator('***************')  #provide your own IBM cloud API key
language_translator = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
language_translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com/instances/2b8fa6b6-408f-4edc-bf24-4343f5e07f5e')


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text.strip())


def detect_lang(x):
    return detect(x)


def translate_lang(x, lang):
    try:
        if lang == "en" or len(x) == 0:  # check for english and skip the translation
            return x
    except Exception as e:
        print(str(e))

    try:
        translation = language_translator.translate(text=x, model_id=lang + '-en').get_result()
        translated = translation['translations'][0]['translation']
        return translated
    except Exception as e:
        logging.info("Exception caught : ", str(e))
        return x


def main(args):
    data = pd.read_csv(args.inputfile)

    data["language"] = data.item_description.apply(lambda x: detect_lang(str(x)))
    data["clean_text"] = data.item_description.apply(lambda x: deEmojify(str(x)))
    data["item_desc_tr"] = data.apply(lambda x: translate_lang(x.clean_text, x.language), axis=1)

    data = data.drop(['language', 'clean_text'], axis=1)

    data.to_csv(args.outputfile, index=False)      # writing the translated file to csv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument("--inputfile", type=str, default='data/ProductInfo.csv', help='name of the csv file')
    parser.add_argument("--outputfile", type=str, default='output/translated_ProductInfo.csv', help='name of the output csv file')
    parser.add_argument("--logfile", type=str, default='output/products_info.log', help='log file name')
    args = parser.parse_args()

    logging.basicConfig(filename=args.logfile, format='%(asctime)s %(message)s', level=logging.INFO)
    main(args)

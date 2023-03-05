import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm


class TextInformation:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        self.soup = BeautifulSoup(
            response.text,
            'html.parser',
            from_encoding='utf-8')

    def get_information(self):
        information = self.soup.find('span', {'style': 'vertical-align:3pt'})

        if information:
            next_sibling = information.next_sibling
            try:
                return next_sibling.strip()
            except AttributeError:
                return "No next sibling found"
        else:
            return "Element not found"

    def get_date(self):
        date = self.soup.find('p', {'class': 'assnatenregistr'})

        if date:
            date_text = date.text.strip()
            words = date_text.split(" ")
            day = words[-3]
            month = words[-2]
            year = words[-1]
            return f"{day} {month} {year}"
        else:
            return "Element not found"

    def get_texts(self):
        texts = self.soup.find_all('p', {'class': 'assnatLoiTexte'})
        if texts:
            return [text.text.strip() for text in texts]
        else:
            return "Elements not found"


def clean_data(input_file, output_file):
    # lecture des données
    data = pd.read_csv(input_file)
    to_analz = data.replace(regex=[r'\\xa0'], value=' ')

    # suppression du fichier existant s'il existe
    if os.path.exists(output_file):
        os.remove(output_file)

    # enregistrement des données nettoyées dans un nouveau fichier csv
    to_analz.to_csv(output_file, index=False, encoding='utf-8-sig')


def main(urls):
    start_time = time.time()
    result = []
    with tqdm(total=len(urls), bar_format='{bar}') as pbar:
        for url in urls:
            pbar.update(1)
            print("Processing: ", url)
            text_info = TextInformation(url)
            information = text_info.get_information()
            if information == "Element not found":
                continue
            date = text_info.get_date()
            texts = text_info.get_texts()
            result.append([information, date, texts])

    df = pd.DataFrame(result, columns=['Information', 'Date', 'Texts'])
    df = df.replace(regex=[r'\\xa0'], value=' ')

    # suppression du fichier existant s'il existe
    if os.path.exists('raw_data.csv'):
        os.remove('raw_data.csv')

    # enregistrement des données dans un fichier csv
    df.to_csv('raw_data.csv', index=False, encoding='utf-8-sig')

    # nettoyage des données et enregistrement dans un nouveau fichier csv
    clean_data('raw_data.csv', 'to_analz.csv')

    elapsed_time = time.time() - start_time
    elapsed_time_minutes = round(elapsed_time / 60, 1)
    print("--- %s minutes ---" % (elapsed_time_minutes))


urls = [f"https://www.assemblee-nationale.fr/dyn/opendata/PRJLANR5L15B{i:04d}.html" for i in range(
    3737, 6000) if i != 3651 and i != 3726 and i != 3736 and i != 3829 and i != 4426 and i != 4426]
main(urls)

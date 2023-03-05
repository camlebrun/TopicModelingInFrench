import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
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
        """Get the information from the webpage"""
        try:
            soup = self.soup
            # On a déjà stocké self.soup dans l'initialisation, on peut donc le réutiliser directement
            information = self.soup.find('span', {'style': 'vertical-align:3pt'})

            next_sibling = information.next_sibling
            if next_sibling is not None:
                try:
                    return next_sibling.text.strip()
                except AttributeError:
                    pass
            else:
                print("Error: next sibling is None")
        except BaseException:
            print(f"Error getting information from {self.url}")

    def get_date(self):
        date = self.soup.find('p', {'class': 'assnatenregistr'})

        if date:
            date_text = date.text.strip()
            words = date_text.split(" ")
            day = words[-3]
            month = words[-2]
            year = words[-1]
            return f"{day} {month} {year}"
        return None

    def get_texts(self):
        texts = self.soup.find_all('p', {'class': 'assnatLoiTexte'})
        if texts:
            return [text.text.strip() for text in texts]
        return None
    
    def get_helo(self):
        section3 = self.soup.find('div', {'class': 'assnatSection3'})
        if section3:
            return   [text.text.strip() for text in section3]
        return None


def clean_data(input_file, output_file):
    # lecture des données
    data = pd.read_csv(input_file)
    to_analz_2 = data.replace(regex=[r'\"\[\''], value='').replace(regex=[r'\'\]\"'], value='').replace(regex=[r'\\xa0'], value=' ')

    # suppression du fichier existant s'il existe
    if os.path.exists(output_file):
        os.remove(output_file)

    # enregistrement des données nettoyées dans un nouveau fichier csv
    to_analz_2.to_csv(output_file, index=False, encoding='utf-8-sig')


def main(urls):
    start_time = time.time()
    result = []
    for url in tqdm(urls):
        print("Processing: ", url)
        text_info = TextInformation(url)
        information = text_info.get_information()
        date = text_info.get_date()
        texts = text_info.get_texts()
        helo = text_info.get_helo()
        if information is not None and date is not None and texts is not None and helo is not None:
            result.append([information, date, texts, helo])
        else:
            continue

    df = pd.DataFrame(result, columns=['Information', 'Date', 'exposee', 'texte_lois'])
    #df = df.replace(regex=[r'\"\[\''], value='').replace(regex=[r'\'\]\"'], value='').replace(regex=[r'\\xa0'], value=' ')

   


    # enregistrement des données brutes dans un fichier csv
    df.to_csv('raw_data.csv', index=False, encoding='utf-8-sig')

    # nettoyage des données et enregistrement dans un nouveau fichier csv
    clean_data('raw_data.csv', 'cleaned_data.csv')

    elapsed_time = time.time() - start_time
    elapsed_time_minutes = round(elapsed_time / 60, 1)
    print("--- %s minutes ---" % (elapsed_time_minutes))




urls = [f"https://www.assemblee-nationale.fr/dyn/opendata/PRJLANR5L15B{i:04d}.html" for i in range(
    0, 5000)]
main(urls)
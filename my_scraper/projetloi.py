# Ajout des imports nécessaires
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

# Définition de la classe TextInformation
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

class WebScraper:
    def __init__(self, urls):
        self.urls = urls
        self.result = []
        
    def scrape(self, output_file):
        for url in tqdm(self.urls):
            print("Processing: ", url)
            text_info = TextInformation(url)
            information = text_info.get_information()
            date = text_info.get_date()
            texts = text_info.get_texts()
            helo = text_info.get_helo()
            self.result.append({
                'url': url,
                'information': information,
                'date': date,
                'texts': texts,
                'helo': helo
            })
            time.sleep(0.1) # Pause de 0.1 seconde entre chaque requête pour éviter de surcharger le serveur
        
        # save scraped data to output file
        df = pd.DataFrame(self.result)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
    def clean_data(self, input_file, output_file):
        # check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: input file {input_file} not found.")
            return
            
        # read input file
        data = pd.read_csv(input_file)
        
        # clean the data
        to_analz_2 = data.replace(regex=[r'\[\''], value='').replace(regex=[r'\]\''], value='').replace(regex=[r'\\xa0'], value=' ')

        # remove output file if it already exists
        if os.path.exists(output_file):
            os.remove(output_file)

        # save cleaned data to output file
        to_analz_2.to_csv(output_file, index=False, encoding='utf-8-sig')

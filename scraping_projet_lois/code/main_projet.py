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
            year = words[-1].replace(".", "")
            return f"{day} {month} {year}"
        return None

    def get_motifs(self):
        try:
            div_assnat = self.soup.select('div.assnatSection2')
            #motifs = div_assnat[0].find_all('p', {'class': 'assnatLoiTexte'})
            motifs_text = [div_assnat.text.strip() for div_assnat in div_assnat]
            return motifs_text
        except Exception as e:
            motifs_text = None
            print("Erreur :", e)
            return motifs_text

    def get_projet_lois(self):
        try:
            section4 = self.soup.select('div.assnatSection4')
            if section4:
                # If section 4 exists, extract its content
                section4 = section4[0].find_all('p', {'class': 'assnatLoiTexte'})
                projet_lois = [motif.text.strip() for motif in section4]
            else:
                # If section 4 doesn't exist, extract the specified section
                projet_lois = self.soup.select('div.assnatSection3')
                projet_lois = projet_lois[0].find_all('p', {'class': 'assnatLoiTexte'})
                projet_lois = [motif.text.strip() for motif in projet_lois]

            return projet_lois
        except Exception as e:
            projet_lois = None
            return projet_lois

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
            motifs = text_info.get_motifs()
            projet_lois = text_info.get_projet_lois()
            if date is not None:
                self.result.append({
                    'url': url,
                    'information': information,
                    'date': date,
                    'motifs': motifs,
                    'projet_lois': projet_lois
                })

        
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
        to_analz_2 = data.replace(regex=[r'\[\''], value='').replace(regex=[r'\]\''], value='').replace(regex=[r'\\xa0'], value=' ').replace(regex=[r'\\"'], value='').replace(regex=[r'\\n'], value='').replace(regex=[r'\\t'], value='')

        if os.path.exists(output_file):
            os.remove(output_file)

        # save cleaned data to output file
        to_analz_2.to_csv(output_file, index=False, encoding='utf-8-sig')
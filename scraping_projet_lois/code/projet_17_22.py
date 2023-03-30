import main_projet as projetloi
urls = [f"https://www.assemblee-nationale.fr/dyn/opendata/PRJLANR5L15B{i:04d}.html" for i in range(
    0, 5200)]
scraper = projetloi.WebScraper(urls)
scraper.scrape('output_file.csv')
cleaner = projetloi.WebScraper(urls)
cleaner.clean_data('output_file.csv', 'output_file_cleaned.csv')
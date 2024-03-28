from funzioni_scraping_keywords_description import estrai_descrizione, crea_db

# Let's assume "file_path" is the path to your JSON file
file_path = r'C:\Users\Carletti\Downloads\Fintastico,Fleetmatica,flair-tech,FINSCIENCE,Fees,Feelera.json'
descrizioni, startup_data = estrai_descrizione(file_path)
output_file = r'C:\Users\Carletti\Desktop\startup_database.csv'
db_startup = crea_db(startup_data, output_file)


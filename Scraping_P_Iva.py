from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

siti_web = [
    "https://www.busforfun.com/",
    "https://www.kilometrorosso.com/"
]

footer_data_list = []

for sito in siti_web:
    driver.get(sito)

    footer = driver.find_element(By.TAG_NAME, value="footer")
    footer_text = {footer.text}
    footer_data_list.append({"Footer Content": footer_text})


driver.quit()

footer_df = pd.DataFrame(footer_data_list)
footer_df.to_csv("partita_iva.csv", index=False)


#def scraping_footer(siti_web):
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_experimental_option("detach", True)

#    driver = webdriver.Chrome(options=chrome_options)

#    footer_data_list = []

#    for sito in siti_web:
#        driver.get(sito)

#        footer = driver.find_element(By.TAG_NAME, value="footer")
#        footer_text = footer.text
#        footer_data_list.append({"Site": sito, "Footer Content": footer_text})

#    driver.quit()

#    footer_df = pd.DataFrame(footer_data_list)
#    footer_df.to_csv("footer_content.csv", index=False)
#    return footer_df

#def extract_piva_from_csv(csv_file):
#    df = pd.read_csv(csv_file)
#    piva_list = []

#    for index, row in df.iterrows():
#        footer_content = row["Footer Content"]
#        piva_match = re.search(r'(P\.IVA|P\.I\.)\s*([0-9]{11,12})', footer_content)
#        if piva_match:
#            piva_list.append({"Site": row["Site"], "Partita IVA": piva_match.group(2)})

#    piva_df = pd.DataFrame(piva_list)
#    piva_df.to_csv("piva_numbers.csv", index=False)
#    return piva_df

# Esempio di utilizzo
#siti_web = [
#    "https://www.busforfun.com/",
#    "https://www.kilometrorosso.com/"
#]

# Esegui la funzione di scraping per ottenere il dataframe con i contenuti del footer
# footer_df = scraping_footer(siti_web)

# Estrai la Partita IVA dal dataframe e salvala in un nuovo file CSV
# extract_piva_from_csv("footer_content.csv")
import pandas as pd
import spacy

# Carica il file JSON contenente le informazioni sulle startup
startup_data = pd.read_json(r'C:\Users\Carletti\Downloads\Fintastico,Fleetmatica,flair-tech,FINSCIENCE,Fees,Feelera.json', lines=True)

# Assicurati che il DataFrame contenga le informazioni desiderate
print(startup_data.head())

# Estrai le descrizioni delle startup
descriptions = startup_data['description']

# Visualizza le prime descrizioni per verificare
print(descriptions.head())


# Carica il modello linguistico di SpaCy per la lingua inglese
nlp = spacy.load("en_core_web_sm")

# Funzione per estrarre verbi e complementi oggetto da una descrizione
def extract_verbs_objects(description):
    doc = nlp(description)
    verbs = []
    objects = []
    for token in doc:
        if token.pos_ == "VERB":
            verbs.append(token.lemma_)
            for child in token.children:
                if child.dep_ == "dobj":
                    objects.append(child.text)
    return verbs, objects

# Dizionario per memorizzare i verbi e i complementi oggetto per ogni startup
startup_verbs_objects = {}


# Stampa i risultati per ogni startup
for startup_name, data in startup_verbs_objects.items():
    print("Startup:", startup_name)
    print("Verbi:", data['Verbi'])
    print("Complementi oggetto:", data['Complementi oggetto'])
    print()


# Esegui l'estrazione per ciascuna descrizione di ogni startup
startup_data_list = []

# Esegui l'estrazione per ciascuna descrizione di ogni startup
for startup_name, website, description in zip(startup_data['name'], startup_data['website'], startup_data['description']):
    verbs, objects = extract_verbs_objects(description)
    startup_data_list.append({'Startup': startup_name, 'Sito web': website, 'Verbi': verbs, 'Complementi oggetto': objects})

# Creazione di un DataFrame dai dati della lista di dizionari
df = pd.DataFrame(startup_data_list)

print (df)


 ###NON HO SALVATO IL DATAFRAME COME CSV

keyword_data = pd.read_csv(r'C:\Users\Carletti\Downloads\blendX_Tech radar_ARCHITETTURA_ Coresignal .csv')

# Assicurati che il DataFrame contenga le informazioni desiderate
print(keyword_data.head())

# Estrai le keyword dalla colonna appropriata
keywords = keyword_data.iloc[:, 0]  # Sostituisci 'keyword_column_name' con il nome effettivo della colonna contenente le keyword

# Visualizza le prime keyword per verificare
print(keywords)


# Lista per memorizzare i match trovati
matches = []

# Itera su ogni riga del DataFrame delle startup
for index, row in df.iterrows():
    startup_name = row['Startup']
    website = row['Sito web']
    verbs, objects = extract_verbs_objects(description)
    
    # Confronta le keywords con i verbi e i complementi oggetto
    for keyword in keywords:
        if keyword in verbs or keyword in objects:
            matches.append({'name': startup_name, 'website': website, 'Keyword': keyword})

# Crea un nuovo DataFrame con i match trovati
matches_df = pd.DataFrame(matches)

# Salva il nuovo DataFrame in un file CSV
matches_df.to_csv('matches.csv', index=False)

# Visualizza il nuovo DataFrame
print(matches_df)
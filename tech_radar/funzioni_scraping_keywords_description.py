import pandas as pd
import spacy
from collections import Counter

# Carica il modello linguistico di SpaCy per la lingua italiana
nlp = spacy.load("en_core_web_sm")

def estrai_descrizione(file_path):
    # Carica il file JSON delle startup e crea il DataFrame
    startup_data = pd.read_json(file_path, lines=True)
    # Estrai le descrizioni delle startup
    descrizioni = startup_data['description']
    return descrizioni, startup_data

def estrai_elementi(descrizione):
    sostantivi_aggettivi = []
    verbi = []
    doc = nlp(descrizione)
    for token in doc:
        if token.pos_ in ['NOUN', 'ADJ']:
            sostantivi_aggettivi.append(token.text)
        elif token.pos_ == 'VERB':
            verbi.append(token.lemma_)
    return sostantivi_aggettivi, verbi

def crea_db(startup_data, output_file):
    db_startup = []
    
    # Funzione locale per contare le frequenze
    def conta_frequenza(lista):
        return dict(Counter(lista))
    
    for name, website, description in zip(startup_data['name'], startup_data['website'], startup_data['description']):
        sostantivi_aggettivi, verbi = estrai_elementi(description)
        
        # Calcola le frequenze di sostantivi/aggettivi e verbi
        freq_sostantivi_aggettivi = conta_frequenza(sostantivi_aggettivi)
        freq_verbi = conta_frequenza(verbi)
        
        # Aggiungi le informazioni al database
        db_startup.append({
            'name': name,
            'website': website,
            'sostantivi_aggettivi': sostantivi_aggettivi,
            'conteggio_sostantivi_aggettivi': freq_sostantivi_aggettivi,
            'verbi': verbi,
            'conteggio_verbi': freq_verbi
        })
        
    # Salva i risultati come file CSV
    df = pd.DataFrame(db_startup)
    df.to_csv(output_file, index=False)
    print(f"I risultati sono stati salvati su {output_file}")
    
    return db_startup

# Let's assume "file_path" is the path to your JSON file
file_path = r'C:\Users\Carletti\Downloads\Fintastico,Fleetmatica,flair-tech,FINSCIENCE,Fees,Feelera.json'
descrizioni, startup_data = estrai_descrizione(file_path)
output_file = r'C:\Users\Carletti\Desktop\startup_database.csv'
db_startup = crea_db(startup_data, output_file)






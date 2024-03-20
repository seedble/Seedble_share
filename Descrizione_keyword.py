import spacy
nlp = spacy.load("en_core_web_sm")

# Descrizione
text = "BusForFun Business is the European leader in B2B integrated mobility solutions, helping complex organizations to run and improve their employees transportation services."

doc = nlp(text)
# Parole chiave dalla tabella_keyword
#tabella_keyword = ["B2B", "mobility solution", "transportation", "fatture", ""]

print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

# Estrazione delle parole chiave dalla descrizione
# parole_chiave_trovate = []
#for parola_chiave in tabella_keyword:
#    if parola_chiave.lower() in descrizione.lower():
#        parole_chiave_trovate.append(parola_chiave)

# Creazione della nuova colonna keyword
#keyword = ", ".join(parole_chiave_trovate)

# Stampare la descrizione e le parole chiave trovate
#print("Descrizione:", descrizione)
#print("Keyword:", keyword)

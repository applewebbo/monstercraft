import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from game.models import HangmanWord

words = [
    # 5-8 ANNI
    ("CANE", "Migliore amico dell'uomo", 1, "5-8"),
    ("GATTO", "Animale che fa miao", 1, "5-8"),
    ("MELA", "Frutto rosso o verde", 1, "5-8"),
    ("GIOCO", "Attività divertente", 1, "5-8"),
    ("BIMBO", "Un bambino piccolo", 1, "5-8"),
    ("FIORE", "Profuma in primavera", 2, "5-8"),
    ("CIELO", "Azzurro e grandissimo", 2, "5-8"),
    ("CUORE", "Simbolo dell'amore", 2, "5-8"),
    ("STELLA", "Brilla nel cielo notturno", 2, "5-8"),
    ("SORRISO", "Si fa quando si è felici", 3, "5-8"),
    ("PALLONCINO", "Si gonfia alle feste", 3, "5-8"),
    ("ARCOBALENO", "I sette colori dopo la pioggia", 3, "5-8"),
    # 9-12 ANNI
    ("ALBERO", "Ha foglie e tronco", 1, "9-12"),
    ("SCUOLA", "Dove si va per imparare", 1, "9-12"),
    ("MUSICA", "Si ascolta e si balla", 1, "9-12"),
    ("PIANETA", "La Terra lo è", 1, "9-12"),
    ("CORAGGIO", "Forza d'animo", 2, "9-12"),
    ("SQUADRA", "Un gruppo unito che gioca insieme", 2, "9-12"),
    ("FANTASIA", "Immaginare mondi magici", 2, "9-12"),
    ("SCOPERTA", "Trovare qualcosa di nuovo", 2, "9-12"),
    ("VITTORIA", "Quando si vince una gara", 2, "9-12"),
    ("AVVENTURA", "Un viaggio emozionante", 3, "9-12"),
    ("SPETTACOLO", "Cose bellissime da guardare", 3, "9-12"),
    ("INVENZIONE", "Creare qualcosa che non esisteva", 3, "9-12"),
    ("CONOSCENZA", "Sapere tante cose nuove", 3, "9-12"),
    # 13-17 ANNI
    ("INTERNET", "La rete globale", 1, "13-17"),
    ("COMPUTER", "Macchina per elaborare dati", 1, "13-17"),
    ("SISTEMA", "Insieme di elementi connessi", 1, "13-17"),
    ("GALASSIA", "Insieme di stelle e pianeti", 2, "13-17"),
    ("ELETTRONE", "Particella con carica negativa", 2, "13-17"),
    ("HARDWARE", "Componenti fisiche di un PC", 2, "13-17"),
    ("SOFTWARE", "I programmi di un computer", 2, "13-17"),
    ("ATOMO", "L'unità base della materia", 2, "13-17"),
    ("ALGORITMO", "Sequenza logica di istruzioni", 3, "13-17"),
    ("METABOLISMO", "Insieme delle reazioni chimiche nel corpo", 3, "13-17"),
    ("CRITTOGRAFIA", "Tecnica per nascondere messaggi", 3, "13-17"),
    ("ECOSISTEMA", "Ambiente e organismi che lo abitano", 3, "13-17"),
    # ADULT
    ("ECONOMIA", "Scienza che studia produzione e consumo", 1, "ADULT"),
    ("POLITICA", "Arte del governare", 1, "ADULT"),
    ("SOCIETA", "Insieme di individui", 1, "ADULT"),
    ("ELEZIONI", "Si va a votare", 1, "ADULT"),
    ("INFLAZIONE", "Aumento generale dei prezzi", 2, "ADULT"),
    ("DEMOCRAZIA", "Forma di governo", 2, "ADULT"),
    ("SINDACATO", "Associazione di lavoratori", 2, "ADULT"),
    ("MERCATO", "Luogo di scambio economico", 2, "ADULT"),
    ("REFERENDUM", "Votazione popolare diretta", 3, "ADULT"),
    ("MACROECONOMIA", "Studio del sistema economico globale", 3, "ADULT"),
    ("PSICANALISI", "Teoria fondata da Freud", 3, "ADULT"),
    ("GLOBALIZZAZIONE", "Mercato unico mondiale", 3, "ADULT"),
    ("NEUROSCIENZE", "Studio del sistema nervoso", 3, "ADULT"),
]

print("Cancellazione vecchie parole in corso...")
HangmanWord.objects.all().delete()

for w, h, d, age in words:
    HangmanWord.objects.create(word=w, hint=h, difficulty=d, age_group=age)

print(f"Caricate {len(words)} nuove parole per l'impiccato suddivise per fasce d'età!")

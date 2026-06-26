import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from game.models import Question

questions_data = [
    # MATH - Dif 1
    {"c": "MATH", "d": 1, "t": "Quanto fa 7 + 8?", "o1": "13", "o2": "14", "o3": "15", "o4": "16", "co": 3},
    {"c": "MATH", "d": 1, "t": "Quanto fa 9 x 5?", "o1": "45", "o2": "50", "o3": "40", "o4": "35", "co": 1},
    {"c": "MATH", "d": 1, "t": "Se ho 10 mele e ne mangio 3, quante ne restano?", "o1": "6", "o2": "7", "o3": "8", "o4": "9", "co": 2},
    {"c": "MATH", "d": 1, "t": "Quanto fa 20 diviso 4?", "o1": "3", "o2": "4", "o3": "5", "o4": "6", "co": 3},
    {"c": "MATH", "d": 1, "t": "Qual è il doppio di 14?", "o1": "24", "o2": "26", "o3": "28", "o4": "30", "co": 3},
    # MATH - Dif 2
    {"c": "MATH", "d": 2, "t": "Qual è la radice quadrata di 81?", "o1": "7", "o2": "8", "o3": "9", "o4": "10", "co": 3},
    {"c": "MATH", "d": 2, "t": "Risolvi: 25% di 80", "o1": "15", "o2": "20", "o3": "25", "o4": "30", "co": 2},
    {"c": "MATH", "d": 2, "t": "Quanto fa 12 x 12?", "o1": "124", "o2": "132", "o3": "144", "o4": "156", "co": 3},
    {"c": "MATH", "d": 2, "t": "Risolvi: 3 + 5 x 2", "o1": "16", "o2": "13", "o3": "10", "o4": "15", "co": 2},
    {"c": "MATH", "d": 2, "t": "Quanto fa 7 elevato alla seconda?", "o1": "14", "o2": "49", "o3": "42", "o4": "21", "co": 2},
    # MATH - Dif 3
    {"c": "MATH", "d": 3, "t": "Risolvi l'equazione: 3x - 4 = 11", "o1": "x=4", "o2": "x=5", "o3": "x=6", "o4": "x=3", "co": 2},
    {"c": "MATH", "d": 3, "t": "Qual è l'area di un triangolo con base 10 e altezza 5?", "o1": "25", "o2": "50", "o3": "15", "o4": "30", "co": 1},
    {"c": "MATH", "d": 3, "t": "Calcola il M.C.D. tra 24 e 36", "o1": "4", "o2": "6", "o3": "12", "o4": "18", "co": 3},
    {"c": "MATH", "d": 3, "t": "Qual è il logaritmo in base 2 di 8?", "o1": "2", "o2": "3", "o3": "4", "o4": "16", "co": 2},
    {"c": "MATH", "d": 3, "t": "Risolvi: (4 + 2)^2 - 10", "o1": "26", "o2": "14", "o3": "36", "o4": "20", "co": 1},

    # GEO - Dif 1
    {"c": "GEO", "d": 1, "t": "Qual è la capitale della Spagna?", "o1": "Barcellona", "o2": "Siviglia", "o3": "Madrid", "o4": "Valencia", "co": 3},
    {"c": "GEO", "d": 1, "t": "In quale continente si trova l'Egitto?", "o1": "Europa", "o2": "Asia", "o3": "Africa", "o4": "America", "co": 3},
    {"c": "GEO", "d": 1, "t": "Qual è l'oceano più grande?", "o1": "Atlantico", "o2": "Indiano", "o3": "Pacifico", "o4": "Artico", "co": 3},
    {"c": "GEO", "d": 1, "t": "La forma dell'Italia ricorda...", "o1": "Uno stivale", "o2": "Una chitarra", "o3": "Una stella", "o4": "Un quadrato", "co": 1},
    {"c": "GEO", "d": 1, "t": "Roma è la capitale di quale stato?", "o1": "Spagna", "o2": "Francia", "o3": "Italia", "o4": "Grecia", "co": 3},
    # GEO - Dif 2
    {"c": "GEO", "d": 2, "t": "Qual è il fiume più lungo d'Europa?", "o1": "Danubio", "o2": "Reno", "o3": "Volga", "o4": "Tamigi", "co": 3},
    {"c": "GEO", "d": 2, "t": "La capitale del Canada è...", "o1": "Toronto", "o2": "Vancouver", "o3": "Montreal", "o4": "Ottawa", "co": 4},
    {"c": "GEO", "d": 2, "t": "Qual è la montagna più alta del mondo?", "o1": "K2", "o2": "Monte Bianco", "o3": "Everest", "o4": "Kilimangiaro", "co": 3},
    {"c": "GEO", "d": 2, "t": "Quanti sono gli Stati Uniti d'America?", "o1": "48", "o2": "50", "o3": "52", "o4": "51", "co": 2},
    {"c": "GEO", "d": 2, "t": "Qual è l'isola più grande del mondo?", "o1": "Australia", "o2": "Groenlandia", "o3": "Madagascar", "o4": "Gran Bretagna", "co": 2},
    # GEO - Dif 3
    {"c": "GEO", "d": 3, "t": "Quale stretto separa la Spagna dal Marocco?", "o1": "Stretto di Messina", "o2": "Stretto di Gibilterra", "o3": "Stretto di Bering", "o4": "Stretto di Magellano", "co": 2},
    {"c": "GEO", "d": 3, "t": "Qual è la capitale dell'Islanda?", "o1": "Oslo", "o2": "Helsinki", "o3": "Reykjavik", "o4": "Stoccolma", "co": 3},
    {"c": "GEO", "d": 3, "t": "Il deserto di Atacama si trova in...", "o1": "Cile", "o2": "Egitto", "o3": "Mongolia", "o4": "Stati Uniti", "co": 1},
    {"c": "GEO", "d": 3, "t": "Quale paese europeo è diviso in cantoni?", "o1": "Germania", "o2": "Austria", "o3": "Svizzera", "o4": "Belgio", "co": 3},
    {"c": "GEO", "d": 3, "t": "Qual è il lago più grande per estensione d'Italia?", "o1": "Lago Maggiore", "o2": "Lago di Como", "o3": "Lago di Garda", "o4": "Lago d'Iseo", "co": 3},

    # ENG - Dif 1
    {"c": "ENG", "d": 1, "t": "Come si dice 'Libro' in inglese?", "o1": "Pen", "o2": "Book", "o3": "Table", "o4": "Chair", "co": 2},
    {"c": "ENG", "d": 1, "t": "Come si traduce 'Hello'?", "o1": "Addio", "o2": "Ciao", "o3": "Grazie", "o4": "Prego", "co": 2},
    {"c": "ENG", "d": 1, "t": "Come si dice 'Cane' in inglese?", "o1": "Cat", "o2": "Dog", "o3": "Bird", "o4": "Fish", "co": 2},
    {"c": "ENG", "d": 1, "t": "Qual è il verbo 'essere' alla prima persona singolare?", "o1": "I am", "o2": "I is", "o3": "I are", "o4": "I be", "co": 1},
    {"c": "ENG", "d": 1, "t": "Che colore è 'Red'?", "o1": "Giallo", "o2": "Rosso", "o3": "Verde", "o4": "Blu", "co": 2},
    # ENG - Dif 2
    {"c": "ENG", "d": 2, "t": "Qual è il plurale irregolare di 'Man'?", "o1": "Mans", "o2": "Menses", "o3": "Men", "o4": "Manes", "co": 3},
    {"c": "ENG", "d": 2, "t": "Cosa significa 'Breakfast'?", "o1": "Pranzo", "o2": "Cena", "o3": "Colazione", "o4": "Merenda", "co": 3},
    {"c": "ENG", "d": 2, "t": "Scegli il passato remoto (past simple) di 'See'", "o1": "Seed", "o2": "Seen", "o3": "Saw", "o4": "Seeing", "co": 3},
    {"c": "ENG", "d": 2, "t": "Completa: 'She ___ to the cinema yesterday'", "o1": "go", "o2": "goes", "o3": "went", "o4": "gone", "co": 3},
    {"c": "ENG", "d": 2, "t": "Cosa significa 'Awesome'?", "o1": "Terribile", "o2": "Noioso", "o3": "Fantastico", "o4": "Strano", "co": 3},
    # ENG - Dif 3
    {"c": "ENG", "d": 3, "t": "Che cosa indica l'idioma 'Piece of cake'?", "o1": "Un dolce", "o2": "Una cosa molto facile", "o3": "Un grosso problema", "o4": "Un segreto", "co": 2},
    {"c": "ENG", "d": 3, "t": "Qual è il Present Perfect di 'Eat'?", "o1": "Has eaten", "o2": "Ate", "o3": "Has ate", "o4": "Eating", "co": 1},
    {"c": "ENG", "d": 3, "t": "Scegli il sinonimo di 'Stubborn'", "o1": "Happy", "o2": "Sad", "o3": "Obstinate", "o4": "Clever", "co": 3},
    {"c": "ENG", "d": 3, "t": "Cosa vuol dire il phrasal verb 'Look forward to'?", "o1": "Guardare indietro", "o2": "Non vedere l'ora", "o3": "Cercare qualcosa", "o4": "Ignorare", "co": 2},
    {"c": "ENG", "d": 3, "t": "Quale parola è scritta correttamente?", "o1": "Accommodate", "o2": "Acommodate", "o3": "Accomodate", "o4": "Accomodati", "co": 1},

    # CHEM - Dif 1
    {"c": "CHEM", "d": 1, "t": "Qual è il simbolo chimico dell'Oro?", "o1": "Or", "o2": "Au", "o3": "Ag", "o4": "O", "co": 2},
    {"c": "CHEM", "d": 1, "t": "Qual è la formula chimica dell'anidride carbonica?", "o1": "CO2", "o2": "CO", "o3": "H2O", "o4": "O2", "co": 1},
    {"c": "CHEM", "d": 1, "t": "L'acqua allo stato solido si chiama...", "o1": "Gas", "o2": "Vapore", "o3": "Ghiaccio", "o4": "Roccia", "co": 3},
    {"c": "CHEM", "d": 1, "t": "Quale sostanza usiamo per salare il cibo?", "o1": "Zucchero", "o2": "Sale da cucina", "o3": "Pepe", "o4": "Bicarbonato", "co": 2},
    {"c": "CHEM", "d": 1, "t": "Simbolo chimico dell'idrogeno?", "o1": "I", "o2": "Id", "o3": "H", "o4": "Ho", "co": 3},
    # CHEM - Dif 2
    {"c": "CHEM", "d": 2, "t": "Chi inventò la tavola periodica degli elementi?", "o1": "Newton", "o2": "Mendeleev", "o3": "Einstein", "o4": "Galileo", "co": 2},
    {"c": "CHEM", "d": 2, "t": "Qual è il gas nobile usato nei palloncini per farli volare?", "o1": "Elio", "o2": "Argo", "o3": "Neo", "o4": "Xeno", "co": 1},
    {"c": "CHEM", "d": 2, "t": "Quanti protoni ha un atomo di Carbonio?", "o1": "4", "o2": "6", "o3": "8", "o4": "12", "co": 2},
    {"c": "CHEM", "d": 2, "t": "Una sostanza con pH 2 è considerata...", "o1": "Basica", "o2": "Neutra", "o3": "Acida", "o4": "Metallica", "co": 3},
    {"c": "CHEM", "d": 2, "t": "Qual è il simbolo del Sodio?", "o1": "So", "o2": "S", "o3": "Na", "o4": "Nd", "co": 3},
    # CHEM - Dif 3
    {"c": "CHEM", "d": 3, "t": "Quale di questi è un metallo alcalino?", "o1": "Magnesio", "o2": "Litio", "o3": "Ferro", "o4": "Rame", "co": 2},
    {"c": "CHEM", "d": 3, "t": "Che tipo di legame si forma tra un metallo e un non-metallo?", "o1": "Covalente", "o2": "Ionico", "o3": "Metallico", "o4": "A idrogeno", "co": 2},
    {"c": "CHEM", "d": 3, "t": "Qual è il nome IUPAC dell'acido acetico?", "o1": "Acido metanoico", "o2": "Acido propanoico", "o3": "Acido etanoico", "o4": "Acido butanoico", "co": 3},
    {"c": "CHEM", "d": 3, "t": "Cosa indica il numero di Avogadro?", "o1": "Massa di un elettrone", "o2": "Numero di particelle in una mole", "o3": "Velocità della luce", "o4": "Costante di gravità", "co": 2},
    {"c": "CHEM", "d": 3, "t": "La formula del glucosio è...", "o1": "C6H12O6", "o2": "C12H22O11", "o3": "CH4", "o4": "CO2", "co": 1},

    # SCI - Dif 1
    {"c": "SCI", "d": 1, "t": "Quale organo pompa il sangue nel corpo?", "o1": "Polmoni", "o2": "Cervello", "o3": "Cuore", "o4": "Fegato", "co": 3},
    {"c": "SCI", "d": 1, "t": "Di che colore sono le foglie che fanno la fotosintesi?", "o1": "Rosso", "o2": "Verde", "o3": "Giallo", "o4": "Blu", "co": 2},
    {"c": "SCI", "d": 1, "t": "Che animale è la rana?", "o1": "Rettile", "o2": "Anfibio", "o3": "Mammifero", "o4": "Pesce", "co": 2},
    {"c": "SCI", "d": 1, "t": "Il sole è un pianeta o una stella?", "o1": "Pianeta", "o2": "Stella", "o3": "Asteroide", "o4": "Cometa", "co": 2},
    {"c": "SCI", "d": 1, "t": "Quanti sensi ha tradizionalmente l'essere umano?", "o1": "4", "o2": "5", "o3": "6", "o4": "7", "co": 2},
    # SCI - Dif 2
    {"c": "SCI", "d": 2, "t": "Quale parte della cellula contiene il DNA?", "o1": "Mitocondrio", "o2": "Citoplasma", "o3": "Nucleo", "o4": "Membrana", "co": 3},
    {"c": "SCI", "d": 2, "t": "Come si chiama la forza che ci tiene ancorati a terra?", "o1": "Magnetismo", "o2": "Gravità", "o3": "Inerzia", "o4": "Attrito", "co": 2},
    {"c": "SCI", "d": 2, "t": "Qual è il mammifero più grande della terra?", "o1": "Elefante", "o2": "Giraffa", "o3": "Balenottera azzurra", "o4": "Orca", "co": 3},
    {"c": "SCI", "d": 2, "t": "Chi formulò la teoria della relatività?", "o1": "Newton", "o2": "Galileo", "o3": "Einstein", "o4": "Darwin", "co": 3},
    {"c": "SCI", "d": 2, "t": "Come si chiamano le cellule rosse del sangue?", "o1": "Leucociti", "o2": "Trombociti", "o3": "Eritrociti", "o4": "Neuroni", "co": 3},
    # SCI - Dif 3
    {"c": "SCI", "d": 3, "t": "Cos'è un buco nero?", "o1": "Un pianeta vuoto", "o2": "Una stella collassata con gravità immensa", "o3": "Una nuvola di gas", "o4": "Un'illusione ottica", "co": 2},
    {"c": "SCI", "d": 3, "t": "Quale organello è la centrale energetica della cellula?", "o1": "Nucleo", "o2": "Ribosoma", "o3": "Apparato di Golgi", "o4": "Mitocondrio", "co": 4},
    {"c": "SCI", "d": 3, "t": "A quale temperatura l'acqua ha la massima densità?", "o1": "0 °C", "o2": "4 °C", "o3": "100 °C", "o4": "-4 °C", "co": 2},
    {"c": "SCI", "d": 3, "t": "Chi è considerato il padre della genetica?", "o1": "Darwin", "o2": "Pasteur", "o3": "Mendel", "o4": "Fleming", "co": 3},
    {"c": "SCI", "d": 3, "t": "In fisica, cosa descrive la Seconda Legge di Newton?", "o1": "F = m * a", "o2": "E = mc^2", "o3": "Azione e reazione", "o4": "Conservazione dell'energia", "co": 1},

    # ITA - Dif 1
    {"c": "ITA", "d": 1, "t": "Qual è il plurale di 'Lupo'?", "o1": "Lupe", "o2": "Lupi", "o3": "Lupis", "o4": "Lupas", "co": 2},
    {"c": "ITA", "d": 1, "t": "Che tempo verbale è 'Io mangio'?", "o1": "Passato prossimo", "o2": "Futuro", "o3": "Presente", "o4": "Imperfetto", "co": 3},
    {"c": "ITA", "d": 1, "t": "L'alfabeto italiano quante lettere contiene (senza straniere)?", "o1": "21", "o2": "26", "o3": "24", "o4": "18", "co": 1},
    {"c": "ITA", "d": 1, "t": "Completa: 'Rosso di sera bel tempo si...'", "o1": "Avvera", "o2": "Spera", "o3": "Fa", "o4": "Domani", "co": 2},
    {"c": "ITA", "d": 1, "t": "Quale parola ha un accento sbagliato?", "o1": "Perché", "o2": "Caffè", "o3": "Citta", "o4": "Papà", "co": 3},
    # ITA - Dif 2
    {"c": "ITA", "d": 2, "t": "Come si chiama un nome che deriva da un altro (es. fiore -> fioraio)?", "o1": "Alterato", "o2": "Derivato", "o3": "Primitivo", "o4": "Composto", "co": 2},
    {"c": "ITA", "d": 2, "t": "In quale secolo visse Dante Alighieri?", "o1": "XII", "o2": "XIII-XIV", "o3": "XV", "o4": "XVI", "co": 2},
    {"c": "ITA", "d": 2, "t": "Come si dice correttamente?", "o1": "Qual'è", "o2": "Qual' e", "o3": "Qual è", "o4": "Qual' è", "co": 3},
    {"c": "ITA", "d": 2, "t": "Che figura retorica è 'Il mare sorrideva'?", "o1": "Personificazione", "o2": "Ossimoro", "o3": "Litote", "o4": "Sinestesia", "co": 1},
    {"c": "ITA", "d": 2, "t": "Cosa esprime il modo congiuntivo?", "o1": "Certezza", "o2": "Ordine", "o3": "Dubbio o desiderio", "o4": "Azione passata", "co": 3},
    # ITA - Dif 3
    {"c": "ITA", "d": 3, "t": "Chi è l'autore della raccolta di poesie 'Ossi di seppia'?", "o1": "Ungaretti", "o2": "Quasimodo", "o3": "Saba", "o4": "Montale", "co": 4},
    {"c": "ITA", "d": 3, "t": "Che tipo di subordinata è: 'Penso che tu abbia ragione'?", "o1": "Causale", "o2": "Oggettiva", "o3": "Soggettiva", "o4": "Relativa", "co": 2},
    {"c": "ITA", "d": 3, "t": "Come si chiama una rima in cui la parola finale coincide solo per le vocali?", "o1": "Assonanza", "o2": "Consonanza", "o3": "Baciata", "o4": "Alternata", "co": 1},
    {"c": "ITA", "d": 3, "t": "Chi scrisse 'Il fu Mattia Pascal'?", "o1": "Pirandello", "o2": "Svevo", "o3": "D'Annunzio", "o4": "Verga", "co": 1},
    {"c": "ITA", "d": 3, "t": "Qual è l'anagramma perfetto di 'Calendario'?", "o1": "Locandiera", "o2": "Almanacco", "o3": "Decoraliano", "o4": "Nessuno", "co": 1},

    # HIST - Dif 1
    {"c": "HIST", "d": 1, "t": "Chi ha scoperto l'America?", "o1": "Vasco da Gama", "o2": "Cristoforo Colombo", "o3": "Magellano", "o4": "Marco Polo", "co": 2},
    {"c": "HIST", "d": 1, "t": "In che anno è stata scoperta l'America?", "o1": "1492", "o2": "1500", "o3": "1392", "o4": "1453", "co": 1},
    {"c": "HIST", "d": 1, "t": "Chi era il re degli dei nell'antica Roma?", "o1": "Zeus", "o2": "Apollo", "o3": "Giove", "o4": "Marte", "co": 3},
    {"c": "HIST", "d": 1, "t": "Come si chiamavano gli antichi sovrani egizi?", "o1": "Imperatori", "o2": "Zar", "o3": "Faraoni", "o4": "Re", "co": 3},
    {"c": "HIST", "d": 1, "t": "Quale popolo ha costruito il Colosseo?", "o1": "I Greci", "o2": "I Romani", "o3": "Gli Egizi", "o4": "Gli Etruschi", "co": 2},
    # HIST - Dif 2
    {"c": "HIST", "d": 2, "t": "Chi fu il primo Imperatore Romano?", "o1": "Giulio Cesare", "o2": "Ottaviano Augusto", "o3": "Nerone", "o4": "Traiano", "co": 2},
    {"c": "HIST", "d": 2, "t": "Quando è finita la Seconda Guerra Mondiale?", "o1": "1943", "o2": "1945", "o3": "1948", "o4": "1950", "co": 2},
    {"c": "HIST", "d": 2, "t": "Dove è nato Napoleone Bonaparte?", "o1": "A Parigi", "o2": "In Corsica", "o3": "A Roma", "o4": "In Sicilia", "co": 2},
    {"c": "HIST", "d": 2, "t": "Chi dipinse il soffitto della Cappella Sistina?", "o1": "Leonardo da Vinci", "o2": "Raffaello", "o3": "Michelangelo", "o4": "Caravaggio", "co": 3},
    {"c": "HIST", "d": 2, "t": "Quale evento storico ha segnato l'inizio della Rivoluzione Francese?", "o1": "Presa della Bastiglia", "o2": "Morte di Luigi XVI", "o3": "Battaglia di Waterloo", "o4": "Trattato di Versailles", "co": 1},
    # HIST - Dif 3
    {"c": "HIST", "d": 3, "t": "Quale patto firmarono Germania e URSS prima della 2° Guerra Mondiale?", "o1": "Patto Atlantico", "o2": "Patto Ribbentrop-Molotov", "o3": "Trattato di Yalta", "o4": "Patto d'Acciaio", "co": 2},
    {"c": "HIST", "d": 3, "t": "In che anno cadde l'Impero Romano d'Occidente?", "o1": "476 d.C.", "o2": "1453 d.C.", "o3": "312 d.C.", "o4": "410 d.C.", "co": 1},
    {"c": "HIST", "d": 3, "t": "Chi guidò i Mille nella spedizione del 1860?", "o1": "Mazzini", "o2": "Cavour", "o3": "Garibaldi", "o4": "Vittorio Emanuele II", "co": 3},
    {"c": "HIST", "d": 3, "t": "Come si chiamava la regina di Francia ghigliottinata nel 1793?", "o1": "Maria Stuarda", "o2": "Maria Teresa", "o3": "Maria Antonietta", "o4": "Caterina de' Medici", "co": 3},
    {"c": "HIST", "d": 3, "t": "Chi è stato il primo Presidente degli Stati Uniti d'America?", "o1": "Abraham Lincoln", "o2": "Thomas Jefferson", "o3": "George Washington", "o4": "John Adams", "co": 3},
]

for q in questions_data:
    Question.objects.update_or_create(
        text=q["t"],
        defaults={
            "category": q["c"],
            "difficulty": q["d"],
            "option_1": q["o1"],
            "option_2": q["o2"],
            "option_3": q["o3"],
            "option_4": q["o4"],
            "correct_option": q["co"]
        }
    )

print(f"Inserite o aggiornate {len(questions_data)} domande con successo!")

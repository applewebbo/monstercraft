import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from game.models import Question

# Hardcoded Logic and Extra questions
extra_questions = [
    # 5-8 LOGIC
    {"age": "5-8", "c": "LOGIC", "d": 1, "t": "Se oggi è lunedì, che giorno è domani?", "o1": "Domenica", "o2": "Martedì", "o3": "Mercoledì", "o4": "Venerdì", "co": 2},
    {"age": "5-8", "c": "LOGIC", "d": 2, "t": "Qual è il contrario di 'Alto'?", "o1": "Grande", "o2": "Largo", "o3": "Basso", "o4": "Magro", "co": 3},
    {"age": "5-8", "c": "LOGIC", "d": 2, "t": "Il papà di Marco ha 3 figli: Qui, Quo e...?", "o1": "Qua", "o2": "Marco", "o3": "Pippo", "o4": "Gigi", "co": 2},
    {"age": "5-8", "c": "LOGIC", "d": 3, "t": "Se hai una mela e mezza, quanti mezzi hai in tutto?", "o1": "Due", "o2": "Tre", "o3": "Uno", "o4": "Quattro", "co": 2},
    {"age": "5-8", "c": "LOGIC", "d": 3, "t": "Trova l'intruso: Treno, Aereo, Macchina, Mela", "o1": "Treno", "o2": "Aereo", "o3": "Macchina", "o4": "Mela", "co": 4},
    
    # 9-12 LOGIC
    {"age": "9-12", "c": "LOGIC", "d": 1, "t": "Cosa diventa più grande più ne togli?", "o1": "Un buco", "o2": "Un palloncino", "o3": "Un debito", "o4": "Il pane", "co": 1},
    {"age": "9-12", "c": "LOGIC", "d": 2, "t": "Sono alto da giovane, basso da vecchio. Chi sono?", "o1": "L'albero", "o2": "La candela", "o3": "L'uomo", "o4": "Il gatto", "co": 2},
    {"age": "9-12", "c": "LOGIC", "d": 2, "t": "Se 3 gatti mangiano 3 topi in 3 minuti, 100 gatti quanto impiegano per 100 topi?", "o1": "100 minuti", "o2": "10 minuti", "o3": "3 minuti", "o4": "1 minuto", "co": 3},
    {"age": "9-12", "c": "LOGIC", "d": 3, "t": "Ho città senza case, fiumi senza acqua, mari senza pesci. Cosa sono?", "o1": "Il deserto", "o2": "Una mappa", "o3": "Un libro", "o4": "Lo spazio", "co": 2},
    {"age": "9-12", "c": "LOGIC", "d": 3, "t": "Quale parola di 5 lettere diventa più corta se le aggiungi 2 lettere?", "o1": "Porta", "o2": "Corta", "o3": "Treno", "o4": "Gatto", "co": 2},

    # 13-17 LOGIC
    {"age": "13-17", "c": "LOGIC", "d": 1, "t": "Se 5 macchine producono 5 pezzi in 5 minuti, quanto impiegano 100 macchine per 100 pezzi?", "o1": "100 minuti", "o2": "50 minuti", "o3": "5 minuti", "o4": "20 minuti", "co": 3},
    {"age": "13-17", "c": "LOGIC", "d": 2, "t": "Ci sono 3 mele, ne prendi 2. Quante mele hai?", "o1": "1", "o2": "2", "o3": "3", "o4": "0", "co": 2},
    {"age": "13-17", "c": "LOGIC", "d": 2, "t": "Un treno elettrico va verso nord. Verso dove va il fumo?", "o1": "Sud", "o2": "Est", "o3": "Nord", "o4": "Da nessuna parte", "co": 4},
    {"age": "13-17", "c": "LOGIC", "d": 3, "t": "Se Maria è la sorella dell'unica figlia di mia madre, chi è Maria per me?", "o1": "Mia madre", "o2": "Mia zia", "o3": "Mia sorella", "o4": "Sono io o mia sorella", "co": 4},
    {"age": "13-17", "c": "LOGIC", "d": 3, "t": "Quale numero manca: 1, 1, 2, 3, 5, 8, ...?", "o1": "10", "o2": "11", "o3": "12", "o4": "13", "co": 4},

    # ADULT LOGIC
    {"age": "ADULT", "c": "LOGIC", "d": 1, "t": "A quale sequenza appartiene il numero 21: 1, 2, 3, 5, 8...?", "o1": "Numeri primi", "o2": "Fibonacci", "o3": "Progressione geometrica", "o4": "Potenze di 2", "co": 2},
    {"age": "ADULT", "c": "LOGIC", "d": 2, "t": "Tutti gli X sono Y. Alcuni Y sono Z. Possiamo dedurre che...", "o1": "Tutti gli X sono Z", "o2": "Alcuni X sono Z", "o3": "Nessun X è Z", "o4": "Non si può dedurre la relazione tra X e Z", "co": 4},
    {"age": "ADULT", "c": "LOGIC", "d": 2, "t": "Un uomo guarda un ritratto e dice: 'Non ho fratelli o sorelle, ma il padre di quest'uomo è il figlio di mio padre'. Di chi è il ritratto?", "o1": "Del padre", "o2": "Di se stesso", "o3": "Del figlio", "o4": "Del nonno", "co": 3},
    {"age": "ADULT", "c": "LOGIC", "d": 3, "t": "Quante volte puoi sottrarre 10 da 100?", "o1": "10", "o2": "Una volta sola", "o3": "Infinite", "o4": "100", "co": 2},
    {"age": "ADULT", "c": "LOGIC", "d": 3, "t": "A è fratello di B. B è fratello di C. C è padre di D. Che cos'è A per D?", "o1": "Padre", "o2": "Zio", "o3": "Cugino", "o4": "Nonno", "co": 2},
]

# Generate random Math questions
math_questions = []

# 5-8 Math (Additions and subtractions under 20)
for _ in range(30):
    a = random.randint(1, 10)
    b = random.randint(1, 9)
    res = a + b
    options = [res, res+1, res-1, res+2]
    random.shuffle(options)
    co = options.index(res) + 1
    math_questions.append({
        "age": "5-8", "c": "MATH", "d": random.choice([1, 2]),
        "t": f"Quanto fa {a} + {b}?", "o1": str(options[0]), "o2": str(options[1]), "o3": str(options[2]), "o4": str(options[3]), "co": co
    })

# 9-12 Math (Multiplications and larger operations)
for _ in range(30):
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    res = a * b
    options = [res, res+a, res-b, res+2]
    random.shuffle(options)
    co = options.index(res) + 1
    math_questions.append({
        "age": "9-12", "c": "MATH", "d": random.choice([1, 2, 3]),
        "t": f"Quanto fa {a} x {b}?", "o1": str(options[0]), "o2": str(options[1]), "o3": str(options[2]), "o4": str(options[3]), "co": co
    })

# 13-17 Math (Algebra basics)
for _ in range(30):
    x = random.randint(2, 10)
    y = random.randint(2, 10)
    res = x * y
    # Equation: x * A = res, solve for A
    options = [y, y+1, y-1, y*2]
    random.shuffle(options)
    co = options.index(y) + 1
    math_questions.append({
        "age": "13-17", "c": "MATH", "d": random.choice([2, 3]),
        "t": f"Risolvi: {x}X = {res}. Quanto vale X?", "o1": str(options[0]), "o2": str(options[1]), "o3": str(options[2]), "o4": str(options[3]), "co": co
    })

# Adult Math (Percentages and fractions)
for _ in range(30):
    perc = random.choice([10, 20, 25, 50])
    num = random.choice([40, 60, 80, 100, 120, 200])
    res = int((perc / 100) * num)
    options = [res, res+5, res-5, res*2]
    random.shuffle(options)
    co = options.index(res) + 1
    math_questions.append({
        "age": "ADULT", "c": "MATH", "d": random.choice([2, 3]),
        "t": f"Qual è il {perc}% di {num}?", "o1": str(options[0]), "o2": str(options[1]), "o3": str(options[2]), "o4": str(options[3]), "co": co
    })

all_new = extra_questions + math_questions

# To ensure exactly doubling, we need ~180 more.
# Currently we generated 20 logic + 120 math = 140 questions.
# Let's generate some more procedural geography and history with slight variations to reach 181.

capitals = [
    ("Italia", "Roma", "Milano", "Napoli", "Torino"),
    ("Spagna", "Madrid", "Barcellona", "Siviglia", "Valencia"),
    ("Germania", "Berlino", "Monaco", "Francoforte", "Amburgo"),
    ("Francia", "Parigi", "Lione", "Marsiglia", "Nizza"),
    ("Giappone", "Tokyo", "Kyoto", "Osaka", "Seoul"),
    ("Regno Unito", "Londra", "Manchester", "Edimburgo", "Dublino"),
    ("Canada", "Ottawa", "Toronto", "Vancouver", "Montreal"),
    ("Australia", "Canberra", "Sydney", "Melbourne", "Brisbane"),
    ("Egitto", "Il Cairo", "Alessandria", "Giza", "Luxor"),
    ("Brasile", "Brasilia", "Rio de Janeiro", "San Paolo", "Buenos Aires"),
    ("Cina", "Pechino", "Shanghai", "Hong Kong", "Taipei")
]

for _ in range(41):
    country, right, w1, w2, w3 = random.choice(capitals)
    options = [right, w1, w2, w3]
    random.shuffle(options)
    co = options.index(right) + 1
    
    age = random.choice(["9-12", "13-17", "ADULT"])
    d = random.choice([1, 2])
    
    all_new.append({
        "age": age, "c": "GEO", "d": d,
        "t": f"Qual è la capitale di: {country}?", "o1": str(options[0]), "o2": str(options[1]), "o3": str(options[2]), "o4": str(options[3]), "co": co
    })


for q in all_new:
    Question.objects.create(
        age_group=q["age"],
        category=q["c"],
        difficulty=q["d"],
        text=q["t"],
        option_1=q["o1"],
        option_2=q["o2"],
        option_3=q["o3"],
        option_4=q["o4"],
        correct_option=q["co"]
    )

print(f"Generate e inserite {len(all_new)} nuove domande procedurali!")

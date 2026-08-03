# MonsterCraft 👾

MonsterCraft è un dungeon crawler web-based interattivo che combina esplorazione su griglia, minigiochi di abilità, enigmi e un sistema di combattimento unico, sviluppato per offrire un'esperienza di gioco fluida direttamente nel browser.

## 🛠️ Tecnologie Utilizzate
- **Backend:** Python + Django
- **Frontend Interattivo:** HTMX & Alpine.js
- **Stile e UI:** HTML/CSS
- **Gestione Pacchetti:** `uv`
- **Database:** SQLite (per lo sviluppo locale)

## 🎮 Il Gioco

In MonsterCraft navighi attraverso dungeon generati casualmente alla ricerca del portale d'uscita, ma fai attenzione: le stanze sono piene di mostri, trappole e segreti!

### Esplorazione e Sopravvivenza
- Muoviti sulla mappa utilizzando le frecce direzionali o i tasti `W` `A` `S` `D`.
- Esplora il dungeon svelando le celle per trovare la via d'uscita.
- Guadagna punti avanzando ed esplorando, ma tieni sempre d'occhio le tue **Vite**!
- Cerca le **Pozioni Nascoste** (disponibili dai livelli più avanzati) per recuperare vita o le **Pergamene Magiche** per ottenere aiuti preziosi in combattimento.

### Gli Scontri (Minigiochi)
Incontrare un mostro non significa la fine, ma l'inizio di una sfida! Durante le battaglie verrai messo alla prova con uno dei seguenti minigiochi (che si alterneranno in modo equo grazie a un sistema integrato a "sacchetto"):

1. **❓ Domanda di Cultura/Logica:** Rispondi correttamente alle domande per sconfiggere il mostro. Se hai raccolto una Pergamena, puoi usare il comando "Usa Aiuto" per eliminare alcune risposte sbagliate!
2. **🎯 Colpo di Precisione:** Ferma il cursore in rapido movimento esattamente nell'area verde. La difficoltà aumenta man mano che scendi in profondità nei dungeon.
3. **🔥💧🌿 Scontro Elementale:** Una variante strategica della morra cinese. Scegli il tuo elemento per attaccare il mostro (Acqua spegne Fuoco, Fuoco brucia Pianta, Pianta assorbe Acqua).

### Trappole e Ostacoli
- **Il Pozzo (Simon Says):** Se cadi in una trappola dovrai affrontare una sequenza di memoria visiva e riprodurla correttamente premendo le frecce direzionali.

### L'Enigma del Portale
- Quando raggiungi l'uscita (la cella rossa), non potrai fuggire immediatamente. Dovrai superare il Guardiano indovinando la parola segreta in stile **Impiccato** (con un timer basato sulla tua velocità!).
- Completa la parola prima di esaurire i tentativi per accedere al piano successivo!

## ⌨️ Accessibilità da Tastiera
MonsterCraft è progettato per essere giocabile interamente utilizzando solo la tastiera per offrirti un'esperienza Arcade pura:
- Frecce direzionali per il movimento sulla griglia, la scelta delle pietre nel pozzo e le selezioni nelle battaglie.
- Il tasto `Invio` e la `Barra Spaziatrice` per confermare le azioni, superare i dialoghi, attaccare e muoversi nei menù, senza dover cliccare col mouse.

## 🚀 Come avviare il progetto in locale

Poiché il progetto utilizza esclusivamente `uv` per la gestione delle dipendenze, assicurati di averlo installato.

1. Sincronizza le dipendenze:
   ```bash
   uv sync
   ```

2. Esegui le migrazioni del database:
   ```bash
   uv run python manage.py migrate
   ```

3. (Opzionale) Seeding del database (per domande e parole per l'enigma):
   ```bash
   uv run python manage.py loaddata <i_tuoi_fixture>
   ```

4. Avvia il server di sviluppo:
   ```bash
   uv run python manage.py runserver
   ```

5. Apri il browser all'indirizzo `http://127.0.0.1:8000/`.

## 🧪 Comandi e Test
Questo progetto utilizza `just` come task runner. Puoi lanciare l'intera suite di test e controllare la test coverage semplicemente con:

```bash
just test
```

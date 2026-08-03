# MonsterCraft 👾

MonsterCraft is an interactive, web-based dungeon crawler that combines grid exploration, skill mini-games, puzzles, and a unique combat system, designed to offer a smooth gaming experience directly in your browser.

## 🛠️ Technologies Used
- **Backend:** Python + Django
- **Interactive Frontend:** HTMX & Alpine.js
- **Styling & UI:** HTML/CSS
- **Package Management:** `uv`
- **Database:** SQLite (for local development)

## 🎮 The Game

In MonsterCraft, you navigate through randomly generated dungeons in search of the exit portal. But beware: the rooms are filled with monsters, traps, and secrets!

### Exploration and Survival
- Move around the map using the arrow keys or `W` `A` `S` `D`.
- Explore the dungeon by revealing cells to find the way out.
- Earn points by advancing and exploring, but always keep an eye on your **Lives**!
- Search for **Hidden Potions** (available in later levels) to recover health, or **Magic Scrolls** to get valuable help in combat.

### Encounters (Mini-games)
Meeting a monster doesn't mean the end, but the beginning of a challenge! During battles, you'll be tested with one of the following mini-games (which alternate evenly thanks to an integrated "bag" system):

1. **❓ Culture/Logic Question:** Answer the questions correctly to defeat the monster. If you have collected a Scroll, you can use the "Use Help" command to eliminate some wrong answers!
2. **🎯 Precision Strike:** Stop the fast-moving cursor exactly in the green area. The difficulty increases as you delve deeper into the dungeons.
3. **🔥💧🌿 Elemental Clash:** A strategic variant of rock-paper-scissors. Choose your element to attack the monster (Water extinguishes Fire, Fire burns Plant, Plant absorbs Water).

### Traps and Obstacles
- **The Well (Simon Says):** If you fall into a trap, you'll face a visual memory sequence and must reproduce it correctly by pressing the arrow keys.

### The Portal Enigma
- When you reach the exit (the red cell), you cannot escape immediately. You must overcome the Guardian by guessing the secret word in a **Hangman** style game (with a timer based on your speed!).
- Complete the word before running out of attempts to access the next floor!

## ⌨️ Keyboard Accessibility
MonsterCraft is designed to be fully playable using only the keyboard, offering a pure Arcade experience:
- Arrow keys for grid movement, choosing stones in the well, and making selections in battles.
- `Enter` and `Spacebar` keys to confirm actions, skip dialogs, attack, and navigate menus without needing a mouse.

## 🚀 How to run the project locally

Since the project exclusively uses `uv` for dependency management, make sure you have it installed.

1. Sync dependencies:
   ```bash
   uv sync
   ```

2. Run database migrations:
   ```bash
   uv run python manage.py migrate
   ```

3. (Optional) Database seeding (for questions and words for the enigma):
   ```bash
   uv run python manage.py loaddata <your_fixtures>
   ```

4. Start the development server:
   ```bash
   uv run python manage.py runserver
   ```

5. Open your browser at `http://127.0.0.1:8000/`.

## 🧪 Commands and Testing
This project uses `just` as a task runner. You can run the entire test suite and check test coverage simply with:

```bash
just test
```

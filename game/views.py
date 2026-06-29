import json
import random

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from .models import HangmanWord, Question, Score


def start(request):
    """
    Renders the Start Screen of MonsterCraft and handles game initialization.
    """
    if request.method == "POST":
        request.session["level"] = 1
        request.session["score"] = 0
        request.session["lives"] = 3
        request.session["monster_helps"] = 0
        request.session["asked_questions"] = []
        request.session["asked_words"] = []
        request.session["age_group"] = request.POST.get("age_group", "9-12")
        request.session.modified = True
        return redirect("game:game")

    return render(request, "game/start.html")


def index(request):
    """
    Renders the main game map.
    """
    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)
    monster_helps = request.session.get("monster_helps", 0)

    # Calculate grid size based on level
    grid_size = min(5 + (level - 1) * 2, 25)

    # 0 = Empty, 1 = Wall, 2 = Monster, 3 = Pit, 4 = Exit
    grid = [[1 for _ in range(grid_size)] for _ in range(grid_size)]

    # Generazione Labirinto tramite DFS
    stack = [(0, 0)]
    grid[0][0] = 0
    visited = {(0, 0)}

    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited:
                neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            grid[cy + dy // 2][cx + dx // 2] = 0
            grid[ny][nx] = 0
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()

    # Creazione percorsi multipli rompendo alcuni muri
    # Assicuriamoci che a livelli maggiori ci siano più percorsi alternativi
    num_loops = max(0, level - 1)
    walls = []
    for y in range(1, grid_size - 1):
        for x in range(1, grid_size - 1):
            if grid[y][x] == 1:
                # Controlla se il muro divide due percorsi vuoti orizzontalmente o verticalmente
                if (grid[y][x - 1] == 0 and grid[y][x + 1] == 0) or (
                    grid[y - 1][x] == 0 and grid[y + 1][x] == 0
                ):
                    walls.append((x, y))

    if walls:
        random.shuffle(walls)
        for i in range(min(num_loops, len(walls))):
            wx, wy = walls[i]
            grid[wy][wx] = 0

    # 3. Exit (sempre accessibile grazie all'algoritmo)
    grid[grid_size - 1][grid_size - 1] = 4

    path_cells = [
        (x, y) for y in range(grid_size) for x in range(grid_size) if grid[y][x] == 0
    ]
    if (0, 0) in path_cells:
        path_cells.remove((0, 0))
    if (grid_size - 1, grid_size - 1) in path_cells:
        path_cells.remove((grid_size - 1, grid_size - 1))

    # 1. Add Monsters (~20% della mappa visibile)
    num_monsters = int(len(path_cells) * 0.20)
    if num_monsters > 0 and len(path_cells) > 0:
        monster_cells = random.sample(path_cells, min(num_monsters, len(path_cells)))
        for mx, my in monster_cells:
            grid[my][mx] = 2
            path_cells.remove((mx, my))

    # 2. Add Pits
    # Compaiono solo se sono stati creati percorsi multipli (num_loops > 0)
    if num_loops > 0:
        num_pits = max(1, int(level / 2))
        if num_pits > 0 and len(path_cells) > 0:

            def is_reachable():
                queue = [(0, 0)]
                visited = {(0, 0)}
                while queue:
                    cx, cy = queue.pop(0)
                    if (cx, cy) == (grid_size - 1, grid_size - 1):
                        return True
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = cx + dx, cy + dy
                        if (
                            0 <= nx < grid_size
                            and 0 <= ny < grid_size
                            and (nx, ny) not in visited
                        ):
                            if grid[ny][nx] in [0, 2, 4, 5, 7, 8]:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
                return False

            available_pits = list(path_cells)
            random.shuffle(available_pits)
            pits_placed = 0
            for px, py in available_pits:
                if pits_placed >= num_pits:
                    break
                # Prova a piazzare la trappola
                grid[py][px] = 3
                if is_reachable():
                    pits_placed += 1
                    path_cells.remove((px, py))
                else:
                    # Rimuovi la trappola perché blocca l'unica strada
                    grid[py][px] = 0

    # 3. Add hidden rewards (from level 3)
    if level >= 3 and len(path_cells) > 0:
        # 1 reward per dungeon (if available path cells)
        reward_type = random.choices([7, 8], weights=[1, 2], k=1)[0]
        rx, ry = random.choice(path_cells)
        grid[ry][rx] = reward_type
        path_cells.remove((rx, ry))

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "monster_helps": monster_helps,
        "grid_size": grid_size,
        "map_data_json": json.dumps(grid),
    }
    return render(request, "game/map.html", context)


def get_question(request):
    """
    Restituisce un frammento HTML (modale) tramite HTMX con una domanda casuale in base alla difficoltà.
    """
    level = request.session.get("level", 1)

    # Difficoltà crescente
    if level <= 2:
        difficulty = 1
    elif level <= 4:
        difficulty = 2
    else:
        difficulty = 3

    age_group = request.session.get("age_group", "9-12")
    asked = request.session.get("asked_questions", [])

    question = (
        Question.objects.filter(age_group=age_group, difficulty=difficulty)
        .exclude(id__in=asked)
        .order_by("?")
        .first()
    )

    # Fallback se finite quelle della difficoltà corrente
    if not question:
        question = (
            Question.objects.filter(age_group=age_group)
            .exclude(id__in=asked)
            .order_by("?")
            .first()
        )

    # Fallback se finite tutte in assoluto
    if not question:
        question = Question.objects.filter(age_group=age_group).order_by("?").first()

    if question:
        asked.append(question.id)
        request.session["asked_questions"] = asked
        request.session.modified = True

    x = request.GET.get("x", "")
    y = request.GET.get("y", "")
    score = request.GET.get("score", 0)

    try:
        monster_helps = int(
            request.GET.get("monster_helps", request.session.get("monster_helps", 0))
        )
    except ValueError:
        monster_helps = 0

    eliminate_options = []
    if question:
        wrong_options = [i for i in range(1, 5) if i != question.correct_option]
        if not question.option_4 and 4 in wrong_options:
            wrong_options.remove(4)
        eliminate_options = random.sample(wrong_options, min(2, len(wrong_options)))

    context = {
        "question": question,
        "x": x,
        "y": y,
        "score": score,
        "monster_helps": monster_helps,
        "eliminate_options": eliminate_options,
    }
    return render(request, "game/partials/question_modal.html", context)


def answer_question(request):
    """
    Valida la risposta.
    """
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    try:
        q_id = int(request.POST.get("question_id", 0))
        answer = int(request.POST.get("answer", 0))
        x = request.POST.get("x", "")
        y = request.POST.get("y", "")
    except ValueError:
        return HttpResponseBadRequest("Invalid input")

    question = Question.objects.filter(id=q_id).first()
    if not question:
        return HttpResponseBadRequest("Question not found")

    correct = question.correct_option == answer

    context = {
        "correct": correct,
        "x": x,
        "y": y,
    }
    return render(request, "game/partials/answer_result.html", context)


def save_score(request):
    if request.method == "POST":
        initials = request.POST.get("initials", "AAA")[:3].upper()
        try:
            score = int(request.POST.get("score", 0))
            level = int(request.POST.get("level", 1))
        except ValueError:
            score = 0
            level = 1

        age_group = request.session.get("age_group")
        Score.objects.create(
            initials=initials, score=score, level=level, age_group=age_group
        )

        # Keep only the top 30 scores
        top_scores_ids = list(
            Score.objects.order_by("-score", "-level", "-id").values_list(
                "id", flat=True
            )[:30]
        )
        Score.objects.exclude(id__in=top_scores_ids).delete()

        return redirect("game:leaderboard")
    return HttpResponseBadRequest("Invalid method")


def leaderboard(request):
    scores = Score.objects.all().order_by("-score", "-level")[:30]
    return render(request, "game/leaderboard.html", {"scores": scores})


def hangman(request):
    """
    Renders the Hangman mini-game between levels.
    """
    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)

    # Difficoltà e tentativi decrescenti, curva ammorbidita
    if level <= 4:
        difficulty = 1
        max_attempts = 7
    elif level <= 8:
        difficulty = 1
        max_attempts = 6
    elif level <= 12:
        difficulty = 2
        max_attempts = 5
    elif level <= 16:
        difficulty = 2
        max_attempts = 4
    else:
        difficulty = 3
        max_attempts = 3

    age_group = request.session.get("age_group", "9-12")
    asked_words = request.session.get("asked_words", [])

    word_obj = (
        HangmanWord.objects.filter(age_group=age_group, difficulty=difficulty)
        .exclude(id__in=asked_words)
        .order_by("?")
        .first()
    )

    if not word_obj:
        word_obj = (
            HangmanWord.objects.filter(age_group=age_group)
            .exclude(id__in=asked_words)
            .order_by("?")
            .first()
        )

    if not word_obj:
        word_obj = HangmanWord.objects.exclude(id__in=asked_words).order_by("?").first()

    # Se finite tutte le parole, resetta l'elenco e ripesca
    if not word_obj:
        asked_words = []
        word_obj = HangmanWord.objects.filter(age_group=age_group).order_by("?").first()
        if not word_obj:
            word_obj = HangmanWord.objects.order_by("?").first()

    # Se proprio non ci sono parole nel DB, ne usiamo una di default
    if not word_obj:

        class DefaultWord:
            id = 0
            word = "MONSTER"
            hint = "Una creatura spaventosa"

        word_obj = DefaultWord()

    if getattr(word_obj, "id", 0) != 0:
        asked_words.append(word_obj.id)
        request.session["asked_words"] = asked_words
        request.session.modified = True

    word = word_obj.word.upper()

    # Scegliamo un paio di lettere da rivelare (circa 25% della parola)
    num_revealed = max(1, len(word) // 4)
    revealed_letters = list(set(random.sample(word, num_revealed)))

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "word": word,
        "hint": word_obj.hint,
        "revealed_letters": json.dumps(revealed_letters),
        "max_attempts": max_attempts,
    }

    return render(request, "game/hangman.html", context)


def update_state(request):
    """
    Aggiorna in modo asincrono lo stato del gioco nella sessione.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request.session["level"] = data.get(
                "level", request.session.get("level", 1)
            )
            request.session["score"] = data.get(
                "score", request.session.get("score", 0)
            )
            request.session["lives"] = data.get(
                "lives", request.session.get("lives", 3)
            )
            request.session["monster_helps"] = data.get(
                "monster_helps", request.session.get("monster_helps", 0)
            )
            request.session.modified = True
            return JsonResponse({"status": "ok"})
        except Exception:
            return HttpResponseBadRequest("Invalid payload")
    return HttpResponseBadRequest("Invalid method")

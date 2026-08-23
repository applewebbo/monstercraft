import json
import random

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from .models import Question, Score


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

        # Clear saved map state
        request.session.pop("saved_map", None)
        request.session.pop("saved_player_x", None)
        request.session.pop("saved_player_y", None)
        request.session.pop("saved_map_level", None)

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

    saved_map_level = request.session.get("saved_map_level")
    if saved_map_level == level and request.session.get("saved_map"):
        grid = request.session.get("saved_map")
        grid_size = len(grid)
        player_x = request.session.get("saved_player_x", 0)
        player_y = request.session.get("saved_player_y", 0)
    else:
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
                if (
                    0 <= nx < grid_size
                    and 0 <= ny < grid_size
                    and (nx, ny) not in visited
                ):
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
            (x, y)
            for y in range(grid_size)
            for x in range(grid_size)
            if grid[y][x] == 0
        ]
        if (0, 0) in path_cells:
            path_cells.remove((0, 0))
        if (grid_size - 1, grid_size - 1) in path_cells:
            path_cells.remove((grid_size - 1, grid_size - 1))

        # 1. Add Monsters (~20% della mappa visibile)
        num_monsters = int(len(path_cells) * 0.20)
        if num_monsters > 0 and len(path_cells) > 0:
            monster_cells = random.sample(
                path_cells, min(num_monsters, len(path_cells))
            )
            for mx, my in monster_cells:
                grid[my][mx] = 2
                path_cells.remove((mx, my))

        # 2. Add Pits (from level 2)
        # Compaiono solo se sono stati creati percorsi multipli (num_loops > 0)
        if level >= 2 and num_loops > 0:
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

        # 3. Add hidden rewards (from level 4)
        if level >= 4 and len(path_cells) > 0:
            # 1 reward per dungeon (if available path cells)
            reward_type = random.choices([7, 8], weights=[1, 2], k=1)[0]
            rx, ry = random.choice(path_cells)
            grid[ry][rx] = reward_type
            path_cells.remove((rx, ry))

        player_x = 0
        player_y = 0

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "monster_helps": monster_helps,
        "grid_size": grid_size,
        "map_data_json": json.dumps(grid),
        "player_x": player_x,
        "player_y": player_y,
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


def memory(request):
    import json
    import random

    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)
    age_group = request.session.get("age_group", "9-12")

    if age_group == "5-8":
        if level <= 3:
            pairs = [
                ("1 + 1", "2"),
                ("2 + 2", "4"),
                ("3 + 1", "4"),
                ("5 + 0", "5"),
                ("1 + 3", "4"),
                ("2 + 1", "3"),
                ("3 + 3", "6"),
                ("4 + 4", "8"),
            ]
        elif level <= 7:
            pairs = [
                ("5 + 5", "10"),
                ("6 + 4", "10"),
                ("7 + 2", "9"),
                ("10 - 2", "8"),
                ("8 - 3", "5"),
                ("9 - 1", "8"),
                ("4 + 5", "9"),
                ("6 + 6", "12"),
            ]
        else:
            pairs = [
                ("2 x 2", "4"),
                ("3 x 2", "6"),
                ("10 - 5", "5"),
                ("12 - 4", "8"),
                ("4 x 2", "8"),
                ("5 x 2", "10"),
                ("6 x 2", "12"),
                ("7 x 2", "14"),
            ]
    elif age_group == "9-12":
        if level <= 3:
            pairs = [
                ("3 x 3", "9"),
                ("4 x 4", "16"),
                ("5 x 5", "25"),
                ("6 x 6", "36"),
                ("7 x 7", "49"),
                ("8 x 8", "64"),
                ("9 x 9", "81"),
                ("10 x 10", "100"),
            ]
        elif level <= 7:
            pairs = [
                ("Capitale Italia", "Roma"),
                ("Capitale Francia", "Parigi"),
                ("Capitale UK", "Londra"),
                ("Capitale Spagna", "Madrid"),
                ("Capitale Germania", "Berlino"),
                ("Capitale Giappone", "Tokyo"),
                ("Capitale Egitto", "Il Cairo"),
                ("Capitale USA", "Washington"),
            ]
        else:
            pairs = [
                ("12 x 12", "144"),
                ("15 x 3", "45"),
                ("100 / 4", "25"),
                ("50 x 2", "100"),
                ("75 / 3", "25"),
                ("90 / 2", "45"),
                ("11 x 11", "121"),
                ("20 x 5", "100"),
            ]
    else:
        if level <= 3:
            pairs = [
                ("2³", "8"),
                ("3²", "9"),
                ("4²", "16"),
                ("5³", "125"),
                ("√64", "8"),
                ("√81", "9"),
                ("√100", "10"),
                ("2⁴", "16"),
            ]
        elif level <= 7:
            pairs = [
                ("H2O", "Acqua"),
                ("CO2", "Anidride Carbonica"),
                ("O2", "Ossigeno"),
                ("NaCl", "Sale da cucina"),
                ("Au", "Oro"),
                ("Ag", "Argento"),
                ("Fe", "Ferro"),
                ("C", "Carbonio"),
            ]
        else:
            pairs = [
                ("Prima Guerra Mondiale", "1914"),
                ("Seconda Guerra Mondiale", "1939"),
                ("Scoperta America", "1492"),
                ("Unità d'Italia", "1861"),
                ("Caduta Muro Berlino", "1989"),
                ("Rivoluzione Francese", "1789"),
                ("Sbarco sulla Luna", "1969"),
                ("Caduta Impero Romano", "476"),
            ]

    num_pairs = min(4 + (level // 3), 8)
    selected_pairs = random.sample(pairs, num_pairs)

    cards = []
    for i, (q, a) in enumerate(selected_pairs):
        cards.append({"id": i, "text": q, "pair_id": i})
        cards.append({"id": i + 100, "text": a, "pair_id": i})

    random.shuffle(cards)

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "cards_json": json.dumps(cards),
        "time_limit": 60 + (level * 5),
    }
    return render(request, "game/memory.html", context)


def dropgame(request):
    import json

    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)
    age_group = request.session.get("age_group", "9-12")

    if age_group == "5-8":
        categories = ["Vocali", "Consonanti"]
        items = [
            {"name": "A", "category": "Vocali"},
            {"name": "E", "category": "Vocali"},
            {"name": "I", "category": "Vocali"},
            {"name": "B", "category": "Consonanti"},
            {"name": "F", "category": "Consonanti"},
            {"name": "Z", "category": "Consonanti"},
        ]
    elif age_group == "9-12":
        categories = ["Pari", "Dispari"]
        items = [
            {"name": "24", "category": "Pari"},
            {"name": "100", "category": "Pari"},
            {"name": "8", "category": "Pari"},
            {"name": "13", "category": "Dispari"},
            {"name": "27", "category": "Dispari"},
            {"name": "99", "category": "Dispari"},
        ]
    else:
        categories = ["Metalli", "Non Metalli"]
        items = [
            {"name": "Ferro", "category": "Metalli"},
            {"name": "Rame", "category": "Metalli"},
            {"name": "Oro", "category": "Metalli"},
            {"name": "Ossigeno", "category": "Non Metalli"},
            {"name": "Carbonio", "category": "Non Metalli"},
            {"name": "Cloro", "category": "Non Metalli"},
        ]

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "categories_json": json.dumps(categories),
        "items_json": json.dumps(items),
        "target_score": 5 + (level // 2),
    }
    return render(request, "game/dropgame.html", context)


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

            if "map_data" in data:
                request.session["saved_map"] = data["map_data"]
                request.session["saved_player_x"] = data.get("player_x", 0)
                request.session["saved_player_y"] = data.get("player_y", 0)
                request.session["saved_map_level"] = request.session["level"]

            request.session.modified = True
            return JsonResponse({"status": "ok"})
        except Exception:
            return HttpResponseBadRequest("Invalid payload")
    return HttpResponseBadRequest("Invalid method")


def pit_minigame(request):
    """
    Renders the Pit minigame (Simon Says).
    """
    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)

    # Difficulty increases with level
    # Max sequence length is 8
    # Formula: start with 3, add 1 every 2 levels, max 8.
    sequence_length = min(8, 3 + (level // 2))

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "sequence_length": sequence_length,
    }

    return render(request, "game/pit_minigame.html", context)


def pit_result(request):
    """
    Handles the result of the pit minigame.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            win = data.get("win", False)

            if win:
                # Add some score for surviving the pit? (optional)
                request.session["score"] = request.session.get("score", 0) + 5
            else:
                # Lose a life
                lives = request.session.get("lives", 3)
                request.session["lives"] = lives - 1

            request.session.modified = True
            return JsonResponse({"status": "ok"})
        except Exception:
            return HttpResponseBadRequest("Invalid payload")
    return HttpResponseBadRequest("Invalid method")


def timing_game(request):
    """
    Renders the Timing Minigame modal.
    """
    x = request.GET.get("x", "")
    y = request.GET.get("y", "")
    level = request.GET.get("level", 1)

    context = {
        "x": x,
        "y": y,
        "level": level,
    }
    return render(request, "game/partials/timing_modal.html", context)


def rps_game(request):
    """
    Renders the Rock-Paper-Scissors modal.
    """
    x = request.GET.get("x", "")
    y = request.GET.get("y", "")

    context = {
        "x": x,
        "y": y,
    }
    return render(request, "game/partials/rps_modal.html", context)


def lockpicker(request):
    """
    Renders the Lock Picker mini-game (Mastermind style) between levels.
    """
    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)

    # Difficulty (code length) increases slightly with level
    if level <= 4:
        code_length = 3
        max_attempts = 6
    elif level <= 10:
        code_length = 3
        max_attempts = 5
    else:
        code_length = 4
        max_attempts = 6

    colors = [
        "#FFEB3B",
        "#4CAF50",
        "#f44336",
        "#03a9f4",
        "#9C27B0",
        "#FF9800",
    ]  # Yellow, Green, Red, Blue, Purple, Orange

    # generate secret code
    secret_code = [random.choice(colors) for _ in range(code_length)]

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "code_length": code_length,
        "max_attempts": max_attempts,
        "secret_code": json.dumps(secret_code),
        "available_colors": json.dumps(colors),
    }

    return render(request, "game/lockpicker.html", context)


def whackamole(request):
    """
    Renders the Whack-a-Mole mini-game between levels.
    """
    level = request.session.get("level", 1)
    score = request.session.get("score", 0)
    lives = request.session.get("lives", 3)

    # Difficulty (speed/number of moles) increases gently with level
    target_score = 5 + (level // 3) * 2  # Easier target: 5 initially
    time_limit = 20  # seconds (more time)
    spawn_rate = max(600, 1200 - (level * 40))  # ms (moles spawn slower)

    context = {
        "level": level,
        "score": score,
        "lives": lives,
        "target_score": target_score,
        "time_limit": time_limit,
        "spawn_rate": spawn_rate,
    }

    return render(request, "game/whackamole.html", context)

from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("", views.start, name="start"),
    path("game/", views.index, name="game"),
    path("question/", views.get_question, name="question"),
    path("answer/", views.answer_question, name="answer"),
    path("save_score/", views.save_score, name="save_score"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("hangman/", views.hangman, name="hangman"),
    path("update_state/", views.update_state, name="update_state"),
    path("pit_minigame/", views.pit_minigame, name="pit_minigame"),
    path("pit_result/", views.pit_result, name="pit_result"),
    path("timing_game/", views.timing_game, name="timing_game"),
    path("rps_game/", views.rps_game, name="rps_game"),
]

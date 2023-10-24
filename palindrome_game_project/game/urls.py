from django.urls import path
from .views import create_game, get_board, update_board, list_games

urlpatterns = [
    path('create/', create_game),
    path('board/<str:game_id>/', get_board),
    path('update/<str:game_id>/', update_board),
    path('list/', list_games),
]

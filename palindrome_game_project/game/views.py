from django.shortcuts import render

# Create your views here.
import random
import string
import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Game
from .serializers import GameSerializer

@api_view(['POST'])
def create_game(request):
    game_id = generate_game_id()
    new_game = Game(game_id=game_id, string="")
    new_game.save()
    serializer = GameSerializer(new_game)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_board(request, game_id):
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = GameSerializer(game)
    return Response(serializer.data)

@api_view(['POST'])
def update_board(request, game_id):
    character = request.data.get('character', '').lower()
    if character.isalpha() and len(character) == 1:
        try:
            game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        
        game.string += character
        game.string += str(random.randint(0, 9))
        game.save()
        
        if len(game.string) == 6:
            if game.string == game.string[::-1]:
                result = "Palindrome"
            else:
                result = "Not Palindrome"
            return Response({"result": result}, status=status.HTTP_200_OK)
        
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid character"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_games(request):
    games = Game.objects.all()
    game_ids = [game.game_id for game in games]
    return Response({"game_ids": game_ids}, status=status.HTTP_200_OK)

def generate_game_id():
    timestamp = str(int(time.time()))
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    game_id = f"{timestamp}{random_chars}"
    return game_id

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .services import CharacterService
from .serializers import CharacterSerializer


class CharacterListCreateView(APIView):
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 100)
        result = CharacterService.get_all_active(page, limit)
        serializer = CharacterSerializer(result['data'], many=True)
        return Response({
            'data': serializer.data,
            'meta': result['meta']
        })

    def post(self, request):
        character = CharacterService.create(request.data)
        serializer = CharacterSerializer(character)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CharacterDetailView(APIView):
    def get_object(self, character_id):
        character = CharacterService.get_by_id(character_id)
        if not character:
            raise NotFound(detail="Персонаж не найден")
        return character

    def get(self, request, character_id):
        character = self.get_object(character_id)
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    def put(self, request, character_id):
        character = CharacterService.update(character_id, request.data, partial=False)
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    def patch(self, request, character_id):
        character = CharacterService.update(character_id, request.data, partial=True)
        serializer = CharacterSerializer(character)
        return Response(serializer.data)

    def delete(self, request, character_id):
        CharacterService.delete(character_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
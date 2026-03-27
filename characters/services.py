from django.core.exceptions import ObjectDoesNotExist
from .models import Character
from .serializers import CharacterCreateUpdateSerializer

class CharacterService:
    @staticmethod
    def get_all_active(page=1, limit=10):
        # пагинация
        start = (page - 1) * limit
        end = start + limit
        queryset = Character.active.all()
        total = queryset.count()
        items = queryset[start:end]
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        return {
            'data': items,
            'meta': {
                'total': total,
                'page': page,
                'limit': limit,
                'totalPages': total_pages,
            }
        }
    def get_all_active():
        return Character.active.all()    
        
    @staticmethod
    def get_by_id(character_id):
        try:
            return Character.active.get(id=character_id)
        except Character.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        serializer = CharacterCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update(character_id, data, partial=False):
        character = Character.active.get(id=character_id)
        serializer = CharacterCreateUpdateSerializer(character, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete(character_id):
        character = Character.active.get(id=character_id)
        character.soft_delete()
        return True
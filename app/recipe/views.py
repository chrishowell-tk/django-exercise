from rest_framework.response import Response
from rest_framework import viewsets, mixins, status

from core.models import Ingredient, Recipe

from recipe import serializers

class IngredientViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def perform_create(serializer):
        """Create a new object"""
        serializer.save()

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Find recipe by searching based on name"""
        queryset = self.queryset
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()

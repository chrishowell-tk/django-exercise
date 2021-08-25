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

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.order_by('-name').distinct()

    def perform_create(serializer):
        """Create a new object"""
        serializer.save()

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string ids to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter()

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save()

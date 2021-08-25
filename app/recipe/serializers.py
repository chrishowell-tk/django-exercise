from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    ingredients = IngredientSerializer(
        many=True,
        allow_null=True,
        required=False
    )

    def create(self, validated_data):
        """
        Create a new recipe initially without the ingredients,
        then add the ingredients one by one and create the PK-FK relationship.
        - validated_data contains the payload from the POST request.

        POST payload example on 'recipes/':
        {
            "name": "Penne carbonara",
            "description": "Super creamy and Amazing",
            "ingredients": [
                {"name": "Pasta"},
                {"name": "Carbonara sauce"}
            ]
        }
        """
        ingredients_payload = validated_data.pop('ingredients', [])

        # new_recipe will not have the ingredients initially
        new_recipe = Recipe.objects.create(**validated_data)

        # add the PK-FK relationship for all the ingredients-recipe
        for ingredient in ingredients_payload:
            Ingredient.objects.create(recipe=new_recipe, **ingredient)

        return new_recipe

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients'
        )
        read_only_fields = ('id',)

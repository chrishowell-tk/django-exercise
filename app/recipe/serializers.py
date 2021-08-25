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
        Create a new recipe without ingredients, then build up the PK-FK
        relationship by adding ingredients to it if they exist.
        """
        ingredients_payload = validated_data.pop('ingredients', [])

        # new_recipe will not have the ingredients initially
        new_recipe = Recipe.objects.create(**validated_data)

        # add the PK-FK relationship for all the ingredients-recipe
        for ingredient in ingredients_payload:
            Ingredient.objects.create(recipe=new_recipe, **ingredient)

        return new_recipe

    def update(self, instance, validated_data):
        """
        Update the list of ingredients for a recipe.
        """
        instance.name = validated_data.get('name', instance.name)
        Ingredient.objects.filter(recipe=instance.id).delete()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=instance, **ingredient)
        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients'
        )
        read_only_fields = ('id',)

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer, IngredientSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample Recipe',
        'description': 'Put it in the oven'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


def sample_ingredient(**params):
    """Create and return a sample ingredient"""
    defaults = {
        'name': 'Sample ingredient',
    }
    defaults.update(params)

    return defaults


class RecipeAPITests(TestCase):
    """Test the recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_recipe_list(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipe_by_id(self):
        """Test retrieving a single recipe by id"""
        recipe = sample_recipe()

        res = self.client.get(detail_url(recipe.id))
        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_create_basic_recipe(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Chocolate cheesecake',
            'description': 'Delicious chocolatey goodness',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients"""
        recipe = sample_recipe()
        ingredient1 = sample_ingredient()
        ingredient2 = sample_ingredient(name='Tomato')
        ingredients = [ingredient1, ingredient2]
        payload = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': ingredients,
        }

        res = self.client.post(RECIPES_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all().order_by('id')
        ingredient_serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(ingredients.count(), 2)
        self.assertEqual(
            ingredient1['name'], ingredient_serializer.data[0]['name']
        )
        self.assertEqual(
            ingredient2['name'], ingredient_serializer.data[1]['name']
        )

    def test_recipe_update_add_ingredient(self):
        """Test updating a recipe with an ingredient"""
        recipe = sample_recipe()

        payload = {
            'name': 'Yummy scrummy chicken',
            'description': 'Wow this tastes good',
            'ingredients': [
                {'name': 'Chicken'}
            ]
        }

        url = detail_url(recipe.id)
        self.client.patch(url, data=payload, format='json')
        res = self.client.get(url)

        recipe.refresh_from_db()
        ingredients = recipe.ingredients.all()
        self.assertEqual(recipe.name, res.data['name'], )
        self.assertEqual(len(ingredients), 1)

        for ingredient in ingredients:
            self.assertIn(ingredient.name, 'Chicken')

    def test_recipe_update_add_ingredients(self):
        """Test updating a recipe with new ingredients"""
        recipe = sample_recipe()
        ingredient = Ingredient.objects.create(
            name='Basil',
            recipe=recipe
        )
        recipe.ingredients.add(ingredient)
        payload = {
            'ingredients': [
                {'name': 'Basil'},
                {'name': 'Chicken'}
            ]
        }

        url = detail_url(recipe.id)
        self.client.patch(url, data=payload, format='json')
        res = self.client.get(url)

        recipe.refresh_from_db()

        res_recipe = res.data
        ingredients = res_recipe['ingredients']

        self.assertEqual(recipe.name, res.data['name'], )
        self.assertEqual(len(ingredients), 2)
        for ingredient in ingredients:
            self.assertIn(ingredient['name'], 'Chicken Basil')

    def test_recipe_deletion(self):
        """Test deleting a recipe"""
        recipe = sample_recipe()
        ingredient = Ingredient.objects.create(
            name='Paprika',
            recipe=recipe
        )
        recipe.ingredients.add(ingredient)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_searching_for_a_recipe_by_name(self):
        """Test searching for a recipe by name where the recipe matches"""
        sample_recipe(name='Quesadilla')

        res = self.client.get(RECIPES_URL, {'name': 'Que'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_searching_for_a_recipe_by_name_no_match(self):
        """
            Test searching for a recipe by name
            where the recipe does not match
        """
        sample_recipe(name='Quesadilla')

        res = self.client.get(RECIPES_URL, {'name': 'Piz'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

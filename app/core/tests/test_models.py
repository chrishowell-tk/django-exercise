from django.test import TestCase
from core.models import Recipe, Ingredient

def sample_recipe(**params):
    """Create a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Put it on a plate'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)

class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""

        ingredient = Ingredient.objects.create(
            name='Cucumber',
            recipe=sample_recipe()
        )
        self.assertEqual(str(ingredient), ingredient.name)

from recipe_source import RecipeSource
from recipe import Ingredient

selector_to_property = {
    "amount": ".wprm-recipe-ingredient-amount",
    "unit": ".wprm-recipe-ingredient-unit",
    "name": ".wprm-recipe-ingredient-name",
}

class SkinnyTasteRecipe(RecipeSource):
    def get_recipe(self):
        self._get_body()
        
        ings = []
        
        ingredients = self.soup.select_one('.wprm-recipe-ingredient-group')
        for ingredient in ingredients.find_all(['li']):
            fields = {f: self.get_text_from_selector(ingredient, s) for f, s in selector_to_property.items()}
            my_ing = Ingredient(**fields)
            ings.append(my_ing)
        return ings

    def get_text_from_selector(self, ingredient, selector):
        try:
            amount = ingredient.select_one(selector).string
        except AttributeError:
            amount = None
        return amount
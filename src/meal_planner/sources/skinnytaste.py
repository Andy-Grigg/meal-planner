from typing import TYPE_CHECKING

from meal_planner.classes import Ingredient
from meal_planner.sources._base_source import _BaseSource

if TYPE_CHECKING:
    from bs4.element import Tag


INGREDIENTS_SELECTOR = '.wprm-recipe-ingredient-group'

PROP_TO_SELECTOR = {
    "amount": ".wprm-recipe-ingredient-amount",
    "unit": ".wprm-recipe-ingredient-unit",
    "name": ".wprm-recipe-ingredient-name",
}


class SkinnyTasteRecipe(_BaseSource):
    def get_recipe(self) -> list[Ingredient]:
        ingredients_tag = self.soup.select_one(INGREDIENTS_SELECTOR)
        individual_ingredients_tags = ingredients_tag.find_all(['li'])
        ingredients = [self.make_ingredient(ing_tag) for ing_tag in individual_ingredients_tags]
        return ingredients

    def make_ingredient(self, ingredient_el: "Tag"):
        fields = {f: self.get_text_from_selector(ingredient_el, s) for f, s in PROP_TO_SELECTOR.items()}
        ingredient = Ingredient(**fields)
        return ingredient

    @staticmethod
    def get_text_from_selector(ingredient: "Tag", selector: str) -> str | None:
        try:
            amount = ingredient.select_one(selector).string
        except AttributeError:
            amount = None
        return amount

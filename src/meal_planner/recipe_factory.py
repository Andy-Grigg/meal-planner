from abc import ABC
import requests
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from .models import (
    Ingredient,
    Recipe as RecipeModel
)

if TYPE_CHECKING:
    from bs4.element import Tag


class UnknownRecipeProvider(NotImplementedError):
    pass


class RecipeFactory(ABC):
    hostname = None
    recipe_scrapers = {}
    ingredients: list["Ingredient"]

    def __init_subclass__(cls, **kwargs):
        cls.recipe_scrapers[cls.hostname] = cls

    def __init__(
            self,
            name: str,
            url: str | None = None,
            ingredients: list["Ingredient"] | None = None
    ):
        assert name, "All recipes must have a name"
        self.name = name
        self.url = url
        self._ingredients = ingredients
        self._soup = None

    @classmethod
    def create_recipe(cls, *args, **kwargs) -> "RecipeModel":
        if "url" not in kwargs or kwargs["url"] is None:
            recipe = ManualRecipe(name=kwargs["name"])
        else:
            url = kwargs["url"]
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            recipe = None
            for source, klass in cls.recipe_scrapers.items():
                if source and source in hostname:
                    recipe = klass(*args, **kwargs).model
            if recipe is None:
                raise UnknownRecipeProvider(f"No implementation found for {hostname}")

        recipe_model = RecipeModel(
            name=recipe.name,
            url=recipe.url,
            ingredients=recipe.ingredients,
        )
        return recipe_model


class ManualRecipe(RecipeFactory):
    @property
    def ingredients(self) -> list["Ingredient"]:
        return self._ingredients if self._ingredients is not None else []


class WebpageRecipe(RecipeFactory):
    @property
    def soup(self) -> BeautifulSoup | None:
        if not self.url:
            return None
        if not self._soup:
            body = requests.get(self.url).content
            self._soup = BeautifulSoup(body, features="html.parser")
        return self._soup

    @property
    def ingredients(self) -> list["Ingredient"]:
        raise NotImplementedError


class SkinnyTasteRecipe(WebpageRecipe):
    hostname = "skinnytaste.com"

    INGREDIENTS_SELECTOR = '.wprm-recipe-ingredient-group'

    PROP_TO_SELECTOR = {
        "amount": ".wprm-recipe-ingredient-amount",
        "unit": ".wprm-recipe-ingredient-unit",
        "name": ".wprm-recipe-ingredient-name",
    }

    @property
    def ingredients(self) -> list["Ingredient"]:
        if self._ingredients is None:
            ingredients_tag = self.soup.select_one(self.INGREDIENTS_SELECTOR)
            individual_ingredients_tags = ingredients_tag.find_all(['li'])
            self._ingredients = [self._make_ingredient(ing_tag) for ing_tag in individual_ingredients_tags]
        return self._ingredients

    def _make_ingredient(self, ingredient_el: "Tag"):
        fields = {f: self._get_text_from_selector(ingredient_el, s) for f, s in self.PROP_TO_SELECTOR.items()}
        ingredient = Ingredient(**fields)
        return ingredient

    @staticmethod
    def _get_text_from_selector(ingredient: "Tag", selector: str) -> str | None:
        try:
            amount = ingredient.select_one(selector).string
        except AttributeError:
            amount = None
        return amount


class FoodNetworkRecipe(WebpageRecipe):
    hostname = "foodnetwork.com"

    @property
    def ingredients(self) -> list["Ingredient"]:
        if self._ingredients is None:
            ingredients_tag = self.soup.find_all('section', attrs={'data-module': 'recipe-ingredients'})
            assert len(ingredients_tag) == 1, f"Expected 1 Ingredients block - found {len(ingredients_tag)}"
            individual_ingredients_tags = ingredients_tag[0].findChildren(
                "p",
                attrs={"class": "o-Ingredients__a-Ingredient"},
                recursive=True
            )
            ing_tag: Tag
            self._ingredients = []
            for ing_tag in individual_ingredients_tags:
                span_tag = ing_tag.findChild(name="span", attrs={"class": "o-Ingredients__a-Ingredient--CheckboxLabel"})
                name = span_tag.string
                if name == "Deselect All":
                    continue
                ing = Ingredient(name=name)
                self._ingredients.append(ing)
        return self._ingredients

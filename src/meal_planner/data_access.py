from typing import Optional, TYPE_CHECKING, Any
import logging

from pymongo import MongoClient
from pydantic import BaseModel


from bunnet import Document, init_bunnet

if TYPE_CHECKING:
    from .classes import Ingredient as ClIngredient

logger = logging.getLogger("discord.meal_planner.data_access")


class Ingredient(BaseModel):
    name: str
    amount: Optional[str | float | int]
    unit: Optional[str]


class Recipe(Document):
    name: str
    url: Optional[str]
    ingredients: list[Ingredient]


class _MongoConnection:
    instance: "_MongoConnection"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(_MongoConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # Bunnet uses Pymongo client under the hood
        self.client = MongoClient("mongodb://user:hunter2@localhost:27017")

        # Initialize bunnet with the Product document class
        init_bunnet(database=self.client.db_name, document_models=[Recipe])


def requires_connection(func):
    def wrapper(*args, **kwargs):
        _MongoConnection()
        return func(*args, **kwargs)
    return wrapper


@requires_connection
def get_recipe(recipe_name: str):
    recipe = Recipe.find_one(Recipe.name == recipe_name).run()
    return recipe


@requires_connection
def write_recipe(name: str, url: str, ingredients: list["ClIngredient"]):
    logger.info(ingredients)
    ingredients = [Ingredient(name=i.name, amount=i.amount, unit=i.unit) for i in ingredients]
    logger.info(name)
    logger.info(url)
    recipe = Recipe(name=name, url=url, ingredients=ingredients)
    recipe.insert()

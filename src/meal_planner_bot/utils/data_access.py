import logging
import os

from bunnet import init_bunnet
from pymongo import MongoClient

from .models import Ingredient, Recipe

logger = logging.getLogger("discord.meal_planner_bot.data_access")
CONN_STRING = os.getenv("MONGO_CONNECTION_STRING")


class _MongoConnection:
    instance: "_MongoConnection"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self, connection_string: str | None = CONN_STRING):
        self.client = MongoClient(connection_string)
        init_bunnet(database=self.client.db_name, document_models=[Recipe])


def requires_connection(func):
    def wrapper(*args, **kwargs):
        _MongoConnection()
        return func(*args, **kwargs)

    return wrapper


@requires_connection
def get_recipe(recipe_name: str, raise_on_missing: bool = False) -> Recipe:
    recipe = Recipe.find_one(Recipe.name == recipe_name).run()
    if not recipe and raise_on_missing:
        raise ValueError(f"Recipe {recipe_name} not found in database.")
    return recipe


@requires_connection
def write_recipe(name: str, url: str, ingredients: list[Ingredient]) -> None:
    logger.info(f"Writing recipe {name} to database.")
    recipe = Recipe(name=name, url=url, ingredients=ingredients)
    recipe.insert()
    logger.info("Success.")


@requires_connection
def delete_recipe(name: str) -> None:
    logger.info(f"Deleting recipe {name} from database.")
    get_recipe(name, raise_on_missing=True).delete()


@requires_connection
def get_all_recipes() -> list[Recipe]:
    recipes = Recipe.find_all().run()
    return recipes

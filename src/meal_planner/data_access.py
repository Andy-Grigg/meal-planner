import logging

from pymongo import MongoClient
from bunnet import init_bunnet

from .models import Recipe, Ingredient

logger = logging.getLogger("discord.meal_planner.data_access")


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
def get_recipe(recipe_name: str) -> Recipe:
    recipe = Recipe.find_one(Recipe.name == recipe_name).run()
    if not recipe:
        raise ValueError(f"Recipe {recipe_name} not found in database.")
    return recipe


@requires_connection
def write_recipe(name: str, url: str, ingredients: list[Ingredient]) -> None:
    logger.info(f"Writing recipe {name} to database.")
    recipe = Recipe(name=name, url=url, ingredients=ingredients)
    recipe.insert()
    logger.info(f"Success.")


@requires_connection
def delete_recipe(name: str) -> None:
    logger.info(f"Deleting recipe {name} from database.")
    recipe_to_delete = get_recipe(name).delete()


@requires_connection
def get_all_recipes() -> list[Recipe]:
    recipes = Recipe.find_all().run()
    return recipes

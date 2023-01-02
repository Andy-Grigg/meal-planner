import logging

from . import data_access
from .calendar_access import ICalConnection
from .models import MealPlan, Recipe
from .recipe_factory import RecipeFactory

logger = logging.getLogger("discord.helper_functions")

__all__ = [
    "convert_calendar_to_meal_plans",
    "create_recipe",
    "get_recipe",
    "delete_recipe",
    "get_all_recipes",
]


def convert_calendar_to_meal_plans(
    ical: ICalConnection,
    number_of_days: int,
) -> list[MealPlan]:
    events = ical.get_n_events_starting_today(number_of_days)

    logger.info("Extracting meal plans from calendar.")
    meal_plans = []
    for event in events:
        recipe = data_access.get_recipe(event.summary)
        if recipe is None:
            logger.info(f"Recipe {event.summary} not found in database.")
            if event.url:
                create_recipe(name=event.summary, url=event.url)
            else:
                logger.info("No URL provided. Ignoring.")
        else:
            logger.info(f"Recipe {recipe.name} found in database.")
        mp = MealPlan(name=event.summary, date=event.start.date(), recipe=recipe)
        meal_plans.append(mp)
    logger.info(f"Generated {len(meal_plans)} meal plans.")
    return meal_plans


def create_recipe(name: str, url: str | None = None) -> Recipe:
    logger.info(f"Retrieving recipe {name} from url and writing to database.")
    new_recipe = RecipeFactory.create_recipe(name=name, url=url)
    if new_recipe:
        data_access.write_recipe(
            name=new_recipe.name,
            url=new_recipe.url,
            ingredients=new_recipe.ingredients,
        )
    return new_recipe


def get_all_recipes() -> list[Recipe]:
    logger.info("Retrieving all recipes.")
    all_recipes = data_access.get_all_recipes()
    return all_recipes


def get_recipe(name: str) -> Recipe:
    return data_access.get_recipe(name)


def delete_recipe(name: str):
    logger.info(f"Deleting recipe {name}.")
    data_access.delete_recipe(name)


def add_ingredient_to_recipe():
    pass

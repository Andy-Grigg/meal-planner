from typing import TYPE_CHECKING
import logging

from meal_planner import Recipe, MealPlan
from meal_planner import data_access

if TYPE_CHECKING:
    from meal_planner import ICalConnection
    from datetime import date

logger = logging.getLogger("discord.helper_functions")


def create_shopping_list_from_calendar(
        ical: "ICalConnection",
        number_of_days: int = 7
) -> list[MealPlan]:
    events = ical.get_events_from_today_onwards(number_of_days)

    meal_plans = []
    for event in events:
        recipe = data_access.get_recipe(event.summary)
        if recipe is None and event.url:
            logger.info(f'Cache miss for {event.summary}. Retrieving from url.')
            recipe = Recipe.create_recipe(name=event.summary, url=event.url)
            if recipe is not None:
                data_access.write_recipe(name=recipe.name, url=recipe.url, ingredients=recipe.ingredients)
        elif recipe is None:
            logger.info(f'{event.summary} has no URL. Ignoring.')
        else:
            logger.info(f'Cache hit for {recipe.name}')
        mp = MealPlan(name=event.summary, date=event.start.date(), recipe=recipe)
        meal_plans.append(mp)
    return meal_plans


def create_meal_plan_from_calendar(
        ical: "ICalConnection",
        number_of_days: int = 7
) -> dict["datetime.date", str]:
    events = ical.get_events_from_today_onwards(number_of_days)

    meal_names_by_date = {}
    for event in events:
        meal_names_by_date[event.start.date()] = event.summary
    return meal_names_by_date


if __name__ == "__main__":
    import os
    from meal_planner import ICalConnection

    ical = ICalConnection(os.getenv("CALENDAR_URL"))
    list = create_shopping_list_from_calendar(ical, 7)
    print(list)

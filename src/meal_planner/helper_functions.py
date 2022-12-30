from typing import TYPE_CHECKING
from meal_planner import Recipe, MealPlan

if TYPE_CHECKING:
    from meal_planner import ICalConnection
    from datetime import date


def create_shopping_list_from_calendar(
        ical: "ICalConnection",
        number_of_days: int = 7
) -> list[MealPlan]:
    events = ical.get_events_from_today_onwards(number_of_days)

    meal_plans = []
    for event in events:
        recipe = Recipe.create_recipe(name=event.summary, url=event.url)
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

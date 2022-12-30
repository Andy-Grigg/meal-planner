import os
from meal_planner import ICalConnection, create_meal_plans_from_calendar

# TODO: Register a URL through discord
ical = ICalConnection(os.getenv("CALENDAR_URL"))

# TODO: Where do I store it? I'm going to need a database of users or something
plans = create_meal_plans_from_calendar(ical, 7)

plans_dict = sorted(plans, key=lambda x: x.date)

# TODO: Post shopping list through discord
for plan in plans_dict:
    print(f"{plan.date}: {plan.name}")
    if plan.recipe:
        for ingredient in plan.recipe.ingredients:
            print("  " + str(ingredient))

import os
from meal_planner import ICalConnection, create_meal_plans_from_calendar

ical = ICalConnection(os.getenv("CALENDAR_URL"))

plans = create_meal_plans_from_calendar(ical, 7)

plans_dict = sorted(plans, key=lambda x: x.date)

for plan in plans_dict:
    print(f"{plan.date}: {plan.name}")
    if plan.recipe:
        for ingredient in plan.recipe.ingredients:
            print("  " + str(ingredient))

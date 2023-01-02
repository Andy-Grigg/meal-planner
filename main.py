import os
from meal_planner import (
    convert_calendar_to_meal_plans,
    ICalConnection,
    delete_recipe,
    get_all_recipes,
    create_and_persist_recipe,
)

get_all_recipes()

create_and_persist_recipe("Cheddar stew")

for r in get_all_recipes():
    print(r)

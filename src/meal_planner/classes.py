from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime
    from .recipe import Recipe


class MealPlan:
    def __init__(self, name: str, date: "datetime.date", recipe: "Recipe | None") -> None:
        self.name = name
        self.date = date
        self.recipe = recipe


class Ingredient:
    def __init__(self, amount: float, unit: str, name: str) -> None:
        self.amount = amount
        self.unit = unit
        self.name = name

        if not self.name:
            raise ValueError("Ingredient must have a name.")

        if self.unit and not self.amount:
            raise ValueError("Unit can only be specified with a amount.")

    def __repr__(self) -> str:
        if self.unit:
            return f"{self.name} ({self.amount} {self.unit})"
        elif self.amount:
            return f"{self.name} ({self.amount})"
        else:
            return self.name

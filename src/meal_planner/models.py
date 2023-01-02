from datetime import date
from typing import Optional

from bunnet import Document
from pydantic import validator, BaseModel


class Ingredient(BaseModel):
    name: str
    amount: Optional[str | float | int]
    unit: Optional[str]

    @validator('unit')
    def unit_only_allowed_if_with_amount(cls, v, values, **kwargs):
        if 'amount' not in values:
            raise ValueError("Unit can only be specified with a amount.")
        return v

    def __str__(self) -> str:
        if self.unit:
            return f"{self.name} ({self.amount} {self.unit})"
        elif self.amount:
            return f"{self.name} ({self.amount})"
        else:
            return self.name


class Recipe(Document):
    name: str
    url: Optional[str]
    ingredients: list[Ingredient]

    def __str__(self) -> str:
        if self.url:
            return f"{self.name} ({self.url}): {len(self.ingredients)} ingredients"
        else:
            return f"{self.name}: {len(self.ingredients)} ingredients"

    @property
    def shopping_list(self) -> str:
        shopping_list = [f"- {str(ingredient)}" for ingredient in self.ingredients]
        shopping_list.insert(0, str(self))
        return "\n".join(shopping_list)


class MealPlan(BaseModel):
    name: str
    date: date
    recipe: Recipe | None

    def __str__(self) -> str:
        return f"{self.date.strftime('%A %x')}: {self.name}"

    @property
    def shopping_list(self) -> str:
        if not self.recipe:
            return str(self) + " - no recipe"
        return self.recipe.shopping_list

import pytest
from pydantic import ValidationError

from meal_planner_bot.utils import Ingredient


def test_ingredient_name_only():
    new_ing = Ingredient(name="Test Ingredient")
    assert new_ing.name == "Test Ingredient"


def test_ingredient_no_name_raises_exception():
    with pytest.raises(ValidationError, match="field required"):
        Ingredient()


@pytest.mark.parametrize("amount", [0, 1, 12.5, "Three", "Half", "A good pinch"])
def test_ingredient_name_and_amount(amount):
    new_ing = Ingredient(name="Test Ingredient", amount=amount)
    assert new_ing.name == "Test Ingredient"
    assert new_ing.amount == str(amount)


def test_ingredient_name_amount_unit():
    new_ing = Ingredient(name="Test Ingredient", amount=5, unit="Bulbs")
    assert new_ing.name == "Test Ingredient"
    assert new_ing.amount == "5"
    assert new_ing.unit == "Bulbs"


def test_ingredient_unit_without_amount_raises_exception():
    with pytest.raises(
        ValidationError, match="Unit can only be specified with an amount."
    ):
        Ingredient(name="Test", unit="lb")

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from meal_planner import Ingredient


class _BaseSource(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self._soup = None

    @property
    def soup(self) -> BeautifulSoup:
        if not self._soup:
            body = requests.get(self.url).content
            self._soup = BeautifulSoup(body, features="html.parser")
        return self._soup

    @abstractmethod
    def get_recipe(self) -> list["Ingredient"]:
        pass

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup


class RecipeSource(ABC):
    def __init__(self, url):
        self.url = url
        self.soup = None

    def _get_body(self):
        body = requests.get(self.url).content
        self.soup = BeautifulSoup(body, features="html.parser")  

    @abstractmethod
    def get_recipe(self):
        pass

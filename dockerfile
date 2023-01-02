# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /usr/src/app

COPY . .

RUN pip install poetry && poetry install

CMD [ "poetry", "run", "python", "./src/meal_planner_bot/bot.py" ]

import os
import logging
from functools import wraps

import discord
from discord import app_commands

from meal_planner import (
    convert_calendar_to_meal_plans,
    create_and_persist_recipe,
    get_calendar,
    get_all_recipes,
    delete_recipe,
    get_recipe,
)


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

guild = discord.Object(id=GUILD_ID)

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

logger = logging.getLogger("discord.meal_planner")


def database_access(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        interaction = args[0]
        logger.info(f'{interaction.data["name"]} request received from user "{interaction.user}"')
        await interaction.response.defer()
        try:
            output = await func(*args, **kwargs)
        except Exception as e:
            logger.info(f'Something went wrong... {str(e)}')
            await interaction.followup.send("Something went wrong. Check your args and try again.")
            return None
        await interaction.followup.send("Done")
        logger.info(f'{interaction.data["name"]} completed')
        return output
    return wrapper


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    logger.info("Bot Ready")


@tree.command(
    name="shoppinglist",
    description="Get a shopping list for n days (default 10)",
    guild=guild,
)
@database_access
async def on_message(interaction, number_of_days: int = 10):
    ical = get_calendar(os.getenv("CALENDAR_URL"))
    plans = convert_calendar_to_meal_plans(ical, number_of_days)
    for plan in plans:
        await interaction.user.send(plan.shopping_list)
        logger.info(f'Sent message for plan "{plan.name}"')


@tree.command(
    name="mealplan",
    description="Get planned meals for n days (default 10)",
    guild=guild,
)
@database_access
async def on_message(interaction, number_of_days: int = 10):
    ical = get_calendar(os.getenv("CALENDAR_URL"))
    plans = convert_calendar_to_meal_plans(ical, number_of_days)
    await interaction.user.send("\n".join([str(p) for p in plans]))


@tree.command(
    name="addrecipe",
    description="Add a recipe with a name and an optional url to the recipe",
    guild=guild,
)
@database_access
async def on_message(interaction, name: str, url: str | None = None):
    logger.info(f"name: {name}")
    logger.info(f"url: {url}")
    recipe = create_and_persist_recipe(name, url)
    await interaction.user.send(f'Successfully imported recipe "{str(recipe)}".')


@tree.command(
    name="recipes",
    description="List all available recipes",
    guild=guild,
)
@database_access
async def on_message(interaction):
    all_recipes = get_all_recipes()
    await interaction.user.send("\n".join([str(r) for r in all_recipes]))


@tree.command(
    name="deleterecipe",
    description="Delete a recipe by name",
    guild=guild,
)
@database_access
async def on_message(interaction, name: str):
    delete_recipe(name)
    await interaction.user.send(f"Deleted recipe {name}")


@tree.command(
    name="recipedetails",
    description="Get the details of a specific recipe",
    guild=guild,
)
@database_access
async def on_message(interaction, name: str):
    recipe = get_recipe(name)
    await interaction.user.send(recipe.shopping_list)


client.run(TOKEN)

import os
import logging

import discord
from discord import app_commands

from meal_planner import (
    create_shopping_list_from_calendar,
    create_meal_plan_from_calendar,
    ICalConnection,
)


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

guild = discord.Object(id=GUILD_ID)

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

logger = logging.getLogger("discord.meal_planner")


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    logger.info("Bot Ready")


@tree.command(
    name="shoppinglist",
    description="Get a shopping list for the next 7 days",
    guild=guild,
)
async def on_message(interaction):
    logger.info(f"shoppinglist request received from user {interaction.user}")
    await interaction.response.defer()

    logger.info("Getting calendar")
    ical = ICalConnection(os.getenv("CALENDAR_URL"))

    logger.info("Extracting meal plans from calendar")
    plans = create_shopping_list_from_calendar(ical, 7)
    plans_dict = sorted(plans, key=lambda x: x.date)

    logger.info("Generated meal plans")
    for plan in plans_dict:
        response = f"{plan.date}: {plan.name}\n"
        if plan.recipe:
            for ingredient in plan.recipe.ingredients:
                response += f"- {ingredient}\n"
        await interaction.user.send(response)
        logger.info(f'Sent message for plan "{plan.name}"')
    await interaction.followup.send("Done!")
    logger.info("Done")


@tree.command(
    name="mealplan",
    description="Get the planned meals for the next 7 days",
    guild=guild,
)
async def on_message(interaction):
    logger.info(f'mealplan request received from user "{interaction.user}"')
    await interaction.response.defer()

    logger.info("Getting calendar")
    ical = ICalConnection(os.getenv("CALENDAR_URL"))

    logger.info("Extracting meal plans from calendar")
    meal_plans_for_week = create_meal_plan_from_calendar(ical, 7)
    meal_plans_for_week = dict(sorted(meal_plans_for_week.items()))

    logger.info("Generated meal plans")
    response = ""
    for date, plan_name in meal_plans_for_week.items():
        response += f"{date}: {plan_name}\n"
    await interaction.user.send(response)
    await interaction.followup.send("Done!")
    logger.info("Done")


client.run(TOKEN)

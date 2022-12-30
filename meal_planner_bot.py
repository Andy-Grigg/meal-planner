import os
import logging

import discord
from discord import app_commands

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

guild = discord.Object(id=GUILD_ID)

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

logging.basicConfig()
logger = logging.getLogger("bot")


@client.event
async def on_ready():
    await tree.sync(guild=guild)
    logger.info("Bot Ready")


@tree.command(
    name="mealplan",
    description="Print the current plan for the next week",
    guild=guild,
)
async def on_message(interaction):
    logger.info("mealplan request received")
    await interaction.response.defer()

    from meal_planner import create_meal_plans_from_calendar, ICalConnection

    ical = ICalConnection(os.getenv("CALENDAR_URL"))
    logger.info("Calendar retrieved")

    plans = create_meal_plans_from_calendar(ical, 7)
    plans_dict = sorted(plans, key=lambda x: x.date)

    # TODO: Post shopping list through discord

    logger.info("Plan created")
    for plan in plans_dict:
        response = f"{plan.date}: {plan.name}\n"
        if plan.recipe:
            for ingredient in plan.recipe.ingredients:
                response += f"- {ingredient}\n"
            await interaction.user.send(response)
            logger.info(f"Sent message for plan {plan.name}")
    await interaction.followup.send("Done!")
    logger.info("Done")

client.run(TOKEN)

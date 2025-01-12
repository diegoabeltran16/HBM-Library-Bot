"""
DeweyBot Main Script
--------------------
This script initializes the Dewey Discord Bot and handles basic command interaction.
It uses `discord.py` for bot operations and `dotenv` to securely load the bot token from an environment file.
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('configs/.env')  # Ensures the bot token is loaded without hardcoding sensitive credentials
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieves the bot token from the environment variables

# Set up intents (required by discord.py 2.0 and above)
intents = discord.Intents.default()  # Loads default intents (basic events like message creation)
intents.messages = True  # Explicitly enable message reading (required for command handling)

# Initialize the bot with a command prefix (!) and specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    Event handler that triggers when the bot successfully connects to Discord.
    Prints a confirmation message with the bot's name.
    """
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    """
    A simple command that responds with a greeting message.

    Parameters:
    ctx (commands.Context): The context in which the command was invoked.
    """
    await ctx.send("Hello! I'm DeweyBot.")

# Run the bot using the token retrieved from the environment
bot.run(TOKEN)

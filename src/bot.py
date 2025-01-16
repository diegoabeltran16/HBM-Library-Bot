import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from src.ms_graph import get_access_token
from src.db_manager import initialize_database, insert_reference, fetch_references

# Load environment variables
load_dotenv('configs/.env')
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Initialize bot intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize the database
initialize_database()


@bot.event
async def on_ready():
    """
    Handles bot startup logic, syncing commands, and logging bot status.
    """
    print("Bot is connecting...")
    try:
        synced_commands = await bot.tree.sync()  # Sync global commands
        print(f"Logged in as {bot.user.name}. Synced Commands: {[cmd.name for cmd in synced_commands]}")
    except Exception as e:
        print(f"Error during command sync: {e}")

    # Test Microsoft Graph authentication
    token = get_access_token()
    if token:
        print(f"Access Token: {token}")
    else:
        print("Failed to obtain access token.")


@bot.tree.command(name="add_reference", description="Add an academic reference with type, identifier, title, and author(s).")
async def add_reference(interaction: discord.Interaction, reference_type: str, identifier: str, title: str, authors: str):
    """
    Slash command to add an academic reference.
    """
    valid_types = ["B", "D", "SA", "N", "MA", "C", "T", "AVM", "BLG", "L", "O", "SM", "E"]

    if reference_type not in valid_types:
        await interaction.response.send_message(
            f"Invalid reference type '{reference_type}'. Supported types are: {', '.join(valid_types)}.",
            ephemeral=True
        )
        return

    if not identifier.replace(".", "").isalnum():
        await interaction.response.send_message(
            "Invalid identifier. It should be a valid numeric or alphanumeric value.",
            ephemeral=True
        )
        return

    if not title.strip():
        await interaction.response.send_message("Title cannot be empty.", ephemeral=True)
        return

    if not authors.strip():
        await interaction.response.send_message("Author(s) field cannot be empty.", ephemeral=True)
        return

    try:
        result = insert_reference(str(interaction.user.id), reference_type, identifier, title, authors)
        await interaction.response.send_message(result, ephemeral=False)

    except Exception as e:
        await interaction.response.send_message("An error occurred while adding the reference.", ephemeral=True)
        print(f"Error: {e}")


@bot.tree.command(name="search_reference", description="Search for academic references by criteria.")
async def search_reference(interaction: discord.Interaction, query: str):
    """
    Slash command to search for academic references based on a query parameter.
    """
    if not query.strip():
        await interaction.response.send_message("Query cannot be empty.", ephemeral=True)
        return

    try:
        results = fetch_references({"query": query})

        if results:
            response = "\n".join(
                [f"ID: {r[0]}, Type: {r[2]}, Identifier: {r[3]}, Title: {r[4]}, Authors: {r[5]}, Added: {r[6]}" for r in results]
            )
            await interaction.response.send_message(f"Search Results:\n{response}", ephemeral=False)
        else:
            await interaction.response.send_message("No references found matching the criteria.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error occurred during the search.", ephemeral=True)
        print(f"Error: {e}")


try:
    print("Starting the bot...")
    bot.run(TOKEN)
except Exception as e:
    print(f"Error starting the bot: {e}")

import os
import csv
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from ms_graph import get_access_token  # Import the Microsoft Graph authentication function

# Load environment variables from the .env file
load_dotenv('configs/.env')  # Load environment variables from the correct path
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieves the bot token from the environment variables

# Print statement to confirm if the token is being loaded
print(f"Loaded token: {TOKEN}")

# Set up intents (required by discord.py 2.0 and above)
intents = discord.Intents.default()  # Loads default intents (basic events like message creation)
intents.messages = True  # Enable message reading (required for command handling)
intents.message_content = True  # Enable message content intent

# Initialize the bot with a command prefix (!) and specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    Event handler that triggers when the bot successfully connects to Discord.
    Prints a confirmation message with the bot's name.
    Also syncs slash commands with Discord.
    """
    await bot.tree.sync()  # Syncs the slash commands with Discord
    print(f'Logged in as {bot.user.name} and slash commands are ready!')

    # Test Microsoft Graph authentication
    token = get_access_token()
    if token:
        print(f"Access Token: {token}")
    else:
        print("Failed to obtain access token.")

@bot.tree.command(name="add_reference", description="Add an academic reference with type, identifier, title, and author(s).")
async def add_reference(interaction: discord.Interaction, reference_type: str, identifier: str, title: str, authors: str):
    """
    Slash command to add an academic reference with type, identifier, title, and author(s).

    Parameters:
    interaction (discord.Interaction): The context of the interaction (slash command).
    reference_type (str): The type of reference (e.g., B for Book, D for Dictionary).
    identifier (str): A Dewey Decimal number or another unique identifier.
    title (str): The title of the reference.
    authors (str): The author(s) of the reference.

    Returns:
    Sends a success message or an error message back to the user based on the input validity.
    """
    # Step 1: Define supported reference types
    valid_types = ["B", "D", "SA", "N", "MA", "C", "T", "AVM", "BLG", "L", "O", "SM", "E"]

    # Step 2: Validate the reference type
    if reference_type not in valid_types:
        await interaction.response.send_message(
            f"Invalid reference type '{reference_type}'. Supported types are: {', '.join(valid_types)}.",
            ephemeral=True
        )
        return

    # Step 3: Validate the identifier
    if not identifier.replace(".", "").isalnum():
        await interaction.response.send_message(
            "Invalid identifier. It should be a valid numeric or alphanumeric value.",
            ephemeral=True
        )
        return

    # Step 4: Validate the title
    if not title.strip():
        await interaction.response.send_message("Title cannot be empty.", ephemeral=True)
        return

    # Step 5: Validate authors
    if not authors.strip():
        await interaction.response.send_message("Author(s) field cannot be empty.", ephemeral=True)
        return

    try:
        # Step 6: Store the reference in the CSV file
        store_reference_in_csv(reference_type, identifier, title, authors)

        # Step 7: Send a success message
        await interaction.response.send_message(
            f"Reference '{title}' by {authors} added successfully under type '{reference_type}' with identifier '{identifier}'.",
            ephemeral=False
        )
    except Exception as e:
        await interaction.response.send_message("An error occurred while adding the reference.", ephemeral=True)
        print(f"Error: {e}")

def store_reference_in_csv(reference_type, identifier, title, authors):
    """
    Appends a new academic reference to a CSV file.

    Parameters:
    reference_type (str): The type of the reference (e.g., B for Book, D for Dictionary).
    identifier (str): The Dewey Decimal number or another unique identifier.
    title (str): The title of the reference.
    authors (str): The author(s) of the reference.
    """
    # Path to the CSV file in your OneDrive-synced folder
    csv_file_path = "C:/Users/diego_dx9e5pi/OneDrive/Biblioteca - Library/academic_references.csv"

    try:
        # Open the file in append mode and write the new reference
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([reference_type, identifier, title, authors, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        raise

# Error handling for bot startup
try:
    print("Starting the bot...")
    bot.run(TOKEN)
except Exception as e:
    print(f"Error starting the bot: {e}")

# Imports
import discord
from discord.ext import commands
import httpx

# Intents + Prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='d!', intents=intents)

# When bot is ready
@bot.event
async def on_ready():
    print(f'Dog command is now ready!')

# Dog command
@bot.command(name='dog')
async def get_dog_picture(ctx):
    """Get a random dog picture."""
    dog_api_url = 'https://dog.ceo/api/breeds/image/random'

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(dog_api_url)
            dog_data = response.json()

        dog_picture_url = dog_data['message']
        await ctx.send(f"Found a funny dog picture!\n{dog_picture_url}")
    except Exception as e:
        print(f'Error fetching dog picture: {e}')
        await ctx.send('An error occurred while fetching the dog picture. Please try again later.')

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `d!help` for a list of available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Check the command usage with `!help`.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"Error executing the command: {error.original}")
    else:
        await ctx.send(f"An error occurred: {error}")

# Bot token
bot.run('your_token')

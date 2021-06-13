import discord, os
from discord.ext import commands

token = os.getenv("IOASIS_TOKEN")

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Start!")

@bot.command(brief = "For developers only.")
async def reload(ctx, extension):
    bot.reload_extension(extension)
    print("Reload complete.")

bot.load_extension("cf_cog")
bot.run(token)
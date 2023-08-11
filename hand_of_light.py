import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import eien_utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="#",intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"User: {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return
    if eien_utils.should_reply(message):
        await message.reply(embed=eien_utils.ping_reminder_embed())

bot.run(TOKEN)

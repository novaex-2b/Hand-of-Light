import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import eien
import eien_utils

load_dotenv()
TOKEN = os.getenv('PROD_TOKEN')
#TOKEN = os.getenv('TEST_TOKEN')

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

@bot.command()
@commands.has_any_role(eien.Guild.moderations_roles)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send('Command tree synced!')

@bot.tree.command(name="reminder")
@commands.has_any_role(eien.Guild.moderations_roles)
@app_commands.describe(role='the fan role to ping')
async def reminder(interaction: discord.Interaction, role: discord.Role):
    reminder_modal = eien_utils.Reminder()
    reminder_modal.set_role(role)
    await interaction.response.send_modal(reminder_modal)

@bot.tree.command(name="schedule")
@commands.has_any_role(eien.Guild.moderations_roles)
async def schedule(interaction: discord.Interaction):
    schedule_modal = eien_utils.Schedule()
    await interaction.response.send_modal(schedule_modal)

bot.run(TOKEN)

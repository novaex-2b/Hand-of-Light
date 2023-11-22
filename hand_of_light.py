import discord
from discord.ext import commands
from discord import app_commands
from tinydb import TinyDB,Query
from typing import Literal
import os
from dotenv import load_dotenv
import eien
import eien_utils
import time
import logging

load_dotenv()
TOKEN = os.getenv('PROD_TOKEN')
#TOKEN = os.getenv('TEST_TOKEN')
db = TinyDB("db.json")
searcher = Query()

bot = commands.Bot(command_prefix="#",intents=discord.Intents.all())
handler = logging.FileHandler(filename='log/hol.log',encoding='utf-8',mode='w')

@bot.event
async def on_ready():
    print(f"User: {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return
    if eien_utils.should_reply(message):
        db.insert({"username":message.author.display_name,"user_id":message.author.id,"time":int(time.time())})
        await message.reply(embed=eien_utils.ping_reminder_embed(),ephemeral=True)

@bot.command()
@commands.check_any(commands.is_owner(),commands.has_any_role(eien.Guild.moderations_roles))
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send('Command tree synced!')

@bot.tree.command(name="reminder")
@commands.check_any(commands.is_owner(),commands.has_any_role(eien.Guild.moderations_roles))
@app_commands.describe(role='the fan role to ping')
async def reminder(interaction: discord.Interaction, role: discord.Role):
    reminder_modal = eien_utils.Reminder()
    reminder_modal.set_role(role)
    await interaction.response.send_modal(reminder_modal)

@bot.tree.command(name="schedule")
@commands.check_any(commands.is_owner(),commands.has_any_role(eien.Guild.moderations_roles))
async def schedule(interaction: discord.Interaction):
    schedule_modal = eien_utils.Schedule()
    await interaction.response.send_modal(schedule_modal)

@bot.tree.command(name="mentionwarns")
@commands.check_any(commands.is_owner(),commands.has_any_role(eien.Guild.moderations_roles))
@app_commands.describe(user='the user to check')
async def mention_warns(interaction: discord.Interaction, user: discord.User):
    print(user.id)
    warn_count = len(db.search(searcher.user_id == user.id))
    await interaction.response.send_message(content="<@{}> has been warned {} time(s) for leaving mentions on in replies".format(user.id,warn_count))

@bot.tree.command(name="ping")
@commands.check_any(commands.is_owner(), commands.has_any_role(eien.Guild.moderations_roles))
async def ping(interaction: discord.Interaction):
    latency = int(bot.latency * 1000)
    em = None
    if latency < 51:
        em = discord.Embed(title="Pong!",description="The latency is {}ms".format(latency),colour=discord.Colour.from_rgb(156,207,216))
    elif latency < 101:
        em = discord.Embed(title="Pong!",description="The latency is {}ms".format(latency),colour=discord.Colour.from_rgb(246,193,119))
    else:
        em = discord.Embed(title="Pong!",description="The latency is {}ms".format(latency),colour=discord.Colour.from_rgb(235,111,146))
    await interaction.response.send_message(embed=em,ephemeral=True)

@bot.tree.command(name="when")
@commands.check_any(commands.is_owner(), commands.has_any_role(eien.Guild.moderations_roles))
@app_commands.describe(checkdate='The date to get the interval to.')
async def when(interaction: discord.Interaction, checkdate: str):
    when_embed = eien_utils.when_util(checkdate)
    await interaction.response.send_message(embed=when_embed,ephemeral=True)

@bot.tree.command(name="help")
@commands.check_any(commands.is_owner(), commands.has_any_role(eien.Guild.moderations_roles))
@app_commands.describe(command='The command to view info for')
async def help(interaction: discord.Interaction, command: Literal["when","reminder","schedule","mentionwarns","ping"]=None):
    help_embed = eien_utils.help_embed(command)
    await interaction.response.send_message(embed=help_embed,ephemeral=True)

@bot.tree.command(name="blaise")
@commands.check_any(commands.is_owner(), commands.has_any_role(eien.Guild.moderations_roles))
async def blaise(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File("../res/little_shit.mp4"))

bot.run(TOKEN, log_handler=handler)

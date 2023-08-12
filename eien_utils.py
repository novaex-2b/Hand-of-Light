import discord
import eien

def should_reply(message):
    if (len(message.mentions) < 1):
        return False
    author_roles = [role.id for role in message.author.roles]
    if any(role in eien.ALLOWED_ROLES for role in author_roles):
        return False
    mentioned_member = message.mentions[0]
    if (mentioned_member.id in eien.TALENTS):
        return True

def ping_reminder_embed():
    WARNING = "Please turn off mentions in your replies to any of the talents. See the image below on where to locate this option."
    em = discord.Embed(description=WARNING,colour=discord.Colour.from_rgb(235,111,146))
    em.set_image(url="https://i.imgur.com/1NmLHzF.png")
    return em

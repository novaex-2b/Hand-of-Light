import discord
import eien
from discord import ui
from dateparser import parse
from datetime import timedelta
from innertube import InnerTube

def should_reply(message):
    if (len(message.mentions) < 1):
        return False
    author_roles = [role.id for role in message.author.roles]
    if any(role in eien.Guild.replies_allowed for role in author_roles):
        return False
    mentioned_member = message.mentions[0]
    if (mentioned_member.id in eien.Guild.talents):
        return True

def ping_reminder_embed():
    em = discord.Embed(description=eien.Placeholders.reply_warning,colour=discord.Colour.from_rgb(235,111,146))
    em.set_image(url=eien.Placeholders.mention_img)
    return em

class Reminder(ui.Modal, title='Stream Reminder'):
    role = ""
    stream_url = ui.TextInput(label='URL',placeholder=eien.Placeholders.announce_url)
    reminder_text = ui.TextInput(label='Reminder Caption',style=discord.TextStyle.paragraph,placeholder=eien.Placeholders.announce_reminder)

    def set_role(self,role: discord.Role):
        self.role = str(role.id)

    def fetch_stream_time(self):
        vid_id = str(self.stream_url).split("watch?v=")[1]
        vid_data = InnerTube("WEB").player(video_id=vid_id)
        start_time = vid_data["playabilityStatus"]["liveStreamability"]["liveStreamabilityRenderer"]["offlineSlate"]["liveStreamOfflineSlateRenderer"]["scheduledStartTime"]
        return start_time

    async def on_submit(self, interaction: discord.Interaction):
        time_until = "[<t:" + self.fetch_stream_time() + ":R>](" + str(self.stream_url) + ")"
        reminder_str = "```\n <@&" + self.role + "> " + str(self.reminder_text).format(time_until) + "\n```"
        em = discord.Embed(description=reminder_str)
        await interaction.response.send_message(embed=em)

class Schedule(discord.ui.Modal, title='Schedule Input'):
    name = discord.ui.TextInput(label="Name",placeholder=eien.Placeholders.schedule_talent)
    in_timezone = discord.ui.TextInput(label="TIMEZONE",placeholder=eien.Placeholders.schedule_tz)
    in_schedule = discord.ui.TextInput(label="DATES,TIMES,AND ACTIVITIES",style=discord.TextStyle.paragraph,placeholder=eien.Placeholders.schedule_example)

    def ordinal(self,n):
        s = ('th', 'st', 'nd', 'rd') + ('th',)*10
        v = n%100
        if v > 13:
            return f'{n}{s[v%10]}'
        else:
            return f'{n}{s[v]}'

    def parse_schedule(self):
        parsed_schedule = []
        for stream in str(self.in_schedule).split('\n'):
            stream_time,stream_title = stream.split('~')
            stream_time = stream_time + " " + str(self.in_timezone)
            parsed_schedule.append((parse(stream_time,settings={'PREFER_DATES_FROM': 'future'}),stream_title))
        parsed_tz = parsed_schedule[0][0].strftime("UTC%z")
        return parsed_schedule,parsed_tz

    def date_range(self,first_stream):
        week_start = first_stream - timedelta(days=first_stream.weekday() % 7)
        week_end = week_start + timedelta(days=6)
        return "({} - {})".format(self.ordinal(week_start.day),self.ordinal(week_end.day))

    def make_schedule(self):
        parsed_schedule,parsed_tz = self.parse_schedule()
        schedule_text = f"**{str(self.name)}'s** Schedule {self.date_range(parsed_schedule[0][0])}\n\n"
        for stream in parsed_schedule:
            schedule_text += f"<t:{str(int(stream[0].timestamp()))}:F> **{stream[1]}**\n"
        schedule_text += "\n*Times displayed are automatically converted to your local timezone.*"
        return schedule_text,parsed_tz

    async def on_submit(self, interaction: discord.Interaction):
        schedule_text,parsed_tz = self.make_schedule()
        em = discord.Embed(description=schedule_text)
        em.add_field(name="Markdown",value=f"```\n{schedule_text}\n```",inline=False)
        em.add_field(name="Talent",value=f"`{self.name}`")
        em.add_field(name="Input Timezone",value=f"`{self.in_timezone}`")
        em.add_field(name="Parsed Timezone",value=f"`{parsed_tz}`")
        em.add_field(name="Date,Time, and Stream",value=f"```{str(self.in_schedule)}```",inline=False)
        await interaction.response.send_message(embed = em)

import discord
from discord.ext import commands
from discord.ui import Select, View
from datetime import datetime
import platform
import ezcord
import psutil
import time
import sqlite3

class BotInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()  

    def get_uptime(self):
        # Berechnet die Uptime des Bots
        uptime_seconds = int(time.time() - self.start_time)
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Dynamisch die Uptime-Formatierung erstellen
        uptime_string = ""
        if days > 0:
            uptime_string += f"{days} Tage "
        if hours > 0 or days > 0:
            uptime_string += f"{hours} Stunden "
        if minutes > 0 or hours > 0 or days > 0:
            uptime_string += f"{minutes} Minuten "
        uptime_string += f"{seconds} Sekunden"
        
        return uptime_string
    
    @commands.slash_command(name="botinfo", description="Zeigt Informationen über den Bot an")
    async def botinfo(self, ctx):
       
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        bot_avatar = self.bot.user.display_avatar.url
        bot_created_at = self.bot.user.created_at.strftime("%d.%m.%Y")
        if self.bot.user.discriminator == "0":
            bot_username = self.bot.user.name
        else:  
            bot_username = f"{self.bot.user.name}#{self.bot.user.discriminator}"
        
        # Holen der Bot-Anwendungsinformationen
        application_info = await self.bot.application_info()
        
       
        if hasattr(application_info, 'team'):
            team_name = application_info.team.name
            team_members = application_info.team.members
            developers = "\n".join([f"{member.name}#{member.discriminator}" for member in team_members])
        else:
            team_name = "Kein Team"
            developers = f"Owner: {application_info.owner.name}#{application_info.owner.discriminator}"

        guild_count = len(self.bot.guilds)
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        total_channels = sum(len(guild.channels) for guild in self.bot.guilds)
        total_emojis = sum(len(guild.emojis) for guild in self.bot.guilds)
        total_commands = len(self.bot.application_commands)
        total_shards = self.bot.shard_count or 1

        python_version = platform.python_version()
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        pycord_version = discord.__version__
        ezcord_version = ezcord.__version__
        bot_latency = round(self.bot.latency * 1000, 2)
        api_start = time.perf_counter()
        await ctx.respond("<:load:1316792001454411840> | Lade bot-infos...", ephemeral=False)
        api_latency = round((time.perf_counter() - api_start) * 1000, 2)
        db_start = time.perf_counter()
        conn = sqlite3.connect("database/latency_test.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ping_test (id INTEGER PRIMARY KEY)")
        conn.commit()
        db_latency = round((time.perf_counter() - db_start) * 1000, 2)
        conn.close()
        uptime = self.get_uptime()   


        embed = discord.Embed(color=0x00ff00)
        embed.set_thumbnail(url=bot_avatar)

        embed.set_author(name=f"{bot_name}'s Information", icon_url=bot_avatar)
        embed.add_field(name="<:bot:1314904250987315230> About Bot", value=f"> Bot's Mention: <@!{bot_id}>\n > Bot's Username: {bot_username} \n > Bot's ID: {bot_id}\n > Bot's Owner: {team_name}", inline=False)
        embed.add_field(name="<:discordstats:1314912164837855313> Discord Stats", value=f"> Total Guilds: {guild_count}\n > Total Users: {total_members} \n > Total Channels: {total_channels}\n > Total Emojis: {total_emojis} \n > Total Commands: {total_commands} ", inline=False)
        embed.add_field(name="<:system:1314917509563945030> System Info", value=f"> Total Shards: ``{total_shards}``\n > Uptime: ``{uptime}`` \n > CPU Usage: ``{cpu_usage}%``\n > Memory Usage: ``{memory_usage}%``\n > My Websocket Latency: ``{bot_latency}ms`` ({bot_latency / 1000:.3f}s)\n> API Latency: ``{api_latency}ms`` ({api_latency / 1000:.3f}s) ms\n> Database Latency: ``{db_latency}ms`` ({db_latency / 1000:.3f}s)\n > Python Version: ``{python_version}``\n > pycord Version: ``{pycord_version}``\n > ezcord Version: ``{ezcord_version}``", inline=False)

        # Auswahlmenü (Select-Menu)
        select = Select(
            placeholder="Wählen Sie die Information, die Sie sehen möchten",
            options=[
            discord.SelectOption(label="Home", value="home", emoji="<:home:1314949585092739082>"),
            discord.SelectOption(label="About Bot", value="about_bot", emoji="<:bot:1314904250987315230>"),
            discord.SelectOption(label="Discord Stats", value="discord_stats", emoji="<:discordstats:1314912164837855313>"),
            discord.SelectOption(label="System Info", value="system_info", emoji="<:system:1314917509563945030>"),
            discord.SelectOption(label="Shard Info", value="shard_info", emoji="<:shard:1314948118009086034>"),
            discord.SelectOption(label="Developer", value="developer", emoji="👨‍💻")
            ]
        )

        async def select_callback(interaction):
            selected_value = select.values[0]
            
            
            guild_count = len(self.bot.guilds)
            total_members = sum(guild.member_count for guild in self.bot.guilds)
            total_channels = sum(len(guild.channels) for guild in self.bot.guilds)
            total_emojis = sum(len(guild.emojis) for guild in self.bot.guilds)
            total_commands = len(self.bot.application_commands)
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            bot_latency = round(self.bot.latency * 1000, 2)
            db_start = time.perf_counter()
            conn = sqlite3.connect("database/latency_test.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS ping_test (id INTEGER PRIMARY KEY)")
            conn.commit()
            db_latency = round((time.perf_counter() - db_start) * 1000, 2)
            conn.close()
            
            
            uptime = self.get_uptime()

            embed.clear_fields()
            
            if selected_value == "home":
                embed.add_field(name="<:bot:1314904250987315230> About Bot", value=f"> Bot's Mention: <@!{bot_id}>\n > Bot's Username: {bot_username} \n > Bot's ID: {bot_id}\n > Bot's Owner: {team_name}", inline=False)
                embed.add_field(name="<:discordstats:1314912164837855313> Discord Stats", value=f"> Total Guilds: {guild_count}\n > Total Users: {total_members} \n > Total Channels: {total_channels}\n > Total Emojis: {total_emojis} \n > Total Commands: {total_commands} ", inline=False)
                embed.add_field(name="<:system:1314917509563945030> System Info", value=f"> Total Shards: ``{total_shards}``\n > Uptime: ``{uptime}`` \n > CPU Usage: ``{cpu_usage}%``\n > Memory Usage: ``{memory_usage}%``\n > My Websocket Latency: ``{bot_latency}ms`` ({bot_latency / 1000:.3f}s)\n > Database Latency: ``{db_latency}ms`` ({db_latency / 1000:.3f}s)\n > Python Version: ``{python_version}``\n > pycord Version: ``{pycord_version}``\n > ezcord Version: ``{ezcord_version}``", inline=False)

            elif selected_value == "about_bot":
                embed.add_field(name="<:bot:1314904250987315230> About Bot", value=f"> Bot's Mention: <@!{bot_id}>\n > Bot's Username: {bot_username} \n > Bot's ID: {bot_id}\n > Bot's Owner: {team_name}\n > Created At: {bot_created_at}", inline=False)

            elif selected_value == "discord_stats":
                embed.add_field(name="<:discordstats:1314912164837855313> Discord Stats", value=f"> Total Guilds: {guild_count}\n > Total Users: {total_members} \n > Total Channels: {total_channels}\n > Total Emojis: {total_emojis} \n > Total Commands: {total_commands} ", inline=False)

            elif selected_value == "system_info":
                embed.add_field(name="<:system:1314917509563945030> System Info", value=f"> CPU Usage: ``{cpu_usage}%``\n > Memory Usage: ``{memory_usage}%``\n > My Websocket Latency: ``{bot_latency}ms`` ({bot_latency / 1000:.3f}s)\n > Database Latency: ``{db_latency}ms`` ({db_latency / 1000:.3f}s)\n > Python Version: ``{python_version}``\n > pycord Version: ``{pycord_version}``\n > ezcord Version: ``{ezcord_version}``\n > Uptime: ``{uptime}``", inline=False)

            elif selected_value == "shard_info":
                shard_info = []
                for shard_id in range(total_shards):
                    shard_guilds = [g for g in self.bot.guilds if g.shard_id == shard_id]
                    guild_count = len(shard_guilds)
                    member_count = sum(g.member_count for g in shard_guilds)
                    latency = round(self.bot.latency * 1000)
                    shard_info.append(f"> Shard ID: {shard_id}\n> Server: {guild_count}\n> Members: {member_count}\n> Latency: {latency}ms")

                embed.add_field(name="<:shard:1314948118009086034> Shard Information", value="\n".join(shard_info), inline=False)

            elif selected_value == "developer":
                embed.add_field(name="👨‍💻 Developer Team", value=f"> Team: {team_name}\n > Developer: {developers}", inline=False)
        
            await interaction.response.edit_message(embed=embed)

        select.callback = select_callback
        view = View()
        view.add_item(select)

        await ctx.interaction.edit_original_response(content=None, embed=embed, view=view)

def setup(bot):
    bot.add_cog(BotInfoCog(bot))

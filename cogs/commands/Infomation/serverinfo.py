import discord
from discord.ext import commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="serverinfo", description="💻 | Zeigt Praktische Infomationen Über diesen Server")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        # Serverdaten
        server_name = guild.name
        server_id = guild.id
        owner = guild.owner
        created_at = guild.created_at.strftime("%d.%m.%Y, %H:%M:%S")
        member_count = guild.member_count
        role_count = len(guild.roles)
        channel_count = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count
        user_joined_at = guild.get_member(ctx.author.id).joined_at.strftime("%d.%m.%Y, %H:%M:%S")
        members = sum(1 for member in guild.members if not member.bot)
        bots = sum(1 for member in guild.members if member.bot)
        custom_emojis = len(guild.emojis)
        categories = len(guild.categories)
        category_info = "\n".join([f"{category.name}: {len(category.channels)} Kanäle" for category in guild.categories])

        # Embed
        embed = discord.Embed(title=f"<:help:1314694961156984893> 〢 {server_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="<:daten:1314695566248247336> 〢 Discord Daten:", value=f"```• Server erstellt: {created_at}```\n```• Server beigetreten: {user_joined_at}```", inline=False)
        embed.add_field(name="<:serverid:1314701721758335126> 〢 ServerID:", value=f"```• {server_id}```", inline=False)
        embed.add_field(name="<:Emojis:1314704938353295430> 〢 Emojis:", value=f"```• {custom_emojis}```", inline=False)
        embed.add_field(name="<:owner:1314702691955376201> 〢 Server Owner:", value=f"```• {str(owner)}```", inline=False)
        embed.add_field(name="<:member:1314703172429680650> 〢 Member:", value=f"```• Mitglieder: {members} Bots: {bots}```", inline=False)
        embed.add_field(name="<:Serveraufbau:1314707679016652950> 〢 Serveraufbau:", value=f"```• Kanäle: {text_channels + voice_channels},Kategorien: {categories}, Rollen: {role_count}```", inline=False)
        embed.add_field(name="<:Boosts:1314710771695095818> 〢 Boost Anzahl:", value=f"```• {boost_count}```\n```• LVL: {boost_level}```", inline=False)

        await ctx.respond(embed=embed)

# Cog Setup
def setup(bot):
    bot.add_cog(ServerInfo(bot))

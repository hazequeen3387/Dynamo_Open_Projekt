import discord
from discord.ext import commands
from datetime import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="📑| User infomationen")
    async def userinfo(self, ctx: discord.ApplicationContext, user: discord.User = None):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return
        
        user = user or ctx.author

        
        user_discord_name = user.name
        user_nickname = user.display_name
        user_joined_at = None
        
        
        if ctx.guild:
            member = ctx.guild.get_member(user.id)
            if member:
                user_joined_at = member.joined_at
            else:
                user_joined_at = "N/A"  

        
        user_creation_date = user.created_at.strftime("%d.%m.%Y, %H:%M:%S")

       
        if user_joined_at != "N/A":
            user_joined_at = user_joined_at.strftime("%Y-%m-%d %H:%M:%S")
        
        rlist = []
        for role in member.roles:
            rlist.append(str(role.mention))
        rlist.reverse()

        embed = discord.Embed(title=f"<:help:1314694961156984893> 〢 {user_discord_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        
       
        embed.add_field(name="<:daten:1314695566248247336> 〢 Discord Daten:", value=f"```• Discord Installiert: {user_creation_date}```\n```• Server beigetreten: {user_joined_at if user_joined_at != 'N/A' else 'Nicht auf dem Server'}```", inline=False)
        embed.add_field(name="<:userid:1314701721758335126> 〢 UserID:", value=f"```• {user.id}```", inline=False)
        embed.add_field(name=f"Rollen: {len(member.roles) - 1}", value=','.join(rlist),inline=False)
        embed.set_author(name=f"{user_nickname}", icon_url=user.avatar.url if user.avatar else None)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(UserInfo(bot))

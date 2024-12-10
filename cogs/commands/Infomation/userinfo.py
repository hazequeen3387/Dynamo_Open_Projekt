import discord
from discord.ext import commands

class UserInfoView(discord.ui.View):
    def __init__(self, user, member):
        super().__init__()
        self.user = user 
        self.member = member
        self.user_discord_name = member.name
        self.user_nickname = member.display_name
        self.user_creation_date = member.created_at.strftime("%d.%m.%Y, %H:%M:%S")
        self.user_joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Nicht auf dem Server"

    @discord.ui.button(label="🔰 Home", style=discord.ButtonStyle.green)
    async def home_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Du kannst diesen Button nicht verwenden!", ephemeral=True)

        embed = discord.Embed(title=f"<:help:1314694961156984893> 〢 {self.user_discord_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=self.member.avatar.url if self.member.avatar else None)
        
        embed.add_field(
            name="<:daten:1314695566248247336> 〢 Discord Daten:",
            value=f"```• Discord Installiert: {self.user_creation_date}```\n"
                  f"```• Server beigetreten: {self.user_joined_at}```",
            inline=False
        )
        embed.add_field(name="<:userid:1314701721758335126> 〢 UserID:", value=f"```• {self.member.id}```", inline=False)
        rlist = [str(role.mention) for role in self.member.roles if role.name != "@everyone"]
        embed.add_field(name=f"Rollen: {len(self.member.roles) - 1}", value=', '.join(rlist) if rlist else "Keine Rollen", inline=False)
        embed.set_author(name=f"{self.user_nickname}", icon_url=self.member.avatar.url if self.member.avatar else None)
        
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Avatar", style=discord.ButtonStyle.gray)
    async def avatar_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Du kannst diesen Button nicht verwenden!", ephemeral=True)

        embed = discord.Embed(title=f"🖼 Avatar von {self.member.display_name}")
        embed.set_image(url=self.member.avatar.url if self.member.avatar else None)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Banner", style=discord.ButtonStyle.blurple)
    async def banner_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Du kannst diesen Button nicht verwenden!", ephemeral=True)

        embed = discord.Embed(title=f"Banner von {self.member.display_name}")
        
        try:
            user = await interaction.client.fetch_user(self.member.id)
            banner = user.banner
            
            if banner:
                embed.set_image(url=banner.url)
            else:
                embed.add_field(name=" ", value="Dieser User hat keinen Banner")
        except:
            embed.add_field(name=" ", value="Banner konnte nicht geladen werden")
            
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Berechtigungen", style=discord.ButtonStyle.red)
    async def permissions_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Du kannst diesen Button nicht verwenden!", ephemeral=True)

        perms = [perm[0] for perm in self.member.guild_permissions if perm[1]]
        embed = discord.Embed(title=f"🛡 Berechtigungen von {self.member.display_name}", description=", ".join(perms), color=discord.Color.red())
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Rollen", style=discord.ButtonStyle.blurple)
    async def roles_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            return await interaction.response.send_message("❌ Du kannst diesen Button nicht verwenden!", ephemeral=True)

        roles = [role.mention for role in self.member.roles if role.name != "@everyone"]
        roles_text = ", ".join(roles) if roles else "Keine Rollen"
        embed = discord.Embed(title=f"🔷 Rollen von {self.member.display_name}", description=roles_text, color=discord.Color.blue())
        await interaction.response.edit_message(embed=embed)


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="userinfo", description="📑 Zeigt Informationen über einen Nutzer.")
    async def userinfo(self, ctx: discord.ApplicationContext, user: discord.User = None):
        user = user or ctx.author
        member = ctx.guild.get_member(user.id) or user

        user_discord_name = member.name
        user_nickname = member.display_name
        user_creation_date = member.created_at.strftime("%d.%m.%Y, %H:%M:%S")
        user_joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Nicht auf dem Server"
        rlist = [str(role.mention) for role in member.roles if role.name != "@everyone"]

        embed = discord.Embed(title=f"<:help:1314694961156984893> 〢 {user_discord_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        embed.add_field(
            name="<:daten:1314695566248247336> 〢 Discord Daten:",
            value=f"```• Discord Installiert: {user_creation_date}```\n"
                  f"```• Server beigetreten: {user_joined_at}```",
            inline=False
        )
        embed.add_field(name="<:userid:1314701721758335126> 〢 UserID:", value=f"```• {member.id}```", inline=False)
        embed.add_field(name=f"Rollen: {len(member.roles) - 1}", value=', '.join(rlist) if rlist else "Keine Rollen", inline=False)
        embed.set_author(name=f"{user_nickname}", icon_url=member.avatar.url if member.avatar else None)

        view = UserInfoView(ctx.author, member)
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(UserInfo(bot))

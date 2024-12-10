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

        view = ServerInfoButtons(ctx, guild)
        await ctx.respond(embed=embed, view=view)

        


class ServerInfoButtons(discord.ui.View):
    def __init__(self, ctx, guild):
        super().__init__()
        self.ctx = ctx
        self.guild = guild

    # Home Button
    @discord.ui.button(label="Home", style=discord.ButtonStyle.primary, emoji="🏠")
    async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = self.guild
        server_name = guild.name
        created_at = guild.created_at.strftime("%d.%m.%Y, %H:%M:%S")
        member_count = guild.member_count
        role_count = len(guild.roles)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        boost_count = guild.premium_subscription_count
        boost_level = guild.premium_tier
        custom_emojis = len(guild.emojis)
        categories = len(guild.categories)
        user_joined_at = guild.get_member(interaction.user.id).joined_at.strftime("%d.%m.%Y, %H:%M:%S")
        owner = guild.owner
        members = sum(1 for member in guild.members if not member.bot)
        bots = sum(1 for member in guild.members if member.bot)

        embed = discord.Embed(title=f"<:help:1314694961156984893> 〢 {server_name}", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="<:daten:1314695566248247336> 〢 Discord Daten:", 
                        value=f"```Server erstellt: {created_at}```\n```Beigetreten: {user_joined_at}```", inline=False)
        embed.add_field(name="<:serverid:1314701721758335126> 〢 ServerID:", 
                        value=f"```{guild.id}```", inline=False)
        embed.add_field(name="<:Emojis:1314704938353295430> 〢 Emojis:", 
                        value=f"```{custom_emojis}```", inline=False)
        embed.add_field(name="<:owner:1314702691955376201> 〢 Server Owner:", 
                        value=f"```{str(owner)}```", inline=False)
        embed.add_field(name="<:member:1314703172429680650> 〢 Member:", 
                        value=f"```Mitglieder: {members} Bots: {bots}```", inline=False)
     
        embed.add_field(name="<:Serveraufbau:1314707679016652950> 〢 Serveraufbau:", value=f"```• Kanäle: {text_channels + voice_channels},Kategorien: {categories}, Rollen: {role_count}```", inline=False)
        embed.add_field(name="<:Boosts:1314710771695095818> 〢 Boost Anzahl:", value=f"```• {boost_count}```\n```• LVL: {boost_level}```", inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    # Server Avatar Button
    @discord.ui.button(label="ServerAvatar", style=discord.ButtonStyle.secondary, emoji="🖼")
    async def server_avatar(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild_icon = self.ctx.guild.icon.url if self.ctx.guild.icon else "Kein Server-Avatar vorhanden."
        embed = discord.Embed(title="Server Avatar", color=discord.Color.blue())
        if self.ctx.guild.icon:
            embed.set_image(url=guild_icon)
        else:
            embed.description = "Kein Server-Avatar vorhanden."
        await interaction.response.edit_message(embed=embed, view=self)

    # Server Banner Button
    @discord.ui.button(label="Serverbanner", style=discord.ButtonStyle.secondary, emoji="🎭")
    async def server_banner(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="Server Banner", color=discord.Color.blue())
        if self.ctx.guild.banner:
            embed.set_image(url=self.ctx.guild.banner.url)
        else:
            embed.description = "Kein Server-Banner vorhanden."
        await interaction.response.edit_message(embed=embed, view=self)

    
    @discord.ui.button(label="Server Emojis", style=discord.ButtonStyle.success, emoji="😝")
    async def server_emojis(self, button: discord.ui.Button, interaction: discord.Interaction):
        emojis = self.ctx.guild.emojis
        embed = discord.Embed(title="Server Emojis", color=discord.Color.green())
        
        if emojis:
            
            chunk_size = 20
            emoji_chunks = [emojis[i:i + chunk_size] for i in range(0, len(emojis), chunk_size)]
            
            for i, chunk in enumerate(emoji_chunks, 1):
                emoji_list = " ".join(str(emoji) for emoji in chunk)
                embed.add_field(
                    name=f"Emojis Liste {i}", 
                    value=emoji_list, 
                    inline=False
                )
            
            embed.set_footer(text=f"Insgesamt {len(emojis)} Emojis")
        else:
            embed.description = "Dieser Server hat keine benutzerdefinierten Emojis."
        
        await interaction.response.edit_message(embed=embed, view=self)

    
    @discord.ui.button(label="Server Rollen", style=discord.ButtonStyle.danger, emoji="🌐")
    async def server_roles(self, button: discord.ui.Button, interaction: discord.Interaction):
        roles = self.ctx.guild.roles[1:]  # Skip @everyone role
        embed = discord.Embed(title="Server Rollen", color=discord.Color.red())
        
        if roles:
            chunk_size = 20
            role_chunks = [roles[i:i + chunk_size] for i in range(0, len(roles), chunk_size)]
            
            for i, chunk in enumerate(role_chunks, 1):
                role_mentions = ", ".join([role.mention for role in chunk])
                embed.add_field(
                    name=f"Rollen Liste {i}", 
                    value=role_mentions, 
                    inline=False
                )
            
            embed.set_footer(text=f"Insgesamt {len(roles)} Rollen")
        else:
            embed.description = "Keine Rollen vorhanden."
            
        await interaction.response.edit_message(embed=embed, view=self)

# Cog Setup
def setup(bot):
    bot.add_cog(ServerInfo(bot))

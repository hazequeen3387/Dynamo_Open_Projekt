import discord
from discord.ext import commands
from datetime import timedelta
from discord import Option

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.slash_command(description="Lösche eine bestimmte Anzahl von Nachrichten im aktuellen Kanal")
    async def clear(self, ctx, amount: int):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        if ctx.author.guild_permissions.manage_messages:
            deleted_messages = await ctx.channel.purge(limit=amount + 1)
            await ctx.respond(f"{len(deleted_messages) - 1} Nachrichten wurden gelöscht.", ephemeral=True)
        else:
            await ctx.respond("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)

    @commands.slash_command(name="roleall", description="Vergebe eine Rolle an alle User oder Bots.")
    @commands.has_permissions(manage_roles=True)
    async def roleall(
        self, 
        ctx: discord.ApplicationContext, 
        role: discord.Role, 
        target: Option(str, description="Wähle, ob die Rolle an 'user' oder 'bot' vergeben wird.", choices=["user", "bot"]) # type: ignore
    ):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        await ctx.defer(ephemeral=True)

        if role >= ctx.guild.me.top_role:
            await ctx.respond("Ich kann keine Rolle vergeben, die höher oder gleich meiner höchsten Rolle ist.", ephemeral=True)
            return
        
        count = 0
        for member in ctx.guild.members:
            if (target == "user" and not member.bot) or (target == "bot" and member.bot):
                if role not in member.roles:
                    try:
                        await member.add_roles(role)
                        count += 1
                    except discord.Forbidden:
                        await ctx.respond(f"Ich habe keine Berechtigung, die Rolle für {member.display_name} zu ändern.", ephemeral=True)
                        return

        await ctx.respond(f"Die Rolle **{role.name}** wurde erfolgreich an **{count}** Mitglieder ({target}) vergeben.", ephemeral=True)

    @commands.slash_command(description="Timeoute einen Member")
    @commands.has_permissions(moderate_members=True)
    async def timeout(
            self, ctx,
            member: discord.Option(discord.Member, "Wähle ein Member aus"), # type: ignore
            reason: discord.Option(str, "Wähle ein Grund aus", choices=[
                "Extremes Chatverhalten | Mute - 2 Stunden",
                "Extreme Beleidigungen | Mute - 1 Woche",
                "Missachtung von Team Anweisungen | Mute - 1 Tag",
                "Sensible Themen | Mute - 4 Tage",
                "Extreme Provokation | Mute 1 Woche",
                "Support-Missbrauch | Mute - 1 Tag",
            ], required=True) # type: ignore
    ):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        durations = {
            "Extremes Chatverhalten | Mute - 2 Stunden": timedelta(hours=2),
            "Extreme Beleidigungen | Mute - 1 Woche": timedelta(weeks=1),
            "Missachtung von Team Anweisungen | Mute - 1 Tag": timedelta(days=1),
            "Sensible Themen | Mute - 4 Tage": timedelta(days=4),
            "Extreme Provokation | Mute 1 Woche": timedelta(weeks=1),
            "Support-Missbrauch | Mute - 1 Tag": timedelta(days=1),
        }
        duration = durations[reason]

        try:
            await member.timeout_for(duration, reason=reason)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich getimeoutet",
                description=f"Der Member {member.mention} wurde getimeoutet\nGrund: {reason}",
                color=discord.Color.green()
            )
        except discord.Forbidden:
            embed = discord.Embed(
                title="⛔ | Fehler beim Timeout",
                description="Ich habe keine Berechtigung, um diesen Member zu timeouten.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        await ctx.respond(embed=embed)

    @commands.slash_command(description="Entferne einen Timeout")
    @commands.has_permissions(moderate_members=True)
    async def removetimeout(
            self, ctx,
            member: Option(discord.Member, "Wähle einen Member"), # type: ignore
    ):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="✅ | User wurde erfolgreich entmuted",
                description=f"Der Member {member.mention} wurde entmuted.",
                color=discord.Color.green()
            )
        except discord.Forbidden:
            embed = discord.Embed(
                title="⛔ | Fehler beim Entmuten",
                description="Ich habe keine Berechtigung, um diesen Member zu entmuten.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        await ctx.respond(embed=embed)

    @commands.slash_command(description="🚨 | Kicke einen Member vom Server")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self, 
        ctx, 
        member: Option(discord.Member, "Wähle einen Member, der gekickt werden soll"), # type: ignore
        reason: Option(str, "Gib einen Grund für den Kick an", required=False) # type: ignore
    ):
        guild = ctx.guild
        if guild is None:
            await ctx.respond("Dieses Command kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        if member == ctx.guild.owner:
            await ctx.respond("Ich kann den Besitzer des Servers nicht kicken.", ephemeral=True)
            return

        if member.top_role >= ctx.author.top_role:
            await ctx.respond("Du kannst keine Mitglieder kicken, die eine gleich hohe oder höhere Rolle als du haben.", ephemeral=True)
            return

        reason_text = reason if reason else "Kein Grund angegeben."
        
        
        try:
            dm_embed = discord.Embed(
                title="⛔ | Du wurdest vom Server gekickt",
                description=(
                    f"**Server:** {guild.name}\n"
                    f"**Grund:** {reason_text}"
                ),
                color=discord.Color.red()
            )
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass

        
        try:
            await member.kick(reason=reason_text)
            embed = discord.Embed(
                title="✅ | Member erfolgreich gekickt",
                description=f"{member.mention} wurde vom Server gekickt.\nGrund: {reason_text}",
                color=discord.Color.green()
            )
        except discord.Forbidden:
            embed = discord.Embed(
                title="⛔ | Fehler beim Kicken",
                description="Ich habe keine Berechtigung, um diesen Member zu kicken.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))

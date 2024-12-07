import discord
from discord.ext import commands

class InviteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="invite", description="📥 | Lade auf deinem Server ein oder trete unserem Support bei")
    async def invite(self, ctx):
       
        await ctx.respond(f"https://discord.gg/fRuCXJK85R\nhttps://discord.com/oauth2/authorize?client_id={self.bot.user.id}")

        
        embed = discord.Embed(
            title="Lade mich ein!",
           
            color=discord.Color.green()
        )
        embed.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url)
        embed.add_field(name="<:partner:1314732957017047070> | Gefällt dir unser Bot?", value=f"> • Falls du uns unterstützen willst, oder einfach nur mehr über {self.bot.user.name} wissen willst, [trete unserem Discord bei.](https://discord.gg/fRuCXJK85R)\n\n>  | Über unseren Server\n > • Unser [Server](https://discord.gg/fRuCXJK85R) ausführliche Tutorials.\n\n<:file:1314734131283886154> | Sonstige Informationenn > • Jeder Join hilft uns!\n\n<:link:1314734623200247819> | Bot Hinzufügen\n > 🔗 • [Klicke hier Um Bot Hinzuzufügen](https://discord.com/oauth2/authorize?client_id={self.bot.user.id})", inline=False)
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(InviteCommand(bot))

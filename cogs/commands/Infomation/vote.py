import discord
from discord.ext import commands
from discord.ui import Button, View

class VoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="vote", description="✨ | jetzt für und bekomme ein großes Dankeschön!")
    async def vote(self, ctx):
        vote_button = Button(label="Vote", url="https://top.gg/bot/1183600303476572251",emoji="<:top:1314723021583421612>")

        embed = discord.Embed(
            title="<:vote:1314722633186807808> | Vote für mich!",
            description="> <:Serveraufbau:1314707679016652950>   Vote mit dem unteren Button und trage einen großen Beitrag,\n >  zur Entwicklung bei.\n\n > <:messages:1314726452280688700> [Bot Hinzufügen](https://discord.com/oauth2/authorize?client_id=1183600303476572251) 〢 <:help:1314694961156984893> [Support](https://discord.gg/fRuCXJK85R)",
            color=discord.Color.blue()
        )
        

        view = View()
        view.add_item(vote_button)
        

        await ctx.respond(embed=embed, view=view)

# Setup the cog
def setup(bot):
    bot.add_cog(VoteCommand(bot))

import discord
from discord.ext import commands
import time
import sqlite3

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @discord.slash_command(name="ping", description="Zeigt die Bot-Latenz, API-Latenz und Datenbank-Latenz an.")
    async def ping(self, ctx: discord.ApplicationContext):
        
        bot_latency = round(self.bot.latency * 1000, 2)  
        
        
        api_start = time.perf_counter()
        await ctx.respond("⏳ Pinging...", ephemeral=False)
        api_latency = round((time.perf_counter() - api_start) * 1000, 2)

        
        db_start = time.perf_counter()
        conn = sqlite3.connect("latency_test.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ping_test (id INTEGER PRIMARY KEY)")
        conn.commit()
        db_latency = round((time.perf_counter() - db_start) * 1000, 2)
        conn.close()

       
        embed = discord.Embed(
            title="🏓 • Pong",
            description="Schauen Sie sich an, wie schnell unser Bot ist!",
            color=discord.Color.blue(),
        )
        embed.add_field(name="🤖 | **Bot Latency**", value=f"{bot_latency}ms ({bot_latency / 1000:.3f}s)", inline=False)
        embed.add_field(name="💻 | **API Latency**", value=f"{api_latency}ms ({api_latency / 1000:.3f}s)", inline=False)
        embed.add_field(name="📁 | **Database Latency**", value=f"{db_latency}ms ({db_latency / 1000:.3f}s)", inline=False)
        embed.set_footer(text=f"© {time.strftime('%Y')} • heute um {time.strftime('%H:%M')} Uhr")

        
        await ctx.interaction.edit_original_response(content=None, embed=embed)



def setup(bot):
    bot.add_cog(PingCommand(bot))

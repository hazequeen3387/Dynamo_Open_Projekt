import discord
from discord.ext import commands
import requests, time
import sqlite3
import clashai

class chatbotAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect('database/ai_setup.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ai_channels
                     (guild_id INTEGER, channel_id INTEGER, guild_name TEXT)''')
        conn.commit()
        conn.close()

    @discord.slash_command(name="ai_setup", description="Set up the AI channel for this server")
    @commands.has_permissions(administrator=True)
    async def ai_setup(self, ctx, channel: discord.TextChannel):
        
        conn = sqlite3.connect('database/ai_setup.db')
        c = conn.cursor()
        
        
        c.execute('SELECT * FROM ai_channels WHERE guild_id = ?', (ctx.guild_id,))
        if c.fetchone():
            c.execute('UPDATE ai_channels SET channel_id = ?, guild_name = ? WHERE guild_id = ?',
                      (channel.id, ctx.guild.name, ctx.guild.id))
        else:
            c.execute('INSERT INTO ai_channels VALUES (?, ?, ?)',
                      (ctx.guild.id, channel.id, ctx.guild.name))
        
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="<:chatgpt:1316773144438247505> | Kanal erfolgreich konfiguriert:",
            description=f"Der AI-Kanal wurde erfolgreich auf {channel.mention} gesetzt.\n\n <:bothinzufgen:1316779017059438673> [Bot Hinzufügen](https://discord.com/oauth2/authorize?client_id=1183600303476572251) 〢 <:help:1314694961156984893> [Support](https://discord.gg/fRuCXJK85R)",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(name="ai_disable", description="Disable AI for this server")
    @commands.has_permissions(administrator=True)
    async def ai_disable(self, ctx):
        conn = sqlite3.connect('database/ai_setup.db')
        c = conn.cursor()
    
        c.execute('DELETE FROM ai_channels WHERE guild_id = ?', (ctx.guild.id,))
    
        conn.commit()
        conn.close()

        await ctx.respond("AI has been disabled for this server", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        
        conn = sqlite3.connect('database/ai_setup.db')
        c = conn.cursor()
        c.execute('SELECT channel_id FROM ai_channels WHERE guild_id = ?', (message.guild.id,))
        result = c.fetchone()
        conn.close()

        if not result or message.channel.id != result[0]:
            return

        url = 'https://api.clashai.eu/v1/chat/completions'
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Provide your response and include 2-3 relevant follow-up suggestions, separated by '|' at the end of your message. Example: Your response...|Suggestion 1|Suggestion 2|Suggestion 3"},
                {"role": "user", "content": message.content}
            ]
        }
        headers = {'Authorization': 'Bearer sk-hrRJrEOfH6vJRuk6g4AzL52lPvUiS0gYLfkpMv5tO0GlnqiH'}

        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers)

        if response.ok:
            print(f"> Request took {round(time.time() - start_time, 2)} seconds")
            try:
                api_response = response.json()['choices'][0]['message']['content']
                parts = api_response.split('|')
                main_response = parts[0]
                suggestions = parts[1:] if len(parts) > 1 else []
            except KeyError as e:
                main_response = f"Error accessing response: {e}\nResponse: {response.json()}"
                suggestions = []
        else:
            main_response = f"Request failed with status code {response.status_code}\nError response: {response.text}"
            suggestions = []

        embed = discord.Embed(
            title="ASFA Bot",
            description=f"Response: {main_response}",
            color=discord.Color.blue()
        )

        embed.set_footer(text="AI Response")
        
        class VerticalButtonView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="\u200b", disabled=True, row=0))
                
            def add_vertical_button(self, label, row):
                button = discord.ui.Button(
                    label=label.strip()[:80],
                    style=discord.ButtonStyle.secondary,
                    disabled=True,
                    row=row
                )
                self.add_item(button)

        view = VerticalButtonView()
        
    
        for i, suggestion in enumerate(suggestions[:3]):
            view.add_vertical_button(suggestion, i + 1)

        await message.reply(embed=embed, view=view)




def setup(bot):
    bot.add_cog(chatbotAI(bot))

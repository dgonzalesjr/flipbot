import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def flip(ctx):
    embed = discord.Embed(
        title="🎯 MATCH FOUND: Charizard",
        description="**Price**: $350\n**Buyer Max**: $400",
        color=0x00ff00
    )
    embed.add_field(
        name="Listing", value="[View Card](https://example.com)", inline=False
    )

    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(label="💳 Buy Now",
                          style=discord.ButtonStyle.link,
                          url="https://example.com/checkout"
                          ))

    await ctx.send(embed=embed, view=view)

bot.run(TOKEN)

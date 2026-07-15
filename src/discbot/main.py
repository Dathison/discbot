import os
import random
from urllib.parse import urlparse, urlunparse

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

botName = os.environ["BOT_NAME"]
discordToken = os.environ["DISCORD_TOKEN"]
testGuildId = os.environ["TEST_SERVER"]
guildIds = [
    discord.Object(id=int(gid))
    for gid in os.environ["MAIN_SERVERS"].split(",") + [testGuildId]
]


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)


def isValidUrl(url: str) -> bool:
    (
        """Checks whether a string is a valid URL and returns True/False. """
        """(Requires http(s)://)"""
    )
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])

    except ValueError:
        return False


@bot.event
async def on_ready() -> None:
    for server in guildIds:
        bot.tree.copy_global_to(guild=server)
        await bot.tree.sync(guild=server)
    print(f"Connected to {len(bot.guilds)} server(s):")
    for guild in bot.guilds:
        print(f" - {guild.name} (id: {guild.id})")

    print(f"{botName} online.")


@bot.command(
    description="Basic mic check. "
    "For ensuring the bot is actually running and responding."
)
async def peepee(ctx: commands.Context) -> None:
    await ctx.send("poopoo")


@bot.tree.command(
    name="instagram", description="Convert Instagram links to better embeds."
)
@app_commands.describe(
    input_link="The Instagram link you want to properly embed. "
    "(Requires http(s)://)"
)
async def instagram(interaction: discord.Interaction, input_link: str) -> None:
    if urlparse(input_link):
        if isValidUrl(input_link):
            link = urlparse(input_link)
            new_link = link._replace(netloc="kkinstagram.com", query="")

            await interaction.response.send_message(urlunparse(new_link))

        else:
            await interaction.response.send_message("Not a valid URL.")

    else:
        await interaction.response.send_message("There was an error.")


@bot.tree.command(
    name="reddit", description="Convert Reddit links to better embeds."
)
@app_commands.describe(
    input_link="The Reddit link you want to properly embed. "
    "(Requires http(s)://)"
)
async def reddit(interaction: discord.Interaction, input_link: str) -> None:
    if urlparse(input_link):
        if isValidUrl(input_link):
            link = urlparse(input_link)
            new_link = link._replace(netloc="redditez.com", query="")

            await interaction.response.send_message(urlunparse(new_link))

        else:
            await interaction.response.send_message("Not a valid URL.")

    else:
        await interaction.response.send_message("There was an error.")


@bot.tree.command(
    name="twitter", description="Convert X/Twitter links to better embeds."
)
@app_commands.choices(
    site=[
        app_commands.Choice(name="fxtwitter", value="fxtwitter.com"),
        app_commands.Choice(name="vxtwitter", value="vxtwitter.com"),
        app_commands.Choice(name="stupidpenisx", value="stupidpenisx.com"),
        app_commands.Choice(name="girlcockx", value="girlcockx.com"),
    ]
)
@app_commands.describe(
    input_link="The X/Twitter link you want to properly embed. "
    "(Requires http(s)://)",
    site="The embed service you want to use. "
    "Also removes tracking identifiers.",
)
async def twitter(
    interaction: discord.Interaction,
    input_link: str,
    site: app_commands.Choice[str],
) -> None:
    if urlparse(input_link):
        if isValidUrl(input_link):
            link = urlparse(input_link)
            new_link = link._replace(netloc=site.value, query="")

            await interaction.response.send_message(urlunparse(new_link))

        else:
            await interaction.response.send_message("Not a valid URL.")

    else:
        await interaction.response.send_message("There was an error.")


@bot.tree.command(name="dog", description="Posts a random dog picture.")
@app_commands.describe(user="Someone to tag alongside the dog picture.")
async def dog(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://dog.ceo/api/breeds/image/random") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.dog/{response.status}"
            )
            return

        data = await response.json()

    message = data["message"]

    if user is not None:
        await interaction.response.send_message(
            f"{user.mention} you've been sent a dog."
        )
        if interaction.channel is not None:
            await interaction.channel.send(message)
        else:
            await interaction.followup.send(message)
    else:
        await interaction.response.send_message(message)


@bot.tree.command(name="cat", description="Posts a random cat picture.")
@app_commands.describe(user="Someone to tag alongside the cat picture.")
async def cat(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://api.thecatapi.com/v1/images/search") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.cat/{response.status}"
            )
            return

        data = await response.json()

    message = data[0]["url"]

    if user is not None:
        await interaction.response.send_message(
            f"{user.mention} you've been sent a cat."
        )
        if interaction.channel is not None:
            await interaction.channel.send(message)
        else:
            await interaction.followup.send(message)
    else:
        await interaction.response.send_message(message)


@bot.tree.command(name="catfact", description="Posts a random cat fact.")
@app_commands.describe(user="Someone to tag alongside the cat fact.")
async def catfact(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://meowfacts.herokuapp.com/") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.cat/{response.status}"
            )
            return

        data = await response.json()

    message = data["data"][0]

    if user is not None:
        await interaction.response.send_message(
            f"{user.mention} You should know:\n{message}"
        )
    else:
        await interaction.response.send_message(message)


@bot.tree.command(name="grapes", description="Posts a random duck picture.")
@app_commands.describe(user="Someone to tag alongside the duck picture.")
async def grapes(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://random-d.uk/api/random") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.cat/{response.status}"
            )
            return

        data = await response.json()

    message = data["url"]

    if user is not None:
        await interaction.response.send_message(
            f"Heyyy {user.mention} *bam bam bam* Got any grapes?"
        )
        if interaction.channel is not None:
            await interaction.channel.send(message)
        else:
            await interaction.followup.send(message)
    else:
        await interaction.response.send_message(message)


@bot.tree.command(name="capy", description="Posts a random capy picture.")
@app_commands.describe(user="Someone to tag alongside the capy picture.")
async def capy(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://api.capy.lol/v1/capybara?json=true") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.dog/{response.status}"
            )
            return

        data = await response.json()

    message = data["data"]["url"]

    if user is not None:
        await interaction.response.send_message(
            f"{user.mention} you've been sent a capybara."
        )
        if interaction.channel is not None:
            await interaction.channel.send(message)
        else:
            await interaction.followup.send(message)
    else:
        await interaction.response.send_message(message)


@bot.tree.command(
    name="capyfact", description="Posts three random capybara facts."
)
@app_commands.describe(user="Someone to tag alongside the capybara facts.")
async def capyfact(
    interaction: discord.Interaction, user: discord.Member | None = None
) -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://api.capy.lol/v1/facts") as response,
    ):
        if response.status != 200:
            await interaction.response.send_message(
                f"https://http.dog/{response.status}"
            )
            return

        data = await response.json()

    facts = random.sample(data["data"], 3)
    message = "\n".join(f"- {fact}" for fact in facts)

    if user is not None:
        await interaction.response.send_message(
            f"{user.mention} You should know:\n{message}"
        )
    else:
        await interaction.response.send_message(message)


bot.run(discordToken)

import os
import traceback
import discord
from discord.ext.commands import Context
from discord import option
from insulter import insult, addInsult
from diceRoller import interpDice, addMacro
from bag import addToBag, findInbag, removeFromBag, printBag
from fileIO import getJSONFileContent, findOrCreateFile
from PokemonSession import PokemonSession
import DatabaseInteraction
from PokemonType import Pokemon
import constants

SESSION = PokemonSession()

def logCommandInfo(ctx, command) -> None:
    user = ctx.author
    channel = ctx.channel
    print(f"{command} called by {user} in {channel}")

def getServerFilePrefix(ctx) -> str:
    server_name = ctx.guild.name.replace(" ", "_")
    server_id = ctx.guild.id
    return f"{server_name}_{server_id}"

def getWhiteListServers() -> list[str]:
    servers = os.environ["SERVERS"].split(",")
    for s in servers:
        s = int(s.strip())
    return servers
#TODO make it so only the server admin can ask for this file to be created
async def autoCompleteRollMacros(ctx: discord.AutocompleteContext) -> list:
    filePrefix = getServerFilePrefix(ctx.interaction)
    fileName = f"{constants.USER_DATA_PATH}/{filePrefix}Macros.json"

    try:
        findOrCreateFile(fileName)  
        content = getJSONFileContent("baseRollMacros.json")
        serverContent = getJSONFileContent(fileName)
        baseKeys = list(content.keys())
        serverKeys = list(serverContent.keys())
        joinnedKeys = baseKeys + serverKeys
        return joinnedKeys
    except Exception as e:
        print(e)
        return []

def discordBotCommands():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)
    SERVERS = getWhiteListServers()
    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")

    @bot.slash_command(guild_ids=SERVERS, name="hello", description="A command for being nice to our future robot overlords")
    async def hello(ctx):
        logCommandInfo(ctx, "hello")
        await ctx.respond("Hello!")

    @bot.slash_command(guild_ids=SERVERS, name="r", description="A command for rolling either die macros or saved macros")
    @option(name="dice",
            description="e.g. \"2d6 + 4\" macros like \"[healing potion] + 4d2 can be used as well.\"",
            autocomplete=discord.utils.basic_autocomplete(autoCompleteRollMacros))
    async def roll(ctx, dice:str):
        await fullRoll(ctx, dice)

    @bot.slash_command(guild_ids=SERVERS, name="roll", description="A command for rolling either die macros or saved macros")
    @option(name="dice",
            description="e.g. \"2d6 + 4\" macros like \"[healing potion] + 4d2 can be used as well.\"", 
            autocomplete=discord.utils.basic_autocomplete(autoCompleteRollMacros))
    async def roll2(ctx, dice:str):
        await fullRoll(ctx, dice)

    async def fullRoll(ctx, dice:str):
        logCommandInfo(ctx, "roll")
        filePrefix = getServerFilePrefix(ctx)
        result = interpDice(dice, filePrefix)
        await ctx.respond(f"{dice} = {result[0]}`\n {result[2]} \n {result[1]}`")

    @bot.slash_command(guild_ids=SERVERS, name="addmacro", description="Name a save a die macro to use later")
    @option(name="macro_name", description="e.g. [Sword +1] or [Strength Joe].")
    @option(name="dice", description="e.g. \"2d6 + 4\" macros like \"[healing potion] can be used as well.\"")
    async def addmacro(ctx, macro_name: str, dice):
        logCommandInfo(ctx, "addmacro")
        filePrefix = getServerFilePrefix(ctx)
        result = addMacro(macro_name, dice, filePrefix)
        await ctx.respond(result)

    @bot.slash_command(guild_ids=SERVERS, name="dispardis", description="This is a command currently to insult Pardis created at Mat's request")
    async def insultRequest(ctx: discord.ApplicationContext):
        logCommandInfo(ctx, "dispardis")
        result = insult(getServerFilePrefix(ctx))
        await ctx.respond(result)

    @bot.slash_command(guild_ids=SERVERS, name="addbarb", description="Adds an insult to my list of known insults")
    @option(name="addbarb", description="A cutting remake worth of the highest level bard")
    async def addInsultRequest(ctx, insult: str):
        logCommandInfo(ctx, "addbarb")
        result = addInsult(insult, getServerFilePrefix(ctx))
        await ctx.respond(result)

    @bot.slash_command(guild_ids=SERVERS, name="bagsearch", description="Searches the parties bag of holding")
    @option(name="item_name", description="A name or partial name of the item")
    async def searchBag(ctx, item_name: str):
        logCommandInfo(ctx, "bagsearch")
        try:
            result = findInbag(item_name)
            await ctx.respond(result)
        except Exception as e:
            print(e)
    
    @bot.slash_command(guild_ids=SERVERS, name="bagremove", description="Removes item from the parties bag of holding")
    @option(name="item_name", description="A name of the item")
    async def removeFromBagResponse(ctx, item_name: str):
        logCommandInfo(ctx, "bagremove")
        try:
            result = removeFromBag(item_name)
            await ctx.respond(result)
        except Exception as e:
            print(e)

    @bot.slash_command(guild_ids=SERVERS, name="bagadd", description="Adds item from the parties bag of holding")
    @option(name="item_name", description="A name of the item")
    async def addToBagRequest(ctx, item_name: str):
        logCommandInfo(ctx, "bagadd")
        try:
            result = addToBag(item_name)
            await ctx.respond(result)
        except Exception as e:
            print(e)
    

    @bot.slash_command(guild_ids=SERVERS, name="bagshow", description="Shows contense of bag of holding")
    async def showBagRequest(ctx):
        logCommandInfo(ctx, "bagshow")
        try:
            result = printBag()
            await ctx.respond(result)
        except Exception as e:
            print(e)

    @bot.slash_command(guild_ids=SERVERS, name="help", description="Get help with the bots controls and commands")
    async def help(ctx):
        logCommandInfo(ctx, "help")
        await ctx.respond("This is a help message that has unhelpfully be filled out with a placeholder")

    @bot.slash_command(guild_ids=SERVERS, name="entertallgrass", description="You enter the tall grass what could happen")
    async def pokebattleBegin(ctx):
        try:
            if not DatabaseInteraction.userExists(ctx.author.id):
                DatabaseInteraction.addUser(ctx.author.id, ctx.author.name)
            result = SESSION.startSession()
            if result is None:
                poke = SESSION.getPokemon()
                await ctx.respond(f"A wild f{poke.displayName} has appeared catch them.")
                await ctx.respond(poke.image)
            else:
                await ctx.respond(result)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            await ctx.respond("I'm sorry something went wrong.")
            
    #TODO fix pokemon stuff its fucked
    @bot.slash_command(guild_ids=SERVERS, name="throwpokeball", description="catch the little blighter")
    async def catchPokemon(ctx):
        try:
            if not DatabaseInteraction.userExists(ctx.author.id):
                DatabaseInteraction.addUser(ctx.author.id, ctx.author.name)
            if SESSION.isSessionStarted():
                res = SESSION.attemptCatch(ctx.author)
                await ctx.respond(res)
            else:
                await ctx.respond("There is not currently a pokemon to catch.")
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            await ctx.respond("failure")

    @bot.slash_command(guild_ids=SERVERS, name="checkpokedex", description="Check my currently caught pokemon")
    async def checkpokedex(ctx: Context):
        try:
            if not DatabaseInteraction.userExists(ctx.author.id):
                DatabaseInteraction.addUser(ctx.author.id, ctx.author.name)
            pokemons: list[Pokemon] = DatabaseInteraction.getUserPokemon(ctx.author.id)
            result = f"{ctx.author.name} has the following pokemon: "
            for p in pokemons:
                result += f"\n\t{p.displayName}"
            await ctx.respond(result)
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            await ctx.respond("failure")
    
    bot.run(os.environ["DISCORD_TOKEN"])

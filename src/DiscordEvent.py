import discord
import responses
import os
# deprecated
def discordBotEvent():
    intents = discord.Intents.default()
    intents.message_content = True  
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return
        
        userName = str(message.author)
        userMessage = str(message.content)
        channel = str(message.channel)
        serverID = str(message.guild.id)
        serverName = str(message.guild.name)
        print(f"{serverID}-{serverName}")
        if len(userMessage) == 0:
            return

        print(f"user: {userName} said: {userMessage} channel: {channel}")

        if userMessage[0] == "?":
            await sendMessage(message, userMessage[1:], True)
        elif userMessage[0] == "!":
            await sendMessage(message, userMessage[1:], False)
    
    client.run(os.environ["DISCORD_TOKEN"])

async def sendMessage(message, userMessage: str, private: bool): 
    try:
        response = responses.handleRepsone(userMessage)

        if private: 
            await message.author.send(response) 
        else:
            await message.channel.send(response)
        
    except Exception as e:
        print(e)
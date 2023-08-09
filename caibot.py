import aiohttp
import json
import discord, time
from discord.ext import commands, tasks
from discord.ext.commands import Context
import random
import logging
import asyncio
import websockets
import uuid

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
logging.basicConfig(level=logging.INFO)

URI = "wss://neo.character.ai/ws/"
HEADERS = {"Authorization": " "} # character ai account authorisation token
CHARACTER_ID = " " # chacater ai character id
CHANNEL_ID = [channel_id_1, channel_id] # ids of channels the bot will always respond in (fill in as many as you want)
BLACKLISTED_CHANNELS = [channel_id_1, channel_id] # ids of channels the bot won't have the default 0.2% response chance in (fill in as many as you want)
BOT_TOKEN = " " # discord bot token


async def create_chat():
    chat_id = str(uuid.uuid4())
    async with websockets.connect(URI, extra_headers=HEADERS) as websocket:
        await websocket.send(json.dumps({"command": "create_chat", "request_id": "this can be any json value, and the server echoes it back to you! isn't that funny.", "payload": {"chat": {"creator_id": "1", "visibility": "VISIBILITY_PRIVATE", "type": "TYPE_ONE_ON_ONE", "character_id": CHARACTER_ID, "chat_id": chat_id}, "with_greeting": True}}))
        assert "chat" in json.loads(await websocket.recv())
        return chat_id

@bot.event
async def on_ready():
    bot.history = await create_chat()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name=f"character.ai"))
    print(f'We have logged in as {bot.user}')


async def send_message(message, chat_id, your_name="guy"):
    async with websockets.connect(URI, extra_headers=HEADERS) as websocket:
        await websocket.send(json.dumps({"command": "create_and_generate_turn", "request_id": "user_request", "payload": {"turn": {"turn_key": {"chat_id": chat_id, "turn_id": str(uuid.uuid4())}, "author": {"author_id": "", "name": your_name}, "candidates": [{"candidate_id": "fake_candidate_id", "raw_content": message}], "primary_candidate_id": "fake_candidate_id"}, "num_candidates": 1, "character_id": CHARACTER_ID}}))
        while True:
            candidate = json.loads(await websocket.recv())["turn"]["candidates"][0]
            if "is_final" in candidate and candidate["candidate_id"] != "fake_candidate_id":
                break
        return candidate["raw_content"]

async def example():
    chat_id = await create_chat()
    while True:
        message = input("message: ")
        print(await send_message(message, chat_id, your_name="Greg"))

@bot.event # 0.2% chance to respond in random channels (that arent blacklisted), remove this event if you don't want this feature
async def on_message(message):
    if random.randint(1, 500) == 25 and message.channel.id not in BLACKLISTED_CHANNELS:
        messages = reversed([f"<{message.author.name}> {message.content}" async for message in message.channel.history(limit=20)])
        data = await send_message(message.content, bot.history, your_name=message.author.name)
        await message.reply(data, mention_author=False)
    await bot.process_commands(message)

@bot.listen('on_message')
async def shirt_talk(message):
    if message.channel.id not in CHANNEL_ID:
        return
    if message.author.bot:
        return
    if message.content.startswith("# "):
        return
    if message.content == "!reset":
        bot.history = await create_chat()
        return
    to_send = f"<{message.author.name}> {message.content}"
    async with message.channel.typing():
        data = await send_message(message.content, bot.history, your_name=message.author.name)
        await message.reply(data, mention_author=False)

bot.run(BOT_TOKEN)
# CharacterAIDiscord
Discord chatbot that uses CharacterAI

# Setup:

## Requirements:
Open command prompt or powershell and type `cd <directory>` with directory being the folder you downloaded and unzipped the bot in.
Type `pip install -r requirements.txt`.

## Discord Token
Go to https://discord.com/developers and make an application. Go to the bot section, enable the message intent and copy the token. Open caibot.py in notepad or any code editing software and place the token in BOT_TOKEN.

## CharacterAI Token
(This guide uses Chrome for reference, other browsers could have slightly different methods).
Go to https://beta.character.ai/ and make an account (if you don't have one already) and open a chat with the character you wanna use for the bot.
Press ctrl + shift + i, that should open a side menu.
Go to "network" in the menu.
Type a message to the character, that should make a bar saying "streaming/" appear in the network menu.
Right click it, go to "copy" and select "copy as cURL (bash).
Go to https://curlconverter.com/ , select python and paste what you copied there.
In the headers section copy the authorisation token (including the "Token " part) and put it in `HEADERS = {"Authorization": " "}` in caibot.py.
In the json_data section copy the character_external_id and put it in `CHARACTER_ID`.

## Channels
Copy the ID(s) of the channel(s) you want the bot to always respond in and put them in `CHANNEL_ID`
The bot has a 0.2% chance of responding to random messages outside the `CHANNEL_ID` channels. If you want it to completely ignore some channels, put them in `BLACKLISTED_CHANNELS`.

(make sure to save your changes in caibot.py)

# Run The Bot
## Invite It
In the developer portal, go to OAuth > URL Generator, select "bot" and in the menu under it select "send messages".
Copy the generated URL. That's your bot's invite link.

## Run It
After you cd into the bot's directory, simply run it with `python caibot.py`

Shoutouts to Cyclcrclicly#3420 for making this possible.

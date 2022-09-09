import discord
import os
import random
import lists
import insults
import drWho

client = discord.Client(intents=discord.Intents.all())

DTOKEN=os.environ['TOKEN']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('I have risen')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for words in lists.CENSORED:
      if words in message.content:
        badMessage = message
        await message.delete()
        cleanMessage = censor(badMessage.content)
        await message.channel.send('{} please no cursing in my Christian Minecraft Server'.format(badMessage.author.name))
        await message.channel.send('{} : {}'.format(badMessage.author.name, cleanMessage))
        badMessage = ''
        cleanMessage = ''
  
  
    if message.content.startswith('$hello'):
        await message.channel.send('Sup, broski.')
        print(f'Message from {message.author}: {message.content} {message.author.id}')
      
    elif "time" in message.content:
      response = random.choice(range(0, 4))
      await message.channel.send(drWho.Quotes[response])

    chance = random.choice(range(1,21))
    if chance == 1:
       response = random.choice(range(1,11))
       await message.channel.send(insults.insults[response])

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Um...{member.name}, what are you doing here?'
    )

def ireplace(data, prev_pattern, new_pattern):
    
       # Replaces words while ignoring letters case.
    

    # find the index of the pattern which is going to be replaced
    idx = data.lower().find(prev_pattern.lower())

    # replaces the founded pattern with a new specified pattern
    mod_data = data.replace( 
        data[idx:idx+len(prev_pattern)], new_pattern)
    return mod_data


def censor(msg):
    
        #Censors the message according to given patterns.

    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for pattern in lists.CENSORED:
        if pattern in msg.lower():
            rev_data = pattern
            for char in rev_data:
                for v in vowels:
                    if char == v:
                        # to send asterisk in discord, you gotta use backslash asterisk (\*)
                        rev_data = rev_data.replace(char, '\*') 
                        
            msg = ireplace(msg, pattern, rev_data)
    return msg

client.run(DTOKEN)
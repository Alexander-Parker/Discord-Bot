import discord
import random
import json
import sys
from collections import defaultdict

from markov import generate_message
from fbparse import generate_chain
import config as cfg

#Bot Setup

try:
    mchain = json.loads(open(cfg.output + '.json').read())
except:
    generate_chain(cfg.input + '.json',cfg.output)
    mchain = json.loads(open(cfg.output + '.json').read())

particpants = list(mchain.keys())
for n in cfg.exclude:
    particpants.remove(n)

#Live Commands

TOKEN = cfg.token

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user: 
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!mc'):
        particpant = random.choice(particpants)
        msg = generate_message(mchain, particpant)
        msg += '\n\n' + ' *-' + particpant + '*'
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)


import discord
from discord.ext.commands import Bot
from discord import Game
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

client = Bot(command_prefix=cfg.bot_prefix)

def determine_args(dcord_cmd):
    cmds = dcord_cmd.split(' ')
    return cmds

@client.command(name='hello',
                description='Replies to user.',
                brief='Replies to user.',
                aliases=['Hello', 'hi', 'Hi'],
                pass_context=True)
async def hello(context):
    msg = 'Hello {0.author.mention}'.format(context.message)
    await client.send_message(context.message.channel, msg)

@client.command(name='test',
                description='test',
                brief='test',
                pass_context=True)
async def test(context):
    cmds = determine_args(context.message.content)
    for n in cmds:
        await client.send_message(context.message.channel, n)

@client.command(name='mc',
                description='Markov chain based on Facebook message data.',
                brief='An advanced AI.',
                aliases=['markov', 'Markov'],
                pass_context=True)
async def mc(context, mode='rand'):
    if mode == 'rand':
        particpant = random.choice(particpants)
        msg = generate_message(mchain, particpant)
        msg += '\n\n' + ' *-' + particpant + '*'
        await client.send_message(context.message.channel, msg)
    if mode == 'game':
        particpant = random.choice(particpants)
        msg = generate_message(mchain, particpant)
        await client.send_message(context.message.channel, msg)
        return
    
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Rust"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(cfg.token)


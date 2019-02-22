import discord
from discord.ext.commands import Bot
from discord import Role
from discord import Game
from discord import Server
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
print(particpants)
for n in cfg.exclude:
    particpants.remove(n)

server = None #server is named in the on_ready event
role_id = None #role_id is named in the on_ready event
members = defaultdict(dict)

#Live Commands

client = Bot(command_prefix=cfg.bot_prefix)

@client.command(name='hello',
                description='Replies to user.',
                brief='Replies to user.',
                aliases=['Hello', 'hi', 'Hi'],
                pass_context=True)
async def hello(context):
    msg = 'Hello {0.author.mention}'.format(context.message)
    await client.send_message(context.message.channel, msg)

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

@client.command(pass_context=True)
async def getusers(context, *args):
    role_name = (' '.join(args))
    role_id = server.roles[0]
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await client.send_message(context.message.channel, "Role doesn't exist")
        return    
    for member in server.members:
        if role_id in member.roles:
            await client.send_message(context.message.channel, f"{role_name} - {member.name}")

@client.event
async def on_ready():
    global server
    global role_id
    global members

    server = discord.utils.get(client.servers,id=cfg.server_id)
    for role in server.roles:
        if cfg.main_role == role.name:
            role_id = role
            break
    else:
        print("WARNING: No Main Role Set")

    for member in server.members:
        if role_id in member.roles:
            members

    await client.change_presence(game=Game(name=cfg.game))

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Server Name: '+ server.name)
    print('Role Name: '+ role_id.name)

client.run(cfg.token)
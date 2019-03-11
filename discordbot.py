import discord
from discord.ext.commands import Bot
from discord import Role
from discord import Game
from discord import Server
import random
import json
import sys
import requests
import os
from PIL import Image
from io import BytesIO
from collections import defaultdict
from urllib.request import urlopen
import base64
import asyncio

from markov import generate_message
from fbparse import generate_chain
import config as cfg

#Bot Setup

try:
    mchain = json.loads(open(cfg.output + '.json').read())
except:
    generate_chain(cfg.input + '.json',cfg.output)
    mchain = json.loads(open(cfg.output + '.json').read())

try:
    score_table = json.loads(open(cfg.score_table + '.json').read())
except:
    score_table = defaultdict(dict)

participants = list(mchain.keys())
for n in cfg.exclude:
    participants.remove(n)

server = None #server is named in the on_ready event
role_id = None #role_id is named in the on_ready event
markov_members = defaultdict(dict)

def find_between(s,first,last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last,start)
        return s[start:end]
    except ValueError:
        return ""

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
    global score_table
    if mode == 'rand':
        participant = random.choice(participants)
        msg = generate_message(mchain, participant)
        msg += '\n\n' + ' *-' + participant + '*'
        await client.send_message(context.message.channel, msg)
    if mode == 'game':
        participant = random.choice(participants)
        for member in markov_members:
            if markov_members[member]['fb_name'] == participant:
                participant_emoji = markov_members[member]['emoji']

        game_text = generate_message(mchain, participant)
        game_msg = await client.send_message(context.message.channel, game_text)
        for user in markov_members.keys():
            await client.add_reaction(game_msg, markov_members[user]['emoji'])
        await asyncio.sleep(15)
        await client.send_message(context.message.channel, 'Voting is closed. "Author" was {}'.format(participant))
        game_msg = await client.get_message(game_msg.channel, game_msg.id) 
        votes = defaultdict(dict)
        for reaction in game_msg.reactions:
            reaction_users = await client.get_reaction_users(reaction)
            for user in reaction_users:
                if user == client.user:
                    print('User is the bot - not added to votes table')
                elif user in votes.keys():
                    print('User voted a second time - invalidating vote')
                    votes[user] = 'INVALID'
                else:
                    votes[user] = reaction.emoji
        for voter in votes.keys():
            if voter.id not in score_table.keys():
                score_table[voter.id] = 0
            if votes[voter] == 'INVALID':
                score_table[voter.id] -= 1
                msg = '{} voted more than once. One point deducted. Updated Score: {}'.format(voter.mention,score_table[voter.id])
                await client.send_message(context.message.channel, msg)
            if votes[voter] == participant_emoji:
                score_table[voter.id] += 1
                msg = '{} was correct! One point added. Updated Score: {}'.format(voter.mention,score_table[voter.id])
                await client.send_message(context.message.channel, msg)
        with open(cfg.score_table + '.json','w') as fp:
            json.dump(score_table, fp, sort_keys=True, indent=4)
    if mode == 'score':
        if len(score_table.keys()) == 0:
            await client.send_message(context.message.channel, 'No score data generated yet')
        else:
            for user in score_table.keys():
                msg = '{}: {}'.format(server.get_member(user).name,score_table[user])
                await client.send_message(context.message.channel, msg)

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
    global markov_members

    server = discord.utils.get(client.servers,id=cfg.server_id)
    for role in server.roles:
        if cfg.main_role == role.name:
            role_id = role
            break
    else:
        print("WARNING: No Main Role Set")

    for member in server.members:
        if role_id in member.roles:
            if member.name in cfg.participants.keys():
                markov_members[member.name]['fb_name'] = cfg.participants.get(member.name)
                
                no_space_name = member.name.replace(' ','_')
                markov_members[member.name]['avatar_name'] = no_space_name
                
                fp = no_space_name + '_avatar.png'
                im = Image.open(BytesIO(requests.get(member.avatar_url).content))
                im.thumbnail(cfg.emoji_size)
                im.save(fp, format='png')
                markov_members[member.name]['avatar_fp'] = fp

    existing_emojis = defaultdict(dict)
    for n in client.get_all_emojis():
        existing_emojis[str(n)]['name'] = find_between(str(n),':',':')
        existing_emojis[str(n)]['id'] = find_between(str(n),'<','>')
        existing_emojis[str(n)]['emoji'] = n

    for user in markov_members.keys():
        match = None
        for n in existing_emojis.keys():
            if markov_members[user]['avatar_name'] == existing_emojis[n]['name']:
                match = existing_emojis[n]['emoji']
        if match is None:
            with open(markov_members[user]['avatar_fp'],"rb") as im:
                image_byte = im.read()
                emoji = await client.create_custom_emoji(server,name=markov_members[user]['avatar_name'],image=image_byte)
                markov_members[user]['emoji'] = emoji

        else:
            markov_members[user]['emoji'] = match

    await client.change_presence(game=Game(name=cfg.game))

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Server Name: '+ server.name)
    print('Role Name: '+ role_id.name)

client.run(cfg.token)
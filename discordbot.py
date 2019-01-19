import discord
import sys

TOKEN = '%s'%sys.argv[1]

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!f1'):
        msg1 = "Leaving my f1 fanboy bias aside it more challenging when you realize that there are only 20 drivers that can make it in the world. It also helps that they don't go in a circle for 2 hours or however long a nascar race is. Each track is different and offers a different set of challenges the teams have to get over. They can actually race in the rain which is awesome because  a driver can be amazing in the dry but be terrible in the wet and vice versa so you don't know whats gonna happen. Another thing is the fact that the technology in F1 is just fascinating and no other sport is even close with maybe LMP1 cars be the closest. I have tons more reasons but those are just a few. The only thing that nascar has that F1 doesnt is the engines sound really cool since f1 had to move to v6 to appease all the fucking ENVIRONMENTAL motherfuckers that wanted F1 to be more fuel efficient which is stupid imo but thats for another day"
        await client.send_message(message.channel, msg1)

    if message.content.startswith('!pg'):
        msg2 = "So there I was, putting on my rape shoes, and practicing my sexual harassment pickup lines this morning. I just got done cyberbullying my coworkers. It was time to shave, I yelled at my wife to smile because I demand it, while pinching her butt right after she told me she didn't consent to it. Putting on the shaving cream and thinking about how I can get my son into a fight at the next BBQ, I replaced the worn Gillette brand Mach3 and began to chant 'boys will be boys' as I started to shave. Then suddenly my daughter burst into the bathroom holding her phone. As I began to mansplain to her why she isn't smart enough to know my shaving time is my time she showed me the new Gillette ad. I realized how my every view and behavior I've ever held dear was wrong. I'm calling in sick at the toxic masculinity factory today and registering Democrat. Thanks Gillette, now excuse me while I help to impeach."
        await client.send_message(message.channel, msg2)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)

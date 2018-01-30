import os
import discord
from discord.ext import commands
import random
from os import listdir
from os.path import isfile, join
import os.path
import urllib.request, json 


description = '''Un bot cool.

Encore en développement'''

bot = commands.Bot(command_prefix='!', description=description)


def openData(path):
	with open(path, 'r') as content_file:
		return json.load(content_file)

def writeData(path, data):
	with open(path, 'w') as content_file:
		content_file.write(json.dumps(data, indent=4))



@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')



@bot.event
async def on_message(message):
	await bot.process_commands(message)



@bot.command(pass_context = True)
async def createMemo(ctx, title: str, mem: str):
	if ctx.message.author.id == '181353136106110976' or ctx.message.author.id == '259093795654598656' or ctx.message.author.id == '164371071393464320':
		with open(title + ".mem", 'w') as content_file:
			content_file.write(mem)
		await bot.say("Créé !")


@bot.command()
async def read(file: str):
	if os.path.isfile(file + ".mem"):
		with open(file + ".mem", 'r') as content_file:
			await bot.say("```" + '\n' + content_file.read() + '\n' "```")

@bot.command(pass_context = True)
async def delete(ctx, file: str):
	if ctx.message.author.id == '181353136106110976' or ctx.message.author.id == '259093795654598656' or ctx.message.author.id == '164371071393464320':
		if os.path.isfile(file + ".mem"):
			os.remove(file + ".mem")
			await bot.say("Supprimé !")

@bot.command()
async def list():
	onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
	final = ""
	for f in onlyfiles:
		if ".mem" in f:
			final += "`" + f.split(".")[0] + "`" + ","
	await bot.say(final[:-1])

@bot.command()
async def ubiq():
    with urllib.request.urlopen("https://ubq.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="ubq.mining-pool.fr", url="https://ubq.mining-pool.fr/", description="Welcome to our Ubiq pool", color=0x00ea90)
        embed.set_author(name="Ubiq")
        embed.set_thumbnail(url="https://ubq.mining-pool.fr/ubiq-a1abc2fed205c2e2c78db574ca777125.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  Gh/s", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.ubq.mining-pool.fr:8088", inline=True)
        await bot.say(embed=embed)

@bot.command()
async def pirl():
    with urllib.request.urlopen("http://pirl.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="pirl.mining-pool.fr", url="https://pirl.mining-pool.fr/", description="Welcome to our Pirl pool", color=0x76A114)
        embed.set_author(name="pirl")
        embed.set_thumbnail(url="http://pirl.mining-pool.fr/pirl-c0b197292e6ab60c66af3982d752cb33.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.pirl.mining-pool.fr:8006", inline=True)
        await bot.say(embed=embed)

@bot.command()
async def music():
    with urllib.request.urlopen("https://music.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="music.mining-pool.fr", url="https://music.mining-pool.fr/", description="Welcome to our music pool", color=0xFFB500)
        embed.set_author(name="music")
        embed.set_thumbnail(url="https://music.mining-pool.fr/music-dfadb5d98973047b3bb797a9fee491ca.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.music.mining-pool.fr:8005", inline=True)
        await bot.say(embed=embed)

@bot.command()
async def etc():
    with urllib.request.urlopen("https://etc.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="etc.mining-pool.fr", url="https://etc.mining-pool.fr/", description="Welcome to our etc pool", color=0x4FB859)
        embed.set_author(name="etc")
        embed.set_thumbnail(url="https://etc.mining-pool.fr/etc-fc2f17933bc3b573a3e2bb8ad47a03c8.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.etc.mining-pool.fr:8004", inline=True)
        await bot.say(embed=embed)

@bot.command()
async def eth():
    with urllib.request.urlopen("https://eth.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="eth.mining-pool.fr", url="https://eth.mining-pool.fr/", description="Welcome to our eth pool", color=0x5B99E0 )
        embed.set_author(name="eth")
        embed.set_thumbnail(url="https://eth.mining-pool.fr/eth-063dfbf1fd7e87058e34424100242ffe.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.eth.mining-pool.fr:8003", inline=True)
        await bot.say(embed=embed)

@bot.command()
async def exp():
    with urllib.request.urlopen("https://exp.mining-pool.fr/api/stats") as url:
        data = json.loads(url.read().decode())
        embed=discord.Embed(title="exp.mining-pool.fr", url="https://exp.mining-pool.fr/", description="Welcome to our exp pool", color=0xDC5100 )
        embed.set_author(name="exp")
        embed.set_thumbnail(url="https://exp.mining-pool.fr/exp-0c56250a40f1882cdc30f8c321928a37.jpg")
        embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
        embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
        embed.add_field(name="Stratum", value="stratum+tcp://mine.exp.mining-pool.fr:8056", inline=True)
        await bot.say(embed=embed)

bot.run('MzgxODQwMzI1MjUwOTA4MTcw.DU6I4g.lT-q0k_fcIKSLEuR_Ss1CE2Es7s')

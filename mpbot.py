import aiohttp
import asyncio
import discord
from discord.ext import commands
import os.path
import re
import sys

ALLOWED_USERS = ('181353136106110976', '259093795654598656', '164371071393464320', "304635262334402563")

description = '''Un bot cool.

Encore en développement'''

bot = commands.Bot(command_prefix='!', description=description)
http_session = None


def clean_filename(path):
    result = re.sub('[^a-zA-Z\d\. ]|( ){2,}','', path)  # Keep letters, numbers dots and spaces
    if not result or os.path.splitext(result)[0].isspace():
        return None
    return result


@bot.event
async def on_ready():
    print('Logged in as {user.name} [{user.id}]'.format(user=bot.user))
    print('------')



@bot.event
async def on_message(message):
    await bot.process_commands(message)



@bot.command(pass_context = True)
async def createMemo(ctx, title: str, mem: str):
    if ctx.message.author.id in ALLOWED_USERS:
        filename = clean_filename(title)
        if filename is None:
            await bot.say("Nom invalide")
        else:
            with open('%s.mem' % filename, 'w') as content_file:
                content_file.write(mem)
            await bot.say("Créé !")


@bot.command()
async def read(title: str):
    filename = clean_filename(title)
    if filename is None:
        await bot.say("Nom invalide")
    else:
        try:
            with open('%s.mem' % filename, 'r') as content_file:
                await bot.say("```\n%s\n```" %  content_file.read())
        except IOError:
            pass

@bot.command(pass_context = True)
async def delete(ctx, title: str):
    if ctx.message.author.id in ALLOWED_USERS:
        filename = clean_filename(title)
        if filename is None:
            await bot.say("Nom invalide")
        else:
            try:
                os.remove('%s.mem' % filename)
            except IOError:
                pass
            await bot.say("Supprimé !")

@bot.command()
async def list():
    await bot.say(', '.join(
        '`%s`' % name[:-4] for name in os.listdir('./')
        if name.endswith('.mem')
    ) or 'Aucun fichier')

@bot.command()
async def ubiq():
    async with http_session.get('https://ubq.mining-pool.fr/api/stats') as response:
        data = await response.json()
    embed=discord.Embed(title="ubq.mining-pool.fr", url="https://ubq.mining-pool.fr/", description="Welcome to our Ubiq pool", color=0x00ea90)
    embed.set_author(name="Ubiq")
    embed.set_thumbnail(url="https://ubq.mining-pool.fr/ubiq-a1abc2fed205c2e2c78db574ca777125.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  Gh/s", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.ubq.mining-pool.fr:8088", inline=True)
    await bot.say(embed=embed)

@bot.command()
async def pirl():
    async with http_session.get('http://pirl.mining-pool.fr/api/stats') as response:
        data = await response.json()
    embed=discord.Embed(title="pirl.mining-pool.fr", url="https://pirl.mining-pool.fr/", description="Welcome to our Pirl pool", color=0x76A114)
    embed.set_author(name="pirl")
    embed.set_thumbnail(url="http://pirl.mining-pool.fr/pirl-c0b197292e6ab60c66af3982d752cb33.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.pirl.mining-pool.fr:8006", inline=True)
    await bot.say(embed=embed)

@bot.command()
async def music():
    async with http_session.get('https://music.mining-pool.fr/api/stats') as response:
        data = await response.json()
    embed=discord.Embed(title="music.mining-pool.fr", url="https://music.mining-pool.fr/", description="Welcome to our music pool", color=0xFFB500)
    embed.set_author(name="music")
    embed.set_thumbnail(url="https://music.mining-pool.fr/music-dfadb5d98973047b3bb797a9fee491ca.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.music.mining-pool.fr:8005", inline=True)
    await bot.say(embed=embed)

@bot.command()
async def etc():
    async with http_session.get('https://etc.mining-pool.fr/api/stats') as response:
        data = await response.json()
    embed=discord.Embed(title="etc.mining-pool.fr", url="https://etc.mining-pool.fr/", description="Welcome to our etc pool", color=0x4FB859)
    embed.set_author(name="etc")
    embed.set_thumbnail(url="https://etc.mining-pool.fr/etc-fc2f17933bc3b573a3e2bb8ad47a03c8.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.etc.mining-pool.fr:8004", inline=True)
    await bot.say(embed=embed)

@bot.command()
async def eth():
    async with http_session.get('https://eth.mining-pool.fr/api/stats') as response:
        data = await response.json()
    embed=discord.Embed(title="eth.mining-pool.fr", url="https://eth.mining-pool.fr/", description="Welcome to our eth pool", color=0x5B99E0 )
    embed.set_author(name="eth")
    embed.set_thumbnail(url="https://eth.mining-pool.fr/eth-063dfbf1fd7e87058e34424100242ffe.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.eth.mining-pool.fr:8003", inline=True)
    await bot.say(embed=embed)

@bot.command()
async def exp():
    async with http_session.get("https://exp.mining-pool.fr/api/stats") as response:
        data = await response.json()
    embed=discord.Embed(title="exp.mining-pool.fr", url="https://exp.mining-pool.fr/", description="Welcome to our exp pool", color=0xDC5100 )
    embed.set_author(name="exp")
    embed.set_thumbnail(url="https://exp.mining-pool.fr/exp-0c56250a40f1882cdc30f8c321928a37.jpg")
    embed.add_field(name="Miners", value=str(data['minersTotal']), inline=True)
    embed.add_field(name="Hashrate", value=str(data['hashrate'] / 1000000000) + "  *Gh/s*", inline=True)
    embed.add_field(name="Stratum", value="stratum+tcp://mine.exp.mining-pool.fr:8056", inline=True)
    await bot.say(embed=embed)


def main(token):
    global bot, http_session

    # cannot use bot.run because we need to manage aiohttp session as well
    loop = asyncio.get_event_loop()
    http_session = aiohttp.ClientSession(loop=loop)
    try:
        try:
            loop.run_until_complete(bot.start(token))
        except KeyboardInterrupt:
            pass
        loop.run_until_complete(bot.logout())
    finally:
        pending = asyncio.Task.all_tasks(loop=loop)
        gathered = asyncio.gather(*pending, loop=loop)
        try:
            gathered.cancel()
            loop.run_until_complete(gathered)
            gathered.exception()
        except:
            pass
        loop.run_until_complete(asyncio.sleep(0))   # let http sessions shutdown
        http_session.close()                        # this must be done before the loop is closed
        loop.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Syntaxe : python %s <token>' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1])

import aiohttp
import asyncio
import discord
from discord.ext import commands
from collections import namedtuple
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

# ============================================================================
# Memo commands

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

# ============================================================================
# Mining pool commands

Pool = namedtuple('Pool', 'name server color thumbnail stratum')
POOLS = {
    'ubq': Pool(
        name='Ubiq', color=0x00ea90,
        server='ubq.mining-pool.fr',
        thumbnail='https://ubq.mining-pool.fr/ubiq-a1abc2fed205c2e2c78db574ca777125.jpg',
        stratum='stratum+tcp://mine.ubq.mining-pool.fr:8088',
    ),
    'pirl': Pool(
        name='Pirl', color=0x76A114,
        server='pirl.mining-pool.fr',
        thumbnail='http://pirl.mining-pool.fr/pirl-c0b197292e6ab60c66af3982d752cb33.jpg',
        stratum='stratum+tcp://mine.pirl.mining-pool.fr:8006',
    ),
    'music': Pool(
        name='music', color=0xFFB500,
        server='music.mining-pool.fr',
        thumbnail='https://music.mining-pool.fr/music-dfadb5d98973047b3bb797a9fee491ca.jpg',
        stratum='stratum+tcp://mine.music.mining-pool.fr:8005',
    ),
    'etc': Pool(
        name='ethereum classic', color=0x4FB859,
        server='etc.mining-pool.fr',
        thumbnail='https://etc.mining-pool.fr/etc-fc2f17933bc3b573a3e2bb8ad47a03c8.jpg',
        stratum='stratum+tcp://mine.etc.mining-pool.fr:8004',
    ),
    'eth': Pool(
        name='ethereum', color=0x5B99E0,
        server='eth.mining-pool.fr',
        thumbnail='https://eth.mining-pool.fr/eth-063dfbf1fd7e87058e34424100242ffe.jpg',
        stratum='stratum+tcp://mine.eth.mining-pool.fr:8003',
    ),
    'exp': Pool(
        name='exp', color=0xDC5100,
        server='exp.mining-pool.fr',
        thumbnail='https://exp.mining-pool.fr/exp-0c56250a40f1882cdc30f8c321928a37.jpg',
        stratum='stratum+tcp://mine.exp.mining-pool.fr:8056',
    ),
}


def wallet_shower(pool):
    ''' Generate a command that shows the given pool '''
    async def show_wallet():
        async with http_session.get('https://{pool.server}/api/stats'.format(pool=pool)) as response:
            data = await response.json()

        embed = discord.Embed(
            title=pool.server,
            url='https://{pool.server}/'.format(pool=pool),
            description='Welcome to our {pool.name} pool'.format(pool=pool),
            color=pool.color,
        )
        embed.set_author(name=pool.name)
        embed.set_thumbnail(url=pool.thumbnail)
        embed.add_field(name='Miners', value=str(data['minersTotal']), inline=True)
        embed.add_field(name='Hashrate', value='%s *Gh/s*' % (data['hashrate']/1000000000), inline=True)
        embed.add_field(name='Stratum', value=pool.stratum, inline=True)
        await bot.say(embed=embed)
    return show_wallet

# Register all pools as commands
for ticker, pool in POOLS.items():
    bot.command(name=ticker)(wallet_shower(pool))

# ============================================================================
# Main entry point

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

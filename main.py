import discord, cf, os, random, asyncio
from discord.ext import commands

token = os.getenv("IOASIS_TOKEN")

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Start!")
    cf.init()
    print("Cf Data OK!")

@bot.command(brief = "Enter a tag and a problem difficulty")
async def chal(ctx, tag = "dp", dif = 1500):
    problems = cf.query(tag, dif)
    problem = random.choice(problems)
    print(problem)
    embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem))
    await ctx.send(embed = embed)

@bot.command(brief = "Register your codeforces account")
async def register(ctx, handle):
    problem = random.choice(cf.query("greedy", 800))
    await ctx.send("Please send a Compilation Error to this problem in the following 60 seconds.")
    embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem))
    await ctx.send(embed = embed)
    await asyncio.sleep(60)
    status = cf.status(handle)
    tup = ('COMPILATION_ERROR', problem)
    if tup in status:
        await ctx.send("Successfully registered {}'s handle as {}".format(ctx.author.mention, handle))
    else:
        await ctx.send("{} Failed. Try again.".format(ctx.author.mention))




bot.run(token)
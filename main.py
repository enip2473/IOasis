import discord, cf, os, random, asyncio, userdata, time
from discord.ext import commands

token = os.getenv("IOASIS_TOKEN")

bot = commands.Bot(command_prefix='.')
user_db = userdata.User()

@bot.event
async def on_ready():
    print("Start!")
    cf.init()
    print("Cf Data OK!")

@bot.command(brief = "Enter a tag and a problem difficulty")
async def chal(ctx, tag = "dp", dif = 1500):
    challenge = user_db.get_challenge(ctx.guild.id, ctx.author.name)
    if challenge != []:
        await ctx.send("You have an ongoing challenge")
        return
    problems = cf.query(tag, dif)
    problem = random.choice(problems)
    print(problem)
    embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem), description = "Challenge will start in 15 seconds!\nType cancel to cancel the challenge.")
    await ctx.send(embed = embed)
    # wait for 15 seconds
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
    try:
        await bot.wait_for("message", check=check, timeout=15)
        await ctx.send("Challenge cancelled.")
    except:
        await ctx.send("{} Challenge Start! Time Limit is 1 hour.\n Type .finish after you finish it.".format(ctx.author.mention))
        user_db.insert_challenge(ctx.guild.id, ctx.author.name, problem, dif, round(time.time()))

@bot.command(brief = "Finish the challenge")
async def finish(ctx):
    challenge = user_db.get_challenge(ctx.guild.id, ctx.author.name)
    user = user_db.get_user(ctx.guild.id, ctx.author.name)
    if challenge == []:
        await ctx.send("You don't have any ongoing challenge!")
        return
    handle = user[0][3]
    problemname, difficulty, time = challenge[0]
    status = cf.status(handle)
    if ("OK", problemname) in status:
        # TODO : check time and change rating
        await ctx.send("Challenge complete!")
        user_db.delete_challenge(ctx.guild.id, ctx.author.name)
    else:
        await ctx.send("You haven't completed your {} challenge".format(problemname))

@bot.command(brief = "Register your codeforces account")
async def register(ctx, handle): 
    #check if user in database
    if (arr := user_db.get_user(ctx.guild.id, ctx.author.name)) != []:
        await ctx.send("You have already registered !\nYour handle is {}.".format(arr[0][3]))
        return
    # ask user to submit a CE
    problem = random.choice(cf.query("greedy", 800))
    await ctx.send("Please send a Compilation Error to this problem in the following 60 seconds.")
    embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem))
    await ctx.send(embed = embed)
    await asyncio.sleep(60)

    #check if there's a CE
    status = cf.status(handle)
    tup = ('COMPILATION_ERROR', problem)
    if tup in status:
        await ctx.send("Successfully registered {}'s handle as {}".format(ctx.author.mention, handle))
        user_db.insert(ctx.guild.id, ctx.author.name, handle)
    else:
        await ctx.send("{} Failed. Try again.".format(ctx.author.mention))




bot.run(token)
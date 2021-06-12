import discord, requests
from discord.ext import commands
import cf, os, random, asyncio, userdata, time

def setup(bot):
    bot.add_cog(Codeforces(bot))

class Codeforces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = userdata.Codeforces()
        cf.init()

    @commands.command(brief = "Enter a tag and a problem difficulty")
    async def chal(self, ctx, dif = 1500, tag = "all"):
        # check if the user have registered his handle 
        if self.db.get_user(ctx.guild.id, ctx.author.name) == []:
            await ctx.send("You haven't register your handle!\nType .register to register.")
            return

        # check for ongoing challenges
        challenge = self.db.get_challenge(ctx.guild.id, ctx.author.name)
        if challenge != []:
            await ctx.send("You have an ongoing challenge")
            return

        # return a problem
        problems = cf.query(tag, dif)
        problem = random.choice(problems)
        print(problem)

        embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem), description = "Challenge will start in 15 seconds!\nType cancel to cancel the challenge.")
        await ctx.send(embed = embed)

        # wait for 15 seconds
        def check(message):
            return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
        try:
            await self.bot.wait_for("message", check=check, timeout=15)
            await ctx.send("Challenge cancelled.")
        except:
            await ctx.send("{} Challenge Start! Time Limit is 1 hour.\n Type .finish after you finish it.".format(ctx.author.mention))
            self.db.insert_challenge(ctx.guild.id, ctx.author.name, problem, dif, round(time.time()))

    @commands.command(brief = "Finish the challenge")
    async def finish(self, ctx):
        # check ongoing challenges
        challenge = self.db.get_challenge(ctx.guild.id, ctx.author.name)
        if challenge == []:
            await ctx.send("You don't have any ongoing challenge!")
            return
        
        #get user status
        user = self.db.get_user(ctx.guild.id, ctx.author.name)
        handle = user[0][3]
        problemname, difficulty, time = challenge[0]

        if (time := cf.check_verdict(handle, problemname, "OK")) > 0:
            # TODO : check time and change rating
            await ctx.send("Challenge complete!")
            self.db.delete_challenge(ctx.guild.id, ctx.author.name)
        else:
            await ctx.send("You haven't completed your {} challenge".format(problemname))

    @commands.command(brief = "Register your codeforces account")
    async def register(self, ctx, handle): 

        #check if user in database
        if (arr := self.db.get_user(ctx.guild.id, ctx.author.name)) != []:
            await ctx.send("You have already registered !\nYour handle is {}.".format(arr[0][3]))
            return
        
        # ask user to submit a CE
        problem = random.choice(cf.query("greedy", 800))
        await ctx.send("Please send a Compilation Error to this problem in the following 60 seconds.")
        embed = discord.Embed(title="Codeforces {}".format(problem), url = "https://codeforces.com/problemset/problem/{}".format(problem))
        await ctx.send(embed = embed)
        await asyncio.sleep(60)

        #check if there's a CE
        if cf.check_verdict(handle, problem, "COMPILATION_ERROR") > 0:
            await ctx.send("Successfully registered {}'s handle as {}".format(ctx.author.mention, handle))
            self.db.insert(ctx.guild.id, ctx.author.name, handle)
        else:
            await ctx.send("{} Failed. Try again.".format(ctx.author.mention))



n = int(input())
if n % 2 == 1:
    print(0)
else:
    print(1<<(n//2))
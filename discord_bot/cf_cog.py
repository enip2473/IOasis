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

    async def not_registered_message(self, ctx):
        await ctx.send("You haven't register your handle!\nType .register to register.")
    
    def check_register(self, ctx):
        if handle := self.db.get_handle(ctx.author.id) == "":
            self.not_registered_message(ctx)
            return ""
        return handle

    @commands.command(brief = "Enter a tag and a problem difficulty")
    async def chal(self, ctx, dif = 1500, tag = "all"):
        # check if the user have registered his handle 
        if self.check_register(ctx) == "" : return
        # check for ongoing challenges
        challenge = self.db.get_challenge(ctx.author.id)
        if challenge != None:
            await ctx.send("You have an ongoing challenge.\nType .ff to forfeit it.")
            return

        # return a problem
        problem = random.choice(cf.query(tag, dif))
        print(problem)
        problemname = problem[0]

        embed = discord.Embed(title="Codeforces {}".format(problemname), url = "https://codeforces.com/problemset/problem/{}".format(problemname), description = "Challenge will start in 15 seconds!\nType cancel to cancel the challenge.")
        await ctx.send(embed = embed)

        # wait for 15 seconds
        def check(message):
            return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
        try:
            await self.bot.wait_for("message", check=check, timeout=15)
            await ctx.send("Challenge cancelled.")
        except:
            await ctx.send("{} Challenge Start! Time Limit is 1 hour.\n Type .finish after you finish it.".format(ctx.author.mention))
            self.db.insert_challenge(ctx.author.id, problemname, round(time.time()))

    @commands.command(brief = "Forfeit the challenge")
    async def ff(self, ctx):
        # check ongoing challenges
        challenge = self.db.get_challenge(ctx.author.id)
        if challenge == None:
            await ctx.send("You don't have any ongoing challenge!")
            return
        
        reply = "Challenge failed.\nRating changes :\n"
        # update ratings
        problemname, time = challenge
        problem_rating, problem_tags = cf.get_problem(problemname)
        user_tags = self.db.get_ratings(ctx.author.id)
        new_rating = []

        for tag, user_rating in user_tags:
            if tag in problem_tags:
                message, change = cf.change_rating(user_rating, problem_rating, False)
                reply += "{} : {}".format(tag, message)
                user_rating += change
            new_rating.append(user_rating)

        # delete the challenge and send message
        self.db.update_ratings(ctx.author.id, new_rating)
        self.db.delete_challenge(ctx.author.id)
        
        reply = reply[:-1] # To remove the last \n
        print(reply)
        await ctx.send(reply)

    @commands.command(brief = "Finish the challenge")
    async def finish(self, ctx):
        # check ongoing challenges
        challenge = self.db.get_challenge(ctx.author.id)
        if challenge == None:
            await ctx.send("You don't have any ongoing challenge!")
            return
        
        #get user status
        handle = self.db.get_handle(ctx.author.id)
        problemname, time = challenge

        if (time := cf.check_verdict(handle, problemname, "OK")) > 0:
            # TODO : check time
            reply = "Challenge complete!\nRating changes :\n"
            problem_rating, problem_tags = cf.get_problem(problemname)
            user_tags = self.db.get_ratings(ctx.author.id)
            new_rating = []
            
            for tag, user_rating in user_tags:
                if tag in problem_tags:
                    message, change = cf.change_rating(user_rating, problem_rating, True)
                    reply += "{} : {}".format(tag, message)
                    user_rating += change
                new_rating.append(user_rating)
            
            self.db.delete_challenge(ctx.author.id)
            self.db.update_ratings(ctx.author.id, new_rating)
            
            reply = reply[:-1] # To remove the last \n
            print(reply)
            await ctx.send(reply) 
            
        else:
            await ctx.send("You haven't completed your {} challenge.\nTo forfeit, enter .ff.".format(problemname))

    @commands.command(brief = "Register your codeforces account")
    async def register(self, ctx, handle): 

        #check if user in database
        if (cf_handle := self.db.get_handle(ctx.author.id)) != "":
            await ctx.send("You have already registered !\nYour handle is {}.".format(cf_handle))
            return
        
        # ask user to submit a CE
        problem = random.choice(cf.query("greedy", 800))
        await ctx.send("Please send a Compilation Error to this problem in the following 60 seconds.")
        embed = discord.Embed(title="Codeforces {}".format(problem[0]), url = "https://codeforces.com/problemset/problem/{}".format(problem[0]))
        await ctx.send(embed = embed)
        await asyncio.sleep(60)

        #check if there's a CE
        if cf.check_verdict(handle, problem[0], "COMPILATION_ERROR") > 0:
            await ctx.send("Successfully registered {}'s handle as {}".format(ctx.author.mention, handle))
            self.db.insert_user(ctx.author.id, handle)
        else:
            await ctx.send("{} Failed. Try again.".format(ctx.author.mention))

    @commands.command(brief = "See you current rating on every subject.")
    async def profile(self, ctx): 
        
        #check if user in database
        if self.check_register(ctx) == "" : return
                # get ratings
        ratings = self.db.get_ratings(ctx.author.id)
        string = ""
        for text, rating in ratings:
            string += "{} : {}\n".format(text, rating)
        await ctx.send(string)


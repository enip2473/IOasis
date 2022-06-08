import discord
from discord.ext import commands
from pygal.config import CommonConfig
import cf, random, asyncio, userdata, time, pygal, os


def setup(bot):
    bot.add_cog(Codeforces(bot))

class Codeforces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = userdata.Codeforces()
        cf.init()
    
    def check_register(self, ctx):
        if (handle := self.db.get_handle(ctx.author.id)) == "":
            return ""
        return handle
    
    def radar_chart(self, user, data):
        from pygal.style import Style
        from pygal import Config
        custom_style = Style(
            background= 'rgba(240, 240, 240, 1)',
            plot_background = 'rgba(240, 240, 240, 1)',
            foreground = 'rgba(0, 0, 0, 0.9)',
            foreground_strong = 'rgba(0, 0, 0, 0.9)',
            foreground_subtle = 'rgba(0, 0, 0, 0.5)',
            opacity='.3',
            opacity_hover='.9',
            colors = ('rgb(12,55,149)', 'rgb(117,38,65)', 'rgb(228,127,0)', 'rgb(159,170,0)','rgb(149,12,12)'),
            title_font_size = 30,
            label_font_size	= 20,
            major_label_font_size = 18,
            value_label_font_size = 18,
            font_family= 'Consolas, "Liberation Mono", Menlo, Courier, monospace'
        )

        config = Config()
        config.width = 700
        config.height = 730
        config.fill = True
        config.style = custom_style
        config.stroke_style = {'width': 5.0}
        config.show_legend = False
        config.margin_left = -39
        config.margin_right = -17
        config.margin_bottom = -20
        chart = pygal.Radar(config)
        x_axis = [v[0] for v in data]
        y_axis = [v[1] for v in data]
        chart.x_labels = x_axis
        chart.add(user, y_axis)
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/tmp/" + user + ".png"
        chart.render_to_png(filename = dir_path)
        print(dir_path)
        return dir_path

    def cal_overall_rating(self, ratings): 
        total = 0 
        for rating in ratings: 
            total += rating 
        overall = round(total / 6, 2) 
        return overall

    @commands.command(brief = "Enter a tag and a problem difficulty")
    async def chal(self, ctx, dif = -1, tag = "all"):
        # check if the user have registered his handle 
        if (handle := self.check_register(ctx)) == "":
            await ctx.send("You haven't register your handle!\nType .register to register.")
            return
        # check for ongoing challenges
        challenge = self.db.get_challenge(ctx.author.id)
        if challenge != None:
            await ctx.send("You have an ongoing challenge.\nType .ff to forfeit it.")
            return

        user_info = self.db.get_ratings(ctx.author.id)[1:]
        overall = self.cal_overall_rating([i[1] for i in user_info])
        if dif == -1: 
            dif = max(800, overall // 100 * 100 + 100 * random.randint(0, 3))

        try:# return a problem with best new overall rating
            problems = cf.query(tag, dif)
            solved = cf.solved_problems(handle)
            problems = [problem for problem in problems if problem[0] not in solved]

            best_new_overall, problempool = -1, []
            for problem_name, problem_rating, problem_tags in problems: 
                problem_tags = cf.to_six_main_tags(problem_tags)
                weight = 1.0 / len(problem_tags)
                new_ratings = []
                for user_tag, user_rating in user_info: 
                    change = 0
                    if user_tag in problem_tags: 
                        change = cf.change_rating(weight, user_rating, problem_rating, True)[1]
                    new_ratings.append(user_rating + change)
                new_overall = self.cal_overall_rating(new_ratings)
                if abs(new_overall - best_new_overall) < 10: 
                    problempool.append(problem_name)
                elif best_new_overall < new_overall: 
                    best_new_overall = new_overall
                    problempool = [problem_name]
            
            problempool = list(set(problempool))
            # print("Problem Pool:")
            # for problemname in problempool:
            #     problem_rating, problem_tags = cf.get_problem(problemname)
            #     problem_tags = cf.to_six_main_tags(problem_tags)
            #     print(F"Problem: {problemname}, diff: {problem_rating}, tags: {problem_tags}")
            problemname = random.choice(problempool)
            problem_rating, problem_tags = cf.get_problem(problemname)
            problem_tags = cf.to_six_main_tags(problem_tags)
            print(F"Problem: {problemname}, diff: {problem_rating}, tags: {problem_tags}")
            
        except IndexError:
            await ctx.send("No such problem!")
            return

        embed = discord.Embed(title="Codeforces {}".format(problemname), url = "https://codeforces.com/problemset/problem/{}".format(problemname), description = "Challenge will start in 15 seconds!\nType .cancel to cancel the challenge.")
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
        
        #get solving time
        handle = self.db.get_handle(ctx.author.id)
        problemname, start_time = challenge
        if (end_time := cf.check_verdict(handle, problemname, "OK")) < 0:
            end_time = round(time.time())
        solve_time = max(0, round(end_time - start_time))
        print(start_time, end_time, solve_time) 

        embed = discord.Embed(
            title="Challenge Failed. Rating Changes :",
            description = F"Time spent {solve_time//3600}:{(solve_time//60)%60:02d}:{solve_time%60:02d}",
            color=0x8308af
        )
        
        # update ratings
        problem_rating, problem_tags = cf.get_problem(problemname)
        problem_tags = cf.to_six_main_tags(problem_tags)
        user_tags = self.db.get_ratings(ctx.author.id)
        new_rating = []
        weight = 1.0 / max(1, len(problem_tags))

        # check if the tag is in the problems
        for tag, user_rating in user_tags[1:]:
            if tag in problem_tags:
                message, change = cf.change_rating(weight, user_rating, problem_rating, False)
                embed.add_field(name = tag, value = message, inline = False)
                user_rating += change
            new_rating.append(user_rating)

        # delete the challenge and send message
        self.db.update_ratings(ctx.author.id, new_rating)
        self.db.delete_challenge(ctx.author.id)
        
        await ctx.send(embed = embed)

    @commands.command(brief = "Finish the challenge")
    async def finish(self, ctx):
        # check ongoing challenges
        challenge = self.db.get_challenge(ctx.author.id)
        if challenge == None:
            await ctx.send("You don't have any ongoing challenge!")
            return
        
        #get user status
        handle = self.db.get_handle(ctx.author.id)
        problemname, start_time = challenge

        if (end_time := cf.check_verdict(handle, problemname, "OK")) > 0:
            # get solving time 
            solve_time = max(0, round(end_time - start_time))
            print(start_time, end_time, solve_time) 

            # time exceeded
            if solve_time > 3600: 
                await ctx.invoke(self.bot.get_command('ff')) 
                return 

            # challenge succeed
            embed = discord.Embed(
                title="Challenge Completed! Rating Changes :", 
                description=F"Time spent {solve_time//3600}:{(solve_time//60)%60:02d}:{solve_time%60:02d}",
                color=0x09ec6b
            )
            problem_rating, problem_tags = cf.get_problem(problemname)
            problem_tags = cf.to_six_main_tags(problem_tags)
            user_tags = self.db.get_ratings(ctx.author.id)
            new_rating = []
            weight = 1.0 / max(1, len(problem_tags))
            
            for tag, user_rating in user_tags[1:]:
                if tag in problem_tags:
                    message, change = cf.change_rating(weight, user_rating, problem_rating, True)
                    embed.add_field(name = tag, value = message, inline = False)
                    user_rating += change
                new_rating.append(user_rating)
            
            self.db.delete_challenge(ctx.author.id)
            self.db.update_ratings(ctx.author.id, new_rating)
            # To remove the last \n
            await ctx.send(embed = embed) 
            
        else:
            await ctx.send("You haven't completed your {} challenge.\nTo forfeit, enter .ff.".format(problemname))

    @commands.command(brief = "Register your codeforces account")
    async def register(self, ctx, handle = ""): 
        if handle == "":
            await ctx.send("Usage : .register <your_handle>")
            return
        #check if user in database
        if (cf_handle := self.db.get_handle(ctx.author.id)) != "":
            await ctx.send("You have already registered!\nYour handle is {}.".format(cf_handle))
            return
        
        # ask user to submit a CE
        problem = random.choice(cf.query("greedy", 800))
        await ctx.send("Please send a Compilation Error to this problem in the following 60 seconds.")
        embed = discord.Embed(title="Codeforces {}".format(problem[0]), url = "https://codeforces.com/problemset/problem/{}".format(problem[0]))
        await ctx.send(embed = embed)
        await asyncio.sleep(60)

        #check if there's a CE
        try:
            if cf.check_verdict(handle, problem[0], "COMPILATION_ERROR") > 0:
                await ctx.send("Successfully registered {}'s handle as {}".format(ctx.author.mention, handle))
                self.db.insert_user(ctx.author.id, handle)
            else:
                await ctx.send("{} Failed. Try again.".format(ctx.author.mention))
                return 
        except:
            await ctx.send("{} Network Error. Contact admin or try it later.".format(ctx.author.mention))
            return 
        
        # get past submissions to determine initial ratings 
        await ctx.send("Fetching data from Codeforces...")
        solved = cf.solved_problems(handle)
        user_ratings = [1000] * 6 
        tags = ["implementation", "data structures", "graphs", "math", "dp", "greedy"]
        for name in solved: 
            problem_rating, problem_tags = cf.get_problem(name)
            if problem_rating == 0: 
                continue 
            problem_tags = cf.to_six_main_tags(problem_tags)
            weight = 1.0 / max(1, len(problem_tags))
            for i in range(6): 
                if tags[i] in problem_tags: 
                    change = cf.change_rating(weight, user_ratings[i], problem_rating, True)[1]
                    user_ratings[i] += change 
        user_ratings = [round((rating + 1000) / 2) for rating in user_ratings]
        print(user_ratings)
        self.db.update_ratings(ctx.author.id, user_ratings)
        await ctx.invoke(self.bot.get_command('profile')) 


    @commands.command(brief = "See your current rating on every subject.")
    async def profile(self, ctx): 
        #check if user in database
        if self.check_register(ctx) == "" : 
            await ctx.send("You haven't register your handle!\nType .register to register.")
            return
        # get ratings
        ratings = self.db.get_ratings(ctx.author.id)
        ratings = ratings[1:]
        overall_rating = self.cal_overall_rating([i[1] for i in ratings]) 
        embed = discord.Embed(title = ctx.author.name + "'s Profile")
        embed.add_field(name = "Overall Rating", value = overall_rating, inline=False)
        for text, rating in ratings:
            embed.add_field(name = text, value = rating)
        file = discord.File(self.radar_chart(ctx.author.name, ratings), filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)


    @commands.command(brief = "Develope only: set the ratings of <@handle> to <ratings*6>")
    async def set(self, ctx, *ratings):
        if self.check_register(ctx) == "" : 
            await ctx.send("You haven't register your handle!\nType .register to register.")
            return
        ratings = list(ratings)
        self.db.update_ratings(ctx.author.id, ratings)
        await ctx.send(F"New ratings successfully set for {ctx.author.mention}")
        

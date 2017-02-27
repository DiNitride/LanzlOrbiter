import discord
from discord.ext import commands
import random
import datetime
import asyncio
from utils import checks


def decode_seed(seed: float):
    seed = float(seed)
    backup_seed = 0.50
    if seed < 0.00 or seed > 1.00:
        seed = backup_seed
    if seed < 0.10:
        temperature = random.randint(10, 15)
        weather = random.choice(["Windy", "Sharp Winds", "Heavy Rain", "Foggy"])
        w_type = 0
    elif seed < 0.25:
        temperature = random.randint(15, 20)
        weather = random.choice(["Strong Breeze", "Light Rain", "Windy", "Clear Skies", "Overcast"])
        w_type = 1
    elif seed < 0.75:
        temperature = random.randint(20, 25)
        weather = random.choice(["Bright Skies", "Patchy Clouds", "Clear Skies", "Summer Breeze"])
        w_type = 2
    elif seed < 0.90:
        temperature = random.randint(25, 30)
        weather = random.choice(["Bright Skies", "Clear Skies", "Summer Breeze"])
        w_type = 3
    else:
        temperature = random.randint(30, 35)
        weather = random.choice(["Bright Skies", "Clear Skies", "Summer Breeze"])
        w_type = 4
    return temperature, weather, w_type


def to_f(c):
    f = (c * 1.8) + 32
    return f

weather_messages = {
    0: "It looks like it's going to be very cold\nWrap up warm!",
    1: "A little colder than normal\nGrab a coat",
    2: "Average temperature's across the surface",
    3: "Surface temperature's pushing higher\nA nice summer's day",
    4: "Temperature's look to be sweltering hot day\nStay hydrated"}


class Weather:

    def __init__(self, bot):
        self.bot = bot
        self.seeds = []
        self.today = {"t": 0, "w": 0}

        for x in range(7):
            self.seeds.append(random.random())

        t, w, wt = self.generate()
        self.today["t"] = t
        self.today["w"] = w
        self.today["wt"] = wt

    def forecast(self):
        seed = 0
        for x_seed in self.seeds:
            seed += x_seed
        _raw_seed = seed
        seed /= len(self.seeds)
        return seed, _raw_seed

    def generate(self):
        backup_seed, forecast_seed = self.forecast()
        modifier = random.random()
        seed = (backup_seed + modifier) / 2
        wildcard = random.random()
        if wildcard < 0.5:
            wildcard /= 10
            seed -= wildcard*3
        else:
            wildcard /= 10
            seed += wildcard*3
        temperature, weather, w_type = decode_seed(seed)
        self.seeds.pop(0)
        self.seeds.append(modifier)
        return temperature, weather, w_type

    @commands.command(hidden=True)
    @commands.check(checks.is_owner)
    async def evalseed(self, seed):
        t, w, _ = decode_seed(seed)
        await self.bot.say("temp: {} weather: {}".format(t, w))

    @commands.command(hidden=True)
    @commands.check(checks.is_owner)
    async def science(self, counter):
        counter = int(counter)
        category_counter = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        temp_counter = {
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0,
            25: 0,
            26: 0,
            27: 0,
            28: 0,
            29: 0,
            30: 0,
            31: 0,
            32: 0,
            33: 0,
            34: 0,
            35: 0
        }
        weather_counter = {
            "Bright Skies": 0,
            "Clear Skies": 0,
            "Summer Breeze": 0,
            "Windy": 0,
            "Sharp Winds": 0,
            "Heavy Rain": 0,
            "Foggy": 0,
            "Strong Breeze": 0,
            "Light Rain": 0,
            "Overcast": 0,
            "Patchy Clouds": 0,
            "Sunny": 0,
        }
        previous_type = 0
        streak = 1
        streak_list = []
        day_print = ""
        type_print = ""
        for x in range(counter):
            t, w, wt = self.generate()
            if x == 0:
                previous_type = wt
            if previous_type == wt:
                streak += 1
            else:
                streak_list.append("Type {} for {} days".format(previous_type, streak))
                previous_type = wt
                streak = 1
            category_counter[wt] += 1
            temp_counter[t] += 1
            weather_counter[w] += 1
            day_print += "{}\n".format(x)
            type_print += "{}\n".format(wt)
        with open("days.txt", "w") as file:
            file.write(day_print)
        with open("types.txt", "w") as file:
            file.write(type_print)
        output = "Finished generating {} virtual days. Results:\nOverall: {}\nStreaks: {}" \
                 "\nTemperatures: {}\nWeathers: {}".format(counter, category_counter,
                                                           streak_list, temp_counter, weather_counter)
        if len(output) > 1900:
            for x in range(int(len(output) / 1900)):
                await self.bot.say(output[(x)*1900:(x+1)*1900])
        else:
            await self.bot.say(output)

    @commands.command(pass_context=True)
    @commands.check(checks.perm_manage_roles)
    async def morning(self, ctx):
        """Start the next day"""
        channel = discord.utils.get(ctx.message.server.channels, id="285540192314720257")

        f_seed, _ = self.forecast()
        t, w, wt = decode_seed(f_seed)

        em = discord.Embed(
            title="Weather Forecast", colour=discord.Colour.blue(),
            description="\nAnalysing weather patterns\nHere is today's forecast while you wait\n{}".format(weather_messages[wt]),
            timestamp=datetime.datetime.utcfromtimestamp(1488183325))
        em.set_footer(
            text="DiNitride Space Program")
        em.set_thumbnail(
            url="http://starbounder.org/mediawiki/images/6/62/Satellite_Model.png")
        em.set_author(
            name="Weather Station", url=discord.Embed.Empty,
            icon_url="http://starbounder.org/mediawiki/images/6/62/Clear.png")

        em.add_field(
            name="Forecast Temperature", value="{}°C ({}°F)".format(t, round(to_f(t), 2)))
        em.add_field(
            name="Forecast Weather", value="{}".format(w))

        msg = await self.bot.send_message(channel, embed=em)

        await asyncio.sleep(5)

        t, w, wt = self.generate()
        self.today["t"] = t
        self.today["w"] = w
        self.today["wt"] = wt

        em = discord.Embed(
            title="Today's Weather Analysis",
            colour=discord.Colour.blue(),
            description="\n{}\nHave a good day Lanzl, see you tomorrow".format(weather_messages[wt]),
            timestamp=datetime.datetime.utcfromtimestamp(1488183325))

        em.set_footer(
            text="DiNitride Space Program")
        em.set_thumbnail(
            url="http://starbounder.org/mediawiki/images/6/62/Satellite_Model.png")
        em.set_author(
            name="Weather Station", url=discord.Embed.Empty,
            icon_url="http://starbounder.org/mediawiki/images/6/62/Clear.png")

        em.add_field(
            name="Today's Temperature", value="{}°C ({}°F)".format(t, round(to_f(t), 2)))
        em.add_field(
            name="Today's Weather", value="{}".format(w))

        await self.bot.edit_message(msg, new_content=None, embed=em)

    @commands.command()
    async def weather(self):
        """Check the current day's weather"""
        t = self.today["t"]
        w = self.today["w"]
        wt = self.today["wt"]

        em = discord.Embed(
            title="Today's Weather Analysis",
            colour=discord.Colour.blue(),
            description="{}".format(weather_messages[wt]),
            timestamp=datetime.datetime.utcfromtimestamp(1488183325))

        em.set_footer(
            text="DiNitride Space Program")
        em.set_thumbnail(
            url="http://starbounder.org/mediawiki/images/6/62/Satellite_Model.png")
        em.set_author(
            name="Weather Station", url=discord.Embed.Empty,
            icon_url="http://starbounder.org/mediawiki/images/6/62/Clear.png")

        em.add_field(
            name="Today's Temperature", value="{}°C ({}°F)".format(t, round(to_f(t), 2)))
        em.add_field(
            name="Today's Weather", value="{}".format(w))

        await self.bot.say(embed=em)

    @commands.command(name="forecast")
    async def forecast_command(self):
        """View tomorrow's forecast"""
        f_seed, _ = self.forecast()
        t, w, wt = decode_seed(f_seed)

        em = discord.Embed(
            title="Tomorrow's Weather Forecast", colour=discord.Colour.blue(),
            description="{}".format(weather_messages[wt]),
            timestamp=datetime.datetime.utcfromtimestamp(1488183325))
        em.set_footer(
            text="DiNitride Space Program")
        em.set_thumbnail(
            url="http://starbounder.org/mediawiki/images/6/62/Satellite_Model.png")
        em.set_author(
            name="Weather Station", url=discord.Embed.Empty,
            icon_url="http://starbounder.org/mediawiki/images/6/62/Clear.png")

        em.add_field(
            name="Forecast Temperature", value="{}°C ({}°F)".format(t, round(to_f(t), 2)))
        em.add_field(
            name="Forecast Weather", value="{}".format(w))

        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(Weather(bot))

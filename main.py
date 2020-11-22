#Lib Section
import locale
import discord
from discord.ext import commands
import pymysql

#Credentials Section
TOKEN = 'Nzc5MDk3MzQ1MzQ5Nzc5NDc2.X7bk8g.x5PnC_BVWSIGtsQWlgn41OZv67I'

#Also Database Shit
baseConnect = pymysql.connect(
	host='localhost',
	user='root',
	password='JokerzTribe',
	db='jokerz'
)
cursor = baseConnect.cursor()

#Set Prefix For Commands
bot = commands.Bot(command_prefix='>')

#Events Section
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Streaming(name="Jokerz - Ark Tribe",url="Ark"))
	print("Bot Online!")
	print("Logged As: {0.user}".format(bot))


#Commands Section
@bot.command(name='info') #The Info display 
async def info(ctx):
	embedInfo = discord.Embed(title='Tribe Bot Info', description='Made By Jokerz For Jokerz!', color=10181046)
	embedInfo.add_field(name="Commands", value= """
		>info - Displays This Message.
		>creatures - Display available creatures.
		>stats [creature] - Displays current stats of the specified creature.
		>update [creature] [HP] [Stam] [Torpor] [Oxy] [Weight] [Dmg] [Speed] - Allow to change values for stat display.
		""")
	await ctx.send(embed=embedInfo)


@bot.command(name='stats') #3° try for stats display
async def stats(ctx, creatureIntro):

	sql = "SELECT creatureName, health, stamina, torpidity, oxygen, weight, melee_damage, movement_speed FROM jokerz.creature_stats WHERE  creatureName= '{}';".format(creatureIntro)

	cursor.execute(sql)
	creatureStat_list = cursor.fetchone()

	print(creatureStat_list) #Just to see if working

	embedInfo = discord.Embed(title='Tribe Creature Stats', description='Show stats for {}'.format(creatureStat_list[0]), color=10181046)
	embedInfo.add_field(name="Health", value="{:,}".format(creatureStat_list[1]))
	embedInfo.add_field(name="Stamina", value="{:,}".format(creatureStat_list[2]))
	embedInfo.add_field(name="Torpidity", value="{:,}".format(creatureStat_list[3]))
	embedInfo.add_field(name="Oxygen", value="{:,}".format(creatureStat_list[4]))
	embedInfo.add_field(name="Weight", value="{:,}".format(creatureStat_list[6]))
	embedInfo.add_field(name="Melee Damage", value="{:,}%".format(creatureStat_list[6]))
	embedInfo.add_field(name="Movement Speed", value="{:,}%".format(creatureStat_list[7]))

	creatureStat_list = 0
	await ctx.send(embed=embedInfo)

@bot.command(name='black') #Best Command Ever!
async def black(ctx):
	await ctx.send("Black Es Puto.")

#Bot Initialization Section
bot.run(TOKEN)

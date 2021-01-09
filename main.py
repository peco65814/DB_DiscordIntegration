#Lib Section
import locale
import discord
from discord.ext import commands
import pymysql
import re
import string
import asyncio

#Credentials Section
TOKEN = ''

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
		>update [creature] [HP] [Stam] [Torpor] [Oxy] [Food] [Weight] [Dmg] [Speed] - Allow to change values for stat display.
		""")
	await ctx.send(embed=embedInfo)

@bot.command(name='creatures') #Display available creatures
async def creatures(ctx):

	sql = "SELECT creatureName FROM jokerz.creature_stats"
	cursor.execute(sql)
	creaturesList = cursor.fetchall()

	tupCalc = "{}\n" * len(creaturesList)
	strprint = tupCalc.format(*creaturesList)

	pattern = r"[()',]"
	mod_str = re.sub(pattern, '', strprint)

	print(creaturesList)
	print(mod_str)

	embedInfo = discord.Embed(title='Tribe Creatures List', description='{}'.format(mod_str), color=10181046)

	await ctx.send(embed=embedInfo)


@bot.command(name='stats') #3° try for stats display
async def stats(ctx, creatureIntro):

	sql = "SELECT creatureName, health, stamina, torpidity, oxygen, food, weight, melee_damage, movement_speed, url FROM jokerz.creature_stats WHERE  creatureName= '{}';".format(creatureIntro)

	cursor.execute(sql)
	creatureStat_list = cursor.fetchone()

	print(creatureStat_list) #Just to see if working

	embedInfo = discord.Embed(title='Tribe Creature Stats', description='Show stats for {}'.format(creatureStat_list[0]), color=10181046)
	embedInfo.add_field(name="Health", value="{:,}".format(creatureStat_list[1]))
	embedInfo.add_field(name="Stamina", value="{:,}".format(creatureStat_list[2]))
	embedInfo.add_field(name="Torpidity", value="{:,}".format(creatureStat_list[3]))
	embedInfo.add_field(name="Oxygen", value="{:,}".format(creatureStat_list[4]))
	embedInfo.add_field(name="Food", value="{:,}".format(creatureStat_list[5]))
	embedInfo.add_field(name="Weight", value="{:,}".format(creatureStat_list[6]))
	embedInfo.add_field(name="Melee Damage", value="{:,}%".format(creatureStat_list[7]))
	embedInfo.add_field(name="Movement Speed", value="{:,}%".format(creatureStat_list[8]))
	embedInfo.set_thumbnail(url='{}'.format(creatureStat_list[9]))

	creatureStat_list = 0
	await ctx.send(embed=embedInfo)

@bot.command(name='update')
async def update(ctx, creature, health, stamina, torpidity, oxygen, food, weight, meleeDamage, movementSpeed):

	sql = "UPDATE jokerz.creature_stats set health='{}', stamina='{}', torpidity='{}', oxygen='{}', food='{}', weight='{}', melee_damage='{}', movement_speed='{}' WHERE creatureName='{}' ".format(health, stamina, torpidity, oxygen, food, weight, meleeDamage, movementSpeed, creature)
	cursor.execute(sql)


	await ctx.send("Stats Updated!")

'''@bot.command(name='black') #Best Command Ever!
async def black(ctx):
	await ctx.send("BlackCrow Es Puto.")

@bot.command(name='kako') #Best Command Ever!
async def kako(ctx):
	await ctx.send("Kakosaurio Rex Stats: -10 Cabello | 99.999% Macho Man | 100% CocoLiso")'''

#Bot Initialization Section
bot.run('') #Inserta tu token aqui

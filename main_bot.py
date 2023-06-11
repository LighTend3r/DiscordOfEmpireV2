import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
from random import randint,random,choice
from stat_outil import *
import time
from time import gmtime,strftime,time
from datetime import datetime
import requests

# from discord_components import *

from PIL import Image, ImageDraw, ImageFont
import io


TOKEN_TOP_SERVEUR = open("TOKEN_TOP_SERVEUR").read()

default_intents = discord.Intents.default()
default_intents.members = True

bot = commands.Bot(command_prefix="!",intents = default_intents)


def next_level(current_level, xp):
	return int((current_level**(1.5))*10) <= xp

async def check_if_aventurier(ctx):
	verif = any(role.id == ID_ROLE_AVENTURIER for role in ctx.message.author.roles)
	if not verif:
		channel_reception = discord.utils.find(lambda c : c.id == channel_reception_id, ctx.author.guild.channels)
		await ctx.channel.send(f"Tu ne peux pas commencer l'aventure sans avoir signer la charte dans {channel_reception.mention}, l'ami {ctx.author.mention} !")
		return False
	return True

async def récompense_week(ctx):
	result = collection.find({}).sort([("niveau_week", pymongo.DESCENDING), ("xp_week", pymongo.DESCENDING)])
	rank = []
	page = 1
	for n, x in enumerate(result, start=1):
		author_niveau = x["niveau_week"]
		author_name = x["name"]
		author_id = x["_id"]
		author_xp = x["xp_week"]
		author_potion = x["potion"]
		rank.append((n,author_name,author_niveau,author_xp,author_id,author_potion))

	message = ""
	max_page = page*10
	if max_page > rank[-1][0]-1:
		max_page = rank[-1][0]

	for i in range((page-1)*10,max_page):
		if i == 0:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!week`\n\n"
			rank[i][5][3] += 1
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		elif i == 1:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 3 potion de `!vote`\n\n"
			rank[i][5][2] += 3
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		if i in [2,3,4]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 2 potion de `!vote`\n\n"
			rank[i][5][2] += 2
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		if i in [5,6,7,8,9]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!vote`\n\n"
			rank[i][5][2] += 1
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
	embed = discord.Embed(title="Clasement de la semaine",description=message)

	embed.set_footer(text=f"Bien joué à tous <3")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id":auhtor_id},{"$set":{"niveau_week":1}})
		collection.update_one({"_id":auhtor_id},{"$set":{"xp_week":0}})
	channel_recompense = discord.utils.find(lambda c : c.id == channel_recompense_mentuel_hebdomadaire, ctx.author.guild.channels)
	await channel_recompense.send(embed=embed)

async def récompense_month(ctx):
	result = collection.find({}).sort([("niveau_month", pymongo.DESCENDING), ("xp_month", pymongo.DESCENDING)])
	rank = []
	page = 1
	for n, x in enumerate(result, start=1):
		author_niveau = x["niveau_month"]
		author_name = x["name"]
		author_id = x["_id"]
		author_xp = x["xp_month"]
		author_potion = x["potion"]
		rank.append((n,author_name,author_niveau,author_xp,author_id,author_potion))


	message = ""
	max_page = page*10
	if max_page > rank[-1][0]-1:
		max_page = rank[-1][0]

	for i in range((page-1)*10,max_page):

		if i == 0:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 5 potion de `!week`,\n\n"
			rank[i][5][3] += 5
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		elif i == 1:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 3 potion de `!week`\n\n"
			rank[i][5][3] += 3
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		if i in [2,3,4]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 2 potion de `!week`\n\n"
			rank[i][5][3] += 2
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
		if i in [5,6,7,8,9]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!week`\n\n"
			rank[i][5][3] += 1
			collection.update_one({"_id":rank[i][4]},{"$set":{"potion":rank[i][5]}})
	embed = discord.Embed(title="Clasement du mois",description=message)

	embed.set_footer(text=f"Bien joué à tous <3")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id":auhtor_id},{"$set":{"niveau_month":1}})
		collection.update_one({"_id":auhtor_id},{"$set":{"xp_month":0}})
	channel_recompense = discord.utils.find(lambda c : c.id == channel_recompense_mentuel_hebdomadaire, ctx.author.guild.channels)
	await channel_recompense.send(embed=embed)

def check_if_it_is_me(ctx):
	"""Fonction pour chexk si c'est LighTender#8830 qui exécute la commande

	Args:
		ctx (dict): ctx
	"""
	return ctx.message.author.id == 338768773865537536


mongo_url = open("URL_MONGO.txt").read()
cluster = pymongo.MongoClient(mongo_url)
db = cluster["databaseb"]
collection = db["aventurier"]
collection_faction = db["faction"]
collection_event = db["event"]
cooldown_mine = 60 #seconde

ID_ROLE_AVENTURIER = 858347087648391209
ID_ROLE_FAC_FEU = 858749538248032306
ID_ROLE_FAC_EAU = 858749652077379595
ID_ROLE_FAC_AIR = 858749989836423168
ID_ROLE_FAC_TERRE = 858749738089840640
ID_ROLE_CHEAT = 860534436663656448
ID_ROLE_TUTO = 862285262335639552

channel_recompense_mentuel_hebdomadaire = 867769031770243083
channel_lobaratoire_terre_id = 863469621406859284
channel_lobaratoire_feu_id = 863789573830082570
channel_lobaratoire_eau_id = 863789453054181426
channel_lobaratoire_air_id = 863789381898338334
channel_reception_id = 862788903152779264
channel_next_level_id = 859436535463542803
channel_règlement_id = 859885182265458708
channel_commande_actuelles_id = 858388015013560350
channel_report_id = 859883210015375380
channel_zone_de_récolte_id = 862811056879173632
channel_bienvenue_feu_id = 862706671964258384
channel_bienvenue_eau_id = 862706720887537674
channel_bienvenue_air_id = 862706781452369940
channel_bienvenue_terre_id = 862706935769464892
chat_générale_feu_id = 858774169821904901
chat_générale_eau_id = 858775436783124480
chat_générale_air_id = 858775705697779762
chat_générale_terre_id = 858775682029322250

emoji_potion_rose_id = 863788978259886100
emoji_potion_rouge_id = 863788952603459624
emoji_potion_orange_id = 863788987977039872
emoji_potion_bleu_id = 863788996743659580
emoji_wood_id = 858476508129919007
emoji_stone_id = 859171707066515466
emoji_iron_id = 859176992096518166
emoji_gold_id = 865148702666260490
emoji_diamond_id = 865151701169209354

message_reception_id = 862798392430034955


@bot.event  # décorateur
async def on_ready():  # async = cooroutine
	# DiscordComponents(bot)
	print("Le bot est pret")


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):  # Vérifie que c le cooldown
		message = ""
		if error.retry_after >= 3600*24:
			time = strftime('%d %H %M %S', gmtime(error.retry_after)).split(" ")
			message = "{}j {}h {}m {}s".format(time[0], time[1], time[2], time[3])
		elif error.retry_after >= 3600:
			time = strftime('%H %M %S', gmtime(error.retry_after)).split(" ")
			message = "{}h {}m {}s".format(time[0], time[1], time[2])
		elif error.retry_after >= 60:
			time = strftime('%M %S', gmtime(error.retry_after)).split(" ")
			message = "{}m {}s".format(time[0], time[1])
		else:
			time = strftime('%S', gmtime(error.retry_after)).split(" ")
			message = "{}s".format(time[0])
		await ctx.send("{}, réessayer dans {}".format(ctx.author.mention, message))
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send(f"La commande est introuvable veuillez réessayer, l'ami {ctx.author.mention}", delete_after=10)
	elif isinstance(error, commands.CommandError):
		channle_report = discord.utils.find(
			lambda c: c.id == channel_report_id, ctx.author.guild.channels)
		await ctx.send(f"Il y a eu une erreur dans la commande, veuillez mettre le screenshoot dans le salon {channle_report.mention}, pour que le problème soit régler, l'ami {ctx.author.mention}")
		print(error)
	else:
		print("l'erreur est :")
		print(f"{datetime.now()} --> {error}")
		LighTender = discord.utils.find(lambda me: me.id == 338768773865537536, ctx.author.guild.members)
		await LighTender.send(f"{error}")
		print('-------------------------------------------------------------------------------------------------------')


@bot.event
async def on_member_join(member):
	member_id = member.id
	if collection.count_documents({"_id": member_id}) == 0:
		role_tuto = discord.utils.find(lambda r: r.id == ID_ROLE_TUTO, member.guild.roles)

		channel_reception = discord.utils.find(
			lambda c: c.id == channel_reception_id, member.guild.channels)
		channel_règlement = discord.utils.find(
			lambda c: c.id == channel_règlement_id, member.guild.channels)
		channel_commande_actuelles = discord.utils.find(
			lambda c: c.id == channel_commande_actuelles_id, member.guild.channels)
		channel_zone_de_récolte = discord.utils.find(
			lambda c: c.id == channel_zone_de_récolte_id, member.guild.channels)
		await member.send("Bienvenue à toi, jeune aventurier !" +
                    "\n\nTu es nouveau dans le coin ? Eh bien aujourd'hui est un grand jour pour toi puisque **TU** vas pouvoir rejoindre nos rangs !" +
                    "\n\nLe but du jeu est simple, l'ami : obtenir des ressources, te construire une maison, rejoindre une faction et devenir le meilleur aventurier de Discord of Empire !" +
                    "\nTu pourras commencer par récolter du bois et de la pierre grâce aux commandes !wood et !mine qui ne te quitteront plus, puis tu pourras améliorer ta pioche, miner du fer, etc... C'est pas beau ça, l'ami ?" +
                    "\n\nMais ce n'est pas tout... Grâce à ces ressources, tu pourras t'acheter une maison pour ainsi accéder à l'une des quatre grandes factions du serveur ! Ces quatre factions sont la faction du Feu, la faction de l'Eau, la faction de l'Air, et bien sûr la faction de la Terre !" +
                    "\nRejoindre l'une de ces dernières est le cœur de ton aventure, car cela te donnera des avantages sur la récolte de ressources, et te permettra de rivaliser avec les autres factions lors des events organisés, l'ami !" +
                    "\n\nSi tu veux plus d'informations, n'hésite surtout pas à mentionné les @guide, l'ami, ils sont là pour t'aider !" +
                    "\n\nBien sûr, notre auberge dispose de panneaux informatifs, on appelle ça des channels dans le jargon, qui pourront te guider dans ton aventure, notamment :" +
                    f"\n    - {channel_reception.mention} : l'un des plus importants pour que la population se porte bien." +
                    f"\n    - {channel_commande_actuelles.mention} : ce channel liste toutes les commandes et privilièges auxquelles tu as accès dans ton aventure." +
                    f"\n    - Les channels {channel_zone_de_récolte.mention} qui te permettent d'utiliser tes commandes et privilèges." +
                    "\n\nEt puis petite précision supplémentaire, si tu as une quelconque idée pour améliorer Discord of Empire (celui-ci est en cours de construction), tu peux partager ton idée dans le channel #suggestion, ça m'aiderait beaucoup, l'ami !")
		await member.send(f"\n\n**Mais avant tout ça, je te propose d'aller voir notre chef LighTender à la {channel_reception.mention} dans L'Auberge, c'est ici que tout commence !**" +
                    "\n\nBonne chance à toi, jeune aventurier !" +
                    "\n\n*Pour tout problème rencontré, veuillez contacter LighTender#8830 !*")
		await member.add_roles(role_tuto)
	else:
		role = discord.utils.find(
			lambda r: r.id == ID_ROLE_AVENTURIER, member.guild.roles)
		await member.add_roles(role)
		result = collection.find({"_id": member_id})
		for x in result:
			author_house = x["house"]
		if author_house[0] != "pas_de_faction":
			if author_house[0][:-2] == "Faction du Feu":
				role_feu = discord.utils.find(
					lambda r: r.id == ID_ROLE_FAC_FEU, member.guild.roles)
				await member.add_roles(role_feu)
			elif author_house[0][:-2] == "Faction de l'Eau":
				role_eau = discord.utils.find(
					lambda r: r.id == ID_ROLE_FAC_EAU, member.guild.roles)
				await member.add_roles(role_eau)
			elif author_house[0][:-2] == "Faction de l'Air":
				role_air = discord.utils.find(
					lambda r: r.id == ID_ROLE_FAC_AIR, member.guild.roles)
				await member.add_roles(role_air)
			elif author_house[0][:-2] == "Faction de la Terre":
				role_terre = discord.utils.find(
					lambda r: r.id == ID_ROLE_FAC_TERRE, member.guild.roles)
				await member.add_roles(role_terre)


@bot.event
async def on_raw_reaction_add(payload):  # sourcery no-metrics
	emoji_potion_rose = discord.utils.find(
		lambda c: c.id == emoji_potion_rose_id, payload.member.guild.emojis)
	emoji_potion_rouge = discord.utils.find(
		lambda c: c.id == emoji_potion_rouge_id, payload.member.guild.emojis)
	emoji_potion_orange = discord.utils.find(
		lambda c: c.id == emoji_potion_orange_id, payload.member.guild.emojis)
	emoji_potion_bleu = discord.utils.find(
		lambda c: c.id == emoji_potion_bleu_id, payload.member.guild.emojis)
	if payload.emoji.name == "✅" and payload.channel_id == channel_reception_id and payload.message_id == message_reception_id:
		verif = False
		for role in payload.member.roles:
			if role.id == ID_ROLE_AVENTURIER:
				verif = True
		if verif:
			return await payload.member.send(f"Tu as déjà signé la charte, l'ami {payload.member.mention}, une seule fois suffit !")
		author = payload.member
		author_mention = author.mention
		role = discord.utils.find(
			lambda r: r.id == ID_ROLE_AVENTURIER, author.guild.roles)

		stuff = {
			"bois": 0,
			"sève": 0,
			"poudre_magique": 0,
			"pierre": 0,
			"charbon": 0,
			"fer": 0,
			"or": 0,
			"diamant": 0,
			"électrum": 0,
			"dracolite": 0,
			"lave": 0,
			"géode": 0,
			"emeraude": 0,
			"saphire": 0,
			"rubis": 0,
			"quartz": 0,
			"potion": [0, 0, 0, 0]
		}

		biome =  {
			"Commun":[
				"Plaine"
			],
			"Peu_commun":[
			],
			"Rare":[
			],
			"Légendaire":[
			],
			"Mythique":[
			]
		}

		collection.insert_one({"_id": author.id, "name": author.display_name, "niveau": 1, "xp": 0, "niveau_month": 1, "xp_month": 0, "niveau_week": 1, "xp_week": 0, "hav_hache": False, "hav_pioche": False, "hav_house": False, "hav_faction": False, "hav_sword": False, "hache": "None", "pioche": "None", "sword": "None", "wood": 0, "sap": 0, "magic_powder": 0, "stone": 0, "coal": 0, "iron": 0, "steel": 0, "gold": 0, "diamond": 0, "électrum": 0, "dracolite": 0, "lava": 0, "quartz": 0, "géode": 0, "emerald": 0, "sapphire": 0, "ruby": 0, "pure_emerald": 0, "pure_sapphire": 0, "pure_ruby": 0,
		                      "incrusted": "none", "incrusted_hache": "none", "+% minerais": 0, "+minerais": [0, 0, 0], "house": ["pas_de_faction", "name", False], "!wood": 0, "!mine": 0, "!géode": 0, "!bank": [0, 0, 0, 0, 0, 0, 0, 0], "first_!wood": False, "invite": 0, "maxObjet": 2, "objet": [], "cooldown_!vote": 0, "cooldown_!day": 0, "cooldown_!week": 0, "cooldown_!claim": 0, "potion": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "using_potion": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "godfather": False, "event_numbers": [0, 1, False, 0, 0, 0, 0, 0, 0, 0], "aventure": [0, stuff, 0], "pass_aventure": 0, "cooldown_!expedition": 0,"cooldown_!biome": 0, "biome": biome, "current_biome": "Plaine","!expedition":0})
		await author.add_roles(role)
		await author.send("Tu as signé la charte, l'ami ? Incroyable ! Tu es désormais un vrai aventurier !" +
                    "\n\nJe peux maintenant t'expliquer comment survivre dans l'empire." +
                    "\n\nTout d'abord, il faut bien des ressources pour te construire une maison, hein l'ami ?" +
                    "\nPour cela, tu vas pouvoir aller couper du bois avec la merveilleuse hache en bois que je vais t'offrir, c'est un cadeau de la maison ! **Pour la récupérer, il te suffit de taper la commande `!buy axe` dans une des zones de récolte.**")
	elif (payload.emoji.name == f"{emoji_potion_rose.name}"
	      and payload.channel_id in [
	          channel_lobaratoire_terre_id,
	          channel_lobaratoire_feu_id,
	          channel_lobaratoire_eau_id,
	          channel_lobaratoire_air_id,
	      ] and payload.member.bot == False):

		author = payload.member

		channel = discord.utils.find(
			lambda c: c.id == payload.channel_id, author.guild.channels)
		author_mention = author.mention
		result = collection.find({"_id": author.id})
		for x in result:
			author_potion = x["potion"]
			author_sap = x["sap"]
			author_magic_powder = x["magic_powder"]
		if author_sap < 300 or author_magic_powder < 2:
			message = ""
			if author_sap < 300:
				message += f"{300-author_sap} sève(s) "
			if author_magic_powder < 2:
				message += f"{2-author_magic_powder} minerai(s) d'or"
			hist = await channel.history(limit=1).flatten()
			for i in hist:
				if i.id == payload.message_id:
					await i.clear_reactions()
					await i.add_reaction(emoji_potion_rose)
					await i.add_reaction(emoji_potion_rouge)
					await i.add_reaction(emoji_potion_bleu)
			return await channel.send(f"Tu ne peut pas fabriquer une potion de multiplicateur de ressources, l'ami {author_mention} ! il te manque {message}", delete_after=10)
		author_potion[0] = author_potion[0] + 1
		collection.update_one({"_id": author.id}, {"$inc": {"sap": -300}})
		collection.update_one({"_id": author.id}, {"$inc": {"magic_powder": -2}})
		collection.update_one({"_id": author.id}, {
		                      "$set": {"potion": author_potion}})
		hist = await channel.history(limit=1).flatten()

		for i in hist:
			if i.id == payload.message_id:
				await i.clear_reactions()
				await i.add_reaction(emoji_potion_rose)
				await i.add_reaction(emoji_potion_rouge)
				await i.add_reaction(emoji_potion_bleu)
		await channel.send(f"Tu viens de fabriquer une potion de multiplicateur de ressources, l'ami {author_mention} ! Tu peux la voir dans ton inventaire en faisant `!inv` et tu peux l'utiliser en faisant `!potion rose`.", delete_after=30)
	elif (payload.emoji.name == f"{emoji_potion_rouge.name}"
	      and payload.channel_id in [
	          channel_lobaratoire_terre_id,
	          channel_lobaratoire_feu_id,
	          channel_lobaratoire_eau_id,
	          channel_lobaratoire_air_id,
	      ] and payload.member.bot == False):
		author = payload.member

		channel = discord.utils.find(
			lambda c: c.id == payload.channel_id, author.guild.channels)
		author_mention = author.mention
		result = collection.find({"_id": author.id})
		for x in result:
			author_potion = x["potion"]
			author_sap = x["sap"]
			author_magic_powder = x["magic_powder"]
		if author_sap < 500 or author_magic_powder < 5:
			message = ""
			if author_sap < 500:
				message += f"{500-author_sap} sève(s) "
			if author_magic_powder < 5:
				message += f"{5-author_magic_powder} poudre magique"

			hist = await channel.history(limit=1).flatten()
			for i in hist:
				if i.id == payload.message_id:
					await i.clear_reactions()
					await i.add_reaction(emoji_potion_rose)
					await i.add_reaction(emoji_potion_rouge)
					await i.add_reaction(emoji_potion_bleu)
			return await channel.send(f"Tu ne peut pas fabriquer une potion d'amélioration d'item, l'ami {author_mention} ! il te manque {message}", delete_after=10)
		author_potion[1] = author_potion[1] + 1
		collection.update_one({"_id": author.id}, {"$inc": {"sap": -500}})
		collection.update_one({"_id": author.id}, {"$inc": {"magic_powder": -5}})
		collection.update_one({"_id": author.id}, {
		                      "$set": {"potion": author_potion}})
		hist = await channel.history(limit=1).flatten()

		for i in hist:
			if i.id == payload.message_id:
				await i.clear_reactions()
				await i.add_reaction(emoji_potion_rose)
				await i.add_reaction(emoji_potion_rouge)
				await i.add_reaction(emoji_potion_bleu)
		await channel.send(f"Tu viens de fabriquer une potion d'amélioration d'item, l'ami {author_mention} ! Tu peux la voir dans ton inventaire en faisant `!inv` et tu peux l'utiliser en faisant `!potion rouge`.", delete_after=30)
	elif (payload.emoji.name == f"{emoji_potion_bleu.name}"
	      and payload.channel_id in [
	          channel_lobaratoire_terre_id,
	          channel_lobaratoire_feu_id,
	          channel_lobaratoire_eau_id,
	          channel_lobaratoire_air_id,
	      ] and payload.member.bot == False):
		author = payload.member

		channel = discord.utils.find(
			lambda c: c.id == payload.channel_id, author.guild.channels)
		author_mention = author.mention
		result = collection.find({"_id": author.id})
		for x in result:
			author_potion = x["potion"]
			author_sap = x["sap"]
			author_quartz = x["quartz"]
			author_magic_powder = x["magic_powder"]
		if author_sap < 200 or author_quartz < 20 or author_magic_powder < 4:
			message = ""
			if author_sap < 200:
				message += f"{200-author_sap} sève(s) "
			if author_quartz < 20:
				message += f"{20-author_quartz} minerai(s) de quartz"
			if author_magic_powder < 4:
				message += f"{4-author_magic_powder} poudre magique"

			hist = await channel.history(limit=1).flatten()
			for i in hist:
				if i.id == payload.message_id:
					await i.clear_reactions()
					await i.add_reaction(emoji_potion_rose)
					await i.add_reaction(emoji_potion_rouge)
					await i.add_reaction(emoji_potion_bleu)
			return await channel.send(f"Tu ne peut pas fabriquer une potion d'amélioration d'item, l'ami {author_mention} ! il te manque {message}", delete_after=10)
		author_potion[2] = author_potion[2] + 1
		collection.update_one({"_id": author.id}, {"$inc": {"sap": -200}})
		collection.update_one({"_id": author.id}, {"$inc": {"magic_powder": -4}})
		collection.update_one({"_id": author.id}, {"$inc": {"quartz": -20}})
		collection.update_one({"_id": author.id}, {
		                      "$set": {"potion": author_potion}})
		hist = await channel.history(limit=1).flatten()

		for i in hist:
			if i.id == payload.message_id:
				await i.clear_reactions()
				await i.add_reaction(emoji_potion_rose)
				await i.add_reaction(emoji_potion_rouge)
				await i.add_reaction(emoji_potion_bleu)
		await channel.send(f"Tu viens de fabriquer une potion de `!vote` instantané, l'ami {author_mention} ! Tu peux la voir dans ton inventaire en faisant `!inv` et tu peux l'utiliser en faisant `!potion bleu`.", delete_after=30)


@bot.command(name='emoji_id', help="Cette commande te permet d'interagir avec un event quand il y en a un")
@commands.check(check_if_it_is_me)
async def emoji_id(ctx):
	print(ctx.author.guild.emojis)


@bot.command(name='event', help="Cette commande te permet d'interagir avec un event quand il y en a un")
async def event(ctx):

	embed = discord.Embed(
		title="**Event**", description="Les events permettent de pimenter le jeu, ils sont disponible lorsque vous appartenez à une faction, dans le channel prévue à cet effet\n\n*Event à venir*")

	await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


''' Event ou il faut le plus grand nombre
@bot.command(name='event')
async def event(ctx,number= 1261415617151):
	member = ctx.message.author
	good_channel_feu = discord.utils.find(lambda c : c.id == 861620310376448011, member.guild.channels)
	good_channel_eau = discord.utils.find(lambda c : c.id == 861620424495202314, member.guild.channels)
	good_channel_air = discord.utils.find(lambda c : c.id == 861621033852600341, member.guild.channels)
	good_channel_terre = discord.utils.find(lambda c : c.id == 861621197024526381, member.guild.channels)
	if number == 1261415617151:
		result1 = collection_event.find({"_id":1})
		result2 = collection_event.find({"_id":2})
		result3 = collection_event.find({"_id":3})
		result4 = collection_event.find({"_id":4})
		for z in result1:
			nb1 = z["nb"]
		for z in result2:
			nb2 = z["nb"]
		for z in result3:
			nb3 = z["nb"]
		for z in result4:
			nb4 = z["nb"]
		embed = discord.Embed(title="**Event**",description="L'objectif de l'event est d'avoir le nombre le plus élevé avant (date), Pour celà vous devez augmenté votre nombre à l'aide la commande `!event <nb_suivant>` dans votre channel d'event, il faut donc bien entendu appartenir à une faction\n\n*__Par exemple__, si le nombre actuel de votre faction est 304, alors dans votrre channel #event, faite la commande `!event 305`, insi vous ferais progressé votre clan de 1 points*\n\nCependant une règle est à respecté, Vous ne pouvez pas faire augmenté le nombre deux fois à la suite\n**Bonne chance a tous** et que **la meilleur faction gagne**")
		embed.add_field(name="Faction :",value=f"Faction du Feu : **{nb1}**\nFaction de l'Eau : **{nb2}**\nFaction de l'Air : **{nb3}**\nFaction de la Terre : **{nb4}**")
		await ctx.channel.send(f"{ctx.author.mention}",embed=embed)
	elif ctx.message.channel.id == good_channel_feu.id and ctx.message.author.bot == False:

		result = collection_event.find({"_id":1})
		for z in result:
			nb = z["nb"]
			last_id_speak = z["last_id_speak"]
		if ctx.message.author.id == last_id_speak:
			await ctx.channel.purge(limit=1)
			return await member.send("Vous ne pouvais pas mettre de chiffre a là suite")
		if number != nb+1:
			await ctx.channel.purge(limit=1)
			return await member.send(f"Vous deviez mettre {nb+1}")
		collection_event.update_one({"_id":1},{"$inc":{"nb":1}})
		collection_event.update_one({"_id":1},{"$set":{"last_id_speak":ctx.message.author.id}})
	elif ctx.message.channel.id == good_channel_eau.id and ctx.message.author.bot == False:

		result = collection_event.find({"_id":2})
		for z in result:
			nb = z["nb"]
			last_id_speak = z["last_id_speak"]
		if ctx.message.author.id == last_id_speak:
			await ctx.channel.purge(limit=1)
			return await member.send("Vous ne pouvais pas mettre de chiffre a là suite")
		if number != nb+1:
			await ctx.channel.purge(limit=1)
			return await member.send(f"Vous deviez mettre {nb+1}")
		collection_event.update_one({"_id":1},{"$inc":{"nb":1}})
		collection_event.update_one({"_id":1},{"$set":{"last_id_speak":ctx.message.author.id}})
	elif ctx.message.channel.id == good_channel_air.id and ctx.message.author.bot == False:

		result = collection_event.find({"_id":3})
		for z in result:
			nb = z["nb"]
			last_id_speak = z["last_id_speak"]
		if ctx.message.author.id == last_id_speak:
			await ctx.channel.purge(limit=1)
			return await member.send("Vous ne pouvais pas mettre de chiffre a là suite")
		if number != nb+1:
			await ctx.channel.purge(limit=1)
			return await member.send(f"Vous deviez mettre {nb+1}")
		collection_event.update_one({"_id":1},{"$inc":{"nb":1}})
		collection_event.update_one({"_id":1},{"$set":{"last_id_speak":ctx.message.author.id}})
	elif ctx.message.channel.id == good_channel_terre.id and ctx.message.author.bot == False:

		result = collection_event.find({"_id":4})
		for z in result:
			nb = z["nb"]
			last_id_speak = z["last_id_speak"]
		if ctx.message.author.id == last_id_speak:
			await ctx.channel.purge(limit=1)
			return await member.send("Vous ne pouvais pas mettre de chiffre a là suite")
		if number != nb+1:
			await ctx.channel.purge(limit=1)
			return await member.send(f"Vous deviez mettre {nb+1}")
		collection_event.update_one({"_id":1},{"$inc":{"nb":1}})
		collection_event.update_one({"_id":1},{"$set":{"last_id_speak":ctx.message.author.id}})
	else:
		ctx.channel.send(f"Pour plus d'information sur l'event faite `!event`")


@bot.command(name='init_event_nb')
@commands.check(check_if_it_is_me)
async def init_data_base(ctx):
	collection_event.insert_one({"_id":1,"name":"Faction du Feu","last_id_speak":0,"nb":0})
	collection_event.insert_one({"_id":2,"name":"Faction de l'Eau","last_id_speak":0,"nb":0})
	collection_event.insert_one({"_id":3,"name":"Faction de l'Air","last_id_speak":0,"nb":0})
	collection_event.insert_one({"_id":4,"name":"Faction de la Terre","last_id_speak":0,"nb":0})

	await ctx.send(f"La base de donné de l'event a bien étais initialisé, {ctx.author.mention}")
'''


#@bot.command(name='embed')
#@commands.check(check_if_it_is_me)
#async def embef(ctx):
#	"""
#	member = ctx.author
#	channel = discord.utils.find(lambda c : c.id == 861727569098440784, member.guild.channels)
#	role_donateur = discord.utils.find(lambda c : c.id == 861728860453994536, member.guild.roles)
#	embed = discord.Embed(title="**Donation**",description=f"Bonjour / Bonsoir !\nVous cherchez à faire une donation ? Ici nous vous expliquons tout.\n\n**LOI A PROPOS DES DONATIONS**\n*D'après l'Article 894 du code civil : La donation est un acte par lequel le donateur se dépouille actuellement et irrévocablement de la chose donnée en faveur du donataire qui l'accepte. Un don est irrévocable.*\nIl n'y aura donc aucun remboursement de don, quel qu'il soit.\n\n{role_donateur.mention} **(A partir de 1€)**\n-  Accès à des **salons privés**\n- Accès à un **salons privé** pour effectué t'es **commande**\n\n\n__**Pour faire une donation :**__ [Tipeee](https://fr.tipeee.com/discord-of-empire)")
#	"""
#	"""
#	member = ctx.author
#	channel = discord.utils.find(lambda c : c.id == 859885182265458708, member.guild.channels)
#	embed = discord.Embed(title="**Bienvenue sur Discord of Empire !**",description="*Un règlement intérieur est nécessaire au bon fonctionnement de la communauté, nul ne peut ignorer ces règles :*\n\n1. Les [Guidelines](https://discord.com/guidelines?utm_source=dfr) et [Termes](https://discord.com/terms?utm_source=dfr) de Discord sont à respecter.\n\n2. La publicité est interdite, sous quelque forme que ce soit.\n\n3. Respectez le sujet de chaque salon et **soyez pertinent**.\n\n4. **Aucun NSFW** n'est autorisé sur le serveur.\n\n5. Gardez une **énergie positive**.\n\n6. Ne discutez pas les actions de la modération en public.\n\n7. Ne pas **spam** ou **troll** sous quelque forme que ce soit.\n\n8. Gardez un profil approprié.\n\n9. Seul le français est accepté\n\n10. Ne pas notifier sans raison liée à la discussion.")
#	embed.set_footer(text="Cette liste est non exhaustive. Le staff se réserve le droit à l'appréciation finale du règlement")
#	"""
#	await channel.send(embed=embed)

'''
@bot.command(name='embed_laboratoire')
@commands.check(check_if_it_is_me)
async def embed_laboratoire(ctx):

	channel_lobaratoire_terre = discord.utils.find(lambda c : c.id == channel_lobaratoire_terre_id, ctx.author.guild.channels)
	channel_lobaratoire_feu = discord.utils.find(lambda c : c.id == channel_lobaratoire_feu_id, ctx.author.guild.channels)
	channel_lobaratoire_eau = discord.utils.find(lambda c : c.id == channel_lobaratoire_eau_id, ctx.author.guild.channels)
	channel_lobaratoire_air = discord.utils.find(lambda c : c.id == channel_lobaratoire_air_id, ctx.author.guild.channels)

	emoji_potion_rose = discord.utils.find(lambda c : c.id == emoji_potion_rose_id, ctx.author.guild.emojis)
	emoji_potion_rouge = discord.utils.find(lambda c : c.id == emoji_potion_rouge_id, ctx.author.guild.emojis)
	emoji_potion_orange = discord.utils.find(lambda c : c.id == emoji_potion_orange_id, ctx.author.guild.emojis)
	emoji_potion_bleu = discord.utils.find(lambda c : c.id == emoji_potion_bleu_id, ctx.author.guild.emojis)

	embed = discord.Embed(title="**Laboratoire**",description="Vous êtes dans le laboratoire ! C'est ici que l'on concocte des potions de toutes sortes permettant d'obtenir temporairement des bonus, comme l'augmentation des capacités de récolte, l'amélioration temporaire des outils, et bien plus !"+
		"Pour fabriquer une potion, il vous suffit d'utiliser les réactions ci-dessous suivant la potion que vous voulez créer.")
	embed.add_field(name="Potions :",value=f"[{emoji_potion_rose}] - Potion multiplicateur de ressources (*Durée : 30min*)\n**Prix** : 300 sèves, 2 poudre magique\n\n[{emoji_potion_rouge}] - Potion d'amélioration d'item (*Durée : 30min*)\n**Prix** : 500 sèves, 5 poudre magique\n\n[{emoji_potion_bleu}] - Potion de `!vote` instantané\n**Prix** : 200 sèves, 20 minerais de quartz et 4 poudre magique\n\n[{emoji_potion_orange}] - Potion de `!week` instantané\n**Prix** : *pas achetable*")
	message = await channel_lobaratoire_terre.send(embed=embed)
	await message.add_reaction(emoji_potion_rose)
	await message.add_reaction(emoji_potion_rouge)
	await message.add_reaction(emoji_potion_bleu)

	message = await channel_lobaratoire_feu.send(embed=embed)
	await message.add_reaction(emoji_potion_rose)
	await message.add_reaction(emoji_potion_rouge)
	await message.add_reaction(emoji_potion_bleu)

	message = await channel_lobaratoire_eau.send(embed=embed)
	await message.add_reaction(emoji_potion_rose)
	await message.add_reaction(emoji_potion_rouge)
	await message.add_reaction(emoji_potion_bleu)

	message = await channel_lobaratoire_air.send(embed=embed)
	await message.add_reaction(emoji_potion_rose)
	await message.add_reaction(emoji_potion_rouge)
	await message.add_reaction(emoji_potion_bleu)
'''
'''
@bot.command(name='init_data_base',aliases=["idb"],help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def init_data_base(ctx):
	collection_faction.insert_one({"_id":1,"name":"Faction du Feu","niveau":1,"nb_of_member":0,"wood":0,"stone":0,"coal":0,"iron":0,"gold":0,"diamond":0,"+% minerais":0,"+minerais":[0,0,0]})#"+minerais":[fer,or,diamant]
	collection_faction.insert_one({"_id":2,"name":"Faction de l'Eau","niveau":1,"nb_of_member":0,"wood":0,"stone":0,"coal":0,"iron":0,"gold":0,"diamond":0,"+% minerais":0,"+minerais":[0,0,0]})
	collection_faction.insert_one({"_id":3,"name":"Faction de l'Air","niveau":1,"nb_of_member":0,"wood":0,"stone":0,"coal":0,"iron":0,"gold":0,"diamond":0,"+% minerais":0,"+minerais":[0,0,0]})
	collection_faction.insert_one({"_id":4,"name":"Faction de la Terre","niveau":1,"nb_of_member":0,"wood":0,"stone":0,"coal":0,"iron":0,"gold":0,"diamond":0,"+% minerais":0,"+minerais":[0,0,0]})

	await ctx.send(f"La base de donné des faction a bien étais initialisé, {ctx.author.mention}")
'''


# Commande pour give quelqu'un
@bot.command(name='command_int', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def command_int(ctx, arg1, arg2: int, member: discord.Member):
	verif = False
	for role in ctx.message.author.roles:
		if role.id == ID_ROLE_AVENTURIER:
			verif = True
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")

	collection.update_one({"_id": member.id}, {"$set": {arg1: arg2}})

	await ctx.send("C'est fait chef")


@bot.command(name='command_str', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def command_str(ctx, arg1, arg2: str, member: discord.Member):
	verif = False
	for role in ctx.message.author.roles:
		if role.id == ID_ROLE_AVENTURIER:
			verif = True
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")

	collection.update_one({"_id": member.id}, {"$set": {arg1: arg2}})
	await ctx.send("C'est fait chef")
#------------------------------------------------------------------

# Initialisation de certaine donné pour le bon fonctionnement du jeux


@bot.command(name='init_biome', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def init_biome(ctx):
	verif = any(role.id == ID_ROLE_AVENTURIER for role in ctx.message.author.roles)
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")
	result = collection.find()
	biome =  {
			"Commun":[
				"Plaine"
			],
			"Peu_commun":[
			],
			"Rare":[
			],
			"Légendaire":[
			],
			"Mythique":[
			]
		}
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {"$set": {"cooldown_!expedition": 0}})
		collection.update_one({"_id": auhtor_id}, {"$set": {"cooldown_!biome": 0}})
		collection.update_one({"_id": auhtor_id}, {"$set": {"!expedition": 0}})
		collection.update_one({"_id": auhtor_id}, {"$set": {"current_biome": "Plaine"}})
		collection.update_one({"_id": auhtor_id}, {
		                      "$set": {"biome": biome}})
	await ctx.send("C'est fait chef")


@bot.command(name='init_little_event', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def init_database(ctx):
	verif = False
	for role in ctx.message.author.roles:
		if role.id == ID_ROLE_AVENTURIER:
			verif = True
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {"$set": {"event_numbers": [
		                      0, 2, False, 0, 0, 0, 0, 0, 0, 0]}})  # [multiplicateur,%lucky,next_pioche(True/False)]
	await ctx.send("C'est fait chef")


@bot.command(name='finish_little_event', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def init_database(ctx):
	verif = False
	for role in ctx.message.author.roles:
		if role.id == ID_ROLE_AVENTURIER:
			verif = True
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {"$set": {"event_numbers": [
		                      0, 1, False, 0, 0, 0, 0, 0, 0, 0]}})  # [multiplicateur,%lucky,next_pioche(True/False)]
	await ctx.send("C'est fait chef")


@bot.command(name='enable_join_faction', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def enable_join_faction(ctx, id: int, join):
	if join == "true" or join == "True":
		collection_faction.update_one({"_id": id}, {'$set': {'can_join': True}})
	elif join == "false" or join == "False":
		collection_faction.update_one({"_id": id}, {'$set': {'can_join': False}})
# --------------------------------------------------------------------

# Give d'objet pour les gens (Cadeau)


@bot.command(name='give_potion_vote', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def give_potion_vote(ctx):
	if not await check_if_aventurier(ctx):
		return
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		author_potion = x["potion"]
		author_potion[2] += 1
		collection.update_one({"_id": auhtor_id}, {
		                      "$set": {"potion": author_potion}})
	await ctx.send("C'est fait chef")


@bot.command(name='give_pass', help="Pour faire des cadeau (Pour le gérant du serveur)")
@commands.check(check_if_it_is_me)
async def give_pass(ctx, member: discord.Member, nb: int):
	if member.id == 338768773865537536:
		result = collection.find()
	else:
		result = collection.find({"_id": member.id})
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {
		                      "$inc": {"pass_aventure": nb}})
	await ctx.send("C'est fait chef")


@bot.command(name='lvl', aliases=["niveau", "level", "Niveau", "Level", "Lvl"], help="Cette commande revoie tout simplement votre Niveau, ainsi que votre Xp")
@commands.cooldown(1, 2, commands.BucketType.user)
async def lvl(ctx):
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_niveau = x["niveau"]
		author_xp = x["xp"]

	IMAGE_WIDTH = 300
	IMAGE_HEIGHT = 100

	# create empty image 600x300
	# RGB, RGBA (with alpha), L (grayscale), 1 (black & white)
	image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))

	# or load existing image
	#image = Image.open('/home/furas/images/lenna.png')

	# create object for drawing
	draw = ImageDraw.Draw(image)
	(44, 47, 51)
	# draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
	draw.rectangle([0, 0, IMAGE_WIDTH, IMAGE_HEIGHT],
	               fill=(44, 47, 51))  # Le grand réctangle
	draw.rounded_rectangle([98-27, 48, 302-27, 72], radius=20, fill=(61, 64, 68),
	                       outline=(35, 39, 42), width=2)  # le barre entière de niveau
	if author_xp > -1:
		draw.rounded_rectangle([100-27, 50, 100-27 + (int(200*(author_xp/int(
			((author_niveau)**1.5)*10)))), 70], radius=20, fill=(21, 214, 30))  # l'xp
	else:
		draw.rounded_rectangle([100-27, 50, 100-27 + 0, 70],
		                       radius=20, fill=(21, 214, 30))  # l'xp
	# draw text_name
	text_name = f'{ctx.author.display_name}'

	font = ImageFont.truetype('Consolas.ttf', 11)

	text_width, text_height = draw.textsize(text_name, font=font)
	x = IMAGE_WIDTH - text_width - 27
	y = 80

	draw.text((x, y), text_name, fill=(255, 255, 255), font=font)

	# draw text_niveau
	text_niveau = f'Niveau : {author_niveau}'

	font = ImageFont.truetype('Consolas.ttf', 16)

	text_width, text_height = draw.textsize(text_niveau, font=font)
	x = 18 + 64 + 8
	y = (IMAGE_HEIGHT - text_height)//2 - 15

	draw.text((x, y), text_niveau, fill=(255, 255, 255), font=font)

	# draw text_xp
	text_xp = f'{author_xp}/{int(((author_niveau)**1.5)*10)}'

	font = ImageFont.truetype('Consolas.ttf', 14)

	text_width, text_height = draw.textsize(text_xp, font=font)
	x = 90
	y = 54

	draw.text((x, y), text_xp, fill=(0, 0, 0), font=font)

	# --- Avatare ---
	AVATAR_SIZE = 64
	avatar_asset = ctx.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

	# read JPG from server to buffer (file-like object)
	buffer_avatar = io.BytesIO()
	await avatar_asset.save(buffer_avatar)
	buffer_avatar.seek(0)

	# read JPG from buffer to Image
	avatar_image = Image.open(buffer_avatar)

	avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))

	circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
	circle_draw = ImageDraw.Draw(circle_image)
	circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
	#avatar_image.putalpha(circle_image)
	#avatar_image.show()

	image.paste(avatar_image, (18, (IMAGE_HEIGHT-AVATAR_SIZE)//2), circle_image)

	draw.ellipse((16, 16, 84, 84), outline=(30, 32, 33), width=3)

	# create buffer
	buffer = io.BytesIO()

	# save PNG in buffer
	image.save(buffer, format='PNG')

	# move to beginning of buffer so `send()` it will read from beginning
	buffer.seek(0)

	# send image
	await ctx.send(f"{ctx.author.mention}", file=discord.File(buffer, 'myimage.png'))


@bot.command(name='godfather', aliases=["parrain","Parrain","Godfather"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def godfather(ctx, member: discord.Member):
	if not await check_if_aventurier(ctx):
		return

	result = collection.find({"_id": ctx.author.id})
	for x in result:
		author_havGodfather = x["godfather"]

	if author_havGodfather:
		return await ctx.channel.send(f"Tu as déjà un parrain, l'ami {ctx.author.mention}")

	if ctx.author.id == member.id:
		return await ctx.channel.send(f"Tu ne peux pas te parrainer toi même, l'ami {ctx.author.mention}")
	collection.update_one({"_id": ctx.author.id}, {"$set": {"godfather": True}})
	collection.update_one({"_id": member.id}, {"$inc": {"invite": 1}})

	await ctx.channel.send(f"{ctx.author.mention} vient de parrainer {member.mention}")
	result = collection.find({"_id": member.id})
	for x in result:
		author_invitation = x["invite"]
		author_potion = x["potion"]
	loots = invitation_loot[str(author_invitation)]
	loots = loots.split("/")
	message = f"Vous avez maintenant {author_invitation} invitation, vous venez d'obtenir "
	for lot in loots:
		lot = lot.split(" ")
		if lot[1] == "vote":
			message += f"{lot[0]} potion `!vote` instantané, "
			author_potion[2] += int(lot[0])
		elif lot[1] == "week":
			message += f"{lot[0]} potion `!week` instantané, "
			author_potion[3] += int(lot[0])
		elif lot[1] == "x2":
			message += f"{lot[0]} potion de multiplicateur de ressources, "
			author_potion[0] += int(lot[0])
		elif lot[1] == "item":
			message += f"{lot[0]} potion d'amélioration d'item, "
			author_potion[1] += int(lot[0])
		elif lot[1] == "unlock_week":
			message += f"Vous débloqué le `!week`, "
		elif lot[1] == "emerald":
			message += f"{lot[0]} émeraude, "
			collection.update_one({"_id": member.id}, {
			                      "$inc": {"emerald": int(lot[0])}})
		elif lot[1] == "geode":
			message += f"{lot[0]} géode, "
			collection.update_one({"_id": member.id}, {"$inc": {"géode": int(lot[0])}})
	collection.update_one({"_id": member.id}, {"$set": {"potion": author_potion}})
	await member.send(message)


@bot.command(name='give', help="Cette commande n'est autorisé que pour faire des test")
#@commands.cooldown(5,120,commands.BucketType.user)
async def give(ctx, nb: int, minéraux: str):
	if not await check_if_aventurier(ctx):
		return
	verif = any(role.id == ID_ROLE_CHEAT for role in ctx.message.author.roles)
	if not verif:
		return await ctx.channel.send(f"Vous devez avoir le rôle cheat pour executé la commande`, {ctx.author.mention}")

	author_id = ctx.author.id
	if nb > 1000000:
		return await ctx.channel.send(f"Votre chiffre est trop élevé, il faut qu'il soit inférieur a 1 000 000, {ctx.author.mention}")

	if minéraux in {"b", "bois"}:
		collection.update_one({"_id": author_id}, {"$inc": {"wood": nb}})
		await ctx.channel.send(f"Vous vous êtes donné {nb} bois, {ctx.author.mention}")
	elif minéraux in {"p", "pierre"}:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": nb}})
		await ctx.channel.send(f"Vous vous êtes donné {nb} pieres, {ctx.author.mention}")
	elif minéraux in {"f", "fer"}:
		collection.update_one({"_id": author_id}, {"$inc": {"iron": nb}})
		await ctx.channel.send(f"Vous vous êtes donné {nb} fer, {ctx.author.mention}")
	elif minéraux in {"o", "or"}:
		collection.update_one({"_id": author_id}, {"$inc": {"gold": nb}})
		await ctx.channel.send(f"Vous vous êtes donné {nb} or, {ctx.author.mention}")
	elif minéraux in {"d", "diamant"}:
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": nb}})
		await ctx.channel.send(f"Vous vous êtes donné {nb} diamant, {ctx.author.mention}")
	else:
		await ctx.channel.send(f"Votre commande n'a pas étais comprise, faite `!give <nb> <matériaux>` avec <matériaux>=b/p/f/o/d, {ctx.author.mention}")


@bot.command(name='mine', aliases=["m","M","Mine"], help="Cette commande te permet de miner des minerais et de la pierre, pour l'utilisé il faut avoir une pioche qu'on obtien en faisant <!buy pickaxe>")
@commands.cooldown(1, cooldown_mine, commands.BucketType.user)
async def mine(ctx):  # sourcery no-metrics  # sourcery no-metrics
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	member = ctx.message.author
	result = collection.find({"_id": author_id})
	for x in result:
		author_pioche = x["hav_pioche"]

	if not author_pioche:  # vérifie si le joueur possède une pioche
		channel_reception = discord.utils.find(
			lambda c: c.id == channel_reception_id, ctx.author.guild.channels)
		return await ctx.channel.send(f"Vous devez commencé l'aventure en signant la charte dans {channel_reception.mention}")

	result = collection.find({"_id": author_id})
	for x in result:
		author_pioche = x["pioche"]
		author_lvl = x["niveau"]
		author_lvl_week = x["niveau_week"]
		author_lvl_month = x["niveau_month"]
		author_xp = x["xp"]
		author_xp_week = x["xp_week"]
		author_xp_month = x["xp_month"]
		author_house = x["house"][0]
		author_incrusted = x["incrusted"]
		author_using_potion = x["using_potion"]
		author_potion = x["potion"]
		author_current_biome = x["current_biome"]
		little_event = x["event_numbers"]
		#"Pioche":[niveau,prix,(pierre_min,pierre_max),%fer]
	if author_current_biome in ["Forêt Ancienne", "Forêt féérique"]:
		return await ctx.send(f"Dans le biome {author_current_biome} tu ne peut pas trouver de pierre, l'ami {ctx.author.mention}")
	pourcentage_minerais_faction = 0
	minerais_en_plus_faction = [0, 0, 0]

	if author_house != "pas_de_faction":
		result_faction = collection_faction.find({"name": author_house[:-2]})

		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	if little_event[2]:
		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat

	if author_using_potion[1] != 0 and author_using_potion[1] >= int(time()):

		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat
	elif author_using_potion[1] != 0:
		author_using_potion[1] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	author_pierres = list(pioche[author_pioche][2])
	author_fer = list(pioche[author_pioche][3])
	author_gold = list(pioche[author_pioche][4])
	author_diamond = list(pioche[author_pioche][5])
	author_géode = list(pioche[author_pioche][6])

	if author_incrusted != "none":
		boost_incrustation = incrustation[author_incrusted][0]

		author_pierres[0] *= boost_incrustation
		author_pierres[1] *= boost_incrustation
		author_fer[1] *= boost_incrustation
		author_gold[1] *= boost_incrustation
		author_diamond[1] *= boost_incrustation
		author_géode[1] *= boost_incrustation

	all_pourcentage_fer = (
		author_fer[0] + author_fer[0]*pourcentage_minerais_faction)*little_event[1]
	all_pourcentage_or = (
		author_gold[0] + author_gold[0]*pourcentage_minerais_faction)*little_event[1]
	all_pourcentage_diamant = (
		author_diamond[0] + author_diamond[0]*pourcentage_minerais_faction)*little_event[1]
	all_pourcentage_géode = (
		author_géode[0] + author_géode[0]*pourcentage_minerais_faction)*little_event[1]
	boost = 1
	if author_using_potion[0] != 0 and author_using_potion[0] >= int(time()):
		boost = 2
	elif author_using_potion[0] != 0:
		author_using_potion[0] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})
	do_stone = True
	boost_biome_pierre = 1
	if author_current_biome in ["Carrière", "Grosse grotte", "Montagne éléctrique"]:
		boost_biome_pierre = 1.5
	elif author_current_biome in ["Grotte", "Volcan"]:
		boost_biome_pierre = 2
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_pierre = 4
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_pierre = 0.25
	elif author_current_biome in ["Forêt d'érable"]:
		boost_biome_pierre = 0.75
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		do_stone = False
		boost_biome_pierre = 0

	boost_biome_fer = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_fer = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_fer = 2
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_fer = 0

	boost_biome_or = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_or = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_or = 2
	elif author_current_biome in ["Montagne éléctrique"]:
		boost_biome_or = 3
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_or = 0

	boost_biome_charbon = (0,0)
	if author_current_biome in ["Grotte"]:
		boost_biome_charbon = (0.01,50)
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_charbon = (0.05,100)

	boost_biome_lave = (0,0)
	if author_current_biome in ["Volcan"]:
		boost_biome_lave = (0.05,1)

	boost_biome_steel = (0,0)
	if author_current_biome in ["Météorite"]:
		boost_biome_steel = (0.2,5)

	boost_biome_electrum = (0,0)
	if author_current_biome in ["Montagne éléctrique"]:
		boost_biome_electrum = (0.01,1)

	boost_biome_dracolite = (0,0)
	if author_current_biome in ["Nid du dragon"]:
		boost_biome_dracolite = (0.005,1)

	boost_biome_emerald = (0,0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_emerald = (0.3,1)
	boost_biome_sapphire = (0,0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_sapphire = (0.08,1)
	boost_biome_ruby = (0,0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_ruby = (0.01,1)

	boost_biome_géode = 1
	if author_current_biome in ["Météorite"]:
		boost_biome_géode = 1.5
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_géode = 0

	boost_biome_diamond = 1
	if author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_diamond = 0


	stone = int((randint(author_pierres[0], author_pierres[1])*boost)*boost_biome_pierre)  # à changé

	hav_iron = False
	hav_gold = False
	hav_diamond = False
	hav_géode = False
	hav_coal = False
	hav_lava = False
	hav_steel = False
	hav_electrum = False
	hav_dracolite = False
	hav_emerald = False
	hav_sapphire = False
	hav_ruby = False
	#Calcule le fer
	rand = random()
	if all_pourcentage_fer >= rand:
		iron = int(((author_fer[1] + minerais_en_plus_faction[0])*boost)*boost_biome_fer)
		hav_iron = True
	#Calcule l'or
	rand = random()
	if all_pourcentage_or >= rand:
		gold = int(((author_gold[1] + minerais_en_plus_faction[1])*boost)*boost_biome_or)
		hav_gold = True
	#Calcule du diamant
	rand = random()
	if all_pourcentage_diamant >= rand:
		diamond = int(((author_diamond[1] + minerais_en_plus_faction[2])*boost)*boost_biome_diamond)
		hav_diamond = True

	rand = random()
	if all_pourcentage_géode >= rand:
		géode = int((author_géode[1] * boost)*boost_biome_géode)
		hav_géode = True

	rand = random()
	if boost_biome_charbon[0] >= rand:
		coal = boost_biome_charbon[1]
		hav_coal = True

	rand = random()
	if boost_biome_lave[0] >= rand:
		lava = boost_biome_lave[1]
		hav_lava = True

	rand = random()
	if boost_biome_steel[0] >= rand:
		steel = boost_biome_steel[1]
		hav_steel = True

	rand = random()
	if boost_biome_electrum[0] >= rand:
		electrum = boost_biome_electrum[1]
		hav_electrum = True
	rand = random()
	if boost_biome_dracolite[0] >= rand:
		dracolite = boost_biome_dracolite[1]
		hav_dracolite = True

	rand = random()
	if boost_biome_emerald[0] >= rand:
		emerald = boost_biome_emerald[1]
		hav_emerald = True
	rand = random()
	if boost_biome_sapphire[0] >= rand:
		sapphire = boost_biome_sapphire[1]
		hav_sapphire = True
	rand = random()
	if boost_biome_ruby[0] >= rand:
		ruby = boost_biome_ruby[1]
		hav_ruby = True

	message = ""

	# pierre
	if do_stone:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
		message += f"Bien joué, l'ami {ctx.author.mention}, tu viens de récolter **{stone} de pierre**"
	if (hav_iron or hav_gold or hav_diamond or hav_géode or hav_coal or hav_lava or hav_steel or hav_electrum) and do_stone:
		message += f", et en plus, il y avait"
	elif (hav_dracolite or hav_emerald or hav_sapphire or hav_ruby) and not do_stone:
		message += f"Wow tu viens de trouver "
	message_pierre = ""
	if hav_iron and do_stone:  # fer
		collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
		message_pierre += f", **{iron} minerai(s) de fer**"
	if hav_gold and do_stone:  # or
		collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
		message_pierre += f", **{gold} minerai(s) d'or**"
	if hav_diamond and do_stone:  # dimant
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
		message_pierre += f", __**{diamond} minerai(s) de diamant**__"
	if hav_géode and do_stone:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
		message_pierre += f", __**{géode} géode(s)**__"
	if hav_coal:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message_pierre += f", **{coal} Charbons**"
	if hav_lava:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"lava": lava}})
		message_pierre += f", **{lava} sceau de lave**"
	if hav_steel:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"steel": steel}})
		message_pierre += f", **{steel} acier**"
	if hav_electrum:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"électrum": electrum}})
		message_pierre += f", **__{electrum} électrum__**"
	if hav_dracolite:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"dracolite": dracolite}})
		message_pierre += f", **__{dracolite} dracolite__**"
	if hav_emerald:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"emerald": emerald}})
		message_pierre += f", **__{emerald} émeraude__**"
	if hav_sapphire:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"sapphire": sapphire}})
		message_pierre += f", **__{sapphire} saphir__**"
	if hav_ruby:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"ruby": ruby}})
		message_pierre += f", **__{ruby} rubis__**"
	if (hav_iron or hav_gold or hav_diamond or hav_géode or hav_coal or hav_lava or hav_steel or hav_electrum) and do_stone:
		message_pierre = message_pierre[1:]
		message += message_pierre
		message += " dans la pierre que tu viens de miner !"
	elif hav_dracolite or hav_emerald or hav_sapphire or hav_ruby:
		message_pierre = message_pierre[1:]
		message += message_pierre
		message += " dans la pierre que tu viens de miner !"
	else:
		message += " !"
	await ctx.channel.send(f"{message}")

	collection.update_one({"_id": author_id}, {"$inc": {"!mine": 1}})
	collection.update_one({"_id": author_id}, {"$inc": {"xp": 2}})
	collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 2}})
	collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 2}})

	if next_level(author_lvl, author_xp+2):
		channel_next_level = discord.utils.find(
			lambda c: c.id == channel_next_level_id, member.guild.channels)

		collection.update_one({"_id": author_id}, {"$inc": {"niveau": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp": -int((author_lvl**(1.5))*10)}})

		await channel_next_level.send(f"{ctx.author.mention} vient d'atteindre le niveau {author_lvl+1}, **Félicitation !**\nSaisissez la commande `!lvl` ou `!stat` pour obtenir plus d'information")
	if next_level(author_lvl_week, author_xp_week+2):
		collection.update_one({"_id": author_id}, {"$inc": {"niveau_week": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp_week": -int((author_lvl_week**(1.5))*10)}})
	if next_level(author_lvl_month, author_xp_month+2):
		collection.update_one({"_id": author_id}, {"$inc": {"niveau_month": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp_month": -int((author_lvl_month**(1.5))*10)}})
	await ctx.channel.send(f"https://thumbs.gfycat.com/KnobbyDelectableGrouse.webp", delete_after=60)


@bot.command(name='wood', aliases=["bois","w","Wood","W"], help="Cette commande te permet de miner du bois, pour l'utilisé il faut avoir une hache qu'on obtien en faisant <!buy axe>")
@commands.cooldown(1, 30, commands.BucketType.user)
async def wood(ctx):  # sourcery no-metrics
	if not await check_if_aventurier(ctx):
		return

	member = ctx.message.author
	author_id = member.id

	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_first_wood = x["first_!wood"]
		author_incrusted_hache = x["incrusted_hache"]

	if not author_hav_hache:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de hache, acheter la **hache_en_bois** **__gratuitement__** en faisant <`!buy axe`>, {ctx.author.mention}")

	if not author_first_wood:
		collection.update_one({"_id": author_id}, {"$set": {"first_!wood": True}})
		await member.send("Tu as récupéré du bois, c'est merveilleux l'ami ! Tu peux regarder les quantités de ressources que tu as en écrivant `!inv` dans une des zones de récolte." +
                    "\n\nContinue de castagner du bois jusqu'à en avoir **50** pour pouvoir t'acheter une pioche en bois ! **Pour la récupérer, il te suffit de taper la commande `!buy pickaxe` dans une des zones de récolte.**")

	result = collection.find({"_id": author_id})

	for x in result:
		#"nom_hache":[niveau,prix,(bois_min,bois_max)]
		author_hache = x["hache"]
		author_lvl = x["niveau"]
		author_lvl_week = x["niveau_week"]
		author_lvl_month = x["niveau_month"]
		author_xp = x["xp"]
		author_xp_week = x["xp_week"]
		author_xp_month = x["xp_month"]
		author_house = x["house"][0]
		author_using_potion = x["using_potion"]
		author_current_biome = x["current_biome"]
		little_event = x["event_numbers"]

	if author_current_biome in ["Grotte", "Grosse grotte", "Volcan", "Météorite", "Montagne éléctrique", "Nid du dragon","Pierre précieuse"]:
		return await ctx.send(f"Dans le biome {author_current_biome} tu ne peut pas trouver de bois, l'ami {ctx.author.mention}")

	pourcentage_minerais_faction = 0
	minerais_en_plus_faction = [0, 0, 0]

	if author_house != "pas_de_faction":
		result_faction = collection_faction.find({"name": author_house[:-2]})

		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	if little_event[2]:
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if hache_stat != "soon":
			author_hache = hache_stat

	if author_using_potion[1] != 0 and author_using_potion[1] >= int(time()):
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if hache_stat != "soon":
			author_hache = hache_stat
	elif author_using_potion[1] != 0:
		author_using_potion[1] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	boost = 1
	if author_using_potion[0] != 0 and author_using_potion[0] >= int(time()):
		boost = 2
	elif author_using_potion[0] != 0:
		author_using_potion[0] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	author_wood = list(hache[author_hache][2])
	author_sap = list(hache[author_hache][3])
	author_magic_powder = list(hache[author_hache][4])

	if author_incrusted_hache != "none":
		boost_incrustation = incrustation[author_incrusted_hache][0]
		author_wood[0] *= boost_incrustation
		author_wood[1] *= boost_incrustation
		author_sap[1] *= boost_incrustation

	boost_biome_bois = 1
	if author_current_biome in ["Forêt","Forêt d'érable","Forêt féérique"]:
		boost_biome_bois = 1.5
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_bois = 4
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_bois = 0.5
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_bois = 0.25

	do_sap = True
	boost_biome_sève = 1
	if author_current_biome in ["Forêt d'érable"]:
		boost_biome_sève = 2
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_sève = 0
		do_sap = False

	boost_biome_magic_powder = 1
	if author_current_biome == "Forêt féérique":
		boost_biome_magic_powder = 4

	boost_biome_coal = (0,0)
	if author_current_biome == "Forêt Ancienne":
		boost_biome_coal = (0.1,100)


	wood = int((randint(author_wood[0], author_wood[1])*boost)*boost_biome_bois)

	hav_sap = False
	hav_magic_three = False
	hav_coal = False

	all_pourcentage_sap = (
		author_sap[0] + author_sap[0]*pourcentage_minerais_faction)*little_event[1]
	all_pourcentage_magic_powder = ((author_magic_powder[0])*little_event[1])*boost_biome_magic_powder
	#Calcule le sève
	rand = random()
	if all_pourcentage_sap >= rand:
		sap = int((author_sap[1] * boost)*boost_biome_sève)
		hav_sap = True
	rand = random()
	if all_pourcentage_magic_powder >= rand:
		magic_powder = author_magic_powder[1]
		hav_magic_three = True

	rand = random()
	if boost_biome_coal[0] >= rand:
		coal = boost_biome_coal[1]
		hav_coal = True

	collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
	collection.update_one({"_id": author_id}, {"$inc": {"!wood": 1}})

	collection.update_one({"_id": author_id}, {"$inc": {"xp": 1}})
	collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 1}})
	collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 1}})

	message = ""

	message += f"Bien joué, l'ami {ctx.author.mention}, tu viens de récolter **{wood} de bois**"
	if hav_sap and do_sap:
		message += f", et en plus, il y avait"
		collection.update_one({"_id": author_id}, {"$inc": {"sap": sap}})
		message_pierre = ""
		message_pierre += f", **{sap} sève(s)**"
		message += message_pierre[1:]
		message += " dans l'arbre que tu viens de couper !"
	if hav_coal:
		message += f", et en plus, il y avait"
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message_pierre = ""
		message_pierre += f", **{coal} charbons**"
		message += message_pierre[1:]
		message += " dans l'arbre que tu viens de couper !"
	else:
		message += " !"
	message2 = ""
	if hav_magic_three:
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"magic_powder": magic_powder}})
		message2 = f"\nWow, l'ami, c'était un arbre Magique, et il a laisser tomber **__{magic_powder} poudre(s) magique(s)__** !"

	await ctx.channel.send(f"{message}\n{message2}")
	await ctx.channel.send(f"https://thumbs.gfycat.com/JitteryAnotherBalloonfish-size_restricted.gif", delete_after=30)

	if next_level(author_lvl, author_xp+1):
		channel_next_level = discord.utils.find(
			lambda c: c.id == channel_next_level_id, member.guild.channels)

		collection.update_one({"_id": author_id}, {"$inc": {"niveau": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp": -int((author_lvl**(1.5))*10)}})
		await channel_next_level.send(f"{ctx.author.mention} vient d'atteindre le niveau {author_lvl+1}, **Félicitation !**\nSaisissez la commande `!lvl` ou `!stat` pour obtenir plus d'information")
	if next_level(author_lvl_week, author_xp_week+1):
		collection.update_one({"_id": author_id}, {"$inc": {"niveau_week": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp_week": -int((author_lvl_week**(1.5))*10)}})

	if next_level(author_lvl_month, author_xp_month+1):
		collection.update_one({"_id": author_id}, {"$inc": {"niveau_month": 1}})
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"xp_month": -int((author_lvl_month**(1.5))*10)}})


@bot.command(name='cooldown',aliases=["Cooldown"], help="Cette commande te permet de connaître le cooldown du !week et !vote")
@commands.cooldown(1, 2, commands.BucketType.user)
async def cooldown(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_vote_cooldown = x["cooldown_!vote"]
		author_week_cooldown = x["cooldown_!week"]
		author_cooldown_expedition = x["cooldown_!expedition"]
		author_cooldown_biome = x["cooldown_!biome"]
		author_invitation = x["invite"]

	t2 = int(time())
	t_vote = int(author_vote_cooldown+60*60*12)
	t_week = int(author_week_cooldown+60*60*24*7)
	message = ""

	t2_vote = int(t_vote - t2)
	t2_week = int(t_week - t2)
	t2_expedition = int(author_cooldown_expedition - t2)
	t2_biome = int(author_cooldown_biome - t2)

	if 0 < t2_vote:

		if t2_vote >= 3600*24:
			t3 = strftime('%d %H %M %S', gmtime(t2_vote)).split(" ")
			message_vote = "{}j {}h {}m {}s".format(int(t3[0])-1, t3[1], t3[2], t3[3])
		elif t2_vote >= 3600:
			t3 = strftime('%H %M %S', gmtime(t2_vote)).split(" ")
			message_vote = "{}h {}m {}s".format(t3[0], t3[1], t3[2])
		elif t2_vote >= 60:
			t3 = strftime('%M %S', gmtime(t2_vote)).split(" ")
			message_vote = "{}m {}s".format(t3[0], t3[1])
		else:
			t3 = strftime('%S', gmtime(t2_vote)).split(" ")
			message_vote = "{}s".format(t3[0])

	if 0 < t2_week:

		if t2_week >= 3600*24:
			t4 = strftime('%d %H %M %S', gmtime(t2_week)).split(" ")
			message_week = "{}j {}h {}m {}s".format(int(t4[0])-1, t4[1], t4[2], t4[3])
		elif t2_week >= 3600:
			t4 = strftime('%H %M %S', gmtime(t2_week)).split(" ")
			message_week = "{}h {}m {}s".format(t4[0], t4[1], t4[2])
		elif t2_week >= 60:
			t4 = strftime('%M %S', gmtime(t2_week)).split(" ")
			message_week = "{}m {}s".format(t4[0], t4[1])
		else:
			t4 = strftime('%S', gmtime(t2_week)).split(" ")
			message_week = "{}s".format(t4[0])

	if t2_expedition > 0:
		if t2_expedition >= 3600:
			t5 = strftime('%H %M %S', gmtime(t2_expedition)).split(" ")
			message_expedition = "{}h {}m {}s".format(t5[0], t5[1], t5[2])
		elif t2_expedition >= 60:
			t5 = strftime('%M %S', gmtime(t2_expedition)).split(" ")
			message_expedition = "{}m {}s".format(t5[0], t5[1])
		else:
			t5 = strftime('%S', gmtime(t2_expedition)).split(" ")
			message_expedition = "{}s".format(t5[0])

	if t2_biome > 0:
		if t2_biome >= 3600:
			t6 = strftime('%H %M %S', gmtime(t2_biome)).split(" ")
			message_biome = "{}h {}m {}s".format(t6[0], t6[1], t6[2])
		elif t2_biome >= 60:
			t6 = strftime('%M %S', gmtime(t2_biome)).split(" ")
			message_biome = "{}m {}s".format(t6[0], t6[1])
		else:
			t6 = strftime('%S', gmtime(t2_biome)).split(" ")
			message_biome = "{}s".format(t6[0])

	url = f"https://api.top-serveurs.net/v1/votes/check?server_token={TOKEN_TOP_SERVEUR}&playername={ctx.author.display_name}"

	reponse = requests.get(url)

	if 'json' in reponse.headers.get('Content-Type'):
		js = reponse.json()
		if js["success"] == True:
			duration = js["duration"]
			if duration > 59:
				message += f"`!claim`: **1h {duration-60}m**"
			else:
				message += f"`!claim`: **{duration}m**"
		else:
			message += "`!claim`: **[prêt](https://top-serveurs.net/discord/vote/discord-of-empire)**"
	else:
		print('Response content is not in JSON format.')
		js = 'spam'

	if (t_vote - t2) < 0:
		message += "\n`!vote`: **prêt**"
	else:
		message += f"\n`!vote`: **{message_vote}**"

	if author_invitation < 5:
		message += f"\n`!week`: il vous manque **{5-author_invitation} invitations**"
	elif (t_week - t2) < 0:
		message += "\n`!week`: **prêt**"
	else:
		message += f"\n`!week`: **{message_week}**"

	if t2_expedition < 0:
		message += "\n`!expedition`: **prêt**"
	else:
		message += f"\n`!expedition`: **{message_expedition}**"

	if t2_biome < 0:
		message += "\n`!biome`: **prêt**"
	else:
		message += f"\n`!biome`: **{message_biome}**"

	embed = discord.Embed(title="**Cooldown**", description=message)

	await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='géode', aliases=["geode","Geode","Géode"], help="Cette commande te permet d'ouvrir des géode, ainsi que le "+"%"+" de chance que tu as d'avoir chaque objet à l'interieur")
@commands.cooldown(1, 2, commands.BucketType.user)
async def géode(ctx, arg1="r"):
	if not await check_if_aventurier(ctx):
		return
	member = ctx.message.author
	author_id = member.id

	result = collection.find({"_id": author_id})
	for x in result:
		author_géode = x["géode"]

	if arg1 == "r":
		embed = discord.Embed(
			title="**Géode**", description="Ouvrée une géode en faisant `!geode open`")
		embed.add_field(name="Chance:", value="Vous avez:\n**80"+"%**"+" de chance de trouver 5 Quartz\n**15"+"%**" +
		                " de chance de trouver 1 Emeraude\n**4"+"%**"+" de chance de trouver 1 Saphire\n**1"+"%**"+" de chance de trouver 1 Rubis")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg1 == "open":
		if author_géode < 1:
			return await ctx.channel.send(f"Vous n'avez pas de géode, {ctx.author.mention}")

		collection.update_one({"_id": author_id}, {"$inc": {"géode": -1}})
		result = collection.find({"_id": author_id})
		for x in result:
			author_lvl = x["niveau"]
			author_lvl_week = x["niveau_week"]
			author_lvl_month = x["niveau_month"]
			author_xp = x["xp"]
			author_xp_week = x["xp_week"]
			author_xp_month = x["xp_month"]

		rand = random()
		xp_sup = 0
		if 1 >= rand > 0.2:  # Quartz 80%
			collection.update_one({"_id": author_id}, {"$inc": {"quartz": 5}})
			await ctx.channel.send(f"Vous venez de trouver {5} quartz, {ctx.author.mention}\nVous avez aussi obtenue 5 xp")
			collection.update_one({"_id": author_id}, {"$inc": {"xp": 5}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 5}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 5}})
			xp_sup = 5
		elif 0.2 >= rand > 0.05:  # Emeraude 15%
			collection.update_one({"_id": author_id}, {"$inc": {"emerald": 1}})
			await ctx.channel.send(f"Vous venez de trouver {1} émeraude, {ctx.author.mention}\nVous avez aussi obtenue 25 xp")
			collection.update_one({"_id": author_id}, {"$inc": {"xp": 25}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 25}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 25}})
			xp_sup = 25
		elif 0.05 >= rand > 0.01:  # Saphire = 4%
			collection.update_one({"_id": author_id}, {"$inc": {"sapphire": 1}})
			await ctx.channel.send(f"Vous venez de trouver {1} saphire, {ctx.author.mention}\nVous avez aussi obtenue 100 xp")
			collection.update_one({"_id": author_id}, {"$inc": {"xp": 100}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 100}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 100}})
			xp_sup = 100
		elif 0.01 >= rand >= 0:  # Rubis = 1%
			collection.update_one({"_id": author_id}, {"$inc": {"ruby": 1}})
			await ctx.channel.send(f"Vous venez de trouver {1} rubis, {ctx.author.mention}\nVous avez aussi obtenue 400 xp")
			collection.update_one({"_id": author_id}, {"$inc": {"xp": 400}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_month": 400}})
			collection.update_one({"_id": author_id}, {"$inc": {"xp_week": 400}})
			xp_sup = 400

		collection.update_one({"_id": author_id}, {"$inc": {"!géode": 1}})

		if next_level(author_lvl, author_xp+xp_sup):
			channel_next_level = discord.utils.find(
				lambda c: c.id == channel_next_level_id, member.guild.channels)

			collection.update_one({"_id": author_id}, {"$inc": {"niveau": 1}})
			collection.update_one({"_id": author_id}, {
			                      "$inc": {"xp": -int((author_lvl**(1.5))*10)}})

			await channel_next_level.send(f"{ctx.author.mention} vient d'atteindre le niveau {author_lvl+1}, **Félicitation !**\nSaisissez la commande `!lvl` ou `!stat` pour obtenir plus d'information")
		if next_level(author_lvl_week, author_xp_week+xp_sup):
			collection.update_one({"_id": author_id}, {"$inc": {"niveau_week": 1}})
			collection.update_one({"_id": author_id}, {
			                      "$inc": {"xp_week": -int((author_lvl_week**(1.5))*10)}})
		if next_level(author_lvl_month, author_xp_month+xp_sup):
			collection.update_one({"_id": author_id}, {"$inc": {"niveau_month": 1}})
			collection.update_one({"_id": author_id}, {
			                      "$inc": {"xp_month": -int((author_lvl_month**(1.5))*10)}})


@bot.command(name='give_invitation', help="Pour le gérant du serveur")
@commands.check(check_if_it_is_me)
async def give_invitation(ctx):
	if not await check_if_aventurier(ctx):
		return
	result = collection.find({"_id": ctx.author.id})
	for x in result:
		author_id = x["_id"]
		author_potion = x["potion"]
		author_invitation = x["invite"]
	collection.update_one({"_id": author_id}, {"$inc": {"invite": 1}})
	vote = 0
	week = 0
	x2 = 0
	item = 0
	emerald = 0
	geode = 0
	hav_vote = False
	hav_week = False
	hav_x2 = False
	hav_item = False
	hav_emerald = False
	hav_geode = False
	loots = invitation_loot[str(author_invitation+1)]
	loots = loots.split("/")
	message = f"Vous avez maintenant {author_invitation} invitation, vous venez d'obtenir "
	for lot in loots:
		lot = lot.split(" ")
		if lot[1] == "vote":
			vote += int(lot[0])
			hav_vote = True
		elif lot[1] == "week":
			week += int(lot[0])
			hav_week = True
		elif lot[1] == "x2":
			x2 += int(lot[0])
			hav_x2 = True
		elif lot[1] == "item":
			item += int(lot[0])
			hav_item = True
		elif lot[1] == "unlock_week":
			pass
		elif lot[1] == "emerald":
			emerald += int(lot[0])
			hav_emerald = True
		elif lot[1] == "geode":
			geode += int(lot[0])
			hav_geode = True
	author_potion[0] += x2
	author_potion[1] += item
	author_potion[2] += vote
	author_potion[3] += week
	collection.update_one({"_id": author_id}, {"$inc": {"emerald": emerald}})
	collection.update_one({"_id": author_id}, {"$inc": {"geode": geode}})
	collection.update_one({"_id": author_id}, {"$set": {"potion": author_potion}})
	message = ""
	if hav_vote:
		message += f"{vote} `!vote` instantané, "
	if hav_week:
		message += f"{week} `!week` instantané, "
	if hav_x2:
		message += f"{x2} potion de multiplicateur de ressources, "
	if hav_item:
		message += f"{item} d'amélioration d'item, "
	if emerald:
		message += f"{emerald} emeraude, "
	if geode:
		message += f"{geode} geode, "
	await ctx.author.send(f"Vous avez reçu {message[:-2]}\nToute ces resource viennes du nombre de personne que vous invité, ce sont des ressources que vous aurez du avoir")
	await ctx.send("C'est fait chef")


@bot.command(name='inventory', aliases=["inv","inventaire","Inv","Inventaire","Inventory"], help="Cette commande te permet de voir tout ce que tu as au niveau matériaux, ainsi que tes outil, hache et pioche")
@commands.cooldown(1, 2, commands.BucketType.user)
async def inv(ctx):
	if not await check_if_aventurier(ctx):
		return

	member = ctx.message.author
	author_id = member.id
	result = collection.find({"_id": author_id})

	for x in result:
		author_wood = x["wood"]
		author_sap = x["sap"]
		author_magic_powder = x["magic_powder"]
		author_pierres = x["stone"]
		author_coal = x["coal"]
		author_fer = x["iron"]
		author_steel = x["steel"]
		author_gold = x["gold"]
		author_diamond = x["diamond"]
		author_électrum = x["électrum"]
		author_dracolite = x["dracolite"]
		author_lava = x["lava"]
		author_géode = x["géode"]
		author_quartz = x["quartz"]
		author_emerald = x["emerald"]
		author_sapphire = x["sapphire"]
		author_ruby = x["ruby"]
		author_pioche = x["pioche"]
		author_hache = x["hache"]
		author_épée = x["sword"]
	emoji_woods = discord.utils.find(
		lambda e: e.id == emoji_wood_id, member.guild.emojis)
	emoji_stone = discord.utils.find(
		lambda e: e.id == emoji_stone_id, member.guild.emojis)
	emoji_iron = discord.utils.find(
		lambda e: e.id == emoji_iron_id, member.guild.emojis)
	emoji_gold = discord.utils.find(
		lambda e: e.id == emoji_gold_id, member.guild.emojis)
	emoji_diamond = discord.utils.find(
		lambda e: e.id == emoji_diamond_id, member.guild.emojis)

	embed = discord.Embed(
		title=f"**__Inventaire de {ctx.author.display_name}__**")
	embed.add_field(name="**Objet:**",
	                value=f"__Hache__: {author_hache}\n__Pioche__: {author_pioche}\n__Epée__ : {author_épée}", inline=False)
	embed.add_field(name="**Matériaux de base:**",
	                value=f"Bois: {author_wood} {emoji_woods}\nSève: {author_sap}\nPoudre magique: {author_magic_powder}\nPierre: {author_pierres} {emoji_stone}\nFer: {author_fer} {emoji_iron}\nOr: {author_gold} {emoji_gold}\nDiamant: {author_diamond} {emoji_diamond}\nDracolite : {author_dracolite}", inline=True)
	embed.add_field(name="**Alliage/Four:**",
	                value=f"Charbon: {author_coal}\nLave: {author_lava}\nAcier : {author_steel}\nElectrum: {author_électrum}")
	embed.add_field(name="**Pierres précieuses:**",
	                value=f"Géode: {author_géode}\nQuartz: {author_quartz}\nEmeraude: {author_emerald}\nSaphire: {author_sapphire}\nRubis: {author_ruby}")

	embed.set_thumbnail(url=ctx.author.avatar_url)
	await ctx.send(f"{ctx.author.mention}", embed=embed)


"""
@bot.command(name='shop',aliases=["magasin"])
async def shop(ctx, arg="r"):
	verif = False
	for role in ctx.message.author.roles:
		if role.id == ID_ROLE_AVENTURIER:
			verif = True
	if not verif:
		return await ctx.channel.send(f"Vous devez commencé l'aventure en faisant `!start`, {ctx.author.mention}")

	author_id = ctx.author.id
	result =  collection.find({"_id":author_id})
	for x in result:
		author_mention = x["name"]
		author_wood = x["wood"]
		author_pierres = x["stone"]
		author_fer = x["iron"]
	if arg=="r":
		embed = discord.Embed(title="**__Magasin__**")
		embed.add_field(name="**Pioche:**", value = "`!shop pickaxe`", inline = True)
	elif arg == "pickaxe":
		embed = discord.Embed(title="**__Magasin de pioche__**")
		embed.add_field(name="Pioche en bois", value = "`!buy pioche`", inline = True)
		embed.add_field(name="Pioche en pierre", value = "`!upgrade pioche`", inline = True)

	await ctx.send(f"{ctx.author.mention}",embed = embed)
"""


@bot.command(name='buy', aliases=["acheter","Acheter","Buy"], help="Cette commande permet d'acheter certain item, pour conaître tout ce que vous pouvais acheter avec cette commande, faite tout simplement !buy, elle évolue en fonction de votre avancé sur le jeu")
@commands.cooldown(1, 2, commands.BucketType.user)
async def buy(ctx, arg="r"):
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_hav_pioche = x["hav_pioche"]
		author_hav_house = x["hav_house"]
		author_hav_sword = x["hav_sword"]
		author_house = x["house"]
		author_wood = x["wood"]
		author_pierres = x["stone"]
		author_fer = x["iron"]
		author_steel = x["steel"]
		author_gold = x["gold"]
		author_diamond = x["diamond"]
		author_emerald = x["emerald"]
		author_sapphire = x["sapphire"]
		author_ruby = x["ruby"]
	if arg == "r":
		embed = discord.Embed(title="**__Achat__**")
		message = ""
		if not author_hav_hache:
			message += "\n__Hache:__\n"
			message += "hache en bois: `!buy axe` [Free]\n"
		if not author_hav_pioche:
			message += "\n__Pioche:__\n"
			piocheenbois = pioche["pioche_en_bois"][1]
			message += f"pioche en bois: `!buy pickaxe [{piocheenbois}]`\n"
		if not author_hav_sword:
			message += "\n__Epée:__\n"
			épéeenacier = épée["épée_en_acier"][1]
			message += f"épée en acier: `!buy sword [{épéeenacier}]`\n"
		if author_hav_pioche:
			message += "\n__Pierre précieuse pur:__\n"
			message += "Emeraude pur: `!buy pure_emerald` [5 Emeraude]\n"
			message += "Saphire pur: `!buy pure_sapphire` [5 Saphire]\n"
			message += "Ruby pur: `!buy pure_Ruby` [5 Rubis]\n"
		embed.add_field(name="**Objet:**", value=message, inline=False)

		if not author_hav_house:
			embed.add_field(name="**Maison:**",
			                value="maison: `!buy house`", inline=False)
		else:
			embed.add_field(name="**Maison:**",
			                value="four: `!buy furnace`", inline=False)
		await ctx.send(f"{ctx.author.mention}", embed=embed)
	elif arg in ["axe", "hache"]:
		next_hache = "hache_en_bois"
		if author_hav_hache:
			return await ctx.channel.send(f"Vous avez déjà une hache, si vous voulez l'amélioré, utilisé <`!upgrade axe`>, {ctx.author.mention}")
		await ctx.author.send("T'as vu ça l'ami, elle est magnifique ma hache, hein ?" +
                        "\n\nTrès bien, maintenant tu peux récupérer du bois ! **Tape `!wood` dans une des zones de récolte pour en récolter**.")
		message = ""
		cant_buy = False
		for prix in hache[next_hache][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
		if cant_buy:
			message = message[1:]
			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_hache}**, {ctx.author.mention} !")
		for prix in hache[next_hache][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})
			elif prix[1] == "diamant":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"diamond": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$set": {"hav_hache": True}})
		collection.update_one({"_id": author_id}, {"$set": {"hache": next_hache}})
		await ctx.channel.send(f"Bien joué, l'ami {ctx.author.mention} ! Tu viens d'obtenir une magnifique **{next_hache}**, toutes mes félicitations !")
	elif arg in ["pickaxe", "pioche"]:
		next_pioche = "pioche_en_bois"
		if author_hav_pioche:
			return await ctx.channel.send(f"Vous avez déjà une pioche, si vous voulez l'amélioré, utilisé `!upgrade pickaxe`, {ctx.author.mention}")
		role_tuto = discord.utils.find(
			lambda r: r.id == ID_ROLE_TUTO, ctx.author.guild.roles)
		message = ""
		cant_buy = False
		for prix in pioche[next_pioche][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
		if cant_buy:
			message = message[1:]
			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_pioche}**, {ctx.author.mention} !")
		await ctx.author.send("C'est bon, l'ami ! Tu as tout ce qu'il faut pour récupérer les ressources primaires ! **Pour miner de la pierre, il te suffit de taper `!mine` dans une des zones de récolte** !" +
                        "\n\nAvec ces ressources, tu pourras améliorer ton équipement avec `!up` et tu pourras t'acheter une maison quand tu auras les moyens avec `!buy house` pour ainsi rejoindre une faction !" +
                        "\n\nSur ce, je te laisse tranquille l'ami, je te souhaite une merveilleuse aventure !")
		await ctx.author.remove_roles(role_tuto)
		for prix in pioche[next_pioche][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})
			elif prix[1] == "diamant":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"diamond": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$set": {"hav_pioche": True}})
		collection.update_one({"_id": author_id}, {"$set": {"pioche": next_pioche}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **{next_pioche}** félicitation !, {ctx.author.mention}")
	elif arg in ["house", "home", "maison"]:
		if author_hav_house:
			return await ctx.channel.send(f"Vous avez déjà une maison, si vous voulez l'amélioré, utilisé `!upgrade house`, {ctx.author.mention}")
		message = ""
		cant_buy = False
		for prix in maison[1][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
		if cant_buy:
			message = message[1:]
			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **maison**, {ctx.author.mention} !")
		for prix in maison[1][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})
		collection.update_one({"_id": author_id}, {"$set": {"hav_house": True}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **Maison** félicitation !,fait `!house` pour plus d'information, {ctx.author.mention}\nFait `!buy` pour voir ce que vous pouvais acheter pour votre maison")
	elif arg == "furnace":
		if not author_hav_house:
			return await ctx.channel.send(f"Vous n'avez pas de maison pour y installé de l'équipement, achetez-en une avec `!buy house`, {ctx.author.mention}")
		if author_house[2]:
			return await ctx.channel.send(f"Vous avez déjà un four, {ctx.author.mention}")
		message = ""
		cant_buy = False
		for prix in furnace_[0].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True

		if cant_buy:
			message = message[1:]
			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **four**, {ctx.author.mention} !")
		for prix in furnace_[0].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})

		author_house[2] = True
		collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})

		await ctx.channel.send(f"Vous venez d'obtenire votre **Four** félicitation !, fait `!house` pour plus d'information, {ctx.author.mention}")
	elif arg in [
            "emerald",
     	      "emeraude",
     	      "émeraude",
     	      "emeraude_pur",
     	      "émeraude_pur",
     	      "pure_emerald",
        ]:
		for prix in "5 emeraude".split("/"):
			prix = prix.split(" ")
			if prix[1] == "emeraude" and int(prix[0]) > author_emerald:
				return await ctx.channel.send(f"il vous manque `{int(prix[0])-author_emerald} d'émeraude'` pour obtenir votre émeraude pur, {ctx.author.mention}")
		for prix in "5 emeraude".split("/"):
			prix = prix.split(" ")
			if prix[1] == "emeraude":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"emerald": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$inc": {"pure_emerald": 1}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **émeraude pur** !, vous pouvez l'incrusté dans votre pioche avec `!inlaid pure_emerald`, {ctx.author.mention}")
	elif arg in ["sapphire", "saphire", "saphire_pur", "pure_sapphire"]:
		for prix in "5 saphire".split("/"):
			prix = prix.split(" ")
			if prix[1] == "saphire" and int(prix[0]) > author_sapphire:
				return await ctx.channel.send(f"il vous manque `{int(prix[0])-author_sapphire} saphire'` pour obtenir votre saphire pur, {ctx.author.mention}")
		for prix in "5 saphire".split("/"):
			prix = prix.split(" ")
			if prix[1] == "saphire":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"sapphire": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$inc": {"pure_sapphire": 1}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **saphire pur** !, vous pouvez l'incrusté dans votre pioche avec `!inlaid pure_sapphire`, {ctx.author.mention}")
	elif arg in ["ruby", "rubis", "rubis_pur", "pure_ruby"]:
		for prix in "5 rubis".split("/"):
			prix = prix.split(" ")
			if prix[1] == "rubis" and int(prix[0]) > author_ruby:
				return await ctx.channel.send(f"il vous manque `{int(prix[0])-author_ruby} rubis'` pour obtenir votre rubis pur, {ctx.author.mention}")
		for prix in "5 rubis".split("/"):
			prix = prix.split(" ")
			if prix[1] == "rubis":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"ruby": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$inc": {"pure_ruby": 1}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **rubis pur** !, vous pouvez l'incrusté dans votre pioche avec `!inlaid pure_ruby`, {ctx.author.mention}")
	elif arg in ["sword", "épée"]:
		next_épée = "épée_en_acier"
		if author_hav_sword:
			return await ctx.channel.send(f"Vous avez déjà une épée, si vous voulez l'amélioré, utilisé <`!upgrade sword`>, l'ami {ctx.author.mention} !")
		message = ""
		cant_buy = False
		for prix in épée[next_épée][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "acier" and int(prix[0]) > author_steel:
				message += f", `{int(prix[0])-author_steel} d'acier`"
				cant_buy = True
		if cant_buy:
			message = message[1:]
			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_épée}**, {ctx.author.mention} !")
		for prix in épée[next_épée][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "acier":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"steel": -int(prix[0])}})

		collection.update_one({"_id": author_id}, {"$set": {"hav_sword": True}})
		collection.update_one({"_id": author_id}, {"$set": {"sword": next_épée}})
		await ctx.channel.send(f"Bien joué, l'ami {ctx.author.mention} ! Tu viens d'obtenir une magnifique **{next_épée}**, toutes mes félicitations !")
	else:
		await ctx.channel.send(f"Votre commande n'a pas étais comprise")


@bot.command(name='upgrade', aliases=["up","Up","Upgrade"], help="Cette commande permet d'améliorer certain item, pour conaître tout ce que vous pouvais améliorer avec cette commande, faite tout simplement !upgrade, elle évolue en fonction de votre avancé sur le jeu")
@commands.cooldown(1, 2, commands.BucketType.user)
async def upgrade(ctx, arg="r"):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	author_mention = ctx.author.mention
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_hav_pioche = x["hav_pioche"]
		author_hav_sword = x["hav_sword"]
		author_wood = x["wood"]
		author_coal = x["coal"]
		author_pierres = x["stone"]
		author_fer = x["iron"]
		author_steel = x["steel"]
		author_gold = x["gold"]
		author_diamond = x["diamond"]
		author_électrum = x["électrum"]
		author_dracolite = x["dracolite"]
		author_hache = x["hache"]
		author_pioche = x["pioche"]
		author_sword = x["sword"]
		author_incrusted = x["incrusted"]
		author_incrusted_hache = x["incrusted_hache"]
	if arg == "r":
		can_pioche = False
		can_hache = False
		can_épée = False
		message = ""
		if author_hav_hache:
			next_hache = niv_hache[str(hache[author_hache][0]+1)]
			can_hache = True
			if hache[next_hache][1] == "---":
				price_axe = "---"
			else:
				price_axe = ""
				for i in hache[next_hache][1].split("/"):
					i = i.split(" ")
					price_axe += f" {i[0]} en {i[1]},"
				price_axe = price_axe[:-1]
		if author_hav_pioche:
			next_pioche = niv_pioche[str(pioche[author_pioche][0]+1)]
			can_pioche = True
			if pioche[next_pioche][1] == "---":
				price_pickaxe = "---"
			else:
				price_pickaxe = ""
				for i in pioche[next_pioche][1].split("/"):
					i = i.split(" ")
					price_pickaxe += f" {i[0]} en {i[1]},"
				price_pickaxe = price_pickaxe[:-1]
		if author_hav_sword:
			next_sword = niv_épée[str(épée[author_sword][0]+1)]
			can_épée = True
			if épée[next_sword][1] == "---":
				price_sword = "---"
			else:
				price_sword = ""
				for i in épée[next_sword][1].split("/"):
					i = i.split(" ")
					price_sword += f" {i[0]} en {i[1]},"
				price_sword = price_sword[:-1]
		if can_hache or can_pioche or can_épée:
			if can_hache:
				message += f"`!upgrade axe` pour :\nAméliorer votre **{author_hache}** en **{next_hache}**\n**Prix :** {price_axe}\n\n"
			if can_pioche:
				message += f"`!upgrade pickaxe` pour :\nAméliorer votre **{author_pioche}** en **{next_pioche}**\n**Prix :** {price_pickaxe}\n\n"
			if can_épée:
				message += f"`!upgrade sword` pour :\nAméliorer votre **{author_sword}** en **{next_sword}**\n**Prix :** {price_sword}"
			embed = discord.Embed(title="**__Upgrade__**")
			embed.add_field(name="**Niveau suivant:**", value=message, inline=True)
			await ctx.send(f"{author_mention}", embed=embed)
		else:
			await ctx.send(f"Tu n'as rien à améliorer, {author_mention}")
	elif arg == "axe" or arg == "hache":
		if not author_hav_hache:
			return await ctx.channel.send(f"Vous n'avez pas de hache, acheter en une **__Gratuitement__** avec <`!buy axe`>, {author_mention}")
		next_hache = niv_hache[str(hache[author_hache][0]+1)]

		if hache[next_hache][1] == "---":
			return await ctx.channel.send(f"Il n'y a plus d'amélioration disponible pour le moment, {author_mention}")

		if author_incrusted != "none":
			await ctx.channel.send(f"Vous avez déjà {author_incrusted_hache} incrusté dans cette hache, vous perderais votre incrustation en améliorant votre hache {author_incrusted_hache}, {author_mention} ?\nDite 'y' pour oui et 'n' pour non, pour continuer ou non l'amélioration")

			def check(message):
				return (message.author.id == ctx.message.author.id and message.channel.id == ctx.message.channel.id and (message.content == "y" or message.content == "n" or message.content == "yes" or message.content == "no"))
			try:
				confimation = await bot.wait_for("message", timeout=30, check=check)
				confimation = confimation.content
				if confimation == "n" or confimation == "no":
					return await ctx.send(f"L'oppération a bien été intérompu, {author_mention}")
			except:
				return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {author_mention}")

		message = ""
		cant_buy = False
		for prix in hache[next_hache][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
			elif prix[1] == "charbon":
				if int(prix[0]) > author_coal:
					message += f", `{int(prix[0])-author_coal} de charbon`"
					cant_buy = True
			elif prix[1] == "électrum":
				if int(prix[0]) > author_électrum:
					message += f", `{int(prix[0])-author_électrum} de électrum`"
					cant_buy = True
		if cant_buy:

			message = message[1:]

			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_hache}**, {ctx.author.mention} !")
		for prix in hache[next_hache][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})
			elif prix[1] == "diamant":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"diamond": -int(prix[0])}})
			elif prix[1] == "charbon":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"coal": -int(prix[0])}})
			elif prix[1] == "électrum":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"électrum": -int(prix[0])}})
		collection.update_one({"_id": author_id}, {"$set": {"hache": next_hache}})
		collection.update_one({"_id": author_id}, {
		                      "$set": {"incrusted_hache": "none"}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **{next_hache}** félicitation !, {author_mention}")
	elif arg == "pickaxe" or arg == "pioche":
		if not author_hav_pioche:
			return await ctx.channel.send(f"Vous n'avez pas de pioche, acheter en une avec <`!buy pickaxe`>, {author_mention}")
		next_pioche = niv_pioche[str(pioche[author_pioche][0]+1)]

		if pioche[next_pioche][1] == "---":
			return await ctx.channel.send(f"Il n'y a plus d'amélioration disponible pour le moment, {author_mention}")

		if author_incrusted != "none":
			await ctx.channel.send(f"Vous avez déjà {author_incrusted} incrusté dans cette pioche, vous perderais votre incrustation en améliorant votre pioche {author_incrusted}, {author_mention} ?\nDite 'y' pour oui et 'n' pour non, pour continuer ou non l'amélioration")

			def check(message):
				return (message.author.id == ctx.message.author.id and message.channel.id == ctx.message.channel.id and (message.content == "y" or message.content == "n" or message.content == "yes" or message.content == "no"))
			try:
				confimation = await bot.wait_for("message", timeout=30, check=check)
				confimation = confimation.content
				if confimation == "n" or confimation == "no":
					return await ctx.send(f"L'oppération a bien été intérompu, {author_mention}")
			except:
				return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {author_mention}")

		message = ""
		cant_buy = False
		for prix in pioche[next_pioche][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				if int(prix[0]) > author_wood:
					message += f", `{int(prix[0])-author_wood} de bois`"
					cant_buy = True
			elif prix[1] == "pierre":
				if int(prix[0]) > author_pierres:
					message += f", `{int(prix[0])-author_pierres} de pierre`"
					cant_buy = True
			elif prix[1] == "fer":
				if int(prix[0]) > author_fer:
					message += f", `{int(prix[0])-author_fer} de fer`"
					cant_buy = True
			elif prix[1] == "or":
				if int(prix[0]) > author_gold:
					message += f", `{int(prix[0])-author_gold} d'or`"
					cant_buy = True
			elif prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
			elif prix[1] == "charbon":
				if int(prix[0]) > author_coal:
					message += f", `{int(prix[0])-author_coal} de charbon`"
					cant_buy = True
			elif prix[1] == "électrum":
				if int(prix[0]) > author_électrum:
					message += f", `{int(prix[0])-author_électrum} de électrum`"
					cant_buy = True
			elif prix[1] == "dracolite":
				if int(prix[0]) > author_dracolite:
					message += f", `{int(prix[0])-author_dracolite} de dracolite`"
					cant_buy = True
		if cant_buy:

			message = message[1:]

			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_pioche}**, {ctx.author.mention} !")
		for prix in pioche[next_pioche][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "bois":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"wood": -int(prix[0])}})
			elif prix[1] == "pierre":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"stone": -int(prix[0])}})
			elif prix[1] == "fer":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"iron": -int(prix[0])}})
			elif prix[1] == "or":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"gold": -int(prix[0])}})
			elif prix[1] == "diamant":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"diamond": -int(prix[0])}})
			elif prix[1] == "charbon":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"coal": -int(prix[0])}})
			elif prix[1] == "électrum":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"électrum": -int(prix[0])}})
			elif prix[1] == "dracolite":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"dracolite": -int(prix[0])}})
		collection.update_one({"_id": author_id}, {"$set": {"pioche": next_pioche}})
		collection.update_one({"_id": author_id}, {"$set": {"incrusted": "none"}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **{next_pioche}** félicitation !, {author_mention}")
	elif arg == "sword" or arg == "épée":
		if not author_hav_sword:
			return await ctx.channel.send(f"Vous n'avez pas d'épée', acheter en une avec <`!buy sword`>, {author_mention}")
		next_épée = niv_épée[str(épée[author_sword][0]+1)]

		if épée[next_épée][1] == "---":
			return await ctx.channel.send(f"Il n'y a plus d'amélioration disponible pour le moment,l'ami {author_mention}")

		message = ""
		cant_buy = False
		for prix in épée[next_épée][1].split("/"):
			prix = prix.split(" ")

			if prix[1] == "diamant":
				if int(prix[0]) > author_diamond:
					message += f", `{int(prix[0])-author_diamond} de diamant`"
					cant_buy = True
			elif prix[1] == "électrum":
				if int(prix[0]) > author_électrum:
					message += f", `{int(prix[0])-author_électrum} de électrum`"
					cant_buy = True
			elif prix[1] == "acier":
				if int(prix[0]) > author_steel:
					message += f", `{int(prix[0])-author_steel} d'acier`"
					cant_buy = True
			elif prix[1] == "dracolite":
				if int(prix[0]) > author_dracolite:
					message += f", `{int(prix[0])-author_dracolite} de dracolite`"
					cant_buy = True

		if cant_buy:

			message = message[1:]

			return await ctx.channel.send(f"il vous manque {message} pour obtenir votre **{next_épée}**, {ctx.author.mention} !")
		for prix in épée[next_épée][1].split("/"):
			prix = prix.split(" ")
			if prix[1] == "acier":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"steel": -int(prix[0])}})
			elif prix[1] == "diamant":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"diamond": -int(prix[0])}})
			elif prix[1] == "dracolite":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"dracolite": -int(prix[0])}})
			elif prix[1] == "électrum":
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"électrum": -int(prix[0])}})
		collection.update_one({"_id": author_id}, {"$set": {"sword": next_épée}})
		await ctx.channel.send(f"Vous venez d'obtenire votre **{next_épée}** félicitation !, {author_mention}")
	else:
		await ctx.channel.send(f"Votre commande n'a pas étais comprise")


# @bot.command(name='item', aliases=["objet","Objet","Item"], help="Cette commande permet de connaître les spécificité de chaque item, pour conaître tout les objets consultable, faite tout simplement !item")
# @commands.cooldown(1, 2, commands.BucketType.user)
# async def item(ctx, arg="r", page=1):
# 	if not await check_if_aventurier(ctx):
# 		return

# 	author_id = ctx.author.id
# 	if arg == "r":
# 		embed = discord.Embed(
# 			title="**__Info__**", description="la commande <`!item <item>`> donne des informations sur l'item séléctioné")
# 		embed.add_field(name="**Hache:**", value="`!item axe`", inline=False)
# 		embed.add_field(name="**Pioche:**", value="`!item pickaxe`", inline=False)
# 		await ctx.send(embed=embed)
# 	elif(arg == "pickaxe" or arg == "pioche"):
# 		page = 1
# 		embed = discord.Embed(title="**__Pioche__**")
# 		message = ""
# 		for pickaxe in list(pioche.keys())[:4]:
# 			if str(pickaxe) != "soon":
# 				pickaxe_name = pickaxe
# 				price_pickaxe = ""
# 				for i in pioche[pickaxe][1].split("/"):
# 					i = i.split(" ")
# 					price_pickaxe += f" {i[0]} en {i[1]},"
# 				price_pickaxe = price_pickaxe[:-1]

# 				message += f"**{pickaxe_name}**: `Niveau : {pioche[pickaxe][0]}`, donne entre `{pioche[pickaxe][2][0]} et {pioche[pickaxe][2][1]} de pierre` "
# 				if pioche[pickaxe][3][0] != 0:
# 					message += f"et a __{pioche[pickaxe][3][0]*100}"+'%' + \
# 						f" de **chance**__ de donné `{pioche[pickaxe][3][1]} de fer` "
# 				if pioche[pickaxe][4][0] != 0:
# 					message += f"et a __{pioche[pickaxe][4][0]*100}"+'%' + \
# 						f" de **chance**__ de donné `{pioche[pickaxe][4][1]} d'or` "
# 				if pioche[pickaxe][5][0] != 0:
# 					message += f"et a __{pioche[pickaxe][5][0]*100}"+'%' + \
# 						f" de **chance**__ de donné `{pioche[pickaxe][5][1]} de diamant` "
# 				if pioche[pickaxe][6][0] != 0:
# 					message += f"et a __{pioche[pickaxe][6][0]*100}"+'%' + \
# 						f" de **chance**__ de donné `{pioche[pickaxe][6][1]} géode`"

# 				message += f"\n__Prix :__{price_pickaxe} \n\n"

# 		embed.add_field(name="Valeur :", value=message, inline=True)
# 		embed.set_footer(text="page 1/2")
# 		m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 		while True:
# 			def check(res):
# 				return ctx.author == res.user and res.channel == ctx.channel
# 			res = await bot.wait_for("button_click", check=check)
# 			action = res.component.label

# 			if page == 1:
# 				if action == "Next Page":
# 					embed = discord.Embed(title="**__Pioche__**")
# 					message = ""
# 					for pickaxe in list(pioche.keys())[4:]:
# 						if str(pickaxe) != "soon":
# 							pickaxe_name = pickaxe
# 							price_pickaxe = ""
# 							for i in pioche[pickaxe][1].split("/"):
# 								i = i.split(" ")
# 								price_pickaxe += f" {i[0]} en {i[1]},"
# 							price_pickaxe = price_pickaxe[:-1]

# 							message += f"**{pickaxe_name}**: `Niveau : {pioche[pickaxe][0]}`, donne entre `{pioche[pickaxe][2][0]} et {pioche[pickaxe][2][1]} de pierre` "
# 							if pioche[pickaxe][3][0] != 0:
# 								message += f"et a __{pioche[pickaxe][3][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][3][1]} de fer` "
# 							if pioche[pickaxe][4][0] != 0:
# 								message += f"et a __{pioche[pickaxe][4][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][4][1]} d'or` "
# 							if pioche[pickaxe][5][0] != 0:
# 								message += f"et a __{pioche[pickaxe][5][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][5][1]} de diamant` "
# 							if pioche[pickaxe][6][0] != 0:
# 								message += f"et a __{pioche[pickaxe][6][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][6][1]} géode`"

# 							message += f"\n__Prix :__{price_pickaxe} \n\n"

# 					embed.add_field(name="Valeur :", value=message, inline=True)
# 					embed.set_footer(text="page 2/2")
# 					page = 2
# 					await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 			if page == 2:
# 				if action == "Previous Page":
# 					embed = discord.Embed(title="**__Pioche__**",
# 					                      description="`!item pickaxe <optionel:page>`")
# 					message = ""
# 					for pickaxe in list(pioche.keys())[:4]:
# 						if str(pickaxe) != "soon":
# 							pickaxe_name = pickaxe
# 							price_pickaxe = ""
# 							for i in pioche[pickaxe][1].split("/"):
# 								i = i.split(" ")
# 								price_pickaxe += f" {i[0]} en {i[1]},"
# 							price_pickaxe = price_pickaxe[:-1]

# 							message += f"**{pickaxe_name}**: `Niveau : {pioche[pickaxe][0]}`, donne entre `{pioche[pickaxe][2][0]} et {pioche[pickaxe][2][1]} de pierre` "
# 							if pioche[pickaxe][3][0] != 0:
# 								message += f"et a __{pioche[pickaxe][3][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][3][1]} de fer` "
# 							if pioche[pickaxe][4][0] != 0:
# 								message += f"et a __{pioche[pickaxe][4][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][4][1]} d'or` "
# 							if pioche[pickaxe][5][0] != 0:
# 								message += f"et a __{pioche[pickaxe][5][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][5][1]} de diamant` "
# 							if pioche[pickaxe][6][0] != 0:
# 								message += f"et a __{pioche[pickaxe][6][0]*100}"+'%' + \
# 									f" de **chance**__ de donné `{pioche[pickaxe][6][1]} géode`"

# 							message += f"\n__Prix :__{price_pickaxe} \n\n"

# 					embed.add_field(name="Valeur :", value=message, inline=True)
# 					embed.set_footer(text="page 1/2")
# 					page = 1
# 					await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])

# 	'''
# 	elif (arg == "pickaxe" or arg == "pioche") and page == 2:
# 		embed = discord.Embed(title="**__Pioche__**",description="`!item pickaxe <optionel:page>`")
# 		message = ""
# 		for pickaxe in list(pioche.keys())[4:]:
# 			if str(pickaxe) != "soon":
# 				pickaxe_name = pickaxe
# 				price_pickaxe = ""
# 				for i in pioche[pickaxe][1].split("/"):
# 					i = i.split(" ")
# 					price_pickaxe += f" {i[0]} en {i[1]},"
# 				price_pickaxe=price_pickaxe[:-1]

# 				message += f"**{pickaxe_name}**: `Niveau : {pioche[pickaxe][0]}`, donne entre `{pioche[pickaxe][2][0]} et {pioche[pickaxe][2][1]} de pierre` "
# 				if pioche[pickaxe][3][0] != 0:
# 					message += f"et a __{pioche[pickaxe][3][0]*100}"+'%'+f" de **chance**__ de donné `{pioche[pickaxe][3][1]} de fer` "
# 				if pioche[pickaxe][4][0] != 0:
# 					message += f"et a __{pioche[pickaxe][4][0]*100}"+'%'+f" de **chance**__ de donné `{pioche[pickaxe][4][1]} d'or` "
# 				if pioche[pickaxe][5][0] != 0:
# 					message += f"et a __{pioche[pickaxe][5][0]*100}"+'%'+f" de **chance**__ de donné `{pioche[pickaxe][5][1]} de diamant` "
# 				if pioche[pickaxe][6][0] != 0:
# 					message += f"et a __{pioche[pickaxe][6][0]*100}"+'%'+f" de **chance**__ de donné `{pioche[pickaxe][6][1]} géode`"


# 				message += f"\n__Prix :__{price_pickaxe} \n\n"


# 		embed.add_field(name="Valeur :", value = message, inline = True)
# 		embed.set_footer(text="page 2/2")
# 		await ctx.channel.send(f"{ctx.author.mention}",embed = embed)
# 	'''
# 	if arg == "axe":
# 		embed = discord.Embed(
# 			title="**__Hache__**", description="*Vous avez **une chance sur 200** de tomber sur un arbre magique, au quel cas celui-ci vous donnera une poudre magique*")
# 		message = ""
# 		for axe in hache.keys():
# 			if axe == "soon":
# 				pass
# 			else:
# 				axe_name = axe
# 				price_axe = ""
# 				for i in hache[axe][1].split("/"):
# 					i = i.split(" ")
# 					price_axe += f" {i[0]} en {i[1]},"
# 				price_axe = price_axe[:-1]

# 				message += f"**{axe_name}**: `Niveau : {hache[axe][0]}`, donne entre `{hache[axe][2][0]} et {hache[axe][2][1]} du bois` "
# 				if hache[axe][3][0] != 0:
# 					message += f"et a __{hache[axe][3][0]*100}"+'%' + \
# 						f" de **chance**__ de donné `{hache[axe][3][1]} de sève` "
# 				message += f"\n__Prix :__{price_axe} \n\n"

# 		embed.add_field(name="Valeur :", value=message, inline=True)
# 		embed.set_footer(text="page 1/1")
# 		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
# 	if arg == "sword" or arg == "épée":
# 		embed = discord.Embed(title="**__Epée__**")
# 		message = ""
# 		for sword in épée.keys():
# 			if sword == "soon":
# 				pass
# 			else:
# 				sword_name = sword
# 				price_sword = ""
# 				for i in épée[sword][1].split("/"):
# 					i = i.split(" ")
# 					price_sword += f" {i[0]} en {i[1]},"
# 				price_sword = price_sword[:-1]

# 				message += f"**{sword_name}**: `Niveau : {épée[sword][0]}`, à __{épée[sword][2]*100} % de chance__ de tué un **petit monstre** et a __{épée[sword][3]*100}% de chance__ de tué un **gros montre**"

# 				message += f"\n__Prix :__{price_sword} \n\n"

# 		embed.add_field(name="Valeur :", value=message, inline=True)
# 		embed.set_footer(text="page 1/1")
# 		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='potion', aliases=["Potion"], help="Cette commande permet de voir et d'utiliser les potions")
@commands.cooldown(1, 5, commands.BucketType.user)
async def potion(ctx, arg="r"):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_potion = x["potion"]
		author_using_potion = x["using_potion"]
		author_cooldown_vote = x["cooldown_!vote"]
		author_cooldown_week = x["cooldown_!week"]
	if arg == "r":
		emoji_potion_rose = discord.utils.find(
			lambda c: c.id == emoji_potion_rose_id, ctx.author.guild.emojis)
		emoji_potion_rouge = discord.utils.find(
			lambda c: c.id == emoji_potion_rouge_id, ctx.author.guild.emojis)
		emoji_potion_orange = discord.utils.find(
			lambda c: c.id == emoji_potion_orange_id, ctx.author.guild.emojis)
		emoji_potion_bleu = discord.utils.find(
			lambda c: c.id == emoji_potion_bleu_id, ctx.author.guild.emojis)

		embed = discord.Embed(title="**__Potion__**",
		                      description="la commande <`!item <item>`> donne des informations sur l'item séléctioné")
		embed.add_field(name="**Vos potion :**", value=f"[{emoji_potion_rose}] - Potion de multiplicateur de ressources : {author_potion[0]}\nUtilisation : `!potion rose`\n\n[{emoji_potion_rouge}] - Potion d'amélioration des items: {author_potion[1]}\nUtilisation : `!potion rouge`\n\n[{emoji_potion_bleu}] - Potion de `!vote` instantané: {author_potion[2]}\nUtilisation : `!potion bleu`\n\n[{emoji_potion_orange}] - Potion de `!week` instantané: {author_potion[3]}\nUtilisation : `!potion orange`", inline=False)
		await ctx.send(embed=embed)
	elif arg == "rose":
		if author_potion[0] < 1:
			return await ctx.send(f"Tu n'as pas de potion de multiplicateur de ressources, l'ami {ctx.author.mention}... Tu peux aller en fabriquer une dans le laboratoire de ta faction, si tu en as une !")
		author_potion[0] -= 1

		t2 = int(time())
		t2 += 60*30

		author_using_potion[0] = t2
		collection.update_one({"_id": author_id}, {
		                      "$set": {"potion": author_potion}})
		collection.update_one({"_id": author_id}, {
		                      "$set": {"using_potion": author_using_potion}})
		await ctx.send(f"Tu as bu une potion de multiplicateur de ressources, l'ami {ctx.author.mention} ! Profites-en pendant 30 minutes !")
	elif arg == "rouge":
		if author_potion[1] < 1:
			return await ctx.send(f"Tu n'as pas de potion d'amélioration d'item, l'ami {ctx.author.mention}... Tu peux aller en fabriquer une dans le laboratoire de ta faction, si tu en as une !")
		author_potion[1] -= 1
		t2 = int(time())
		t2 += 60*30
		author_using_potion[1] = t2
		collection.update_one({"_id": author_id}, {
		                      "$set": {"potion": author_potion}})
		collection.update_one({"_id": author_id}, {
		                      "$set": {"using_potion": author_using_potion}})
		await ctx.send(f"Tu as bu une potion d'amélioration d'item, l'ami {ctx.author.mention} ! Profites-en pendant 30 minutes !")
	elif arg == "bleu":
		if author_potion[2] < 1:
			return await ctx.send(f"Tu n'as pas de potion de `!vote` instantané, l'ami {ctx.author.mention}... Tu peux aller en fabriquer une dans le laboratoire de ta faction, si tu en as une !")
		if author_cooldown_vote == 0 or (author_cooldown_vote + 60*60*12) < time():
			return await ctx.send(f"Tu peut déjà utilisé la commande `!vote`, l'ami {ctx.author.mention} !")
		author_potion[2] -= 1

		collection.update_one({"_id": author_id}, {
		                      "$set": {"potion": author_potion}})
		collection.update_one({"_id": author_id}, {"$set": {"cooldown_!vote": 0}})
		await ctx.send(f"Tu as bu une potion de `!vote` instantané, l'ami {ctx.author.mention} !")
	elif arg == "orange":
		if author_potion[3] < 1:
			return await ctx.send(f"Tu n'as pas potion de `!week` instantané, l'ami {ctx.author.mention}... Tu peux aller en fabriquer une dans le laboratoire de ta faction, si tu en as une !")
		if author_cooldown_week == 0 or (author_cooldown_week + 60*60*24*7) < time():
			return await ctx.send(f"Tu peut déjà utilisé la commande `!week`, l'ami {ctx.author.mention} !")
		author_potion[3] -= 1

		collection.update_one({"_id": author_id}, {
		                      "$set": {"potion": author_potion}})
		collection.update_one({"_id": author_id}, {"$set": {"cooldown_!week": 0}})
		await ctx.send(f"Tu as bu une potion de `!week` instantané, l'ami {ctx.author.mention} !")


@bot.command(name='axe', aliases=["hache","Hache","Axe"], help="Cette commande permet de connaître exactement combien de bois tu récupaire avec tout les bonus que tu as")
@commands.cooldown(1, 2, commands.BucketType.user)
async def axe(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_hache = x["hache"]
		author_house = x["house"][0]
		author_incruqted_hache = x["incrusted_hache"]

	if not author_hav_hache:  # vérifie si le joueur possède une hache
		return await ctx.channel.send(f"Vous n'avez pas encore d'hache, fait <!buy axe> pour en acheter **__gratuitement__** une, {ctx.author.mention}")
	embed = discord.Embed(title=f"**__Hache de {ctx.author.display_name}__**",
	                      description="*Vous avez **une chance sur 200** de tomber sur un arbre magique, au quel cas celui-ci vous donnera une poudre magique*")

	message = ""
	axe_name = author_hache
	price_axe = ""
	for i in hache[axe_name][1].split("/"):
		i = i.split(" ")
		price_axe += f" {i[0]} en {i[1]},"
	price_axe = price_axe[:-1]

	if author_house == "pas_de_faction":
		pourcentage_minerais_faction = 0
		minerais_en_plus_faction = [0, 0, 0]
	else:
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100

	author_wood = list(hache[axe_name][2])
	author_sap = list(hache[axe_name][3])

	if author_incruqted_hache != "none":
		boost_incrustation = incrustation[author_incruqted_hache][0]
		author_wood[0] *= boost_incrustation
		author_wood[1] *= boost_incrustation
		author_sap[1] *= boost_incrustation

	message += f"`Niveau : {hache[axe_name][0]}`, donne entre `{author_wood[0]} et {author_wood[1]} de bois`"

	if hache[axe_name][3][0] != 0:
		message += f" et a __{hache[axe_name][3][0]*100 + (hache[axe_name][3][0]*100)*pourcentage_minerais_faction}" + \
            '%'+f" de **chance**__ de donné `{author_sap[1]} de sève` "

	message += f"\n__Prix :__{price_axe} \n\n"

	embed.add_field(name=f"{author_hache}", value=message, inline=False)
	if author_incruqted_hache == "none" and hache[axe_name][5] == True:
		embed.add_field(name=f"Incrustation:",
		                value="Vons n'avez pas encore d'incrustion, faite `!inlaid <matériaux_pur>` pour incrusté une pierre")
	elif author_incruqted_hache == "none" and hache[axe_name][5] == False:
		embed.add_field(name=f"Incrustation:",
		                value="Vons ne pouvez pas incrusté de pierre précieuse pur sur cette pioche")
	else:
		embed.add_field(name=f"Incrustation:",
		                value=f"{author_incruqted_hache} ({incrustation[author_incruqted_hache][1]})")
	await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='pickaxe', aliases=["pioche","Pioche","Pickaxe"], help="Cette commande permet de connaître exactement combien de minerais tu récupaire avec tout les bonus que tu as")
@commands.cooldown(1, 2, commands.BucketType.user)
async def pickaxe(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_pioche = x["hav_pioche"]
		author_pioche = x["pioche"]
		author_house = x["house"][0]
		author_incrusted = x["incrusted"]

	if not author_hav_pioche:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de pioche, fait <!buy pickaxe> pour en acheter une, {ctx.author.mention}")
	embed = discord.Embed(title=f"**__Pioche de {ctx.author.display_name}__**")

	if author_pioche == "pioche_en_bois":
		embed.set_thumbnail(
			url="https://cdn.discordapp.com/attachments/859888638435000340/865358981866455070/piocheEnBois.png")
	if author_pioche == "pioche_en_pierre":
		embed.set_thumbnail(
			url="https://cdn.discordapp.com/attachments/859888638435000340/865354354360975370/piocheEnPierre.png")
	if author_pioche == "pioche_en_fer":
		embed.set_thumbnail(
			url="https://cdn.discordapp.com/attachments/859888638435000340/865358916162289680/piocheEnFer.png")
	if author_pioche == "pioche_en_or":
		embed.set_thumbnail(
			url="https://cdn.discordapp.com/attachments/859888638435000340/865364944782753832/piocheEnOr.png")
	if author_pioche == "pioche_en_diamant":
		embed.set_thumbnail(
			url="https://cdn.discordapp.com/attachments/859888638435000340/865372078144094238/PiocheEnDimant.png")

	if author_house == "pas_de_faction":
		pourcentage_minerais_faction = 0
		minerais_en_plus_faction = [0, 0, 0]
	else:
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]
	author_pierres = list(pioche[author_pioche][2])
	author_fer = list(pioche[author_pioche][3])
	author_gold = list(pioche[author_pioche][4])
	author_diamond = list(pioche[author_pioche][5])
	author_géode = list(pioche[author_pioche][6])

	if author_incrusted != "none":
		boost_incrustation = incrustation[author_incrusted][0]
		author_pierres[0] *= boost_incrustation
		author_pierres[1] *= boost_incrustation
		author_fer[1] *= boost_incrustation
		author_gold[1] *= boost_incrustation
		author_diamond[1] *= boost_incrustation
		author_géode[1] *= boost_incrustation

	message = ""
	pickaxe_name = author_pioche
	price_pickaxe = ""
	for i in pioche[pickaxe_name][1].split("/"):
		i = i.split(" ")
		price_pickaxe += f" {i[0]} en {i[1]},"
	price_pickaxe = price_pickaxe[:-1]

	all_pourcentage_fer = round(
		(author_fer[0]+author_fer[0]*pourcentage_minerais_faction)*100, 2)
	all_pourcentage_or = round(
		(author_gold[0]+author_gold[0]*pourcentage_minerais_faction)*100, 2)
	all_pourcentage_diamant = round(
		(author_diamond[0]+author_diamond[0]*pourcentage_minerais_faction)*100, 2)
	all_pourcentage_géode = round(
		(author_géode[0]+author_géode[0]*pourcentage_minerais_faction)*100, 2)

	message += f"`Niveau : {pioche[pickaxe_name][0]}`, donne entre `{author_pierres[0]} et {author_pierres[1]} de pierre` "
	if author_fer[0] != 0:
		message += f"et a __{all_pourcentage_fer}"+'%' + \
			f" de **chance**__ de donné **`{author_fer[1] + minerais_en_plus_faction[0]} de fer`** "
	if author_gold[0] != 0:
		message += f"et a __{all_pourcentage_or}"+'%' + \
			f" de **chance**__ de donné `{author_gold[1] + minerais_en_plus_faction[1]} d'or` "
	if author_diamond[0] != 0:
		message += f"et a __{all_pourcentage_diamant}"+'%' + \
			f" de **chance**__ de donné `{author_diamond[1] + minerais_en_plus_faction[2]} de diamant` "
	if author_géode[0] != 0:
		message += f"et a __{all_pourcentage_géode}"+'%' + \
			f" de **chance**__ de donné `{author_géode[1]} géode` "

	message += f"\n__Prix :__{price_pickaxe} \n\n"

	embed.add_field(name=f"{author_pioche}", value=message, inline=False)
	if author_incrusted == "none" and pioche[pickaxe_name][7] == True:
		embed.add_field(name=f"Incrustation:",
		                value="Vons n'avez pas encore d'incrustion, faite `!inlaid <matériaux_pur>` pour incrusté une pierre")
	elif author_incrusted == "none" and pioche[pickaxe_name][7] == False:
		embed.add_field(name=f"Incrustation:",
		                value="Vons ne pouvez pas incrusté de pierre précieuse pur sur cette pioche")
	else:
		embed.add_field(name=f"Incrustation:",
		                value=f"{author_incrusted} ({incrustation[author_incrusted][1]})")
	await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='sword', aliases=["épée","Epée","Sword"], help="Cette commande permet de connaître ton épée")
@commands.cooldown(1, 2, commands.BucketType.user)
async def sword(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_sword = x["hav_sword"]
		author_sword = x["sword"]

	if not author_hav_sword:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore d'épée', fait <!buy sword> pour en acheter une, l'ami {ctx.author.mention} !")

	message = ""
	sword_name = author_sword
	price_sword = ""
	for i in épée[sword_name][1].split("/"):
		i = i.split(" ")
		price_sword += f" {i[0]} en {i[1]},"
	price_sword = price_sword[:-1]

	message = ""
	message += f"`Niveau : {épée[sword_name][0]}`, à __{épée[author_sword][2]*100} % de chance__ de tué un **petit monstre** et a __{épée[author_sword][3]*100}% de chance__ de tué un **gros montre**"

	message += f"\n__Prix :__{price_sword} \n\n"
	embed = discord.Embed(
		title=f"**__Epée de {ctx.author.display_name}__**", description=message)
	await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='invitation', aliases=["invite","Invite","Invitation"], help="Cette commande te permet de connaître le nombre de personne que tu as invitée")
@commands.cooldown(1, 2, commands.BucketType.user)
async def invitation(ctx, arg="r", page=1):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_invitation = x["invite"]
	if arg == "r":
		await ctx.channel.send(f"Vous avez inviter **{author_invitation}** personne(s), {ctx.author.mention}")
	elif arg == "loot" and page == 1:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(1, 10):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="1 à 9 :", value=f"{message}")
		embed.set_footer(text="page 1/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "loot" and page == 2:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(10, 20):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="10 à 19 :", value=f"{message}")
		embed.set_footer(text="page 2/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "loot" and page == 3:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(20, 30):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="20 à 29 :", value=f"{message}")
		embed.set_footer(text="page 3/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "loot" and page == 4:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(30, 40):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="30 à 39 :", value=f"{message}")
		embed.set_footer(text="page 4/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "loot" and page == 5:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(40, 50):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="40 à 49 :", value=f"{message}")
		embed.set_footer(text="page 5/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "loot" and page == 6:
		embed = discord.Embed(title="**Invitation**",
		                      description="`!invite loot <optionel:page>`")
		message = ""
		for i in range(50, 51):
			loots = invitation_loot[str(i)]
			loots = loots.split("/")
			message += f"{i} invitation : "
			for lot in loots:
				lot = lot.split(" ")
				if lot[1] == "vote":
					message += f"{lot[0]} potion `!vote` instantané, "
				elif lot[1] == "week":
					message += f"{lot[0]} potion `!week` instantané, "
				elif lot[1] == "x2":
					message += f"{lot[0]} potion de multiplicateur de ressources, "
				elif lot[1] == "item":
					message += f"{lot[0]} potion d'amélioration d'item, "
				elif lot[1] == "unlock week":
					message += f"{lot[0]} potion vote, "
				elif lot[1] == "unlock_week":
					message += f"Vous débloqué le `!week`, "
				elif lot[1] == "emerald":
					message += f"{lot[0]} émeraude, "
				elif lot[1] == "geode":
					message += f"{lot[0]} géode, "
			message = message[:-2]
			message += "\n"
		embed.add_field(name="50 :", value=f"{message}")
		embed.set_footer(text="page 6/6")
		await ctx.channel.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='stats', aliases=["statistique", "statistiques", "stat","Statistique", "Statistiques", "Stat","Stats"], help="Cette commande te permet de voir quelque statistique sur ton compte")
@commands.cooldown(1, 2, commands.BucketType.user)
async def stat(ctx):
	verif = any(role.id == ID_ROLE_AVENTURIER for role in ctx.message.author.roles)
	if not verif:
		channel_reception = discord.utils.find(
			lambda c: c.id == channel_reception_id, ctx.author.guild.channels)
		return await ctx.channel.send(f"Tu ne peux pas commencer l'aventure sans avoir signer la charte dans {channel_reception.mention}, l'ami {ctx.author.mention} !")

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})

	for x in result:
		nb_command_wood = x["!wood"]
		nb_command_mine = x["!mine"]
		nb_command_géode = x["!géode"]
		nb_command_expedition = x["!expedition"]
		nb_bank = x["!bank"]
		author_lvl = x["niveau"]
		author_xp = x["xp"]
	on_serveur = ctx.author.joined_at.strftime("%m/%d/%Y, %H:%M:%S")
	on_serveur_ago = datetime.timestamp(ctx.author.joined_at)

	embed = discord.Embed(
		title=f"**__Statistique de {ctx.author.display_name}__**")
	embed.add_field(name=f"Niveau : {author_lvl}",
	                value=f"xp : {author_xp}/{int((author_lvl**1.5)*10)}", inline=False)
	embed.add_field(name="**Sur le serveur depuis:**",
	                value=f"{on_serveur}\n<t:{int(on_serveur_ago)}:R>", inline=False)
	message = f"`!wood` : {nb_command_wood}\n`!mine` : {nb_command_mine}\n`!géode` : {nb_command_géode}\n`!expedition` : {nb_command_expedition}\n"
	embed.add_field(name="**Command:**", value=f"{message}", inline=True)

	embed.add_field(name="**Matériaux posé à la `!bank`:**",
	                value=f"{nb_bank[0]} bois\n{nb_bank[1]} pierre\n{nb_bank[2]} fer\n{nb_bank[3]} or\n{nb_bank[4]} diamant", inline=False)
	embed.set_thumbnail(url=ctx.author.avatar_url)

	await ctx.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='command', aliases=["commande","Commande","Command"], help="Cette commande te permet de voir quelque que commande au cas ou tu en a oublié certaine")
@commands.cooldown(1, 2, commands.BucketType.user)
async def command(ctx, arg="r"):
	if not await check_if_aventurier(ctx):
		return
	if arg == "r":
		embed = discord.Embed(title=f"**Commande :**",
		                      description="**__Commande de farm__** : `!command farm`\n**__Commande générale__** : `!command générale`\n**__Commande Maison/Faction__** : `!command maison` ou `!command faction`")
	elif arg == "farm":
		embed = discord.Embed(title=f"**Commande :**", description="**__Commande de farm__**\n`!wood` : [*cooldown: 30 seconde*,*condition: avoir un hache*]Récolte du bois en fonction de votre hache (pour plus d'information faite `!axe`)\n`!mine` :[*cooldown: 1 minue*,*condition: avoir une pioche*] Récolte de la pierre et des minerais (pour plus d'information faite `!pickaxe`)\n`!geode`: Permet d'ouvre une géode (Quartz:80%/Emeraude:15%/Saphire:4%/Rubis:1%)\n`!vote`: [*cooldown : 12 heure*] Récolte instantanément 48 minute de farm (c'est beaucoup wsh)")
	elif arg == "générale" or arg == "génerale" or arg == "generale" or arg == "genérale":
		embed = discord.Embed(title=f"**Commande :**", description="**__Commande générale__**\n`!buy` : permet d'acheté l’équipement\n`!upgrade` : permet d'amélioré l’équipement\n`!inv`: Pour voir son inventaire\n`!item`: Permet de connaître les caractéristiques, d'un **item**\n`!pickaxe`: donne les caractéristique de votre pioche\n`!axe`: donne les caractéristique de votre hache")
	elif arg == "maison" or arg == "faction" or arg == "home" or arg == "house":
		embed = discord.Embed(title=f"**Commande :**", description="**__Commande Maison/Faction__**\n`!house`: Affiche votre maison\n`!furnace <nb> <materiaux>`: pour (1 charbon contre 100 bois\1 sceau de lave contre 10k pierre)\n`!faction`: permet de rejoindre une faction\n`!bank <nb> <matériau>` : permet de mettre *nb* *matériau* dans la banque votre faction avec <matériau>=b/p/f/o/d")

	#embed.set_thumbnail(url=ctx.author.avatar_url)

	await ctx.send(f"{ctx.author.mention}", embed=embed)


@bot.command(name='house', aliases=["home", "maison","Home", "Maison","House"], help="Cette commande te permet de voir ta maison, acheter une maison est indispensable pour rejoindre t'a faction")
@commands.cooldown(1, 2, commands.BucketType.user)
async def house(ctx, arg="r", arg2="nafegtr4egerme"):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_house = x["hav_house"]
		author_house = x["house"]
		author_hav_faction = x["hav_faction"]

	if not author_hav_house:
		message = ""
		for prix in maison[1][1].split("/"):
			prix = prix.split(" ")
			message += f" {prix[0]} en {prix[1]},"
		message = message[1:-1]
		return await ctx.send(f"Vous n'avez pas encore de **maison**, achetées-en une avec `!buy house`, elle vas vous coûter `{message}`,{ctx.author.mention}")
	if arg == "r":
		if not author_hav_faction:
			if author_house[1] == "name":
				embed = discord.Embed(title=f"**__Maison de {ctx.author.display_name}__**",
				                      description="Tu n'as pas encore de **Faction**, rejoins-en une avec `!faction`")
			else:
				embed = discord.Embed(
					title=f"**__Maison de {author_house[1]}__**", description="Tu n'as pas encore de **Faction**, rejoins-en une avec `!faction`")
		else:
			if author_house[1] == "name":
				embed = discord.Embed(title=f"**__Maison de {ctx.author.display_name}__**",
				                      description=f"Vous faite parti de la **{author_house[0]}**")
			else:
				embed = discord.Embed(
					title=f"**__Maison de {author_house[1]}__**", description=f"Vous faite parti de la **{author_house[0]}**")
		message = ""

		if author_house[2] == True:
			message += "Four: `!furnace`"

		if message == "":
			message = "Vous n'avez aucun equipement, vous pouvez aller en acheter au `!buy`"

		embed.add_field(name="Equipement", value=message)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "name" or arg == "nick" or arg == "nickname" or arg == "nom" or arg == "surnom":
		if arg2 != "nafegtr4egerme":
			author_house[1] = str(arg2)
			collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})
			await ctx.channel.send(f"Votre maison a été renomé : **Maison de {author_house[1]}**, {ctx.author.mention}")


@bot.command(name='faction', aliases=["Faction"], help="Cette commande te permet dans un premier temps de choisir t'as faction et dans un second de voir tout ce que tu as besoin de voir sur ta faction")
@commands.cooldown(1, 2, commands.BucketType.user)
async def faction(ctx, arg="r"):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	member = ctx.message.author
	result = collection.find({"_id": author_id})

	for x in result:
		author_mention = x["name"]
		author_hav_house = x["hav_house"]
		author_house = x["house"]
		author_hav_faction = x["hav_faction"]
	result_faction = collection_faction.find({"name": author_house[0][:-2]})

	for y in result_faction:
		nb_of_member = y["nb_of_member"]
		faction_wood = y["wood"]
		faction_stone = y["stone"]
		faction_iron = y["iron"]
		faction_gold = y["gold"]
		faction_diamond = y["diamond"]
		niveau_faction = y["niveau"]

	result_faction = collection_faction.find()
	for y in result_faction:
		if y["_id"] == 1:
			name_feu = y["name"]
			niveau_feu = y["niveau"]
			nb_of_member_feu = y["nb_of_member"]
			if y["can_join"] == True:
				join_feu = True
			else:
				join_feu = False
		elif y["_id"] == 2:
			name_eau = y["name"]
			niveau_eau = y["niveau"]
			nb_of_member_eau = y["nb_of_member"]
			if y["can_join"] == True:
				join_eau = True
			else:
				join_eau = False
		elif y["_id"] == 3:
			name_air = y["name"]
			niveau_air = y["niveau"]
			nb_of_member_air = y["nb_of_member"]
			if y["can_join"] == True:
				join_air = True
			else:
				join_air = False
		elif y["_id"] == 4:
			name_terre = y["name"]
			niveau_terre = y["niveau"]
			nb_of_member_terre = y["nb_of_member"]
			if y["can_join"] == True:
				join_terre = True
			else:
				join_terre = False

	if arg == "r":

		if not author_hav_faction:
			result_faction = collection_faction.find()
			message = ''
			for x in result_faction:
				if x["can_join"]:
					if x["_id"] == 1:
						message += " __Faction du Feu__ : rejoignez-là avec \n`!faction feu`\n\n"
					elif x["_id"] == 2:
						message += "__Faction de l'eau__ : rejoignez-là avec \n`!faction eau`\n\n"
					elif x["_id"] == 3:
						message += "__Faction de l'air__ : rejoignez-là avec \n`!faction air`\n\n"
					elif x["_id"] == 4:
						message += "__Faction de la terre__ : rejoignez-là avec \n`!faction terre`"
				else:
					if x["_id"] == 1:
						message += " __Faction du Feu__ : Cette faction à trop de joueur actif pour être rejoins\n\n"
					elif x["_id"] == 2:
						message += "__Faction de l'eau__ : Cette faction à trop de joueur actif pour être rejoins\n\n"
					elif x["_id"] == 3:
						message += "__Faction de l'air__ : Cette faction à trop de joueur actif pour être rejoins\n\n"
					elif x["_id"] == 4:
						message += "__Faction de la terre__ : Cette faction à trop de joueur actif pour être rejoins\n\n"
			embed = discord.Embed(title=f"**__Faction__**")

			embed.add_field(
				name="Vous avez à disposition **quatre** faction :", value=message, inline=True)

			await ctx.send(f"{ctx.author.mention}", embed=embed)
		else:
			wood, stone, iron, gold, diamond = faction_[
				str(int(niveau_faction)+1)].split("/")
			wood = wood.split(" ")[0]
			stone = stone.split(" ")[0]
			iron = iron.split(" ")[0]
			gold = gold.split(" ")[0]
			diamond = diamond.split(" ")[0]

			if author_house[0] == "Faction du Feu":
				embed = discord.Embed(
					title=f"**__{author_house[0]}__**", colour=discord.Colour.from_rgb(192, 23, 23))
				embed.set_thumbnail(
					url="https://cdn.discordapp.com/attachments/859035096567644160/859805956468506675/BlasonFactionFeu.png")
			elif author_house[0] == "Faction de l'Eau":
				embed = discord.Embed(
					title=f"**__{author_house[0]}__**", colour=discord.Colour.from_rgb(24, 98, 228))
				embed.set_thumbnail(
					url="https://cdn.discordapp.com/attachments/859035096567644160/859807015392378922/BlasonFactionEau.png")
			elif author_house[0] == "Faction de l'Air":
				embed = discord.Embed(
					title=f"**__{author_house[0]}__**", colour=discord.Colour.from_rgb(24, 222, 228))
				embed.set_thumbnail(
					url="https://cdn.discordapp.com/attachments/859035096567644160/859807598920204328/BlasonFactionAir.png")
			elif author_house[0] == "Faction de la Terre":
				embed = discord.Embed(
					title=f"**__{author_house[0]}__**", colour=discord.Colour.from_rgb(230, 140, 17))
				embed.set_thumbnail(
					url="https://cdn.discordapp.com/attachments/859035096567644160/859808442302464020/BlasonFactionTerre.png")
			else:
				embed = discord.Embed(title=f"**__{author_house[0]}__**")

			embed.add_field(name="**Utile :**",
			                value=f"Niveau: {niveau_faction}\nNombre de membre: {nb_of_member}", inline=False)
			embed.add_field(name="**Banque:**",
			                value=f"Bois: {faction_wood}/{wood}\nPierre: {faction_stone}/{stone}\nFer: {faction_iron}/{iron}\nOr: {faction_gold}/{gold}\nDiamant: {faction_diamond}/{diamond}", inline=True)
			embed.add_field(name="**Amélioration:**",
			                value=f"**+10%/Niveau** sur le pourcentage de chaque minerais\nNiveau 1: -\nNiveau 2: -\nNiveau 3: -\nNiveau 4: -\nNiveau 5: -")

			await ctx.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "stat":
		result_faction = collection_faction.find()
		embed = discord.Embed(title=f"**__Faction__**",
		                      description=f"__{name_feu}__ :\nNiveau : **{niveau_feu}**\nMembre : {nb_of_member_feu}\n\n__{name_eau}__ :\nNiveau : **{niveau_eau}**\nMembre : {nb_of_member_eau}\n\n__{name_air}__ :\nNiveau : **{niveau_air}**\nMembre : {nb_of_member_air}\n\n__{name_terre}__ :\nNiveau : **{niveau_terre}**\nMembre : {nb_of_member_terre}\n\n")

		await ctx.send(f"{ctx.author.mention}", embed=embed)
	elif arg == "feu" and author_hav_house:
		if author_hav_faction:
			return await ctx.send(f"Vous avez déjà une faction, {ctx.author.mention}")
		if not join_feu:
			return await ctx.send(f"Cette faction est trop importante pour être rejoins, pour équilibrer les faction, nous vous demandons d'en choisire une autre, l'ami {ctx.author.mention}")

		role_feu = discord.utils.find(
			lambda r: r.id == ID_ROLE_FAC_FEU, member.guild.roles)
		channel_bienvenue_feu = discord.utils.find(
			lambda c: c.id == channel_bienvenue_feu_id, member.guild.channels)

		author_house[0] = role_feu.name

		collection.update_one({"_id": author_id}, {"$set": {"hav_faction": True}})
		collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})
		collection_faction.update_one({"_id": 1}, {"$inc": {"nb_of_member": 1}})

		await member.add_roles(role_feu)
		await ctx.channel.send(f"Vous venez de rejoindre la **{role_feu.name}**, {ctx.author.mention}")
		await channel_bienvenue_feu.send(f"{ctx.author.mention}, viens de rejoindre la **{role_feu.name}**, souhaitez lui la bienvenue")
	elif arg == "eau" and author_hav_house:
		if author_hav_faction:
			return await ctx.send(f"Vous avez déjà une faction, {ctx.author.mention}")
		if not join_eau:
			return await ctx.send(f"Cette faction est trop importante pour être rejoins, pour équilibrer les faction, nous vous demandons d'en choisire une autre, l'ami {ctx.author.mention}")

		role_eau = discord.utils.find(
			lambda r: r.id == ID_ROLE_FAC_EAU, member.guild.roles)
		channel_bienvenue_eau = discord.utils.find(
			lambda c: c.id == channel_bienvenue_eau_id, member.guild.channels)

		author_house[0] = role_eau.name

		collection.update_one({"_id": author_id}, {"$set": {"hav_faction": True}})
		collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})
		collection_faction.update_one({"_id": 2}, {"$inc": {"nb_of_member": 1}})

		await member.add_roles(role_eau)
		await ctx.channel.send(f"Vous venez de rejoindre la **{role_eau.name}**, {ctx.author.mention}")
		await channel_bienvenue_eau.send(f"{ctx.author.mention}, viens de rejoindre la **{role_eau.name}**, souhaitez lui la bienvenue")
	elif arg == "air" and author_hav_house:
		if author_hav_faction:
			return await ctx.send(f"Vous avez déjà une faction, {ctx.author.mention}")
		if not join_air:
			return await ctx.send(f"Cette faction est trop importante pour être rejoins, pour équilibrer les faction, nous vous demandons d'en choisire une autre, l'ami {ctx.author.mention}")

		role_air = discord.utils.find(
			lambda r: r.id == ID_ROLE_FAC_AIR, member.guild.roles)
		channel_bienvenue_air = discord.utils.find(
			lambda c: c.id == channel_bienvenue_air_id, member.guild.channels)

		author_house[0] = role_air.name

		collection.update_one({"_id": author_id}, {"$set": {"hav_faction": True}})
		collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})
		collection_faction.update_one({"_id": 3}, {"$inc": {"nb_of_member": 1}})

		await member.add_roles(role_air)
		await ctx.channel.send(f"Vous venez de rejoindre la **{role_air.name}**, {ctx.author.mention}")
		await channel_bienvenue_air.send(f"{ctx.author.mention}, viens de rejoindre la **{role_air.name}**, souhaitez lui la bienvenue")
	elif arg == "terre" and author_hav_house:
		if author_hav_faction:
			return await ctx.send(f"Vous avez déjà une faction, {ctx.author.mention}")
		if not join_terre:
			return await ctx.send(f"Cette faction est trop importante pour être rejoins, pour équilibrer les faction, nous vous demandons d'en choisire une autre, l'ami {ctx.author.mention}")

		role_terre = discord.utils.find(
			lambda r: r.id == ID_ROLE_FAC_TERRE, member.guild.roles)
		channel_bienvenue_terre = discord.utils.find(
			lambda c: c.id == channel_bienvenue_terre_id, member.guild.channels)

		author_house[0] = role_terre.name

		collection.update_one({"_id": author_id}, {"$set": {"hav_faction": True}})
		collection.update_one({"_id": author_id}, {"$set": {"house": author_house}})
		collection_faction.update_one({"_id": 4}, {"$inc": {"nb_of_member": 1}})

		await member.add_roles(role_terre)
		await ctx.channel.send(f"Vous venez de rejoindre la **{role_terre.name}**, {ctx.author.mention}")
		await channel_bienvenue_terre.send(f"{ctx.author.mention}, viens de rejoindre la **{role_terre.name}**, souhaitez lui la bienvenue")


@bot.command(name='bank', aliases=["banque","Banque","Bank"], help="Cette commande te permet de déposé des matériaux à a banque de ta faction, quand votre faction a remplie la banque, alors la faction passe au niveau supérieur")
@commands.cooldown(1, 2, commands.BucketType.user)
async def bank(ctx, nb=1, matériaux="r"):
	if not await check_if_aventurier(ctx):
		return
	if nb < 0:
		return await ctx.channel.send(f"Vous devez mettre un nombre positif dans la commande !bank <nb> <matériaux>, {ctx.author.mention}")
	author_id = ctx.author.id
	member = ctx.message.author
	result = collection.find({"_id": author_id})

	for x in result:
		author_wood = x["wood"]
		author_pierres = x["stone"]
		author_fer = x["iron"]
		author_gold = x["gold"]
		author_diamond = x["diamond"]
		author_hav_house = x["hav_house"]
		author_house = x["house"]
		author_hav_faction = x["hav_faction"]
		author_bank = x["!bank"]
	result_faction = collection_faction.find({"name": author_house[0][:-2]})
	for y in result_faction:
		_id = y["_id"]
		nb_of_member = y["nb_of_member"]
		faction_wood = y["wood"]
		faction_stone = y["stone"]
		faction_iron = y["iron"]
		faction_gold = y["gold"]
		niveau_faction = y["niveau"]

	if not author_hav_house:
		return await ctx.send(f"Vous n'avez pas encore de maison pour rejoindre une faction, faite `!buy house`, {ctx.author.mention}")
	if not author_hav_faction:
		return await ctx.send(f"Vous n'avez pas encore de  faction, faite `!faction` pour en rejoindre une, {ctx.author.mention}")

	if matériaux == "r" and nb == 1:
		embed = discord.Embed(title="**Banque de la faction:**")
		embed.add_field(
			name=f"Bois: {faction_wood}\nPierre: {faction_stone}\nFer: {faction_iron}\nOr: {faction_gold}", value="`!bank <nb> <matériaux>`")
		await ctx.send(f"{ctx.author.mention}", embed=embed)

	elif matériaux == "b" or matériaux == "bois" or matériaux == "w" or matériaux == "wood":
		if int(nb) > author_wood:
			return await ctx.channel.send(f"il vous manque `{int(nb)-author_wood} de bois` pour faire ce virement, {ctx.author.mention}")
		collection.update_one({"_id": author_id}, {"$inc": {"wood": -int(nb)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"wood": int(nb)}})
		author_bank[0] += int(nb)
		collection.update_one({"_id": author_id}, {"$set": {"!bank": author_bank}})
		await ctx.channel.send(f"Vous avez donné {nb} de bois à la banque de votre faction, {ctx.author.mention}")
	elif matériaux == "p" or matériaux == "pierre" or matériaux == "s" or matériaux == "stone":
		if int(nb) > author_pierres:
			return await ctx.channel.send(f"il vous manque `{int(nb)-author_pierres} de pierre` pour faire ce virement, {ctx.author.mention}")
		collection.update_one({"_id": author_id}, {"$inc": {"stone": -int(nb)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"stone": int(nb)}})
		author_bank[1] += int(nb)
		collection.update_one({"_id": author_id}, {"$set": {"!bank": author_bank}})
		await ctx.channel.send(f"Vous avez donné {nb} de pierre à la banque de votre faction, {ctx.author.mention}")
	elif matériaux == "f" or matériaux == "fer" or matériaux == "i" or matériaux == "iron":
		if int(nb) > author_fer:
			return await ctx.channel.send(f"il vous manque `{int(nb)-author_fer} de fer` pour faire ce virement, {ctx.author.mention}")
		collection.update_one({"_id": author_id}, {"$inc": {"iron": -int(nb)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"iron": int(nb)}})
		author_bank[2] += int(nb)
		collection.update_one({"_id": author_id}, {"$set": {"!bank": author_bank}})
		await ctx.channel.send(f"Vous avez donné {nb} de fer à la banque de votre faction, {ctx.author.mention}")
	elif matériaux == "o" or matériaux == "or" or matériaux == "g" or matériaux == "gold":
		if int(nb) > author_gold:
			return await ctx.channel.send(f"il vous manque `{int(nb)-author_gold} d'or` pour faire ce virement, {ctx.author.mention}")
		collection.update_one({"_id": author_id}, {"$inc": {"gold": -int(nb)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"gold": int(nb)}})
		author_bank[3] += int(nb)
		collection.update_one({"_id": author_id}, {"$set": {"!bank": author_bank}})
		await ctx.channel.send(f"Vous avez donné {nb} d'or à la banque de votre faction, {ctx.author.mention}")
	elif matériaux == "d" or matériaux == "diamant" or matériaux == "diamond":
		if int(nb) > author_diamond:
			return await ctx.channel.send(f"il vous manque `{int(nb)-author_diamond} de diamant` pour faire ce virement, {ctx.author.mention}")
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": -int(nb)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"diamond": int(nb)}})
		author_bank[4] += int(nb)
		collection.update_one({"_id": author_id}, {"$set": {"!bank": author_bank}})
		await ctx.channel.send(f"Vous avez donné {nb} de diamant à la banque de votre faction, {ctx.author.mention}")
	else:
		return await ctx.channel.send(f"Votre commande n'a pas étais comprise, faite `!bank <nb> <matériaux>` avec <matériaux>=b/p/f, {ctx.author.mention}")
	result_faction = collection_faction.find({"name": author_house[0][:-2]})
	for y in result_faction:
		_id = y["_id"]
		faction_wood = y["wood"]
		faction_stone = y["stone"]
		faction_iron = y["iron"]
		faction_gold = y["gold"]
		faction_diamond = y["diamond"]
		niveau_faction = y["niveau"]
	wood, stone, iron, gold, diamond = faction_[str(niveau_faction+1)].split("/")
	wood = int(wood.split(" ")[0])
	stone = int(stone.split(" ")[0])
	iron = int(iron.split(" ")[0])
	gold = int(gold.split(" ")[0])
	diamond = int(diamond.split(" ")[0])

	role_feu = discord.utils.find(
		lambda r: r.id == ID_ROLE_FAC_FEU, member.guild.roles)
	role_eau = discord.utils.find(
		lambda r: r.id == ID_ROLE_FAC_EAU, member.guild.roles)
	role_air = discord.utils.find(
		lambda r: r.id == ID_ROLE_FAC_AIR, member.guild.roles)
	role_terre = discord.utils.find(
		lambda r: r.id == ID_ROLE_FAC_TERRE, member.guild.roles)
	if faction_wood >= wood and faction_stone >= stone and faction_iron >= iron and faction_gold >= gold and faction_diamond >= diamond:

		collection_faction.update_one({"_id": _id}, {"$inc": {"wood": -int(wood)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"stone": -int(stone)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"iron": -int(iron)}})
		collection_faction.update_one({"_id": _id}, {"$inc": {"gold": -int(gold)}})
		collection_faction.update_one(
			{"_id": _id}, {"$inc": {"diamond": -int(diamond)}})

		collection_faction.update_one({"_id": _id}, {"$inc": {"niveau": 1}})

		collection_faction.update_one({"_id": _id}, {"$inc": {"+% minerais": 10}})
		if author_house[0] == role_feu.name:
			chat_générale_feu = discord.utils.find(
				lambda c: c.id == chat_générale_feu_id, member.guild.channels)
			await chat_générale_feu.send(f"Bravo à tous, {role_feu.mention}, votre Faction a atteint le niveau {niveau_faction+1}")
		if author_house[0] == role_eau.name:
			chat_générale_eau = discord.utils.find(
				lambda c: c.id == chat_générale_eau_id, member.guild.channels)
			await chat_générale_eau.send(f"Bravo à tous, {role_eau.mention}, votre Faction a atteint le niveau {niveau_faction+1}")
		if author_house[0] == role_air.name:
			chat_générale_air = discord.utils.find(
				lambda c: c.id == chat_générale_air_id, member.guild.channels)
			await chat_générale_air.send(f"Bravo à tous, {role_air.mention}, votre Faction a atteint le niveau {niveau_faction+1}")
		if author_house[0] == role_terre.name:
			chat_générale_terre = discord.utils.find(
				lambda c: c.id == chat_générale_terre_id, member.guild.channels)
			await chat_générale_terre.send(f"Bravo à tous, {role_terre.mention}, votre Faction a atteint le niveau {niveau_faction+1}")


@bot.command(name='furnace', aliases=["smelt","four","Smelt","Four","Furnace"], help="Cette commande te permet d'échangé certain matériaux contre d'autre, il est achetable dans le !buy quand vous avais acquis une maison")
@commands.cooldown(1, 2, commands.BucketType.user)
async def furnace(ctx, nb=1, matériaux="r"):
	if not await check_if_aventurier(ctx):
		return
	if nb < 0:
		return await ctx.channel.send(f"Vous devez mettre un nombre positif dans la commande !bank <nb> <matériaux>, {ctx.author.mention}")

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})

	for x in result:
		author_wood = x["wood"]
		author_pierres = x["stone"]
		author_fer = x["iron"]
		author_coal = x["coal"]
		author_gold = x["gold"]
		author_lava = x["lava"]
		author_hav_house = x["hav_house"]
		author_house = x["house"]

	if not author_hav_house:
		return await ctx.send(f"Vous n'avez pas encore de maison pour faire cuire/fondre des objets, faite `!buy house`, {ctx.author.mention}")
	if not author_house[2]:
		return await ctx.send(f"Vous n'avez pas encore de four pour faire cuire/fondre des objets, faite `!buy furnace`, {ctx.author.mention}")

	if matériaux == "r" and nb == 1:
		embed = discord.Embed(
			title="**Four**", description="`!furnace <nb> <matériaux>`\n*__Exemple__ : `!furnace 10 coal` va vous donné 10 charbon contre 1k de bois*")
		embed.add_field(name=f"Objets", value="100 bois --> 1 charbon\n10k pierre --> 1 sceau de lave\n400 fer,50 or et 2 sceau de lave --> 1 électrum\n150 fer,150 charbon et 1 sceau de lave --> 10 acier")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(f"{ctx.author.mention}", embed=embed)

	elif matériaux in ["coal", "charbon"]:
		if int(nb*100) > author_wood:
			return await ctx.channel.send(f"il vous manque `{int(nb*100)-author_wood} de bois` pour faire {int(nb)} charbon, {ctx.author.mention}")

		collection.update_one({"_id": author_id}, {"$inc": {"wood": -int(nb*100)}})
		collection.update_one({"_id": author_id}, {"$inc": {"coal": int(nb)}})

		await ctx.channel.send(f"Vous avez d'obtenir {nb} charbon, {ctx.author.mention}")
	elif matériaux in ["lava", "lave"]:
		if int(nb*10000) > author_pierres:
			return await ctx.channel.send(f"il vous manque `{int(nb*10000)-author_pierres} de pierre` pour faire {int(nb)} sceau de lave, {ctx.author.mention}")

		collection.update_one({"_id": author_id}, {
		                      "$inc": {"stone": -int(nb*10000)}})
		collection.update_one({"_id": author_id}, {"$inc": {"lava": int(nb)}})

		await ctx.channel.send(f"Vous avez d'obtenir {nb} sceau de lave, {ctx.author.mention}")
	elif matériaux in ["électrum", "electrum"]:
		if int(nb*50) > author_gold:
			return await ctx.channel.send(f"il vous manque `{int(nb*50)-author_gold} de'or` pour faire {int(nb)} électrum, {ctx.author.mention}")
		if int(nb*400) > author_fer:
			return await ctx.channel.send(f"il vous manque `{int(nb*400)-author_fer} de fer` pour faire {int(nb)} électrum, {ctx.author.mention}")
		if int(nb*2) > author_lava:
			return await ctx.channel.send(f"il vous manque `{int(nb*2)-author_lava} de lave` pour faire {int(nb)} électrum, {ctx.author.mention}")

		collection.update_one({"_id": author_id}, {"$inc": {"iron": -int(nb*400)}})
		collection.update_one({"_id": author_id}, {"$inc": {"gold": -int(nb*50)}})
		collection.update_one({"_id": author_id}, {"$inc": {"lava": -int(nb*2)}})
		collection.update_one({"_id": author_id}, {"$inc": {"électrum": int(nb)}})

		await ctx.channel.send(f"Vous venez d'obtenir {nb} **électrum**, {ctx.author.mention}")
	elif matériaux in ["acier", "steel"]:
		if nb % 10 != 0:
			return await ctx.channel.send(f"Le nombre donné doit être un multiple de 10 quand vous chauffé de l'acier")
		nb = nb//10
		if int(nb*150) > author_coal:
			return await ctx.channel.send(f"il vous manque `{int(nb*150)-author_coal} de charbon'` pour faire {int(nb*10)} acier, {ctx.author.mention}")
		if int(nb*150) > author_fer:
			return await ctx.channel.send(f"il vous manque `{int(nb*150)-author_fer} de fer` pour faire {int(nb*10)} acier, {ctx.author.mention}")
		if int(nb*1) > author_lava:
			return await ctx.channel.send(f"il vous manque `{int(nb*1)-author_lava} de lave` pour faire {int(nb*10)} acier, {ctx.author.mention}")

		collection.update_one({"_id": author_id}, {"$inc": {"iron": -int(nb*150)}})
		collection.update_one({"_id": author_id}, {"$inc": {"coal": -int(nb*150)}})
		collection.update_one({"_id": author_id}, {"$inc": {"lava": -int(nb*1)}})
		collection.update_one({"_id": author_id}, {"$inc": {"steel": int(nb*10)}})

		await ctx.channel.send(f"Vous avez d'obtenir {nb*10} **acier**, {ctx.author.mention}")

	else:
		return await ctx.channel.send(f"Votre commande n'a pas étais comprise, faite `!furnace <nb> <matériaux>` avec <matériaux>=coal/lava/électrum, {ctx.author.mention}")


@bot.command(name='inlaid', aliases=["incrusté","incruste","incruster","Incrusté","Incruste","Incruster","Inlaid"], help="Cette commande te permet d'incrusté des pierres précieuses pur dans ta pioche, mais attention, changé de pioche fait dispaitre la pierre précieuse pur'")
@commands.cooldown(1, 2, commands.BucketType.user)
async def inlaid(ctx, matériaux="r"):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})

	for x in result:
		author_hav_pioche = x["hav_pioche"]

	if not author_hav_pioche:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de pioche pour y incrusté de **pierres précieuse pur**, fait <!buy pickaxe> pour en acheter une, {ctx.author.mention}")
	result = collection.find({"_id": author_id})
	for x in result:
		author_pure_emerald = x["pure_emerald"]
		author_pure_sapphire = x["pure_sapphire"]
		author_pure_ruby = x["pure_ruby"]
		author_incrusted = x["incrusted"]
		author_incrusted_hache = x["incrusted_hache"]
		author_pioche = x["pioche"]
		author_hache = x["hache"]
		author_can_incrsted = pioche[author_pioche][7]
	if matériaux == "r":
		embed = discord.Embed(title="**Incrustation**",
		                      description="`!inlaid <pur_matériaux>`\n*__Exemple__ : `!inlaid pur_emeraude` va vous incrusté la pierre dans votre pioche pour doublé ces stats*")
		embed.add_field(name=f"Vos pierre précieuse pur",
		                value=f"**Emeraude pur**: {author_pure_emerald}, *si incrusté : x2 sur toute récupération de minerais*\n**Saphire pur**: {author_pure_sapphire}, si incrusté : *x3 sur toute récupération de minerais*\n**Rubis pur**: {author_pure_ruby}, *si incrusté : x5 sur toute récupération de minerais*")
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(f"{ctx.author.mention}", embed=embed)

	elif matériaux == "emeraude_pur" or matériaux == "pure_emerald" or matériaux == "emeraude_pure" or matériaux == "pur_emerald":
		if not author_can_incrsted:
			return await ctx.send(f"Votre pioche ne peut pas être incrusté, {ctx.author.mention}")
		elif author_pure_emerald < 1:
			return await ctx.send(f"Votre n'avez pas d'Emeraude pur, {ctx.author.mention}")
		await ctx.channel.send(f"Pour incruster la pioche tapez 'pioche', pour incruster la hache tapez 'hache', {ctx.author.mention}")

		def check(message):
			return (message.author.id == ctx.message.author.id
			        and message.channel.id == ctx.message.channel.id
			        and message.content in ["hache", "pioche", "axe", "pickaxe"])
		try:
			confimation = await bot.wait_for("message", timeout=30, check=check)
			confimation = confimation.content
			if confimation == "hache" or confimation == "axe":
				if author_incrusted_hache != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted_hache} incrusté dans cette hache, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted_hache}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id and message.channel.id == ctx.message.channel.id and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_emerald": -1}})
				collection.update_one({"_id": author_id}, {
				                      "$set": {"incrusted_hache": "pure_emerald"}})
				await ctx.send(f"Vous venez d'incrusté un **Emeraude pur** dans votre {author_hache}, {ctx.author.mention}")
			elif confimation == "pioche" or confimation == "pickaxe":
				if author_incrusted != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted} incrusté dans cette pioche, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id
						        and message.channel.id == ctx.message.channel.id
						        and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_emerald": -1}})
				collection.update_one({"_id": author_id}, {
					                      "$set": {"incrusted": "pure_emerald"}})
				await ctx.send(f"Vous venez d'incrusté un **Emeraude pur** dans votre {author_pioche}, {ctx.author.mention}")
		except:
			return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
	elif matériaux == "saphire_pur" or matériaux == "pure_sapphire" or matériaux == "saphire_pure" or matériaux == "pur_sapphire":
		if not author_can_incrsted:
			return await ctx.send(f"Votre pioche ne peut pas être incrusté, {ctx.author.mention}")
		elif author_pure_sapphire < 1:
			return await ctx.send(f"Votre n'avez pas de Saphir pur, {ctx.author.mention}")
		await ctx.channel.send(f"Pour incruster la pioche tapez 'pioche', pour incruster la hache tapez 'hache', {ctx.author.mention}")

		def check(message):
			return (message.author.id == ctx.message.author.id
			        and message.channel.id == ctx.message.channel.id
			        and message.content in ["hache", "pioche", "axe", "pickaxe"])
		try:
			confimation = await bot.wait_for("message", timeout=30, check=check)
			confimation = confimation.content
			if confimation == "hache" or confimation == "axe":
				if author_incrusted_hache != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted_hache} incrusté dans cette hache, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted_hache}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id
                                            and message.channel.id == ctx.message.channel.id
                                            and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_sapphire": -1}})
				collection.update_one({"_id": author_id}, {
				                      "$set": {"incrusted_hache": "pure_sapphire"}})
				await ctx.send(f"Vous venez d'incrusté un **Saphir pur** dans votre {author_hache}, {ctx.author.mention}")
			elif confimation == "pioche" or confimation == "pickaxe":
				if author_incrusted != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted} incrusté dans cette pioche, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id
                                            and message.channel.id == ctx.message.channel.id
                                            and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_sapphire": -1}})
				collection.update_one({"_id": author_id}, {
				                      "$set": {"incrusted": "pure_sapphire"}})
				await ctx.send(f"Vous venez d'incrusté un **Saphir pur** dans votre {author_pioche}, {ctx.author.mention}")
		except:
			return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
	elif matériaux == "rubis_pur" or matériaux == "pure_ruby" or matériaux == "rubis_pure" or matériaux == "pur_ruby":
		if not author_can_incrsted:
			return await ctx.send(f"Votre pioche ne peut pas être incrusté, {ctx.author.mention}")
		elif author_pure_ruby < 1:
			return await ctx.send(f"Votre n'avez pas de Rubis pur, {ctx.author.mention}")
		await ctx.channel.send(f"Pour incruster la pioche tapez 'pioche', pour incruster la hache tapez 'hache', {ctx.author.mention}")

		def check(message):
			return (message.author.id == ctx.message.author.id
			        and message.channel.id == ctx.message.channel.id
			        and message.content in ["hache", "pioche", "axe", "pickaxe"])
		try:
			confimation = await bot.wait_for("message", timeout=30, check=check)
			confimation = confimation.content
			if confimation == "hache" or confimation == "axe":
				if author_incrusted_hache != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted_hache} incrusté dans cette hache, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted_hache}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id
                                            and message.channel.id == ctx.message.channel.id
                                            and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_ruby": -1}})
				collection.update_one({"_id": author_id}, {
				                      "$set": {"incrusted_hache": "pure_ruby"}})
				await ctx.send(f"Vous venez d'incrusté un **Rubis pur** dans votre {author_hache}, {ctx.author.mention}")
			elif confimation == "pioche" or confimation == "pickaxe":
				if author_incrusted != "none":
					await ctx.channel.send(f"Vous avez déjà {author_incrusted} incrusté dans cette pioche, êtes vous sur de vouloir continué et de remplacé cette {author_incrusted}, {ctx.author.mention} ?\nDite 'y' pour oui et 'n' pour non")

					def check(message):
						return (message.author.id == ctx.message.author.id
                                            and message.channel.id == ctx.message.channel.id
                                            and message.content in ["y", "n", "yes", "no"])
					try:
						confimation = await bot.wait_for("message", timeout=30, check=check)
						confimation = confimation.content
						if confimation == "n" or confimation == "no":
							return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
					except:
						return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")
				collection.update_one({"_id": author_id}, {"$inc": {"pure_ruby": -1}})
				collection.update_one({"_id": author_id}, {
				                      "$set": {"incrusted": "pure_ruby"}})
				await ctx.send(f"Vous venez d'incrusté un **Rubis pur** dans votre {author_pioche}, {ctx.author.mention}")
		except:
			return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")


# 4 fois !mine
@bot.command(name='hour', aliases=["h", "heure","H", "Heure","Hour"], enabled=False)
@commands.cooldown(1, 3600, commands.BucketType.user)
async def hour(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_pioche = x["hav_pioche"]
		nb_invitation = x["invite"]
		author_house = x["house"][0]

	if nb_invitation < 1:
		return await ctx.channel.send(f"Pour utilisé la commande, <`!hour`>, vous devez inviter une personne sur le serveur, pour connaître le nombre de personne que vous avez inviter faite <!invitation>, {ctx.author.mention}")

	if not author_hav_hache:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de hache,, pour acheté une pioche faite `!buy axe`, {ctx.author.mention}")

	if not author_pioche:  # vérifie si le joueur possède une pioche
		await ctx.channel.send(f"Vous n'avez pas encore de pioche, donc le `!mine` n'a pas étais ajouté, pour acheté une pioche faite `!buy pickaxe`, {ctx.author.mention}")

	result = collection.find({"_id": author_id})
	for x in result:
		#"Pioche":[niveau,prix,(pierre_min,pierre_max),%fer]
		author_wood = hache[x["hache"]][2]
		author_pierres = pioche[x["pioche"]][2]
		author_fer = pioche[x["pioche"]][3]
		author_gold = pioche[x["pioche"]][4]
		author_diamond = pioche[x["pioche"]][5]
		author_géode = pioche[x["pioche"]][6]

	if author_house != "pas_de_faction":
		pourcentage_minerais_faction = 0
		minerais_en_plus_faction = [0, 0, 0]
	else:
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	wood = 0
	stone = 0
	hav_iron = False
	iron = 0
	hav_gold = False
	gold = 0
	hav_diamond = False
	diamond = 0
	hav_géode = False
	géode = 0
	#!wood
	nb_range_wood = int((60//15)//(cooldown_mine/120))
	for _ in range(nb_range_wood):
		wood += randint(author_wood[0], author_wood[1])
	#!mine
	nb_range_mine = int((60//15)//(cooldown_mine/60))

	all_pourcentage_fer = author_fer[0] + \
		author_fer[0]*pourcentage_minerais_faction
	all_pourcentage_or = author_gold[0] + \
		author_gold[0]*pourcentage_minerais_faction
	all_pourcentage_diamant = author_diamond[0] + \
		author_diamond[0]*pourcentage_minerais_faction
	all_pourcentage_géode = author_géode[0] + \
		author_géode[0]*pourcentage_minerais_faction

	for _ in range(nb_range_mine):
		stone += randint(author_pierres[0], author_pierres[1])

		#Calcule du fer
		rand = random()
		if all_pourcentage_fer >= rand:
			iron += author_fer[1] + minerais_en_plus_faction[0]
			hav_iron = True
		#Calcule l'or
		rand = random()
		if all_pourcentage_or >= rand:
			gold += author_gold[1] + minerais_en_plus_faction[1]
			hav_gold = True

		#Calcule du diamant
		rand = random()
		if all_pourcentage_diamant >= rand:
			diamond += author_diamond[1] + minerais_en_plus_faction[2]
			hav_diamond = True

		#Calcule des géodes
		rand = random()
		if all_pourcentage_géode >= rand:
			géode += author_géode[1]
			hav_géode = True

	collection.update_one({"_id": author_id}, {"$inc": {"!wood": nb_range_wood}})
	collection.update_one({"_id": author_id}, {"$inc": {"!mine": nb_range_mine}})

	message = ""
	# bois
	collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
	message += f"Vous venez de récolter {wood} bois"

	# pierre
	collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
	message += f", {stone} pierre"

	if hav_iron:  # fer
		collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
		message += f", {iron} fer"

	if hav_gold:  # or
		collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
		message += f", {gold} or"
	if hav_diamond:  # dimant
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
		message += f", {diamond} diamant"
	if hav_géode:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
		message += f", {géode} géode"
	await ctx.channel.send(f"{message}, {ctx.author.mention}")


# 2 fois !mine
@bot.command(name='vote', aliases=["v","V","Vote"], help="Cette commande te permet de voté pour ton serveur préférais, et en contreparti de recevoir une récompense alléchante")
@commands.cooldown(1, 5, commands.BucketType.user)
async def vote(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_pioche = x["hav_pioche"]
		nb_invitation = x["invite"]
		author_house = x["house"][0]
		author_vote_cooldown = x["cooldown_!vote"]
		author_using_potion = x["using_potion"]
		author_incrusted = x["incrusted"]
		author_incrusted_hache = x["incrusted_hache"]
		author_current_biome = x["current_biome"]
		little_event = x["event_numbers"]

	t2 = int(time())

	t = int(t2 - author_vote_cooldown)

	if t < 60*60*12:

		t = 60*60*12-t
		if t >= 3600*24:
			t3 = strftime('%d %H %M %S', gmtime(t)).split(" ")
			message = "{}j {}h {}m {}s".format(t3[0], t3[1], t3[2], t3[3])
		elif t >= 3600:
			t3 = strftime('%H %M %S', gmtime(t)).split(" ")
			message = "{}h {}m {}s".format(t3[0], t3[1], t3[2])
		elif t >= 60:
			t3 = strftime('%M %S', gmtime(t)).split(" ")
			message = "{}m {}s".format(t3[0], t3[1])
		else:
			t3 = strftime('%S', gmtime(t)).split(" ")
			message = "{}s".format(t3[0])

		return await ctx.send("{}, réessayer dans {}".format(ctx.author.mention, message))

	if not author_hav_hache:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de hache,, pour acheté une pioche faite `!buy axe`, {ctx.author.mention}")

	if not author_pioche:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de pioche, donc le `!mine` n'a pas étais ajouté, pour acheté une pioche faite `!buy pickaxe`, {ctx.author.mention}")

	collection.update_one({"_id": author_id}, {"$set": {"cooldown_!vote": t2}})

	result = collection.find({"_id": author_id})
	for x in result:
		#"Pioche":[niveau,prix,(pierre_min,pierre_max),%fer]

		author_pioche = x["pioche"]
		author_hache = x["hache"]

	if author_house == "pas_de_faction":
		pourcentage_minerais_faction = 0
		minerais_en_plus_faction = [0, 0, 0]
	else:
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	if little_event[2]:
		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat
		if hache_stat != "soon":
			author_hache = hache_stat

	if author_using_potion[1] != 0 and author_using_potion[1] >= int(time()):
		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat
		if hache_stat != "soon":
			author_hache = hache_stat
	elif author_using_potion[1] != 0:
		author_using_potion[1] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	author_pierres = list(pioche[author_pioche][2])
	author_fer = list(pioche[author_pioche][3])
	author_gold = list(pioche[author_pioche][4])
	author_diamond = list(pioche[author_pioche][5])
	author_géode = list(pioche[author_pioche][6])
	author_wood = list(hache[author_hache][2])
	author_sap = list(hache[author_hache][3])
	author_magic_powder = hache[author_hache][4]

	if author_incrusted != "none":
		boost_incrustation = incrustation[author_incrusted][0]
		author_pierres[0] *= boost_incrustation
		author_pierres[1] *= boost_incrustation
		author_fer[1] *= boost_incrustation
		author_gold[1] *= boost_incrustation
		author_diamond[1] *= boost_incrustation
		author_géode[1] *= boost_incrustation

	if author_incrusted_hache != "none":
		boost_incrustation = incrustation[author_incrusted_hache][0]
		author_wood[0] *= boost_incrustation
		author_wood[1] *= boost_incrustation
		author_sap[1] *= boost_incrustation
	boost = 1
	temps = int(time())
	if author_using_potion[0] != 0 and author_using_potion[0] >= temps:
		boost = 2
	else:
		author_using_potion[0] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	boost_biome_bois = 1
	if author_current_biome in ["Forêt","Forêt d'érable","Forêt féérique"]:
		boost_biome_bois = 1.5
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_bois = 4
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_bois = 0.5
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_bois = 0.25

	boost_biome_sève = 1
	if author_current_biome in ["Forêt d'érable"]:
		boost_biome_sève = 2
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_sève = 0

	boost_biome_magic_powder = 1
	if author_current_biome == "Forêt féérique":
		boost_biome_magic_powder = 4

	boost_biome_coal = (0,0)
	if author_current_biome == "Forêt Ancienne":
		boost_biome_coal = (0.1,100)

	# ---------------------

	do_stone = True
	boost_biome_pierre = 1
	if author_current_biome in ["Carrière", "Grosse grotte", "Montagne éléctrique"]:
		boost_biome_pierre = 1.5
	elif author_current_biome in ["Grotte", "Volcan"]:
		boost_biome_pierre = 2
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_pierre = 4
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_pierre = 0.25
	elif author_current_biome in ["Forêt d'érable"]:
		boost_biome_pierre = 0.75
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		do_stone = False
		boost_biome_pierre = 0

	boost_biome_fer = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_fer = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_fer = 2
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_fer = 0

	boost_biome_or = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_or = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_or = 2
	elif author_current_biome in ["Montagne éléctrique"]:
		boost_biome_or = 3
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_or = 0

	boost_biome_charbon = (0, 0)
	if author_current_biome in ["Grotte"]:
		boost_biome_charbon = (0.01, 50)
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_charbon = (0.05, 100)

	boost_biome_lave = (0, 0)
	if author_current_biome in ["Volcan"]:
		boost_biome_lave = (0.05, 1)

	boost_biome_steel = (0, 0)
	if author_current_biome in ["Météorite"]:
		boost_biome_steel = (0.2, 5)

	boost_biome_electrum = (0, 0)
	if author_current_biome in ["Montagne éléctrique"]:
		boost_biome_electrum = (0.01, 1)

	boost_biome_dracolite = (0, 0)
	if author_current_biome in ["Nid du dragon"]:
		boost_biome_dracolite = (0.005, 1)

	boost_biome_emerald = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_emerald = (0.3, 1)
	boost_biome_sapphire = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_sapphire = (0.08, 1)
	boost_biome_ruby = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_ruby = (0.01, 1)

	boost_biome_géode = 1
	if author_current_biome in ["Météorite"]:
		boost_biome_géode = 1.5
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_géode = 0

	boost_biome_diamond = 1
	if author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_diamond = 0
	hav_coal_wood = False
	hav_coal = False
	wood = 0
	sap = 0
	hav_sap = False
	magic_powder = 0
	hav_magic_powder = False
	stone = 0
	hav_iron = False
	iron = 0
	hav_gold = False
	gold = 0
	hav_diamond = False
	diamond = 0
	hav_géode = False
	géode = 0
	hav_coal = False
	coal = 0
	hav_lava = False
	lava = 0
	hav_steel = False
	steel = 0
	hav_electrum = False
	electrum = 0
	hav_dracolite = False
	dracolite = 0
	hav_emerald = False
	emerald = 0
	hav_sapphire = False
	sapphire = 0
	hav_ruby = False
	ruby = 0
	#!wood
	nb_range_wood = 0
	do_wood = True
	if author_current_biome not in ["Grotte", "Grosse grotte", "Volcan", "Météorite", "Montagne éléctrique", "Nid du dragon","Pierre précieuse"]:
		all_pourcentage_sap = (
		author_sap[0] + author_sap[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_magic_powder = ((author_magic_powder[0])*little_event[1])*boost_biome_magic_powder
		nb_range_wood = int((60*12//15)//(cooldown_mine/120))
		for _ in range(nb_range_wood):
			wood += int(((randint(author_wood[0], author_wood[1]))*boost)*boost_biome_bois)

			#Calcule la sève
			rand = random()
			if all_pourcentage_sap >= rand:
				sap += int(((author_sap[1])*boost)*boost_biome_sève)
				hav_sap = True
			#Calcule la poudre magique
			rand = random()
			if all_pourcentage_magic_powder >= rand:
				magic_powder += (author_magic_powder[1])*boost
				hav_magic_powder = True
			rand = random()
			if boost_biome_coal[0] >= rand:
				coal += boost_biome_coal[1]
				hav_coal_wood = True
	else:
		do_wood = False
	#!mine
	nb_range_mine = 0
	if author_current_biome not in ["Forêt Ancienne", "Forêt féérique"]:
		nb_range_mine = int((60*12//15)//(cooldown_mine/60))

		all_pourcentage_fer = (
			author_fer[0] + author_fer[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_or = (
			author_gold[0] + author_gold[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_diamant = (
			author_diamond[0] + author_diamond[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_géode = (
			author_géode[0] + author_géode[0]*pourcentage_minerais_faction)*little_event[1]

		for _ in range(nb_range_mine):
			stone += int(((randint(author_pierres[0], author_pierres[1]))*boost)*boost_biome_pierre)

			#Calcule du fer
			rand = random()
			if all_pourcentage_fer >= rand:
				iron += int(((author_fer[1] + minerais_en_plus_faction[0])*boost)*boost_biome_fer)
				hav_iron = True
			#Calcule l'or
			rand = random()
			if all_pourcentage_or >= rand:
				gold += int(((author_gold[1] + minerais_en_plus_faction[1])*boost)*boost_biome_or)
				hav_gold = True

			#Calcule du diamant
			rand = random()
			if all_pourcentage_diamant >= rand:
				diamond += int(((author_diamond[1] + minerais_en_plus_faction[2])*boost)*boost_biome_diamond)
				hav_diamond = True

			#Calcule des géodes
			rand = random()
			if all_pourcentage_géode >= rand:
				géode += int(((author_géode[1])*boost)*boost_biome_géode)
				hav_géode = True

			rand = random()
			if boost_biome_charbon[0] >= rand:
				coal += boost_biome_charbon[1]
				hav_coal = True

			rand = random()
			if boost_biome_lave[0] >= rand:
				lava += boost_biome_lave[1]
				hav_lava = True

			rand = random()
			if boost_biome_steel[0] >= rand:
				steel += boost_biome_steel[1]
				hav_steel = True

			rand = random()
			if boost_biome_electrum[0] >= rand:
				electrum += boost_biome_electrum[1]
				hav_electrum = True
			rand = random()
			if boost_biome_dracolite[0] >= rand:
				dracolite += boost_biome_dracolite[1]
				hav_dracolite = True

			rand = random()
			if boost_biome_emerald[0] >= rand:
				emerald += boost_biome_emerald[1]
				hav_emerald = True
			rand = random()
			if boost_biome_sapphire[0] >= rand:
				sapphire += boost_biome_sapphire[1]
				hav_sapphire = True
			rand = random()
			if boost_biome_ruby[0] >= rand:
				ruby = boost_biome_ruby[1]
				hav_ruby += True

	collection.update_one({"_id": author_id}, {"$inc": {"!wood": nb_range_wood}})
	collection.update_one({"_id": author_id}, {"$inc": {"!mine": nb_range_mine}})

	message = ""
	# bois
	if do_wood:
		collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
		message += f"Vous venez de récolter {wood} bois"

	if hav_sap:  # sève
		collection.update_one({"_id": author_id}, {"$inc": {"sap": sap}})
		message += f", **{sap} sève**"
	if hav_coal_wood:  # sève
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message += f", **{coal} charbon**"

	if hav_magic_powder:  # poudre magique
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"magic_powder": magic_powder}})
		message += f", **__{magic_powder} poudre magique__**"

	# pierre
	if do_stone and do_wood:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
		message += f", {stone} pierre"
	elif do_stone:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
		message += f"Vous venez de récolter {stone} pierre"
	else:
		message = "Vous venez de récolter"

	if hav_iron and do_stone:  # fer
		collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
		message += f", **{iron} fer**"

	if hav_gold and do_stone:  # or
		collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
		message += f", **{gold} or**"
	if hav_diamond and do_stone:  # dimant
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
		message += f", **__{diamond} diamant__**"
	if hav_géode and do_stone:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
		message += f", **__{géode} géode__**"
	if hav_coal:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message += f", **{coal} Charbons**"
	if hav_lava:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"lava": lava}})
		message += f", **{lava} sceau de lave**"
	if hav_steel:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"steel": steel}})
		message += f", **{steel} acier**"
	if hav_electrum:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"électrum": electrum}})
		message += f", **__{electrum} électrum__**"
	if hav_dracolite:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"dracolite": dracolite}})
		message += f", **__{dracolite} dracolite__**"
	if hav_emerald:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"emerald": emerald}})
		message += f", **__{emerald} émeraude__**"
	if hav_sapphire:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"sapphire": sapphire}})
		message += f", **__{sapphire} saphir__**"
	if hav_ruby:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"ruby": ruby}})
		message += f", **__{ruby} rubis__**"

	await ctx.channel.send(f"{message}, {ctx.author.mention}")


@bot.command(name='claim', aliases=["Claim"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def claim(ctx):
	if not await check_if_aventurier(ctx):
		return
	url = f"https://api.top-serveurs.net/v1/votes/claim-username?server_token={TOKEN_TOP_SERVEUR}&playername={ctx.author.display_name}"
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})

	reponse = requests.get(url)

	if 'json' in reponse.headers.get('Content-Type'):
		js = reponse.json()
		if js["claimed"] == 1:
			result = collection.find({"_id": author_id})
			for x in result:
				author_hav_hache = x["hav_hache"]
				author_pioche = x["hav_pioche"]
				author_house = x["house"][0]
				author_using_potion = x["using_potion"]
				author_incrusted = x["incrusted"]
				author_incrusted_hache = x["incrusted_hache"]
				author_current_biome = x["current_biome"]
				little_event = x["event_numbers"]

			if not author_hav_hache:  # vérifie si le joueur possède une pioche
				return await ctx.channel.send(f"Vous n'avez pas encore de hache,, pour acheté une pioche faite `!buy axe`, {ctx.author.mention}")

			if not author_pioche:  # vérifie si le joueur possède une pioche
				return await ctx.channel.send(f"Vous n'avez pas encore de pioche, donc le `!mine` n'a pas étais ajouté, pour acheté une pioche faite `!buy pickaxe`, {ctx.author.mention}")

			result = collection.find({"_id": author_id})
			for x in result:
				#"Pioche":[niveau,prix,(pierre_min,pierre_max),%fer]

				author_pioche = x["pioche"]
				author_hache = x["hache"]

			if author_house == "pas_de_faction":
				pourcentage_minerais_faction = 0
				minerais_en_plus_faction = [0, 0, 0]
			else:
				result_faction = collection_faction.find({"name": author_house[:-2]})
				for y in result_faction:
					pourcentage_minerais_faction = y["+% minerais"]/100
					minerais_en_plus_faction = y["+minerais"]

			if little_event[2]:
				pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
				hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
				if pioche_stat != "soon":
					author_pioche = pioche_stat
				if hache_stat != "soon":
					author_hache = hache_stat

			if author_using_potion[1] != 0:
				if author_using_potion[1] >= int(time()):
					pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
					hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
					if pioche_stat != "soon":
						author_pioche = pioche_stat
					if hache_stat != "soon":
						author_hache = hache_stat
				else:
					author_using_potion[1] = 0
					collection.update_one({"_id": author_id}, {
					                      "$set": {"author_using_potion": author_using_potion}})

			author_pierres = list(pioche[author_pioche][2])
			author_fer = list(pioche[author_pioche][3])
			author_gold = list(pioche[author_pioche][4])
			author_diamond = list(pioche[author_pioche][5])
			author_géode = list(pioche[author_pioche][6])

			author_wood = list(hache[author_hache][2])
			author_sap = list(hache[author_hache][3])
			author_magic_powder = hache[author_hache][4]

			if author_incrusted != "none":
				boost_incrustation = incrustation[author_incrusted][0]

				author_pierres[0] *= boost_incrustation
				author_pierres[1] *= boost_incrustation
				author_fer[1] *= boost_incrustation
				author_gold[1] *= boost_incrustation
				author_diamond[1] *= boost_incrustation
				author_géode[1] *= boost_incrustation

			if author_incrusted_hache != "none":
				boost_incrustation = incrustation[author_incrusted_hache][0]
				author_wood[0] *= boost_incrustation
				author_wood[1] *= boost_incrustation
				author_sap[1] *= boost_incrustation
			boost = 1
			temps = int(time())
			if author_using_potion[0] != 0 and author_using_potion[0] >= temps:
				boost = 2
			else:
				author_using_potion[0] = 0
				collection.update_one({"_id": author_id}, {
				                      "$set": {"author_using_potion": author_using_potion}})
			boost_biome_bois = 1
			if author_current_biome in ["Forêt","Forêt d'érable","Forêt féérique"]:
				boost_biome_bois = 1.5
			elif author_current_biome in ["Grande forêt"]:
				boost_biome_bois = 4
			elif author_current_biome in ["Forêt Ancienne"]:
				boost_biome_bois = 0.5
			elif author_current_biome in ["Grande carrière"]:
				boost_biome_bois = 0.25

			boost_biome_sève = 1
			if author_current_biome in ["Forêt d'érable"]:
				boost_biome_sève = 2
			elif author_current_biome in ["Forêt Ancienne"]:
				boost_biome_sève = 0

			boost_biome_magic_powder = 1
			if author_current_biome == "Forêt féérique":
				boost_biome_magic_powder = 4

			boost_biome_coal = (0,0)
			if author_current_biome == "Forêt Ancienne":
				boost_biome_coal = (0.1,100)

			# ---------------------

			do_stone = True
			boost_biome_pierre = 1
			if author_current_biome in ["Carrière", "Grosse grotte", "Montagne éléctrique"]:
				boost_biome_pierre = 1.5
			elif author_current_biome in ["Grotte", "Volcan"]:
				boost_biome_pierre = 2
			elif author_current_biome in ["Grande carrière"]:
				boost_biome_pierre = 4
			elif author_current_biome in ["Grande forêt"]:
				boost_biome_pierre = 0.25
			elif author_current_biome in ["Forêt d'érable"]:
				boost_biome_pierre = 0.75
			elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
				do_stone = False
				boost_biome_pierre = 0

			boost_biome_fer = 1
			if author_current_biome in ["Grotte"]:
				boost_biome_fer = 1.5
			elif author_current_biome in ["Grosse grotte"]:
				boost_biome_fer = 2
			elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
				boost_biome_fer = 0

			boost_biome_or = 1
			if author_current_biome in ["Grotte"]:
				boost_biome_or = 1.5
			elif author_current_biome in ["Grosse grotte"]:
				boost_biome_or = 2
			elif author_current_biome in ["Montagne éléctrique"]:
				boost_biome_or = 3
			elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
				boost_biome_or = 0

			boost_biome_charbon = (0, 0)
			if author_current_biome in ["Grotte"]:
				boost_biome_charbon = (0.01, 50)
			elif author_current_biome in ["Grosse grotte"]:
				boost_biome_charbon = (0.05, 100)

			boost_biome_lave = (0, 0)
			if author_current_biome in ["Volcan"]:
				boost_biome_lave = (0.05, 1)

			boost_biome_steel = (0, 0)
			if author_current_biome in ["Météorite"]:
				boost_biome_steel = (0.2, 5)

			boost_biome_electrum = (0, 0)
			if author_current_biome in ["Montagne éléctrique"]:
				boost_biome_electrum = (0.01, 1)

			boost_biome_dracolite = (0, 0)
			if author_current_biome in ["Nid du dragon"]:
				boost_biome_dracolite = (0.005, 1)

			boost_biome_emerald = (0, 0)
			if author_current_biome in ["Pierre précieuse"]:
				boost_biome_emerald = (0.3, 1)
			boost_biome_sapphire = (0, 0)
			if author_current_biome in ["Pierre précieuse"]:
				boost_biome_sapphire = (0.08, 1)
			boost_biome_ruby = (0, 0)
			if author_current_biome in ["Pierre précieuse"]:
				boost_biome_ruby = (0.01, 1)

			boost_biome_géode = 1
			if author_current_biome in ["Météorite"]:
				boost_biome_géode = 1.5
			elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
				boost_biome_géode = 0

			boost_biome_diamond = 1
			if author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
				boost_biome_diamond = 0
			hav_coal_wood = False
			hav_coal = False
			wood = 0
			sap = 0
			hav_sap = False
			magic_powder = 0
			hav_magic_powder = False
			stone = 0
			hav_iron = False
			iron = 0
			hav_gold = False
			gold = 0
			hav_diamond = False
			diamond = 0
			hav_géode = False
			géode = 0
			hav_coal = False
			coal = 0
			hav_lava = False
			lava = 0
			hav_steel = False
			steel = 0
			hav_electrum = False
			electrum = 0
			hav_dracolite = False
			dracolite = 0
			hav_emerald = False
			emerald = 0
			hav_sapphire = False
			sapphire = 0
			hav_ruby = False
			ruby = 0
			#!wood
			nb_range_wood = 0
			do_wood = True
			if author_current_biome not in ["Grotte", "Grosse grotte", "Volcan", "Météorite", "Montagne éléctrique", "Nid du dragon","Pierre précieuse"]:
				all_pourcentage_sap = (
				author_sap[0] + author_sap[0]*pourcentage_minerais_faction)*little_event[1]
				all_pourcentage_magic_powder = ((author_magic_powder[0])*little_event[1])*boost_biome_magic_powder
				nb_range_wood = int((60//15)//(cooldown_mine/120))
				for _ in range(nb_range_wood):
					wood += int(((randint(author_wood[0], author_wood[1]))*boost)*boost_biome_bois)

					#Calcule la sève
					rand = random()
					if all_pourcentage_sap >= rand:
						sap += int(((author_sap[1])*boost)*boost_biome_sève)
						hav_sap = True
					#Calcule la poudre magique
					rand = random()
					if all_pourcentage_magic_powder >= rand:
						magic_powder += (author_magic_powder[1])*boost
						hav_magic_powder = True
					rand = random()
					if boost_biome_coal[0] >= rand:
						coal += boost_biome_coal[1]
						hav_coal_wood = True
			else:
				do_wood = False
			#!mine
			nb_range_mine = 0
			if author_current_biome not in ["Forêt Ancienne", "Forêt féérique"]:
				nb_range_mine = int((60//15)//(cooldown_mine/60))

				all_pourcentage_fer = (
					author_fer[0] + author_fer[0]*pourcentage_minerais_faction)*little_event[1]
				all_pourcentage_or = (
					author_gold[0] + author_gold[0]*pourcentage_minerais_faction)*little_event[1]
				all_pourcentage_diamant = (
					author_diamond[0] + author_diamond[0]*pourcentage_minerais_faction)*little_event[1]
				all_pourcentage_géode = (
					author_géode[0] + author_géode[0]*pourcentage_minerais_faction)*little_event[1]

				for _ in range(nb_range_mine):
					stone += int(((randint(author_pierres[0], author_pierres[1]))*boost)*boost_biome_pierre)

					#Calcule du fer
					rand = random()
					if all_pourcentage_fer >= rand:
						iron += int(((author_fer[1] + minerais_en_plus_faction[0])*boost)*boost_biome_fer)
						hav_iron = True
					#Calcule l'or
					rand = random()
					if all_pourcentage_or >= rand:
						gold += int(((author_gold[1] + minerais_en_plus_faction[1])*boost)*boost_biome_or)
						hav_gold = True

					#Calcule du diamant
					rand = random()
					if all_pourcentage_diamant >= rand:
						diamond += int(((author_diamond[1] + minerais_en_plus_faction[2])*boost)*boost_biome_diamond)
						hav_diamond = True

					#Calcule des géodes
					rand = random()
					if all_pourcentage_géode >= rand:
						géode += int(((author_géode[1])*boost)*boost_biome_géode)
						hav_géode = True

					rand = random()
					if boost_biome_charbon[0] >= rand:
						coal += boost_biome_charbon[1]
						hav_coal = True

					rand = random()
					if boost_biome_lave[0] >= rand:
						lava += boost_biome_lave[1]
						hav_lava = True

					rand = random()
					if boost_biome_steel[0] >= rand:
						steel += boost_biome_steel[1]
						hav_steel = True

					rand = random()
					if boost_biome_electrum[0] >= rand:
						electrum += boost_biome_electrum[1]
						hav_electrum = True
					rand = random()
					if boost_biome_dracolite[0] >= rand:
						dracolite += boost_biome_dracolite[1]
						hav_dracolite = True

					rand = random()
					if boost_biome_emerald[0] >= rand:
						emerald += boost_biome_emerald[1]
						hav_emerald = True
					rand = random()
					if boost_biome_sapphire[0] >= rand:
						sapphire += boost_biome_sapphire[1]
						hav_sapphire = True
					rand = random()
					if boost_biome_ruby[0] >= rand:
						ruby = boost_biome_ruby[1]
						hav_ruby += True

			collection.update_one({"_id": author_id}, {"$inc": {"!wood": nb_range_wood}})
			collection.update_one({"_id": author_id}, {"$inc": {"!mine": nb_range_mine}})

			message = ""
			# bois
			if do_wood:
				collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
				message += f"Vous venez de récolter {wood} bois"

			if hav_sap:  # sève
				collection.update_one({"_id": author_id}, {"$inc": {"sap": sap}})
				message += f", **{sap} sève**"
			if hav_coal_wood:  # sève
				collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
				message += f", **{coal} charbon**"

			if hav_magic_powder:  # poudre magique
				collection.update_one({"_id": author_id}, {
				                      "$inc": {"magic_powder": magic_powder}})
				message += f", **__{magic_powder} poudre magique__**"

			# pierre
			if do_stone and do_wood:
				collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
				message += f", {stone} pierre"
			elif do_stone:
				collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
				message += f"Vous venez de récolter {stone} pierre"
			else:
				message = "Vous venez de récolter"

			if hav_iron and do_stone:  # fer
				collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
				message += f", **{iron} fer**"

			if hav_gold and do_stone:  # or
				collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
				message += f", **{gold} or**"
			if hav_diamond and do_stone:  # dimant
				collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
				message += f", **__{diamond} diamant__**"
			if hav_géode and do_stone:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
				message += f", **__{géode} géode__**"
			if hav_coal:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
				message += f", **{coal} Charbons**"
			if hav_lava:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"lava": lava}})
				message += f", **{lava} sceau de lave**"
			if hav_steel:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"steel": steel}})
				message += f", **{steel} acier**"
			if hav_electrum:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"électrum": electrum}})
				message += f", **__{electrum} électrum__**"
			if hav_dracolite:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"dracolite": dracolite}})
				message += f", **__{dracolite} dracolite__**"
			if hav_emerald:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"emerald": emerald}})
				message += f", **__{emerald} émeraude__**"
			if hav_sapphire:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"sapphire": sapphire}})
				message += f", **__{sapphire} saphir__**"
			if hav_ruby:  # géode
				collection.update_one({"_id": author_id}, {"$inc": {"ruby": ruby}})
				message += f", **__{ruby} rubis__**"
			await ctx.channel.send(f"{message}, {ctx.author.mention}")
		elif js["claimed"] == 2:
			await ctx.channel.send(f"Tu as déjà récupérer ta récompense, l'ami {ctx.author.mention} !")
		elif js["claimed"] == 0:
			await ctx.channel.send(f"Tu n'as pas encore voté ou le nom mis n'est pas valide. **ATTENTION, il faut impérativement que ton nom sur discord soi le même que pour voté, le lien du vote :** https://top-serveurs.net/discord/vote/discord-of-empire), l'ami {ctx.author.mention} !")
	else:
		print('Response content is not in JSON format., on !claim')
		js = 'spam'


@bot.command(name='day', aliases=["jour", "j","Jour", "J","Day"], enabled=False)  # 60 fois !mine
@commands.cooldown(1, 3600*24, commands.BucketType.user)
async def day(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_hav_hache = x["hav_hache"]
		author_pioche = x["hav_pioche"]
		nb_invitation = x["invite"]
		author_house = x["house"][0]

	if nb_invitation < 5:
		return await ctx.channel.send(f"Pour utilisé la commande, <`!day`>, vous devez inviter une personne sur le serveur, pour connaître le nombre de personne que vous avez inviter faite <!invitation>, {ctx.author.mention}")

	if not author_hav_hache:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de hache,, pour acheté une pioche faite `!buy axe`, {ctx.author.mention}")

	if not author_pioche:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de pioche, donc le `!mine` n'a pas étais ajouté, pour acheté une pioche faite `!buy pickaxe`, {ctx.author.mention}")

	result = collection.find({"_id": author_id})
	for x in result:
		#"Pioche":[niveau,prix,(pierre_min,pierre_max),%fer]
		author_wood = hache[x["hache"]][2]
		author_pierres = pioche[x["pioche"]][2]
		author_fer = pioche[x["pioche"]][3]
		author_gold = pioche[x["pioche"]][4]
		author_diamond = pioche[x["pioche"]][5]
		author_géode = pioche[x["pioche"]][6]
		author_incrusted = x["incrusted"]

	if author_house != "pas_de_faction":
		pourcentage_minerais_faction = 0
		minerais_en_plus_faction = [0, 0, 0]
	else:
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	stone = 0
	hav_iron = False
	iron = 0
	hav_gold = False
	gold = 0
	hav_diamond = False
	diamond = 0
	hav_géode = False
	géode = 0
	#wood
	nb_range_wood = int((60*24//24)//(cooldown_mine/120))
	wood = sum(
	    randint(author_wood[0], author_wood[1]) for _ in range(nb_range_wood))
	#mine
	nb_range_mine = int((60*24//24)//(cooldown_mine/60))

	all_pourcentage_fer = author_fer[0] + \
		author_fer[0]*pourcentage_minerais_faction
	all_pourcentage_or = author_gold[0] + \
		author_gold[0]*pourcentage_minerais_faction
	all_pourcentage_diamant = author_diamond[0] + \
		author_diamond[0]*pourcentage_minerais_faction
	all_pourcentage_géode = author_géode[0] + \
		author_géode[0]*pourcentage_minerais_faction

	for _ in range(nb_range_mine):
		stone += randint(author_pierres[0], author_pierres[1])

		#Calcule le fer
		rand = random()
		if all_pourcentage_fer >= rand:
			iron += author_fer[1] + minerais_en_plus_faction[0]
			hav_iron = True
		#Calcule l'or
		rand = random()
		if all_pourcentage_or >= rand:
			gold += author_gold[1] + minerais_en_plus_faction[1]
			hav_gold = True
		#Calcule du diamant
		rand = random()
		if all_pourcentage_diamant >= rand:
			diamond += author_diamond[1] + minerais_en_plus_faction[2]
			hav_diamond = True

		rand = random()
		if all_pourcentage_géode >= rand:
			géode += author_géode[1]
			hav_géode = True

	collection.update_one({"_id": author_id}, {"$inc": {"!wood": nb_range_wood}})
	collection.update_one({"_id": author_id}, {"$inc": {"!mine": nb_range_mine}})

	message = ""
	# bois
	collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
	message += f"Vous venez de récolter {wood} bois"

	# pierre
	collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
	message += f", {stone} pierre"

	if hav_iron:  # fer
		collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
		message += f", {iron} fer"

	if hav_gold:  # or
		collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
		message += f", {gold} or"
	if hav_diamond:  # dimant
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
		message += f", {diamond} diamant"
	if hav_géode:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
		message += f", {géode} géode"
	await ctx.channel.send(f"{message}, {ctx.author.mention}")


@bot.command(name='week', aliases=["semaine","Week","Semaine"])
#@commands.cooldown(1, 5, commands.BucketType.user)  # 420 fois !mine
async def week(ctx):
	if not await check_if_aventurier(ctx):
		return
	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_pioche = x["hav_pioche"]
		author_hav_hache = x["hav_hache"]
		nb_invitation = x["invite"]
		author_house = x["house"][0]
		author_vote_cooldown = x["cooldown_!week"]
		author_using_potion = x["using_potion"]
		author_incrusted = x["incrusted"]
		author_incrusted_hache = x["incrusted_hache"]
		author_current_biome = x["current_biome"]
		little_event = x["event_numbers"]

	t2 = int(time())

	t = int(t2 - author_vote_cooldown)

	if t < 60*60*24*7:

		t = 60*60*24*7-t
		if t >= 3600*24:
			t3 = strftime('%d %H %M %S', gmtime(t)).split(" ")
			message = "{}j {}h {}m {}s".format(int(t3[0])-1, t3[1], t3[2], t3[3])
		elif t >= 3600:
			t3 = strftime('%H %M %S', gmtime(t)).split(" ")
			message = "{}h {}m {}s".format(t3[0], t3[1], t3[2])
		elif t >= 60:
			t3 = strftime('%M %S', gmtime(t)).split(" ")
			message = "{}m {}s".format(t3[0], t3[1])
		else:
			t3 = strftime('%S', gmtime(t)).split(" ")
			message = "{}s".format(t3[0])

		return await ctx.send("{}, réessayer dans {}".format(ctx.author.mention, message))

	if nb_invitation < 5:
		return await ctx.channel.send(f"Pour utilisé la commande, <`!week`>, vous devez inviter 5 personne sur le serveur, pour connaître le nombre de personne que vous avez inviter faite <!invitation>, {ctx.author.mention}")

	if not author_hav_hache:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de hache,, pour acheté une pioche faite `!buy axe`, {ctx.author.mention}")

	if not author_pioche:  # vérifie si le joueur possède une pioche
		return await ctx.channel.send(f"Vous n'avez pas encore de pioche, pour acheté une pioche faite `!buy pickaxe`, {ctx.author.mention}")

	result = collection.find({"_id": author_id})
	for x in result:

		#"nom_Pioche":[niveau,prix,(pierre_min,pierre_max),(%fer,nb_fer),(%gold,nb_gold),(%diamond,nb_diamond)]
		author_pioche = x["pioche"]
		author_hache = x["hache"]

	pourcentage_minerais_faction = 0
	minerais_en_plus_faction = [0, 0, 0]
	if author_house != "pas_de_faction":
		result_faction = collection_faction.find({"name": author_house[:-2]})
		for y in result_faction:
			pourcentage_minerais_faction = y["+% minerais"]/100
			minerais_en_plus_faction = y["+minerais"]

	if little_event[2]:
		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat
		if hache_stat != "soon":
			author_hache = hache_stat

	if author_using_potion[1] != 0 and author_using_potion[1] >= int(time()):

		pioche_stat = niv_pioche[str(int(pioche[author_pioche][0])+1)]
		hache_stat = niv_hache[str(int(hache[author_hache][0])+1)]
		if pioche_stat != "soon":
			author_pioche = pioche_stat
		if hache_stat != "soon":
			author_hache = hache_stat
	elif author_using_potion[1] != 0:
		author_using_potion[1] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})

	author_pierres = list(pioche[author_pioche][2])
	author_fer = list(pioche[author_pioche][3])
	author_gold = list(pioche[author_pioche][4])
	author_diamond = list(pioche[author_pioche][5])
	author_géode = list(pioche[author_pioche][6])

	author_wood = list(hache[author_hache][2])
	author_sap = list(hache[author_hache][3])
	author_magic_powder = hache[author_hache][4]

	if author_incrusted != "none":
		boost_incrustation = incrustation[author_incrusted][0]

		author_pierres[0] *= boost_incrustation
		author_pierres[1] *= boost_incrustation
		author_fer[1] *= boost_incrustation
		author_gold[1] *= boost_incrustation
		author_diamond[1] *= boost_incrustation
		author_géode[1] *= boost_incrustation

	if author_incrusted_hache != "none":
		boost_incrustation = incrustation[author_incrusted_hache][0]
		author_wood[0] *= boost_incrustation
		author_wood[1] *= boost_incrustation
		author_sap[1] *= boost_incrustation

	boost = 1
	if author_using_potion[0] != 0 and author_using_potion[0] >= int(time()):
		boost = 2
	elif author_using_potion[0] != 0:
		author_using_potion[0] = 0
		collection.update_one({"_id": author_id}, {
		                      "$set": {"author_using_potion": author_using_potion}})
	boost_biome_bois = 1
	if author_current_biome in ["Forêt","Forêt d'érable","Forêt féérique"]:
		boost_biome_bois = 1.5
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_bois = 4
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_bois = 0.5
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_bois = 0.25

	boost_biome_sève = 1
	if author_current_biome in ["Forêt d'érable"]:
		boost_biome_sève = 2
	elif author_current_biome in ["Forêt Ancienne"]:
		boost_biome_sève = 0

	boost_biome_magic_powder = 1
	if author_current_biome == "Forêt féérique":
		boost_biome_magic_powder = 4

	boost_biome_coal = (0,0)
	if author_current_biome == "Forêt Ancienne":
		boost_biome_coal = (0.1,100)

	# ---------------------

	do_stone = True
	boost_biome_pierre = 1
	if author_current_biome in ["Carrière", "Grosse grotte", "Montagne éléctrique"]:
		boost_biome_pierre = 1.5
	elif author_current_biome in ["Grotte", "Volcan"]:
		boost_biome_pierre = 2
	elif author_current_biome in ["Grande carrière"]:
		boost_biome_pierre = 4
	elif author_current_biome in ["Grande forêt"]:
		boost_biome_pierre = 0.25
	elif author_current_biome in ["Forêt d'érable"]:
		boost_biome_pierre = 0.75
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		do_stone = False
		boost_biome_pierre = 0

	boost_biome_fer = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_fer = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_fer = 2
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_fer = 0

	boost_biome_or = 1
	if author_current_biome in ["Grotte"]:
		boost_biome_or = 1.5
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_or = 2
	elif author_current_biome in ["Montagne éléctrique"]:
		boost_biome_or = 3
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_or = 0

	boost_biome_charbon = (0, 0)
	if author_current_biome in ["Grotte"]:
		boost_biome_charbon = (0.01, 50)
	elif author_current_biome in ["Grosse grotte"]:
		boost_biome_charbon = (0.05, 100)

	boost_biome_lave = (0, 0)
	if author_current_biome in ["Volcan"]:
		boost_biome_lave = (0.05, 1)

	boost_biome_steel = (0, 0)
	if author_current_biome in ["Météorite"]:
		boost_biome_steel = (0.2, 5)

	boost_biome_electrum = (0, 0)
	if author_current_biome in ["Montagne éléctrique"]:
		boost_biome_electrum = (0.01, 1)

	boost_biome_dracolite = (0, 0)
	if author_current_biome in ["Nid du dragon"]:
		boost_biome_dracolite = (0.005, 1)

	boost_biome_emerald = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_emerald = (0.3, 1)
	boost_biome_sapphire = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_sapphire = (0.08, 1)
	boost_biome_ruby = (0, 0)
	if author_current_biome in ["Pierre précieuse"]:
		boost_biome_ruby = (0.01, 1)

	boost_biome_géode = 1
	if author_current_biome in ["Météorite"]:
		boost_biome_géode = 1.5
	elif author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_géode = 0

	boost_biome_diamond = 1
	if author_current_biome in ["Nid du dragon", "Pierre précieuse"]:
		boost_biome_diamond = 0
	hav_coal_wood = False
	hav_coal = False
	wood = 0
	sap = 0
	hav_sap = False
	magic_powder = 0
	hav_magic_powder = False
	stone = 0
	hav_iron = False
	iron = 0
	hav_gold = False
	gold = 0
	hav_diamond = False
	diamond = 0
	hav_géode = False
	géode = 0
	hav_coal = False
	coal = 0
	hav_lava = False
	lava = 0
	hav_steel = False
	steel = 0
	hav_electrum = False
	electrum = 0
	hav_dracolite = False
	dracolite = 0
	hav_emerald = False
	emerald = 0
	hav_sapphire = False
	sapphire = 0
	hav_ruby = False
	ruby = 0
	#!wood
	nb_range_wood = 0
	do_wood = True
	if author_current_biome not in ["Grotte", "Grosse grotte", "Volcan", "Météorite", "Montagne éléctrique", "Nid du dragon","Pierre précieuse"]:
		all_pourcentage_sap = (
		author_sap[0] + author_sap[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_magic_powder = ((author_magic_powder[0])*little_event[1])*boost_biome_magic_powder
		nb_range_wood = int((60*24*7//48)//(cooldown_mine/120))
		for _ in range(nb_range_wood):
			wood += int(((randint(author_wood[0], author_wood[1]))*boost)*boost_biome_bois)

			#Calcule la sève
			rand = random()
			if all_pourcentage_sap >= rand:
				sap += int(((author_sap[1])*boost)*boost_biome_sève)
				hav_sap = True
			#Calcule la poudre magique
			rand = random()
			if all_pourcentage_magic_powder >= rand:
				magic_powder += (author_magic_powder[1])*boost
				hav_magic_powder = True
			rand = random()
			if boost_biome_coal[0] >= rand:
				coal += boost_biome_coal[1]
				hav_coal_wood = True
	else:
		do_wood = False
	#!mine
	nb_range_mine = 0
	if author_current_biome not in ["Forêt Ancienne", "Forêt féérique"]:
		nb_range_mine = int((60*24*7//48)//(cooldown_mine/60))

		all_pourcentage_fer = (
			author_fer[0] + author_fer[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_or = (
			author_gold[0] + author_gold[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_diamant = (
			author_diamond[0] + author_diamond[0]*pourcentage_minerais_faction)*little_event[1]
		all_pourcentage_géode = (
			author_géode[0] + author_géode[0]*pourcentage_minerais_faction)*little_event[1]

		for _ in range(nb_range_mine):
			stone += int(((randint(author_pierres[0], author_pierres[1]))*boost)*boost_biome_pierre)

			#Calcule du fer
			rand = random()
			if all_pourcentage_fer >= rand:
				iron += int(((author_fer[1] + minerais_en_plus_faction[0])*boost)*boost_biome_fer)
				hav_iron = True
			#Calcule l'or
			rand = random()
			if all_pourcentage_or >= rand:
				gold += int(((author_gold[1] + minerais_en_plus_faction[1])*boost)*boost_biome_or)
				hav_gold = True

			#Calcule du diamant
			rand = random()
			if all_pourcentage_diamant >= rand:
				diamond += int(((author_diamond[1] + minerais_en_plus_faction[2])*boost)*boost_biome_diamond)
				hav_diamond = True

			#Calcule des géodes
			rand = random()
			if all_pourcentage_géode >= rand:
				géode += int(((author_géode[1])*boost)*boost_biome_géode)
				hav_géode = True

			rand = random()
			if boost_biome_charbon[0] >= rand:
				coal += boost_biome_charbon[1]
				hav_coal = True

			rand = random()
			if boost_biome_lave[0] >= rand:
				lava += boost_biome_lave[1]
				hav_lava = True

			rand = random()
			if boost_biome_steel[0] >= rand:
				steel += boost_biome_steel[1]
				hav_steel = True

			rand = random()
			if boost_biome_electrum[0] >= rand:
				electrum += boost_biome_electrum[1]
				hav_electrum = True
			rand = random()
			if boost_biome_dracolite[0] >= rand:
				dracolite += boost_biome_dracolite[1]
				hav_dracolite = True

			rand = random()
			if boost_biome_emerald[0] >= rand:
				emerald += boost_biome_emerald[1]
				hav_emerald = True
			rand = random()
			if boost_biome_sapphire[0] >= rand:
				sapphire += boost_biome_sapphire[1]
				hav_sapphire = True
			rand = random()
			if boost_biome_ruby[0] >= rand:
				ruby = boost_biome_ruby[1]
				hav_ruby += True

	collection.update_one({"_id": author_id}, {"$inc": {"!wood": nb_range_wood}})
	collection.update_one({"_id": author_id}, {"$inc": {"!mine": nb_range_mine}})

	message = ""
	# bois
	if do_wood:
		collection.update_one({"_id": author_id}, {"$inc": {"wood": wood}})
		message += f"Vous venez de récolter {wood} bois"

	if hav_sap:  # sève
		collection.update_one({"_id": author_id}, {"$inc": {"sap": sap}})
		message += f", **{sap} sève**"
	if hav_coal_wood:  # sève
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message += f", **{coal} charbon**"

	if hav_magic_powder:  # poudre magique
		collection.update_one({"_id": author_id}, {
		                      "$inc": {"magic_powder": magic_powder}})
		message += f", **__{magic_powder} poudre magique__**"

	# pierre
	if do_stone and do_wood:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
		message += f", {stone} pierre"
	elif do_stone:
		collection.update_one({"_id": author_id}, {"$inc": {"stone": stone}})
		message += f"Vous venez de récolter {stone} pierre"
	else:
		message = "Vous venez de récolter"

	if hav_iron and do_stone:  # fer
		collection.update_one({"_id": author_id}, {"$inc": {"iron": iron}})
		message += f", **{iron} fer**"

	if hav_gold and do_stone:  # or
		collection.update_one({"_id": author_id}, {"$inc": {"gold": gold}})
		message += f", **{gold} or**"
	if hav_diamond and do_stone:  # dimant
		collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamond}})
		message += f", **__{diamond} diamant__**"
	if hav_géode and do_stone:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"géode": géode}})
		message += f", **__{géode} géode__**"
	if hav_coal:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"coal": coal}})
		message += f", **{coal} Charbons**"
	if hav_lava:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"lava": lava}})
		message += f", **{lava} sceau de lave**"
	if hav_steel:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"steel": steel}})
		message += f", **{steel} acier**"
	if hav_electrum:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"électrum": electrum}})
		message += f", **__{electrum} électrum__**"
	if hav_dracolite:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"dracolite": dracolite}})
		message += f", **__{dracolite} dracolite__**"
	if hav_emerald:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"emerald": emerald}})
		message += f", **__{emerald} émeraude__**"
	if hav_sapphire:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"sapphire": sapphire}})
		message += f", **__{sapphire} saphir__**"
	if hav_ruby:  # géode
		collection.update_one({"_id": author_id}, {"$inc": {"ruby": ruby}})
		message += f", **__{ruby} rubis__**"
	collection.update_one({"_id": author_id}, {"$set": {"cooldown_!week": t2}})
	await ctx.channel.send(f"{message}, {ctx.author.mention}")


# @bot.command(name='rank', aliases=["leaderboard", "classement", "top","Leaderboard", "Classement", "Top","Rank"])
# @commands.cooldown(1, 2, commands.BucketType.user)
# async def rank(ctx, arg="rghftgrsc48949dx"):
# 	if not await check_if_aventurier(ctx):
# 		return
# 	if arg == "rghftgrsc48949dx":
# 		result = collection.find({}).sort(
# 			[("niveau", pymongo.DESCENDING), ("xp", pymongo.DESCENDING)])
# 		rank = []
# 		page = 1
# 		n = 0
# 		for x in result:
# 			n += 1
# 			author_niveau = x["niveau"]
# 			author_name = x["name"]
# 			author_xp = x["xp"]
# 			rank.append((n, author_name, author_niveau, author_xp))

# 		message = ""
# 		max_page = page*10
# 		if max_page > rank[-1][0]-1:
# 			max_page = rank[-1][0]

# 		for i in range((page-1)*10, max_page):
# 			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 		embed = discord.Embed(title="Clasement", description=message)

# 		embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 		max_page_nb = int(len(rank)/10)+1

# 		if page == 1 and page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 		elif page == 1:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 		elif page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 		else:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])

# 		while True:
# 			def check(res):
# 				return ctx.author == res.user and res.channel == ctx.channel
# 			res = await bot.wait_for("button_click", check=check)
# 			action = res.component.label
# 			if action == "Next Page":
# 				page += 1
# 			if action == "Previous Page":
# 				page -= 1

# 			message = ""
# 			max_page = page*10
# 			if max_page > rank[-1][0]-1:
# 				max_page = rank[-1][0]

# 			for i in range((page-1)*10, max_page):
# 				message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 			embed = discord.Embed(title="Clasement", description=message)

# 			embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 			if page == 1 and page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 			elif page == 1:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 			elif page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 			else:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])
# 	elif arg == "month" or arg == "mois" or arg == "saison":
# 		result = collection.find({}).sort(
# 			[("niveau_month", pymongo.DESCENDING), ("xp_month", pymongo.DESCENDING)])
# 		rank = []
# 		page = 1
# 		n = 0
# 		for x in result:
# 			n += 1
# 			author_niveau = x["niveau_month"]
# 			author_name = x["name"]
# 			author_xp = x["xp_month"]
# 			rank.append((n, author_name, author_niveau, author_xp))

# 		message = ""
# 		max_page = page*10
# 		if max_page > rank[-1][0]-1:
# 			max_page = rank[-1][0]

# 		for i in range((page-1)*10, max_page):
# 			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 		embed = discord.Embed(title="Clasement", description=message)

# 		embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 		max_page_nb = int(len(rank)/10)+1

# 		if page == 1 and page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 		elif page == 1:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 		elif page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 		else:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])

# 		while True:
# 			def check(res):
# 				return ctx.author == res.user and res.channel == ctx.channel
# 			res = await bot.wait_for("button_click", check=check)
# 			action = res.component.label
# 			if action == "Next Page":
# 				page += 1
# 			if action == "Previous Page":
# 				page -= 1

# 			message = ""
# 			max_page = page*10
# 			if max_page > rank[-1][0]-1:
# 				max_page = rank[-1][0]

# 			for i in range((page-1)*10, max_page):
# 				message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 			embed = discord.Embed(title="Clasement", description=message)

# 			embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 			if page == 1 and page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 			elif page == 1:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 			elif page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 			else:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])
# 	elif arg == "week" or arg == "semaine":
# 		result = collection.find({}).sort(
# 			[("niveau_week", pymongo.DESCENDING), ("xp_week", pymongo.DESCENDING)])
# 		rank = []
# 		page = 1
# 		n = 0
# 		for x in result:
# 			n += 1
# 			author_niveau = x["niveau_week"]
# 			author_name = x["name"]
# 			author_xp = x["xp_week"]
# 			rank.append((n, author_name, author_niveau, author_xp))

# 		message = ""
# 		max_page = page*10
# 		if max_page > rank[-1][0]-1:
# 			max_page = rank[-1][0]

# 		for i in range((page-1)*10, max_page):
# 			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 		embed = discord.Embed(title="Clasement", description=message)

# 		embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 		max_page_nb = int(len(rank)/10)+1

# 		if page == 1 and page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 		elif page == 1:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 		elif page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 		else:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])

# 		while True:
# 			def check(res):
# 				return ctx.author == res.user and res.channel == ctx.channel
# 			res = await bot.wait_for("button_click", check=check)
# 			action = res.component.label
# 			if action == "Next Page":
# 				page += 1
# 			if action == "Previous Page":
# 				page -= 1

# 			message = ""
# 			max_page = page*10
# 			if max_page > rank[-1][0]-1:
# 				max_page = rank[-1][0]

# 			for i in range((page-1)*10, max_page):
# 				message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\n"

# 			embed = discord.Embed(title="Clasement", description=message)

# 			embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 			if page == 1 and page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 			elif page == 1:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 			elif page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 			else:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])
# 	elif arg == "vote" or arg == "claim":
# 		url = f'https://api.top-serveurs.net/v1/servers/{TOKEN_TOP_SERVEUR}/players-ranking'
# 		reponse = requests.get(url)

# 		rank = []
# 		page = 1
# 		if 'json' in reponse.headers.get('Content-Type'):
# 			js = reponse.json()

# 			n = 0

# 			for player in js["players"]:
# 				playername = player["playername"]
# 				for i in ctx.author.guild.members:
# 					if playername in [i.name, i.nick]:
# 						n += 1
# 						vote = player["votes"]
# 						rank.append((n, playername, vote))
# 						break

# 		else:
# 			print('Response content is not in JSON format., on !claim')
# 			js = 'spam'
# 		message = ""
# 		max_page = page*10
# 		if max_page > rank[-1][0]-1:
# 			max_page = rank[-1][0]
# 		for i in range((page-1)*10, max_page):
# 			message += f"**{rank[i][0]}**. {rank[i][1]} à voté {rank[i][2]} fois\n"

# 		embed = discord.Embed(title="Clasement vote", description=message)

# 		embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 		max_page_nb = int(len(rank)/10)+1
# 		if page == 1 and page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 		elif page == 1:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 		elif page == max_page_nb:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 		else:
# 			m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])
# 		while True:
# 			def check(res):
# 				return ctx.author == res.user and res.channel == ctx.channel

# 			if action == "Next Page":
# 				page += 1
# 			if action == "Previous Page":
# 				page -= 1

# 			message = ""
# 			max_page = page*10
# 			if max_page > rank[-1][0]-1:
# 				max_page = rank[-1][0]

# 			for i in range((page-1)*10, max_page):
# 				message += f"**{rank[i][0]}**. {rank[i][1]} à voté {rank[i][2]} fois\n"

# 			embed = discord.Embed(title="Clasement", description=message)

# 			embed.set_footer(text=f"page {page}/{int(len(rank)/10)+1}")
# 			if page == 1 and page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page", disabled=True)]])
# 			elif page == 1:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page", disabled=True), Button(style=1, label="Next Page")]])
# 			elif page == max_page_nb:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page", disabled=True)]])
# 			else:
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="Previous Page"), Button(style=1, label="Next Page")]])


@bot.command(name='canvas')
@commands.check(check_if_it_is_me)
async def canvas(ctx):
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_niveau = x["niveau"]
		author_xp = x["xp"]

	IMAGE_WIDTH = 300
	IMAGE_HEIGHT = 100

	# create empty image 600x300
	# RGB, RGBA (with alpha), L (grayscale), 1 (black & white)
	image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT))

	# or load existing image
	#image = Image.open('/home/furas/images/lenna.png')

	# create object for drawing
	draw = ImageDraw.Draw(image)
	(44, 47, 51)
	# draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
	draw.rectangle([0, 0, IMAGE_WIDTH, IMAGE_HEIGHT],
	               fill=(44, 47, 51))  # Le grand réctangle
	draw.rounded_rectangle([98-27, 48, 302-27, 72], radius=20, fill=(61, 64, 68),
	                       outline=(35, 39, 42), width=2)  # le barre entière de niveau
	draw.rounded_rectangle([100-27, 50, 100-27 + (int(200*(author_xp/int(
		((author_niveau)**1.5)*10)))), 70], radius=20, fill=(21, 214, 30))  # l'xp
	# draw text_name
	text_name = f'{ctx.author.display_name}'

	font = ImageFont.truetype('Consolas.ttf', 11)

	text_width, text_height = draw.textsize(text_name, font=font)
	x = IMAGE_WIDTH - text_width - 27
	y = 80

	draw.text((x, y), text_name, fill=(255, 255, 255), font=font)

	# draw text_niveau
	text_niveau = f'Niveau : {author_niveau}'

	font = ImageFont.truetype('Consolas.ttf', 16)

	text_width, text_height = draw.textsize(text_niveau, font=font)
	x = 18 + 64 + 8
	y = (IMAGE_HEIGHT - text_height)//2 - 15

	draw.text((x, y), text_niveau, fill=(255, 255, 255), font=font)

	# draw text_xp
	text_xp = f'{author_xp}/{int(((author_niveau)**1.5)*10)}'

	font = ImageFont.truetype('Consolas.ttf', 14)

	text_width, text_height = draw.textsize(text_xp, font=font)
	x = 90
	y = 54

	draw.text((x, y), text_xp, fill=(0, 0, 0), font=font)

	# --- Avatare ---
	AVATAR_SIZE = 64
	avatar_asset = ctx.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

	# read JPG from server to buffer (file-like object)
	buffer_avatar = io.BytesIO()
	await avatar_asset.save(buffer_avatar)
	buffer_avatar.seek(0)

	# read JPG from buffer to Image
	avatar_image = Image.open(buffer_avatar)

	avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))

	circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
	circle_draw = ImageDraw.Draw(circle_image)
	circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
	#avatar_image.putalpha(circle_image)
	#avatar_image.show()

	image.paste(avatar_image, (18, (IMAGE_HEIGHT-AVATAR_SIZE)//2), circle_image)

	draw.ellipse((16, 16, 84, 84), outline=(30, 32, 33), width=3)

	# create buffer
	buffer = io.BytesIO()

	# save PNG in buffer
	image.save(buffer, format='PNG')

	# move to beginning of buffer so `send()` it will read from beginning
	buffer.seek(0)

	# send image
	await ctx.send(file=discord.File(buffer, 'myimage.png'))


# @bot.command(name='aventure', aliases=["adventure", "av","Adventure","Aventure","Av"])
# @commands.cooldown(1, 5, commands.BucketType.user)
# async def aventure(ctx):
# 	if not await check_if_aventurier(ctx):
# 		return
# 	author_id = ctx.author.id
# 	result = collection.find({"_id": author_id})
# 	coût_start_adventure = 1
# 	for x in result:
# 		author_hav_house = x["hav_house"]
# 		author_hav_sword = x["hav_sword"]
# 		author_magic_powder = x["magic_powder"]
# 		author_aventure = x["aventure"]
# 		author_pass_aventure = x["pass_aventure"]
# 		author_potion = x["potion"]
# 		author_sword = x["sword"]
# 	stuff = author_aventure[1]
# 	# n = author_aventure[0]
# 	aventure_id = author_aventure[2]
# 	if not author_hav_house:
# 		return ctx.send(f"Tu n'as pas encore de maison, pour commencer l'expédition, achetes-en une avec `!buy house`, l'ami {ctx.author.mention} !")
# 	if not author_hav_sword:
# 		return await ctx.send(f"Tu n'as pas encore d'épes, pour partir en expédition, y allé serais du suicide, vas en une avec `!buy sword`, l'ami {ctx.author.mention} !")
# 	if aventure_id != 0:
# 		await ctx.send(f"Tu as déjà une aventure en cours souhaite tu perdre toute ta progressions en recommençant une ?")
# 	else:
# 		if author_pass_aventure > 0:
# 			await ctx.channel.send(f"Voulez-vous vraiment commencé une aventure, cela coûte {coût_start_adventure} poudre magique ?, (say : yes or no),Vous avez aussi {author_pass_aventure} pass pour faire des aventures gratuitement si vous souhaiter l'utiliser ecriver 'pass' l'ami {ctx.author.mention} !")
# 		else:
# 			await ctx.channel.send(f"Voulez-vous vraiment commencé une aventure, cela coûte {coût_start_adventure} poudre magique ?, (say : yes or no), l'ami {ctx.author.mention} !")

# 	def check(message):
# 		return (message.author.id == ctx.message.author.id
# 		        and message.channel.id == ctx.message.channel.id
# 		        and message.content in ["y", "n", "yes", "no", "pass"])
# 	try:
# 		confimation = await bot.wait_for("message", timeout=30, check=check)
# 		confimation = confimation.content
# 		if confimation == "n" or confimation == "no":
# 			return await ctx.send(f"L'oppération a bien été intérompu, {ctx.author.mention}")
# 		elif confimation == "y" or confimation == "yes":
# 			if author_magic_powder < coût_start_adventure:
# 				return await ctx.send(f"Vous n'avez pas {coût_start_adventure} poudre magique, {ctx.author.mention}")
# 			collection.update_one({"_id": author_id}, {
# 			                      "$inc": {"magic_powder": -coût_start_adventure}})
# 		elif confimation == "pass" and author_pass_aventure > 0:
# 			collection.update_one({"_id": author_id}, {
# 			                      "$inc": {"pass_aventure": -1}})
# 		else:
# 			return await ctx.send(f"Vous n'avez pas de pass, {ctx.author.mention}")
# 	except:
# 		return await ctx.send(f"L'oppération a été intérompu car vous avez attendu trop longtemps, {ctx.author.mention}")

# 	next_nb_path = 5
# 	next_mort = randint(1, next_nb_path)
# 	next_tresors = randint(1, next_nb_path)
# 	while next_tresors == next_mort:
# 		next_tresors = randint(1, next_nb_path)

# 	embed = discord.Embed(
# 		title="Aventure", description=f"Vous avez le choix entre {next_nb_path} chemin, un des chemins est pigés, si vous l'emprinté il vous fait perdre tout le stuff que vous avez accumulé durant cette aventures, le(s) autre(s) vous amènes vers des événements aléatoires, si vous voulez rentrer à la maison avec tout votre butin vous pouvez cliqué sur \"Home back\"")
# 	button_list = []
# 	liste = []
# 	for i in range(1, next_nb_path+1):
# 		liste.append(Button(style=1, label=f"{i}"))

# 	button_list.append(liste)
# 	button_list.append([Button(style=2, label="Home back")])
# 	m = await ctx.channel.send(f"{ctx.author.mention}", embed=embed, components=button_list)
# 	aventure_id = m.id
# 	collection.update_one({"_id": author_id}, {
# 	                      "$set": {"aventure": [0, stuff, aventure_id]}})

# 	while True:

# 		def check(res):
# 			return ctx.author == res.user and res.channel == ctx.channel and res.message.id == aventure_id

# 		res = await bot.wait_for("button_click", check=check)
# 		action = res.component.label

# 		# nombre de chemin et le chemin "piege"
# 		nb_path = next_nb_path
# 		next_nb_path = randint(2, 5)
# 		mort = next_mort
# 		trésors = next_tresors
# 		next_mort = randint(1, next_nb_path)
# 		next_tresors = randint(1, next_nb_path)
# 		while next_tresors == next_mort:
# 			next_tresors = randint(1, next_nb_path)

# 		# Initialise les boutons en fonction du nombre de chemin
# 		button_list = []
# 		liste = []
# 		for i in range(1, next_nb_path+1):
# 			liste.append(Button(style=1, label=f"{i}"))

# 		button_list.append(liste)
# 		button_list.append([Button(style=2, label="Home back")])

# 		if str(mort) == str(action):
# 			embed = discord.Embed(
# 				title="Aventure", description=f"Vous êtes tomber dans un pièges vous avez tout perdu")
# 			init_stuff = {
# 				"bois": 0,
# 				"sève": 0,
# 				"poudre_magique": 0,
# 				"pierre": 0,
# 				"charbon": 0,
# 				"fer": 0,
# 				"or": 0,
# 				"diamant": 0,
# 				"électrum": 0,
# 				"dracolite": 0,
# 				"lave": 0,
# 				"géode": 0,
# 				"emeraude": 0,
# 				"saphire": 0,
# 				"rubis": 0,
# 				"quartz": 0,
# 				"potion": [0, 0, 0, 0]
# 			}
# 			collection.update_one({"_id": author_id}, {
# 			                      "$set": {"aventure": [0, init_stuff, 0]}})
# 			await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=4, label="Loose", disabled=True)]])
# 		elif str(action[3:]) in ["1", "10", "100", "1000"]:
# 			cant_trade = False
# 			message = ""
# 			if len(prix) == 1:
# 				result = collection.find({"_id": author_id})
# 				for x in result:
# 					author_0 = x[str(prix[0][3])]
# 				if author_0 < int(action[3:])*price_liste[0]:
# 					message += f"{int(action[3:])*price_liste[0]-author_0} {prix[0][2]}, "
# 					cant_trade = True
# 			elif len(prix) == 2:
# 				result = collection.find({"_id": author_id})
# 				for x in result:
# 					author_0 = x[str(prix[0][3])]
# 					author_1 = x[str(prix[1][3])]
# 				if author_0 < int(action[3:])*price_liste[0]:
# 					message += f"{int(action[3:])*price_liste[0]-author_0} {prix[0][2]}, "
# 					cant_trade = True
# 				if author_1 < int(action[3:])*price_liste[1]:
# 					message += f"{int(action[3:])*price_liste[1]-author_1} {prix[1][2]}, "
# 					cant_trade = True
# 			elif len(prix) == 3:
# 				result = collection.find({"_id": author_id})
# 				for x in result:
# 					author_0 = x[str(prix[0][3])]
# 					author_1 = x[str(prix[1][3])]
# 					author_2 = x[str(prix[2][3])]
# 				if author_0 < int(action[3:])*price_liste[0]:
# 					message += f"{int(action[3:])*price_liste[0]-author_0} {prix[0][2]}, "
# 					cant_trade = True
# 				if author_1 < int(action[3:])*price_liste[1]:
# 					message += f"{int(action[3:])*price_liste[1]-author_1} {prix[1][2]}, "
# 					cant_trade = True
# 				if author_2 < int(action[3:])*price_liste[2]:
# 					message += f"{int(action[3:])*price_liste[2]-author_2} {prix[2][2]}, "
# 					cant_trade = True

# 			if cant_trade:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"il vous manque {message[:-2]}")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="nb 1",), Button(style=1, label="nb 10"), Button(style=1, label="nb 100")], [Button(style=2, label="Back Adventure",)]])
# 			else:
# 				if len(prix) == 1:
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[0][3]): -price_liste[0]*int(action[3:])}})
# 				elif len(prix) == 2:
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[0][3]): -price_liste[0]*int(action[3:])}})
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[1][3]): -price_liste[1]*int(action)}})
# 				elif len(prix) == 3:
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[0][3]): -price_liste[0]*int(action[3:])}})
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[1][3]): -price_liste[1]*int(action[3:])}})
# 					collection.update_one({"_id": author_id}, {
# 					                      "$inc": {str(prix[2][3]): -price_liste[2]*int(action[3:])}})
# 				collection.update_one({"_id": author_id}, {
# 				                      "$inc": {str(contenue[3]): content*int(action[3:])}})
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous avez reçu {content*int(action[3:])} {contenue[2]}\nVous pouvez encore en acheter si vous le souhaiter")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="nb 1",), Button(style=1, label="nb 10"), Button(style=1, label="nb 100")], [Button(style=2, label="Back Adventure",)]])
# 		elif str(trésors) == str(action):

# 			rand = random()
# 			name_coffre = ""
# 			if 0 <= rand < 0.02:
# 				butin = choice(tresors_liste_légendaire)
# 				name_coffre = "__**Coffre légendaire**__"
# 			elif 0.02 <= rand < 0.15:
# 				butin = choice(tresors_liste_rare)
# 				name_coffre = "**Coffre épique**"
# 			elif 0.15 <= rand < 0.45:
# 				butin = choice(tresors_liste_uncommun)
# 				name_coffre = "__Coffre peu commun__"
# 			elif 0.45 <= rand <= 1:
# 				butin = choice(tresors_liste_commun)
# 				name_coffre = "*Coffre commun*"
# 			nb_butin = randint(butin[0], butin[1])
# 			if butin[2] != "potion":
# 				stuff[butin[2]] += nb_butin
# 			else:
# 				stuff["potion"][nb_butin] += 1
# 			embed = discord.Embed(
# 				title="Aventure", description=f"Tu viens à trouvé {nb_butin} {butin[2]} dans un {name_coffre}")

# 			bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 			pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 				"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 			géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 				"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 			potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 			message = ""
# 			thing = False
# 			if bois != 0:
# 				message += f"Bois: {bois}\n"
# 				thing = True
# 			if sève != 0:
# 				message += f"Sève: {sève}\n"
# 				thing = True
# 			if poudre_magique != 0:
# 				message += f"Poudre magique: {poudre_magique}\n"
# 				thing = True
# 			if pierre != 0:
# 				message += f"Pierre: {pierre}\n"
# 				thing = True
# 			if charbon != 0:
# 				message += f"Charbon: {charbon}\n"
# 				thing = True
# 			if fer != 0:
# 				message += f"Fer: {fer}\n"
# 				thing = True
# 			if or_ != 0:
# 				message += f"Or: {or_}\n"
# 				thing = True
# 			if diamant != 0:
# 				message += f"Diamant: {diamant}\n"
# 				thing = True
# 			if électrum != 0:
# 				message += f"Electrum: {électrum}\n"
# 				thing = True
# 			if dracolite != 0:
# 				message += f"Dracolite: {dracolite}\n"
# 				thing = True
# 			if lave != 0:
# 				message += f"Lave: {lave}\n"
# 				thing = True

# 			message2 = ""
# 			thing2 = False
# 			if géode_ != 0:
# 				message2 += f"Géode: {géode_}\n"
# 				thing2 = True
# 			if quartz != 0:
# 				message2 += f"Quartz: {quartz}\n"
# 				thing2 = True
# 			if emeraude != 0:
# 				message2 += f"Emeraude: {emeraude}\n"
# 				thing2 = True
# 			if saphire != 0:
# 				message2 += f"Saphire: {saphire}\n"
# 				thing2 = True
# 			if rubis != 0:
# 				message2 += f"Rubis: {rubis}\n"
# 				thing2 = True

# 			message3 = ""
# 			thing3 = False
# 			if potion_rouge != 0:
# 				message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 				thing3 = True
# 			if potion_rose != 0:
# 				message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 				thing3 = True
# 			if potion_bleu != 0:
# 				message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 				thing3 = True
# 			if potion_orange != 0:
# 				message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 				thing3 = True
# 			if thing:
# 				embed.add_field(name="**Matériaux de base récolté :**",
# 				                value=message, inline=True)
# 			if thing2:
# 				embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 			if thing3:
# 				embed.add_field(name="**Potion :**", value=message3)

# 			await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 		elif "Home back" == str(action):
# 			bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 			pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 				"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 			géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 				"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 			potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 			message4 = "Tu as réussis as collecter : "
# 			message = "**Ressource de base :** "
# 			thing = False
# 			if bois != 0:
# 				message += f"{bois} bois, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"wood": bois}})
# 				thing = True
# 			if sève != 0:
# 				message += f"{sève} sève, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"sap": sève}})
# 				thing = True
# 			if poudre_magique != 0:
# 				message += f"{poudre_magique} poudre magique, "
# 				collection.update_one({"_id": author_id}, {
# 				                      "$inc": {"magic_powder": poudre_magique}})
# 				thing = True
# 			if pierre != 0:
# 				message += f"{pierre} pierre, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"stone": pierre}})
# 				thing = True
# 			if charbon != 0:
# 				message += f"{charbon} charbon, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"coal": charbon}})
# 				thing = True
# 			if fer != 0:
# 				message += f"{fer} fer, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"iron": fer}})
# 				thing = True
# 			if or_ != 0:
# 				message += f"{or_} or, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"gold": or_}})
# 				thing = True
# 			if diamant != 0:
# 				message += f"{diamant} diamant, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"diamond": diamant}})
# 				thing = True
# 			if électrum != 0:
# 				message += f"{électrum} électrum, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"électrum": électrum}})
# 				thing = True
# 			if dracolite != 0:
# 				message += f"{dracolite} dracolite, "
# 				collection.update_one({"_id": author_id}, {
# 				                      "$inc": {"dracolite": dracolite}})
# 				thing = True
# 			if lave != 0:
# 				message += f"{lave} lave, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"lava": lave}})
# 				thing = True

# 			message2 = "**Ressource de pierre précieuse :** "
# 			thing2 = False
# 			if géode_ != 0:
# 				message2 += f"{géode_} géode, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"géode": géode_}})
# 				thing2 = True
# 			if quartz != 0:
# 				message2 += f"{quartz} quartz, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"quartz": quartz}})
# 				thing2 = True
# 			if emeraude != 0:
# 				message2 += f"{emeraude} émeraude, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"emerald": emeraude}})
# 				thing2 = True
# 			if saphire != 0:
# 				message2 += f"{saphire} saphire, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"sapphire": saphire}})
# 				thing2 = True
# 			if rubis != 0:
# 				message2 += f"{rubis} rubis, "
# 				collection.update_one({"_id": author_id}, {"$inc": {"ruby": rubis}})
# 				thing2 = True

# 			message3 = "**Potion :** "
# 			thing3 = False
# 			if potion_rouge != 0:
# 				message3 += f"{potion_rouge} potion de multiplicateur de ressources, "
# 				author_potion[0] += potion_rouge
# 				thing3 = True
# 			if potion_rose != 0:
# 				message3 += f"{potion_rose} potion d'amélioration d'item, "
# 				author_potion[1] += potion_rose
# 				thing3 = True
# 			if potion_bleu != 0:
# 				message3 += f"{potion_bleu} potion de `!vote` instantané, "
# 				author_potion[2] += potion_bleu
# 				thing3 = True
# 			if potion_orange != 0:
# 				message3 += f"{potion_orange}\n, potion de `!week` instantané, "
# 				author_potion[3] += potion_orange
# 				thing3 = True

# 			if not thing:
# 				message = "Ressource de base :** Rien  "
# 			if not thing2:
# 				message2 = "**Ressource de pierre précieuse :** Rien  "
# 			if not thing3:
# 				message3 = "**Potion :** Rien  "
# 			collection.update_one({"_id": author_id}, {
# 			                      "$set": {"potion": author_potion}})
# 			init_stuff = {
# 				"bois": 0,
# 				"sève": 0,
# 				"poudre_magique": 0,
# 				"pierre": 0,
# 				"charbon": 0,
# 				"fer": 0,
# 				"or": 0,
# 				"diamant": 0,
# 				"électrum": 0,
# 				"dracolite": 0,
# 				"lave": 0,
# 				"géode": 0,
# 				"emeraude": 0,
# 				"saphire": 0,
# 				"rubis": 0,
# 				"quartz": 0,
# 				"potion": [0, 0, 0, 0]
# 			}
# 			collection.update_one({"_id": author_id}, {
# 			                      "$set": {"aventure": [0, init_stuff, 0]}})
# 			embed = discord.Embed(title="Fin de l'aventure",
# 			                      description=f"Vous êtes revenue de l'aventure saint et sauf\n\nVoici ton butin :\n{message4}{message[:-2]} {message2[:-2]} {message3[:-2]}")
# 			await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Home", disabled=True)]])
# 		elif "Yes" == str(action):
# 			if event == 2:  # Petit mosntre

# 				name_little_monster = choice(petit_monstre)
# 				rand = random()
# 				if rand <= épée[author_sword][2]:
# 					rand = random()
# 					name_coffre = ""
# 					if 0 <= rand < 0.001:
# 						butin = choice(tresors_liste_légendaire)
# 						name_coffre = "__**Coffre légendaire**__"
# 					elif 0.001 <= rand < 0.01:
# 						butin = choice(tresors_liste_rare)
# 						name_coffre = "**Coffre épique**"
# 					elif 0.01 <= rand < 0.25:
# 						butin = choice(tresors_liste_uncommun)
# 						name_coffre = "__Coffre peu commun__"
# 					elif 0.25 <= rand <= 1:
# 						butin = choice(tresors_liste_commun)
# 						name_coffre = "*Coffre commun*"
# 					nb_butin = randint(butin[0], butin[1])
# 					if butin[2] != "potion":
# 						stuff[butin[2]] += nb_butin
# 					else:
# 						stuff["potion"][nb_butin] += 1
# 					embed = discord.Embed(
# 						title="Aventure", description=f"Vous avez affronté un {name_little_monster}\n\n Après un rude combat vous le gagné, il a laisser tomber un {name_coffre}, et dedans vous avez trouver **{nb_butin} {butin[2]}**")
# 					bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 					pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 						"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 					géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 						"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 					potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 					message = ""
# 					thing = False
# 					if bois != 0:
# 						message += f"Bois: {bois}\n"
# 						thing = True
# 					if sève != 0:
# 						message += f"Sève: {sève}\n"
# 						thing = True
# 					if poudre_magique != 0:
# 						message += f"Poudre magique: {poudre_magique}\n"
# 						thing = True
# 					if pierre != 0:
# 						message += f"Pierre: {pierre}\n"
# 						thing = True
# 					if charbon != 0:
# 						message += f"Charbon: {charbon}\n"
# 						thing = True
# 					if fer != 0:
# 						message += f"Fer: {fer}\n"
# 						thing = True
# 					if or_ != 0:
# 						message += f"Or: {or_}\n"
# 						thing = True
# 					if diamant != 0:
# 						message += f"Diamant: {diamant}\n"
# 						thing = True
# 					if électrum != 0:
# 						message += f"Electrum: {électrum}\n"
# 						thing = True
# 					if dracolite != 0:
# 						message += f"Dracolite: {dracolite}\n"
# 						thing = True
# 					if lave != 0:
# 						message += f"Lave: {lave}\n"
# 						thing = True
# 					message2 = ""
# 					thing2 = False
# 					if géode_ != 0:
# 						message2 += f"Géode: {géode_}\n"
# 						thing2 = True
# 					if quartz != 0:
# 						message2 += f"Quartz: {quartz}\n"
# 						thing2 = True
# 					if emeraude != 0:
# 						message2 += f"Emeraude: {emeraude}\n"
# 						thing2 = True
# 					if saphire != 0:
# 						message2 += f"Saphire: {saphire}\n"
# 						thing2 = True
# 					if rubis != 0:
# 						message2 += f"Rubis: {rubis}\n"
# 						thing2 = True

# 					message3 = ""
# 					thing3 = False
# 					if potion_rouge != 0:
# 						message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 						thing3 = True
# 					if potion_rose != 0:
# 						message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 						thing3 = True
# 					if potion_bleu != 0:
# 						message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 						thing3 = True
# 					if potion_orange != 0:
# 						message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 						thing3 = True
# 					if thing:
# 						embed.add_field(name="**Matériaux de base récolté :**",
# 						                value=message, inline=True)
# 					if thing2:
# 						embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 					if thing3:
# 						embed.add_field(name="**Potion :**", value=message3)
# 					await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 				else:
# 					embed = discord.Embed(
# 						title="Aventure", description=f"Vous êtes mort au combat...\nFaçe a un vulgaire {name_little_monster}")
# 					init_stuff = {
# 						"bois": 0,
# 						"sève": 0,
# 						"poudre_magique": 0,
# 						"pierre": 0,
# 						"charbon": 0,
# 						"fer": 0,
# 						"or": 0,
# 						"diamant": 0,
# 						"électrum": 0,
# 						"dracolite": 0,
# 						"lave": 0,
# 						"géode": 0,
# 						"emeraude": 0,
# 						"saphire": 0,
# 						"rubis": 0,
# 						"quartz": 0,
# 						"potion": [0, 0, 0, 0]
# 					}
# 					collection.update_one({"_id": author_id}, {
# 					                      "$set": {"aventure": [0, init_stuff, 0]}})
# 					await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=4, label="Loose", disabled=True)]])
# 			if event == 3:  # Gros mosntre
# 				if random() < épée[author_sword][4]:  # un Monstre légendaire apparait
# 					name_big_monster_lengendary = choice(gros_monstre_légendraire)
# 					rand = random()
# 					if rand <= 0.05:
# 						rand = random()
# 						name_coffre = ""
# 						if 0 <= rand < 0.6:
# 							butin = choice(tresors_liste_légendaire)
# 							name_coffre = "__**Coffre légendaire**__"
# 						elif 0.6 <= rand < 0.9:
# 							butin = choice(tresors_liste_rare)
# 							name_coffre = "**Coffre épique**"
# 						elif 0.9 <= rand <= 1:
# 							butin = choice(tresors_liste_uncommun)
# 							name_coffre = "__Coffre peu commun__"

# 						nb_butin = randint(butin[0], butin[1])
# 						if butin[2] != "potion":
# 							stuff[butin[2]] += nb_butin
# 						else:
# 							stuff["potion"][nb_butin] += 1
# 						embed = discord.Embed(
# 							title="Aventure", description=f"Je n'est qun seul mot a dire **Génie**, vous avez affronté un monstre légendaire, est vous êtes sortis victorieux contre un{name_big_monster_lengendary}\n\nIl a laisser tomber un {name_coffre}, et dedans vous avez trouver **{nb_butin} {butin[2]}**")
# 						bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 						pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 							"fer"], stuff["or"], stuff["diamant"], stuff["électrum"],			stuff["dracolite"], stuff["lave"]
# 						géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 							"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 						potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 						message = ""
# 						thing = False
# 						if bois != 0:
# 							message += f"Bois: {bois}\n"
# 							thing = True
# 						if sève != 0:
# 							message += f"Sève: {sève}\n"
# 							thing = True
# 						if poudre_magique != 0:
# 							message += f"Poudre magique: {poudre_magique}\n"
# 							thing = True
# 						if pierre != 0:
# 							message += f"Pierre: {pierre}\n"
# 							thing = True
# 						if charbon != 0:
# 							message += f"Charbon: {charbon}\n"
# 							thing = True
# 						if fer != 0:
# 							message += f"Fer: {fer}\n"
# 							thing = True
# 						if or_ != 0:
# 							message += f"Or: {or_}\n"
# 							thing = True
# 						if diamant != 0:
# 							message += f"Diamant: {diamant}\n"
# 							thing = True
# 						if électrum != 0:
# 							message += f"Electrum: {électrum}\n"
# 							thing = True
# 						if dracolite != 0:
# 							message += f"Dracolite: {dracolite}\n"
# 							thing = True
# 						if lave != 0:
# 							message += f"Lave: {lave}\n"
# 							thing = True

# 						message2 = ""
# 						thing2 = False
# 						if géode_ != 0:
# 							message2 += f"Géode: {géode_}\n"
# 							thing2 = True
# 						if quartz != 0:
# 							message2 += f"Quartz: {quartz}\n"
# 							thing2 = True
# 						if emeraude != 0:
# 							message2 += f"Emeraude: {emeraude}\n"
# 							thing2 = True
# 						if saphire != 0:
# 							message2 += f"Saphire: {saphire}\n"
# 							thing2 = True
# 						if rubis != 0:
# 							message2 += f"Rubis: {rubis}\n"
# 							thing2 = True

# 						message3 = ""
# 						thing3 = False
# 						if potion_rouge != 0:
# 							message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 							thing3 = True
# 						if potion_rose != 0:
# 							message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 							thing3 = True
# 						if potion_bleu != 0:
# 							message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 							thing3 = True
# 						if potion_orange != 0:
# 							message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 							thing3 = True
# 						if thing:
# 							embed.add_field(name="**Matériaux de base récolté :**",
# 							                value=message, inline=True)
# 						if thing2:
# 							embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 						if thing3:
# 							embed.add_field(name="**Potion :**", value=message3)

# 						await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 					else:
# 						embed = discord.Embed(
# 							title="Aventure", description=f"Wow, c'était un monstre légendaire, vous n'avez pas eu de chance, il vous a pulvairiser d'un seuk trait{name_big_monster_lengendary}")
# 						init_stuff = {
# 							"bois": 0,
# 							"sève": 0,
# 							"poudre_magique": 0,
# 							"pierre": 0,
# 							"charbon": 0,
# 							"fer": 0,
# 							"or": 0,
# 							"diamant": 0,
# 							"électrum": 0,
# 							"dracolite": 0,
# 							"lave": 0,
# 							"géode": 0,
# 							"emeraude": 0,
# 							"saphire": 0,
# 							"rubis": 0,
# 							"quartz": 0,
# 							"potion": [0, 0, 0, 0]
# 						}
# 						collection.update_one({"_id": author_id}, {
# 						                      "$set": {"aventure": [0, init_stuff, 0]}})
# 						await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=4, label="Loose", disabled=True)]])
# 				else:
# 					name_little_monster = choice(gros_monstre)
# 					rand = random()
# 					if rand <= épée[author_sword][3]:
# 						rand = random()
# 						name_coffre = ""
# 						if 0 <= rand < 0.1:
# 							butin = choice(tresors_liste_légendaire)
# 							name_coffre = "__**Coffre légendaire**__"
# 						elif 0.1 <= rand < 0.4:
# 							butin = choice(tresors_liste_rare)
# 							name_coffre = "**Coffre épique**"
# 						elif 0.4 <= rand < 0.99:
# 							butin = choice(tresors_liste_uncommun)
# 							name_coffre = "__Coffre peu commun__"
# 						elif 0.99 <= rand <= 1:
# 							butin = choice(tresors_liste_commun)
# 							name_coffre = "*Coffre commun*"
# 						nb_butin = randint(butin[0], butin[1])
# 						if butin[2] != "potion":
# 							stuff[butin[2]] += nb_butin
# 						else:
# 							stuff["potion"][nb_butin] += 1
# 						embed = discord.Embed(
# 							title="Aventure", description=f"Vous avez affronté un {name_little_monster}\n\n Après un rude combat vous le gagné, il a laisser tomber un {name_coffre}, et dedans vous avez trouver **{nb_butin} {butin[2]}**")
# 						bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 						pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 							"fer"], stuff["or"], stuff["diamant"], stuff["électrum"],			stuff["dracolite"], stuff["lave"]
# 						géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 							"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 						potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 						message = ""
# 						thing = False
# 						if bois != 0:
# 							message += f"Bois: {bois}\n"
# 							thing = True
# 						if sève != 0:
# 							message += f"Sève: {sève}\n"
# 							thing = True
# 						if poudre_magique != 0:
# 							message += f"Poudre magique: {poudre_magique}\n"
# 							thing = True
# 						if pierre != 0:
# 							message += f"Pierre: {pierre}\n"
# 							thing = True
# 						if charbon != 0:
# 							message += f"Charbon: {charbon}\n"
# 							thing = True
# 						if fer != 0:
# 							message += f"Fer: {fer}\n"
# 							thing = True
# 						if or_ != 0:
# 							message += f"Or: {or_}\n"
# 							thing = True
# 						if diamant != 0:
# 							message += f"Diamant: {diamant}\n"
# 							thing = True
# 						if électrum != 0:
# 							message += f"Electrum: {électrum}\n"
# 							thing = True
# 						if dracolite != 0:
# 							message += f"Dracolite: {dracolite}\n"
# 							thing = True
# 						if lave != 0:
# 							message += f"Lave: {lave}\n"
# 							thing = True

# 						message2 = ""
# 						thing2 = False
# 						if géode_ != 0:
# 							message2 += f"Géode: {géode_}\n"
# 							thing2 = True
# 						if quartz != 0:
# 							message2 += f"Quartz: {quartz}\n"
# 							thing2 = True
# 						if emeraude != 0:
# 							message2 += f"Emeraude: {emeraude}\n"
# 							thing2 = True
# 						if saphire != 0:
# 							message2 += f"Saphire: {saphire}\n"
# 							thing2 = True
# 						if rubis != 0:
# 							message2 += f"Rubis: {rubis}\n"
# 							thing2 = True

# 						message3 = ""
# 						thing3 = False
# 						if potion_rouge != 0:
# 							message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 							thing3 = True
# 						if potion_rose != 0:
# 							message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 							thing3 = True
# 						if potion_bleu != 0:
# 							message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 							thing3 = True
# 						if potion_orange != 0:
# 							message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 							thing3 = True
# 						if thing:
# 							embed.add_field(name="**Matériaux de base récolté :**",
# 							                value=message, inline=True)
# 						if thing2:
# 							embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 						if thing3:
# 							embed.add_field(name="**Potion :**", value=message3)

# 						await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 					else:
# 						embed = discord.Embed(
# 							title="Aventure", description=f"Vous êtes mort au combat...\nFaçe a un(e) {name_little_monster}")
# 						init_stuff = {
# 							"bois": 0,
# 							"sève": 0,
# 							"poudre_magique": 0,
# 							"pierre": 0,
# 							"charbon": 0,
# 							"fer": 0,
# 							"or": 0,
# 							"diamant": 0,
# 							"électrum": 0,
# 							"dracolite": 0,
# 							"lave": 0,
# 							"géode": 0,
# 							"emeraude": 0,
# 							"saphire": 0,
# 							"rubis": 0,
# 							"quartz": 0,
# 							"potion": [0, 0, 0, 0]
# 						}
# 						collection.update_one({"_id": author_id}, {
# 						                      "$set": {"aventure": [0, init_stuff, 0]}})
# 						await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=4, label="Loose", disabled=True)]])
# 			if event == 4:  # Marchand
# 				objet = choice(marchand)
# 				prix = objet[:-1]
# 				contenue = objet[-1]
# 				content = randint(contenue[0], contenue[1])
# 				message = "**Prix :**\n"
# 				price_liste = []
# 				for i in prix:
# 					price = randint(i[0], i[1])
# 					price_liste.append(price)
# 					message += f"{price} en {i[2]}, "
# 				message += "\n"
# 				message += f"**Contre :**\n{content} {contenue[2]}"
# 				embed = discord.Embed(
# 					title="Aventure", description=f"**Un marchand** vous propose l'échange suivant\n\n{message}\n\nSi vous souhaiter faire le trade,cliquer sur Yes")
# 				event = 6
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Yes",), Button(style=4, label="No",)]])
# 			if event == 5:  # Familler
# 				embed = discord.Embed(
# 					title="Aventure", description=f"vous avez clicker sur oui (famillier)")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 			if event == 6:  # Proposition
# 				embed = discord.Embed(title="Aventure", description=f"{message}")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=1, label="nb 1",), Button(style=1, label="nb 10"), Button(style=1, label="nb 100"), Button(style=1, label="nb 1000")], [Button(style=2, label="Back Adventure",)]])
# 		elif "No" == str(action):
# 			if event == 2:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Peureux que vous êtes vous avez fuis le combat")
# 				bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 				pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 					"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 				géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 					"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 				potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 				message = ""
# 				thing = False
# 				if bois != 0:
# 					message += f"Bois: {bois}\n"
# 					thing = True
# 				if sève != 0:
# 					message += f"Sève: {sève}\n"
# 					thing = True
# 				if poudre_magique != 0:
# 					message += f"Poudre magique: {poudre_magique}\n"
# 					thing = True
# 				if pierre != 0:
# 					message += f"Pierre: {pierre}\n"
# 					thing = True
# 				if charbon != 0:
# 					message += f"Charbon: {charbon}\n"
# 					thing = True
# 				if fer != 0:
# 					message += f"Fer: {fer}\n"
# 					thing = True
# 				if or_ != 0:
# 					message += f"Or: {or_}\n"
# 					thing = True
# 				if diamant != 0:
# 					message += f"Diamant: {diamant}\n"
# 					thing = True
# 				if électrum != 0:
# 					message += f"Electrum: {électrum}\n"
# 					thing = True
# 				if dracolite != 0:
# 					message += f"Dracolite: {dracolite}\n"
# 					thing = True
# 				if lave != 0:
# 					message += f"Lave: {lave}\n"
# 					thing = True
# 				message2 = ""
# 				thing2 = False
# 				if géode_ != 0:
# 					message2 += f"Géode: {géode_}\n"
# 					thing2 = True
# 				if quartz != 0:
# 					message2 += f"Quartz: {quartz}\n"
# 					thing2 = True
# 				if emeraude != 0:
# 					message2 += f"Emeraude: {emeraude}\n"
# 					thing2 = True
# 				if saphire != 0:
# 					message2 += f"Saphire: {saphire}\n"
# 					thing2 = True
# 				if rubis != 0:
# 					message2 += f"Rubis: {rubis}\n"
# 					thing2 = True
# 				if not thing:
# 					message = "Rien"
# 				if not thing2:
# 					message2 = "Rien"

# 				message3 = ""
# 				thing3 = False
# 				if potion_rouge != 0:
# 					message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 					thing3 = True
# 				if potion_rose != 0:
# 					message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 					thing3 = True
# 				if potion_bleu != 0:
# 					message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 					thing3 = True
# 				if potion_orange != 0:
# 					message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 					thing3 = True
# 				if thing:
# 					embed.add_field(name="**Matériaux de base récolté :**",
# 					                value=message, inline=True)
# 				if thing2:
# 					embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 				if thing3:
# 					embed.add_field(name="**Potion :**", value=message3)
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 			if event == 3:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Peureux que vous êtes vous avez fuis le combat")
# 				bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 				pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 					"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 				géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 					"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 				potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 				message = ""
# 				thing = False
# 				if bois != 0:
# 					message += f"Bois: {bois}\n"
# 					thing = True
# 				if sève != 0:
# 					message += f"Sève: {sève}\n"
# 					thing = True
# 				if poudre_magique != 0:
# 					message += f"Poudre magique: {poudre_magique}\n"
# 					thing = True
# 				if pierre != 0:
# 					message += f"Pierre: {pierre}\n"
# 					thing = True
# 				if charbon != 0:
# 					message += f"Charbon: {charbon}\n"
# 					thing = True
# 				if fer != 0:
# 					message += f"Fer: {fer}\n"
# 					thing = True
# 				if or_ != 0:
# 					message += f"Or: {or_}\n"
# 					thing = True
# 				if diamant != 0:
# 					message += f"Diamant: {diamant}\n"
# 					thing = True
# 				if électrum != 0:
# 					message += f"Electrum: {électrum}\n"
# 					thing = True
# 				if dracolite != 0:
# 					message += f"Dracolite: {dracolite}\n"
# 					thing = True
# 				if lave != 0:
# 					message += f"Lave: {lave}\n"
# 					thing = True
# 				message2 = ""
# 				thing2 = False
# 				if géode_ != 0:
# 					message2 += f"Géode: {géode_}\n"
# 					thing2 = True
# 				if quartz != 0:
# 					message2 += f"Quartz: {quartz}\n"
# 					thing2 = True
# 				if emeraude != 0:
# 					message2 += f"Emeraude: {emeraude}\n"
# 					thing2 = True
# 				if saphire != 0:
# 					message2 += f"Saphire: {saphire}\n"
# 					thing2 = True
# 				if rubis != 0:
# 					message2 += f"Rubis: {rubis}\n"
# 					thing2 = True
# 				if not thing:
# 					message = "Rien"
# 				if not thing2:
# 					message2 = "Rien"

# 				message3 = ""
# 				thing3 = False
# 				if potion_rouge != 0:
# 					message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 					thing3 = True
# 				if potion_rose != 0:
# 					message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 					thing3 = True
# 				if potion_bleu != 0:
# 					message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 					thing3 = True
# 				if potion_orange != 0:
# 					message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 					thing3 = True
# 				if thing:
# 					embed.add_field(name="**Matériaux de base récolté :**",
# 					                value=message, inline=True)
# 				if thing2:
# 					embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 				if thing3:
# 					embed.add_field(name="**Potion :**", value=message3)
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 			if event == 4:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"vous avez snobé le marchant")
# 				bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 				pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 					"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 				géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 					"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 				potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 				message = ""
# 				thing = False
# 				if bois != 0:
# 					message += f"Bois: {bois}\n"
# 					thing = True
# 				if sève != 0:
# 					message += f"Sève: {sève}\n"
# 					thing = True
# 				if poudre_magique != 0:
# 					message += f"Poudre magique: {poudre_magique}\n"
# 					thing = True
# 				if pierre != 0:
# 					message += f"Pierre: {pierre}\n"
# 					thing = True
# 				if charbon != 0:
# 					message += f"Charbon: {charbon}\n"
# 					thing = True
# 				if fer != 0:
# 					message += f"Fer: {fer}\n"
# 					thing = True
# 				if or_ != 0:
# 					message += f"Or: {or_}\n"
# 					thing = True
# 				if diamant != 0:
# 					message += f"Diamant: {diamant}\n"
# 					thing = True
# 				if électrum != 0:
# 					message += f"Electrum: {électrum}\n"
# 					thing = True
# 				if dracolite != 0:
# 					message += f"Dracolite: {dracolite}\n"
# 					thing = True
# 				if lave != 0:
# 					message += f"Lave: {lave}\n"
# 					thing = True
# 				message2 = ""
# 				thing2 = False
# 				if géode_ != 0:
# 					message2 += f"Géode: {géode_}\n"
# 					thing2 = True
# 				if quartz != 0:
# 					message2 += f"Quartz: {quartz}\n"
# 					thing2 = True
# 				if emeraude != 0:
# 					message2 += f"Emeraude: {emeraude}\n"
# 					thing2 = True
# 				if saphire != 0:
# 					message2 += f"Saphire: {saphire}\n"
# 					thing2 = True
# 				if rubis != 0:
# 					message2 += f"Rubis: {rubis}\n"
# 					thing2 = True
# 				if not thing:
# 					message = "Rien"
# 				if not thing2:
# 					message2 = "Rien"

# 				message3 = ""
# 				thing3 = False
# 				if potion_rouge != 0:
# 					message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 					thing3 = True
# 				if potion_rose != 0:
# 					message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 					thing3 = True
# 				if potion_bleu != 0:
# 					message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 					thing3 = True
# 				if potion_orange != 0:
# 					message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 					thing3 = True
# 				if thing:
# 					embed.add_field(name="**Matériaux de base récolté :**",
# 					                value=message, inline=True)
# 				if thing2:
# 					embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 				if thing3:
# 					embed.add_field(name="**Potion :**", value=message3)
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 			if event == 5:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"vous avez clicker sur non (famillier)")
# 				bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 				pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 					"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 				géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 					"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 				potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 				message = ""
# 				thing = False
# 				if bois != 0:
# 					message += f"Bois: {bois}\n"
# 					thing = True
# 				if sève != 0:
# 					message += f"Sève: {sève}\n"
# 					thing = True
# 				if poudre_magique != 0:
# 					message += f"Poudre magique: {poudre_magique}\n"
# 					thing = True
# 				if pierre != 0:
# 					message += f"Pierre: {pierre}\n"
# 					thing = True
# 				if charbon != 0:
# 					message += f"Charbon: {charbon}\n"
# 					thing = True
# 				if fer != 0:
# 					message += f"Fer: {fer}\n"
# 					thing = True
# 				if or_ != 0:
# 					message += f"Or: {or_}\n"
# 					thing = True
# 				if diamant != 0:
# 					message += f"Diamant: {diamant}\n"
# 					thing = True
# 				if électrum != 0:
# 					message += f"Electrum: {électrum}\n"
# 					thing = True
# 				if dracolite != 0:
# 					message += f"Dracolite: {dracolite}\n"
# 					thing = True
# 				if lave != 0:
# 					message += f"Lave: {lave}\n"
# 					thing = True
# 				message2 = ""
# 				thing2 = False
# 				if géode_ != 0:
# 					message2 += f"Géode: {géode_}\n"
# 					thing2 = True
# 				if quartz != 0:
# 					message2 += f"Quartz: {quartz}\n"
# 					thing2 = True
# 				if emeraude != 0:
# 					message2 += f"Emeraude: {emeraude}\n"
# 					thing2 = True
# 				if saphire != 0:
# 					message2 += f"Saphire: {saphire}\n"
# 					thing2 = True
# 				if rubis != 0:
# 					message2 += f"Rubis: {rubis}\n"
# 					thing2 = True
# 				if not thing:
# 					message = "Rien"
# 				if not thing2:
# 					message2 = "Rien"

# 				message3 = ""
# 				thing3 = False
# 				if potion_rouge != 0:
# 					message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 					thing3 = True
# 				if potion_rose != 0:
# 					message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 					thing3 = True
# 				if potion_bleu != 0:
# 					message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 					thing3 = True
# 				if potion_orange != 0:
# 					message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 					thing3 = True
# 				if thing:
# 					embed.add_field(name="**Matériaux de base récolté :**",
# 					                value=message, inline=True)
# 				if thing2:
# 					embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 				if thing3:
# 					embed.add_field(name="**Potion :**", value=message3)
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 		elif str(action) == "Back Adventure":
# 			embed = discord.Embed(
# 				title="Aventure", description=f"De retour dans l'aventure, Bonne chance mon gaillard")
# 			bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 			pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 				"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 			géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 				"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 			potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 			message = ""
# 			thing = False
# 			if bois != 0:
# 				message += f"Bois: {bois}\n"
# 				thing = True
# 			if sève != 0:
# 				message += f"Sève: {sève}\n"
# 				thing = True
# 			if poudre_magique != 0:
# 				message += f"Poudre magique: {poudre_magique}\n"
# 				thing = True
# 			if pierre != 0:
# 				message += f"Pierre: {pierre}\n"
# 				thing = True
# 			if charbon != 0:
# 				message += f"Charbon: {charbon}\n"
# 				thing = True
# 			if fer != 0:
# 				message += f"Fer: {fer}\n"
# 				thing = True
# 			if or_ != 0:
# 				message += f"Or: {or_}\n"
# 				thing = True
# 			if diamant != 0:
# 				message += f"Diamant: {diamant}\n"
# 				thing = True
# 			if électrum != 0:
# 				message += f"Electrum: {électrum}\n"
# 				thing = True
# 			if dracolite != 0:
# 				message += f"Dracolite: {dracolite}\n"
# 				thing = True
# 			if lave != 0:
# 				message += f"Lave: {lave}\n"
# 				thing = True
# 			message2 = ""
# 			thing2 = False
# 			if géode_ != 0:
# 				message2 += f"Géode: {géode_}\n"
# 				thing2 = True
# 			if quartz != 0:
# 				message2 += f"Quartz: {quartz}\n"
# 				thing2 = True
# 			if emeraude != 0:
# 				message2 += f"Emeraude: {emeraude}\n"
# 				thing2 = True
# 			if saphire != 0:
# 				message2 += f"Saphire: {saphire}\n"
# 				thing2 = True
# 			if rubis != 0:
# 				message2 += f"Rubis: {rubis}\n"
# 				thing2 = True
# 			if not thing:
# 				message = "Rien"
# 			if not thing2:
# 				message2 = "Rien"
# 			message3 = ""
# 			thing3 = False
# 			if potion_rouge != 0:
# 				message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 				thing3 = True
# 			if potion_rose != 0:
# 				message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 				thing3 = True
# 			if potion_bleu != 0:
# 				message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 				thing3 = True
# 			if potion_orange != 0:
# 				message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 				thing3 = True
# 			if thing:
# 				embed.add_field(name="**Matériaux de base récolté :**",
# 				                value=message, inline=True)
# 			if thing2:
# 				embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 			if thing3:
# 				embed.add_field(name="**Potion :**", value=message3)
# 			await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 		else:

# 			bois, sève, poudre_magique = stuff["bois"], stuff["sève"], stuff["poudre_magique"]
# 			pierre, charbon, fer, or_, diamant, électrum, dracolite, lave = stuff["pierre"], stuff["charbon"], stuff[
# 				"fer"], stuff["or"], stuff["diamant"], stuff["électrum"], stuff["dracolite"], stuff["lave"]
# 			géode_, quartz, emeraude, saphire, rubis = stuff["géode"], stuff[
# 				"quartz"], stuff["emeraude"], stuff["saphire"], stuff["rubis"]
# 			potion_rouge, potion_rose, potion_bleu, potion_orange = stuff["potion"]
# 			message = ""
# 			thing = False
# 			if bois != 0:
# 				message += f"Bois: {bois}\n"
# 				thing = True
# 			if sève != 0:
# 				message += f"Sève: {sève}\n"
# 				thing = True
# 			if poudre_magique != 0:
# 				message += f"Poudre magique: {poudre_magique}\n"
# 				thing = True
# 			if pierre != 0:
# 				message += f"Pierre: {pierre}\n"
# 				thing = True
# 			if charbon != 0:
# 				message += f"Charbon: {charbon}\n"
# 				thing = True
# 			if fer != 0:
# 				message += f"Fer: {fer}\n"
# 				thing = True
# 			if or_ != 0:
# 				message += f"Or: {or_}\n"
# 				thing = True
# 			if diamant != 0:
# 				message += f"Diamant: {diamant}\n"
# 				thing = True
# 			if électrum != 0:
# 				message += f"Electrum: {électrum}\n"
# 				thing = True
# 			if dracolite != 0:
# 				message += f"Dracolite: {dracolite}\n"
# 				thing = True
# 			if lave != 0:
# 				message += f"Lave: {lave}\n"
# 				thing = True
# 			message2 = ""
# 			thing2 = False
# 			if géode_ != 0:
# 				message2 += f"Géode: {géode_}\n"
# 				thing2 = True
# 			if quartz != 0:
# 				message2 += f"Quartz: {quartz}\n"
# 				thing2 = True
# 			if emeraude != 0:
# 				message2 += f"Emeraude: {emeraude}\n"
# 				thing2 = True
# 			if saphire != 0:
# 				message2 += f"Saphire: {saphire}\n"
# 				thing2 = True
# 			if rubis != 0:
# 				message2 += f"Rubis: {rubis}\n"
# 				thing2 = True
# 			if not thing:
# 				message = "Rien"
# 			if not thing2:
# 				message2 = "Rien"

# 			message3 = ""
# 			thing3 = False
# 			if potion_rouge != 0:
# 				message3 += f"Potion de multiplicateur de ressources: {potion_rouge}\n"
# 				thing3 = True
# 			if potion_rose != 0:
# 				message3 += f"Potion d'amélioration d'item: {potion_rose}\n"
# 				thing3 = True
# 			if potion_bleu != 0:
# 				message3 += f"Potion de `!vote` instantané: {potion_bleu}\n"
# 				thing3 = True
# 			if potion_orange != 0:
# 				message3 += f"Potion de `!week` instantané: {potion_orange}\n"
# 				thing3 = True
# 			#if thing:
# 				#embed.add_field(name="**Matériaux de base récolté :**", value =message,inline=True)
# 			#if thing2:
# 			#	embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 			#if thing3:
# 				#embed.add_field(name="**Potion :**", value=message3)
# 			event = choice([1]*20 + [2]*50 + [3]*20 + [4]*10 + [5]*0)
# 			if event == 1:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous avez emprinté le chemin *sans encombres*")
# 				if thing:
# 					embed.add_field(name="**Matériaux de base récolté :**",
# 					                value=message, inline=True)
# 				if thing2:
# 					embed.add_field(name="**Pierres précieuses récolté :**", value=message2)
# 				if thing3:
# 					embed.add_field(name="**Potion :**", value=message3)
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=button_list)
# 			if event == 2:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous venez de rencontrer **un petit monstre** souhaitez vous l'affronter ?")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Yes",), Button(style=4, label="No",)]])
# 			if event == 3:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous venez de rencontrer **un gros monstre** souhaitez vous l'affronter ?")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Yes",), Button(style=4, label="No",)]])
# 			if event == 4:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous venez de rencontrer **un marchand** souhaitez vous commercer avec lui ?")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Yes",), Button(style=4, label="No",)]])
# 			if event == 5:
# 				embed = discord.Embed(
# 					title="Aventure", description=f"Vous avez trouver **un famillier** sur la route souhaitez-vous essyer de l'aprivoiser")
# 				await m.edit(f"{ctx.author.mention}", embed=embed, components=[[Button(style=3, label="Yes",), Button(style=4, label="No",)]])


@bot.command(name='récompense_week')
@commands.check(check_if_it_is_me)
async def récompense_week(ctx):
	if not await check_if_aventurier(ctx):
		return
	result = collection.find({}).sort(
		[("niveau_week", pymongo.DESCENDING), ("xp_week", pymongo.DESCENDING)])
	rank = []
	page = 1
	for n, x in enumerate(result, start=1):
		author_niveau = x["niveau_week"]
		author_name = x["name"]
		author_id = x["_id"]
		author_xp = x["xp_week"]
		author_potion = x["potion"]
		rank.append((n, author_name, author_niveau,
		            author_xp, author_id, author_potion))

	message = ""
	max_page = page*10
	if max_page > rank[-1][0]-1:
		max_page = rank[-1][0]

	for i in range((page-1)*10, max_page):
		if i == 0:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!week`\n\n"
			rank[i][5][3] += 1
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		elif i == 1:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 3 potion de `!vote`\n\n"
			rank[i][5][2] += 3
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		if i in [2, 3, 4]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 2 potion de `!vote`\n\n"
			rank[i][5][2] += 2
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		if i in [5, 6, 7, 8, 9]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!vote`\n\n"
			rank[i][5][2] += 1
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
	embed = discord.Embed(title="Clasement de la semaine", description=message)

	embed.set_footer(text=f"Bien joué à tous <3")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {"$set": {"niveau_week": 1}})
		collection.update_one({"_id": auhtor_id}, {"$set": {"xp_week": 0}})
	await ctx.send("C'est fait chef")
	channel_recompense = discord.utils.find(
		lambda c: c.id == channel_recompense_mentuel_hebdomadaire, ctx.author.guild.channels)
	await channel_recompense.send(embed=embed)


@bot.command(name='récompense_month')
@commands.check(check_if_it_is_me)
async def récompense_month(ctx):
	if not await check_if_aventurier(ctx):
		return
	result = collection.find({}).sort(
		[("niveau_month", pymongo.DESCENDING), ("xp_month", pymongo.DESCENDING)])
	rank = []
	page = 1
	for n, x in enumerate(result, start=1):
		author_niveau = x["niveau_month"]
		author_name = x["name"]
		author_id = x["_id"]
		author_xp = x["xp_month"]
		author_potion = x["potion"]
		rank.append((n, author_name, author_niveau,
		            author_xp, author_id, author_potion))

	message = ""
	max_page = page*10
	if max_page > rank[-1][0]-1:
		max_page = rank[-1][0]

	for i in range((page-1)*10, max_page):

		if i == 0:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 5 potion de `!week`,\n\n"
			rank[i][5][3] += 5
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		elif i == 1:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 3 potion de `!week`\n\n"
			rank[i][5][3] += 3
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		if i in [2, 3, 4]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 2 potion de `!week`\n\n"
			rank[i][5][3] += 2
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
		if i in [5, 6, 7, 8, 9]:
			message += f"**{rank[i][0]}**. __{rank[i][1]}__, Niveau : **{rank[i][2]}**, xp : *{rank[i][3]}/{int(((rank[i][2])**1.5)*10)}*\nRécompense : 1 potion de `!week`\n\n"
			rank[i][5][3] += 1
			collection.update_one({"_id": rank[i][4]}, {"$set": {"potion": rank[i][5]}})
	embed = discord.Embed(title="Clasement du mois", description=message)

	embed.set_footer(text=f"Bien joué à tous <3")
	result = collection.find()
	for x in result:
		auhtor_id = x["_id"]
		collection.update_one({"_id": auhtor_id}, {"$set": {"niveau_month": 1}})
		collection.update_one({"_id": auhtor_id}, {"$set": {"xp_month": 0}})
	await ctx.send("C'est fait chef")
	channel_recompense = discord.utils.find(
		lambda c: c.id == channel_recompense_mentuel_hebdomadaire, ctx.author.guild.channels)
	await channel_recompense.send(embed=embed)


@bot.command(name='expedition', aliases=["expédition","Expedition","Expédition"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def expedition(ctx):
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_biome = x["biome"]
		author_cooldown_expedition = x["cooldown_!expedition"]
	rand = random()

	t2 = int(time())

	t = int(author_cooldown_expedition - t2)

	if t > 0:
		if t >= 3600:
			t3 = strftime('%H %M %S', gmtime(t)).split(" ")
			message = "{}h {}m {}s".format(t3[0], t3[1], t3[2])
		elif t >= 60:
			t3 = strftime('%M %S', gmtime(t)).split(" ")
			message = "{}m {}s".format(t3[0], t3[1])
		else:
			t3 = strftime('%S', gmtime(t)).split(" ")
			message = "{}s".format(t3[0])

		return await ctx.send("{}, réessayer dans {}".format(ctx.author.mention, message))


	message = "Vous venez de trouver un biome : "
	if 0<=rand<0.001: # Mythique 0.1%
		message += "**__Mythique__**"
		découverte_biome = choice(biomes["Mythique"])
		if découverte_biome in author_biome["Mythique"]:
			message += f"\nVous avez découvert le biome {découverte_biome}, mais vous l'avez déjà découvert..., l'ami {ctx.author.mention}"
		else:
			message+= f"\nFélicitation vous avez découvert un nouveau biome, {découverte_biome}, l'ami {ctx.author.mention}"
			author_biome["Mythique"].append(découverte_biome)
			collection.update_one({"_id": author_id}, {"$set": {"biome": author_biome}})

	elif 0.001<=rand<0.001 + 0.01: # Légendaire 1%
		message += "**__Légendaire__**"
		découverte_biome = choice(biomes["Légendaire"])
		if découverte_biome in author_biome["Légendaire"]:
			message += f"\nVous avez découvert le biome {découverte_biome}, mais vous l'avez déjà découvert..., l'ami {ctx.author.mention}"
		else:
			message+= f"\nFélicitation vous avez découvert un nouveau biome, {découverte_biome}, l'ami {ctx.author.mention}"
			author_biome["Légendaire"].append(découverte_biome)
			collection.update_one({"_id": author_id}, {"$set": {"biome": author_biome}})
	elif 0.001 + 0.01<=rand<0.001 + 0.01 + 0.1: # Rare 10%
		message += "**Rare**"
		découverte_biome = choice(biomes["Rare"])
		if découverte_biome in author_biome["Rare"]:
			message += f"\nVous avez découvert le biome {découverte_biome}, mais vous l'avez déjà découvert..., l'ami {ctx.author.mention}"
		else:
			message+= f"\nFélicitation vous avez découvert un nouveau biome, {découverte_biome}, l'ami {ctx.author.mention}"
			author_biome["Rare"].append(découverte_biome)
			collection.update_one({"_id": author_id}, {"$set": {"biome": author_biome}})
	elif 0.001 + 0.01 + 0.1<=rand<0.001 + 0.01 + 0.1 + 0.35: # peu Commun 35%
		message += "**Peu Commun**"
		découverte_biome = choice(biomes["Peu_commun"])
		if découverte_biome in author_biome["Peu_commun"]:
			message += f"\nVous avez découvert le biome {découverte_biome}, mais vous l'avez déjà découvert..., l'ami {ctx.author.mention}"
		else:
			message+= f"\nFélicitation vous avez découvert un nouveau biome, {découverte_biome}, l'ami {ctx.author.mention}"
			author_biome["Peu_commun"].append(découverte_biome)
			collection.update_one({"_id": author_id}, {"$set": {"biome": author_biome}})
	else: # Commun 54%
		message += "**Commun**"
		découverte_biome = choice(biomes["Commun"])
		if découverte_biome in author_biome["Commun"]:
			message += f"\nVous avez découvert le biome {découverte_biome}, mais vous l'avez déjà découvert..., l'ami {ctx.author.mention}"
		else:
			message+= f"\nFélicitation vous avez découvert un nouveau biome, {découverte_biome}, l'ami {ctx.author.mention}"
			author_biome["Commun"].append(découverte_biome)
			collection.update_one({"_id": author_id}, {"$set": {"biome": author_biome}})
	collection.update_one({"_id": author_id}, {"$inc": {"!expedition": 1}})
	collection.update_one({"_id": author_id}, {"$set": {"cooldown_!expedition": t2+60*60*3}})
	await ctx.send(f"{message}")


@bot.command(name='biome', aliases=["biomes","Biome","Biomes"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def biome(ctx, arg="qg58sdfdsyue4qsk"):
	if not await check_if_aventurier(ctx):
		return

	author_id = ctx.author.id
	result = collection.find({"_id": author_id})
	for x in result:
		author_biome = x["biome"]
		author_current_biome = x["current_biome"]
		author_cooldown_biome = x["cooldown_!biome"]
	t2 = int(time())
	if arg != "qg58sdfdsyue4qsk":
		t = int(author_cooldown_biome - t2)
		if t > 0:
			if t >= 3600:
				t3 = strftime('%H %M %S', gmtime(t)).split(" ")
				message = "{}h {}m {}s".format(t3[0], t3[1], t3[2])
			elif t >= 60:
				t3 = strftime('%M %S', gmtime(t)).split(" ")
				message = "{}m {}s".format(t3[0], t3[1])
			else:
				t3 = strftime('%S', gmtime(t)).split(" ")
				message = "{}s".format(t3[0])

			return await ctx.send("{}, vous êtes trop fatiguer pour vous déplacer, réésayer dans {}".format(ctx.author.mention, message))
	rareters = ["Commun","Peu_commun","Rare","Légendaire","Mythique"]
	if arg == "qg58sdfdsyue4qsk":
		message = f"Vous êtes actuellement dans le biome {author_current_biome}\n\n\nVos biome : \n\n"
		for rareter in rareters:
			lieux = author_biome[rareter]
			if lieux  != []:
				if rareter == "Commun":
					message += "**Commun :**\n"
				elif rareter == "Peu_commun":
					message += "**Peu Commun :**\n"
				elif rareter == "Rare":
					message += "**Rare :**\n"
				elif rareter == "Légendaire":
					message += "**Légendaire :**\n"
				elif rareter == "Mythique":
					message += "**Mythique :**\n"
				for i in range(len(lieux)):
					# Commun
					if lieux[i] == "Plaine":
						message += "- **Plaine** : [Rien]\n"
					elif lieux[i] == "Forêt":
						message += "- **Forêt** : [Bois x1.5]\n"
					elif lieux[i] == "Carrière":
						message += "- **Carrière** : [Pierre x1.5]\n"
					# Peu Commun
					elif lieux[i] == "Grande forêt":
						message += "- **Grande forêt** : [Bois x4] [Pierre /4]\n"
					elif lieux[i] == "Grande carrière":
						message += "- **Grande carrière** : [Pierre x4] [Bois /4]\n"
					elif lieux[i] == "Grotte":
						message += "- **Grotte** : [Pierre x2, Fer x1.5, Or x1.5, Charbon obtenable (1"+"%"+" d'obtenir 50 charbon)] [pas de `!wood`]\n"
					# Rare
					elif lieux[i] == "Grosse grotte":
						message += "- **Grosse grotte** : [Pierre x1.5, Fer x2, Or x2, Charbon obtenable (5"+"%"+" d'obtenir 100 charbon)] [pas de `!wood`]\n"
					elif lieux[i] == "Forêt d'érable":
						message += "- **Forêt d'érable** : [Bois x1.5, Sève x2] [Pierre /1.5]\n"
					elif lieux[i] == "Forêt Ancienne":
						message += "- **Forêt Ancienne** : [Charbon obtenable (20"+"%"+" d'obtenir 100 charbon)] [Pas de `!mine`, Bois /2, Pas de sève]\n"
					# Légendaire
					elif lieux[i] == "Volcan":
						message += "- **Volcan** : [Pierre x2, Lave obtenable (5"+"%"+" d'obtenir 1 sceau de lave)] [pas de `!wood`]\n"
					elif lieux[i] == "Météorite":
						message += "- **Météorite** : [Acier obtenable (20"+"%"+" d'obtenir 5 Acier), Géode x1.5] [pas de `!wood`]\n"
					elif lieux[i] == "Montagne éléctrique":
						message += "- **Montagne éléctrique** : [Pierre x1.5, Or x3, Electrum obtenable (1"+"%"+" d'obtenir 1 électrum)] [Pas de `!wood`]\n"
					# Mythique
					if lieux[i] == "Forêt féérique":
						message += "- **Forêt féérique** : [Bois x1.5, Poudre magique 1 chance sur 50] [Pas de `!mine`]\n"
					elif lieux[i] == "Nid du dragon":
						message += "- **Nid du dragon** : [**Que** 1 chance sur 200 d'obtenir une dracolite] [il n'y a que de la dracolite dans le `!mine` et pas de `!wood`]\n"
					elif lieux[i] == "Pierre précieuse":
						message += "- **Pierre précieuse** : [**Que** 30 chance sur 100 d'obtenir une émeraud, 8 chance sur 100 d'obtenir un saphir et 1 chance sur 100 d'obtenir un rubis]\n"
				message += "\n"

		embed = discord.Embed(title=f"Biome de {ctx.author.display_name}",description=message)
		await ctx.send(f"{ctx.author.mention}",embed=embed)

	elif arg == "current" or arg == "actuel" or arg == "actuelle" or arg == "actuels" or arg == "actuelles":
		message = f"Vous êtes actuellement dans le biome {author_current_biome}\n\n"
		embed = discord.Embed(title=f"Biome de {ctx.author.display_name}",description=message)
		await ctx.send(f"{ctx.author.mention}", embed=embed)
	elif arg in ["Plaine","plaine"]:
		if "Plaine" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Plaine**, l'ami {ctx.author.mention}")
		elif "Plaine" in author_biome["Commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Plaine"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": 0}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Plaine**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome **Plaine**, l'ami {ctx.author.mention}")
	elif arg in ["Forêt","forêt","foret","Foret"]:
		if "Forêt" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Forêt**, l'ami {ctx.author.mention}")
		elif "Forêt" in author_biome["Commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Forêt"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Forêt**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Forêt**, l'ami {ctx.author.mention}")
	elif arg in ["Carrière","carière","Carriere","carriere"]:
		if "Carrière" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Carrière**, l'ami {ctx.author.mention}")
		elif "Carrière" in author_biome["Commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Carrière"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Carrière**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Carrière**, l'ami {ctx.author.mention}")


	elif arg in ["Grande_forêt","Grande_foret","grande_forêt","grande_foret"]:
		if "Grande forêt" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Grande forêt**, l'ami {ctx.author.mention}")
		elif "Grande forêt" in author_biome["Peu_commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Grande forêt"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*3}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Grande forêt**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Grande forêt**, l'ami {ctx.author.mention}")
	elif arg in ["Grande_carrière","grande_carrière","Grande_carriere","grande_carriere"]:
		if "Grande carrière" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Grande carrière**, l'ami {ctx.author.mention}")
		elif "Grande carrière" in author_biome["Peu_commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Grande carrière"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*3}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Grande carrière**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Grande carrière**, l'ami {ctx.author.mention}")
	elif arg in ["Grotte","grotte","Grote","grote"]:
		if "Grotte" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Grotte**, l'ami {ctx.author.mention}")
		elif "Grotte" in author_biome["Peu_commun"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Grotte"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*3}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Grotte**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Grotte**, l'ami {ctx.author.mention}")


	elif arg in ["Grosse_grotte","grosse_grotte","Grosse_grote","grosse_grote"]:
		if "Grosse grotte" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Grosse grotte**, l'ami {ctx.author.mention}")
		elif "Grosse grotte" in author_biome["Rare"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Grosse grotte"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*6}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Grosse grotte**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Grosse grotte**, l'ami {ctx.author.mention}")
	elif arg in ["Forêt_d'érable","Foret_d'érable","forêt_d'érable","foret_d'érable","forêt_d'erable","foret_d'erable"]:
		if "Forêt d'érable" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Forêt d'érable**, l'ami {ctx.author.mention}")
		elif "Forêt d'érable" in author_biome["Rare"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Forêt d'érable"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*6}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Forêt d'érable**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Forêt d'érable**, l'ami {ctx.author.mention}")
	elif arg in ["Forêt_Ancienne","Foret_Ancienne","forêt_Ancienne","foret_Ancienne","Forêt_ancienne","Foret_ancienne","forêt_ancienne","foret_ancienne"]:
		if "Forêt Ancienne" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Forêt Ancienne**, l'ami {ctx.author.mention}")
		elif "Forêt Ancienne" in author_biome["Rare"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Forêt Ancienne"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*6}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Forêt Ancienne**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Forêt Ancienne**, l'ami {ctx.author.mention}")


	elif arg in ["Volcan","volcan"]:
		if "Volcan" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Volcan**, l'ami {ctx.author.mention}")
		elif "Volcan" in author_biome["Légendaire"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Volcan"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*12}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Volcan**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Volcan**, l'ami {ctx.author.mention}")
	elif arg in ["Météorite","Meteorite","météorite","meteorite"]:
		if "Météorite" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Météorite**, l'ami {ctx.author.mention}")
		elif "Météorite" in author_biome["Légendaire"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Météorite"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*12}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Météorite**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Météorite**, l'ami {ctx.author.mention}")
	elif arg in ["Montagne_éléctrique","Montagne_electrique","montagne_éléctrique","montagne_electrique"]:
		if "Montagne éléctrique" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Montagne éléctrique**, l'ami {ctx.author.mention}")
		elif "Montagne éléctrique" in author_biome["Légendaire"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Montagne éléctrique"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*12}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Montagne éléctrique**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Montagne éléctrique**, l'ami {ctx.author.mention}")


	elif arg in ["Forêt_féérique","Foret_féérique","forêt_féérique","foret_féérique","Forêt_féerique","Foret_féerique","forêt_féerique","foret_féerique","Forêt_feerique","Foret_feerique","forêt_feerique","foret_feerique","Forêt_feerique","Foret_feerique","forêt_feerique","foret_feerique"]:
		if "Forêt féérique" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Forêt féérique**, l'ami {ctx.author.mention}")
		elif "Forêt féérique" in author_biome["Mythique"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Forêt féérique"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*24}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Forêt féérique**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Forêt féérique**, l'ami {ctx.author.mention}")
	elif arg in ["Nid_du_dragon","nid_du_dragon"]:
		if "Nid du dragon" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Nid du dragon**, l'ami {ctx.author.mention}")
		elif "Nid du dragon" in author_biome["Mythique"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Nid du dragon"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*24}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Nid du dragon**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Nid du dragon**, l'ami {ctx.author.mention}")
	elif arg in ["Pierre_précieuse","Pierre_precieuse","pierre_précieuse","pierre_precieuse"]:
		if "Pierre précieuse" == author_current_biome:
			await ctx.send(f"Vous êtes déjà dans le biome **Pierre précieuse**, l'ami {ctx.author.mention}")
		elif "Pierre précieuse" in author_biome["Mythique"]:
			collection.update_one({"_id": author_id}, {"$set": {"current_biome": "Pierre précieuse"}})
			collection.update_one({"_id": author_id}, {"$set": {"cooldown_!biome": t2+60*60*24}})
			await ctx.send(f"Vous êtes maintenant dans le biome **Pierre précieuse**, l'ami {ctx.author.mention}")
		else:
			await ctx.send(f"Tu n'as pas le biome le biome **Pierre précieuse**, l'ami {ctx.author.mention}")


print(open("TOKEN.txt").read())
bot.run(open("TOKEN.txt").read())

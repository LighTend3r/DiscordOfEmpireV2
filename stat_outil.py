from random import choice

#"nom_hache":[niveau,prix,(bois_min,bois_max),(%sap,nb_sap),(%magic_powder,nb_magic_powder)]
hache ={
	"hache_en_bois":[1,"0 bois",(5,10),(0,0),(0.005,1),False],
	"hache_en_pierre":[2,"150 bois/40 pierre",(10,18),(0.10,1),(0.005,1),False],
	"hache_en_fer":[3,"1000 bois/500 pierre/5 fer",(15,30),(0.20,1),(0.005,1),True],
	"hache_en_or":[4,"7500 bois/4000 pierre/60 fer/8 or",(30,50),(0.35,1),(0.005,1),True],
	"hache_en_diamant":[5,"30000 bois/20000 pierre/400 fer/35 or/4 diamant",(50,75),(0.50,2),(0.005,1),True],
	"hache en électrum":[6,"3000 charbon/30 diamant/10 électrum",(80,110),(0.50,5),(0.005,1),True],
	"soon":[7,"---"]

}


niv_hache ={
	"1":"hache_en_bois",
	"2":"hache_en_pierre",
	"3":"hache_en_fer",
	"4":"hache_en_or",
	"5":"hache_en_diamant",
	"6":"hache en électrum",
	"7":"soon"

}

#"nom_Pioche":[niveau,prix,(pierre_min,pierre_max),(%fer,nb_fer),(%gold,nb_gold),(%diamond,nb_diamond),(%géode,nb_géode),"can_incrsted"]
pioche ={
	"pioche_en_bois":[1,"50 bois",(2,5),(0,0),(0,0),(0,0),(0,0),False],
	"pioche_en_pierre":[2,"120 bois/60 pierre",(5,9),(0.05,1),(0,0),(0,0),(0,0),False],
	"pioche_en_fer":[3,"500 bois/250 pierre/3 fer",(9,15),(0.10,1),(0.02,1),(0,0),(0.001,1),True],
	"pioche_en_or":[4,"5000 bois/2000 pierre/30 fer/3 or",(15,30),(0.20,2),(0.05,1),(0.001,1),(0.005,1),True],
	"pioche_en_diamant":[5,"20000 bois/15000 pierre/150 fer/25 or/2 diamant",(30,50),(0.20,5),(0.05,2),(0.005,1),(0.01,1),True],
	"pioche en électrum":[6,"2000 charbon/10 diamant/5 électrum",(50,80),(0.50,5),(0.1,2),(0.01,1),(0.03,1),True],
	"pioche en dracolite":[7,"5000 charbon/100 diamant/20 électrum/5 dracolite",(80,150),(1,7),(0.2,5),(0.05,2),(0.05,2),True],
	"soon":[8,"---"]

}
niv_pioche ={
	"1":"pioche_en_bois",
	"2":"pioche_en_pierre",
	"3":"pioche_en_fer",
	"4":"pioche_en_or",
	"5":"pioche_en_diamant",
	"6":"pioche en électrum",
	"7": "pioche en dracolite",
	"8":"soon"

}

épée = {  # "nom_de_l'épée":[niveau,coût,%deChanceSupVictoire(ptiMonstre),%deChanceSupVictoire(grosMonstre),%deChance_de trouvé_une_monstre_légendraire]
	"épée_en_acier": [1, "10 acier", 0.25,0.01,0.001],
	"épée_en_diamant": [2, "40 diamant/50 acier", 0.5, 0.05, 0.001],
	"épée_en_électrum": [3, "10 électrum/200 acier", 0.75, 0.1, 0.05],
	"épée_en_dracolite": [4, "5 dracolite/500 acier", 0.98, 0.2, 0.01],
	"soon": [5, "---"]
}
niv_épée ={
	"1":"épée_en_acier",
	"2": "épée_en_diamant",
	"3":"épée_en_électrum",
	"4":"épée_en_dracolite",
	"5": "soon"
}
#[niveau,prix]
maison = [[0],[1,"1000 bois/500 pierre/5 fer/1 or"]]

faction_ ={
	"2":"1000 bois/1000 pierre/10 fer/2 or/0 diamant",
	"3":"10000 bois/4000 pierre/100 fer/10 or/0 diamant",
	"4":"100000 bois/10000 pierre/800 fer/50 or/0 diamant",
	"5":"1000000 bois/250000 pierre/30000 fer/5000 or/50 diamant",
	"6":"10000000 bois/2500000 pierre/100000 fer/10000 or/250 diamant",
	"7": "50000000 bois/25000000 pierre/1000000 fer/100000 or/5000 diamant",
	"8":"100000000000000000000000 bois/500000000000000000000 pierre/3000000000000000000 fer/500000000000000000 or/5000000000000 diamant"
}
furnace_ = ["10000 pierre/100 fer"]

tresors_liste_commun = [(50, 300, "fer")]*10+[(10, 50, "or")]*5+[(2, 10, "diamant")]*2+[(
    10, 100, "charbon")]*10+[(1, 5, "géode")]*1+[(1, 2, "poudre_magique")]*1+[(1, 1, "lave")]*1+[(1000, 5000, "bois")]*30+[(1000, 5000, "pierre")]*30 + [(50, 250, "sève")]*10

tresors_liste_uncommun = [(100, 600, "fer")]*15+[(20, 100, "or")]*7+[(4, 20, "diamant")]*5+[(
    20, 200, "charbon")]*15+[(2, 10, "géode")]*3+[(2, 4, "poudre_magique")]*1+[(1, 2, "lave")]*1+[(2000, 10000, "bois")]*20+[(1000, 5000, "pierre")]*20 + [(100, 500, "sève")]*10 + [(0, 2, "potion")]*3

tresors_liste_rare = [(1000, 3000, "fer")]*15+[(100, 500, "or")]*15+[(1, 5, "électrum")]*7+[(1, 1, "dracolite")]*5+[(20, 40, "diamant")]*13 + [(
    200, 500, "charbon")]*20+[(10, 20, "géode")]*10+[(5, 10, "poudre_magique")]*5+[(3, 7, "lave")]*5 + [(0, 3, "potion")]*5

tresors_liste_légendaire = [(1000, 3000, "fer")]*10+[(500, 2000, "or")]*10+[(2, 10, "électrum")]*10+[(1, 2, "dracolite")]*10+[(40, 100, "diamant")]*10 + [(
    500, 2000, "charbon")]*10+[(20, 50, "géode")]*10+[(10, 50, "poudre_magique")]*10+[(10, 50, "lave")]*10 + [(3, 3, "potion")]*10

petit_monstre = ["Goblin","Gnôme","Squelette","Zombie","Momie"]

gros_monstre = ["Cyclope", "Minotaure", "Harpies", "Manticore"]

gros_monstre_légendraire = [
    "Dragon", "Léviathan", "Béhémot", "Wyvernes", "Phénix", "Chimère", "Hydre"]


pourcentage_marchand_steel = 15
pourcentage_marchand_coal = 50
pourcentage_marchand_lava = 20
pourcentage_marchand_électrum = 10
pourcentage_marchand_mp_emerald = 4
pourcentage_marchand_mp_sapphire = 1
marchand = [[[45, 60, "fer", "iron"], [45, 60, "charbon", "coal"], [1, 2, "lave", "lava"], [4, 6, "acier", "steel"]]]*pourcentage_marchand_steel + [[[75, 100, "bois", "wood"], [1, 1, "charbon", "coal"]]]*pourcentage_marchand_coal + [[[8000, 10000, "pierres", "stone"], [1, 1, "sceau de lave", "lava"]]]*pourcentage_marchand_lava + [[[350, 500, "fer","iron"], [45, 60, "or", "gold"], [1, 3, "sceau de lave", "lava"], [1, 1, "électrum", "électrum"]]]*pourcentage_marchand_électrum + [[[1,2,"saphir","sapphire"],[250,500,"quartz","quartz"],[4000,8000,"sève","sap"],[10,25,"poudre magique","magic_powder"]]]*pourcentage_marchand_mp_sapphire + [[[2,5,"émeraude","emerald"],[500,750,"quartz","quartz"],[5000,10000,"sève","sap"],[2,5,"poudre magique","magic_powder"]]]*pourcentage_marchand_mp_emerald

incrustation = {
	"pure_emerald":[2,"x2 sur toute récupération de minerais"],
	"pure_sapphire":[3,"x3 sur toute récupération de minerais"],
	"pure_ruby":[5,"x5 sur toute récupération de minerais"]
}

invitation_loot = {
	"1":"1 vote",
	"2":"1 vote",
	"3":"1 vote/1 x2",
	"4":"1 vote",
	"5":"1 unlock_week",
	"6":"1 vote",
	"7":"3 vote",
	"8":"1 vote",
	"9":"1 vote",
	"10":"1 week/1 emerald",
	"11":"2 vote",
	"12":"1 vote",
	"13":"1 vote/2 x2",
	"14":"1 vote",
	"15":"1 week",
	"16":"1 vote/1 geode",
	"17":"2 vote/1 geode",
	"18":"1 vote/1 geode",
	"19":"1 vote/3 geode",
	"20":"3 week",
	"21":"1 vote",
	"22":"5 vote",
	"23":"1 vote/3 x2",
	"24":"1 vote",
	"25":"1 week/1 item",
	"26":"4 vote/1 geode",
	"27":"1 vote/2 geode",
	"28":"1 vote/1 geode",
	"29":"1 vote/1 geode",
	"30":"5 week",
	"31":"2 vote",
	"32":"2 vote",
	"33":"3 vote/4 x2",
	"34":"2 vote",
	"35":"1 week/1 item",
	"36":"2 vote/4 geode",
	"37":"2 vote/2 geode",
	"38":"2 vote/2 geode",
	"39":"2 vote/2 geode",
	"40":"10 week",
	"41":"2 vote",
	"42":"2 vote",
	"43":"2 vote/5 x2",
	"44":"7 vote",
	"45":"1 week/1 item",
	"46":"2 vote/2 geode",
	"47":"2 vote/5 geode",
	"48":"2 vote/2 geode",
	"49":"2 vote/2 geode",
	"50":"20 week"
}

biomes =  {
	"Commun":[
		"Plaine", # /
		"Forêt", # Bois +
		"Carrière", # Pierre +
	],
	"Peu_commun":[
		"Grande forêt", # Bois +++ / Pierre --
		"Grande carrière", #Bois -- / Sève -- / Pierre +++
		"Grotte" #  pas de !wood / Pierre ++ / Charbon ~ / Fer + / Or +
	],
	"Rare":[
		"Grosse grotte", # Pas de !wood / Pierre + / Charbon + / Fer ++ / Or ++
		"Forêt d'érable",  # Bois + / Sève ++ / Pierre -
		"Forêt Ancienne" # Bois -- / Charbon ++ / pas de !mine / pas de sève
	],
	"Légendaire":[
		"Volcan", # pas de !wood, / Pierre + / Lave +
		"Météorite", # Acier + / Géode +
		"Montagne éléctrique" # Pierre + / Electrum + / Or ++ / pas de wood
	],
	"Mythique":[
		"Forêt féérique", # Bois + / Poudre Magique +
		"Nid du dragon", # Dracolite + / pas de !wood ni de !mine
		"Pierre précieuse"  # pas de !wood ni de !mine / Emeraude + / Saphir + / Rubis +
	]

}


#"nom_de_l'objet":[niveau,prix,]

luck = { #prix moyen
	"1": (25,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"), #+25% de chance sur les minerais
	"2": (50,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
	"3": (75,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
	"4": (100,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
	"5": (150,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
	"6": (200,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
}

plus_minerais = { #très chère
	"1" : (1,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"), #+1 par minerais
	"2" : (2,"1000 bois/1000 pierre/10 fer/2 or/0 diamant"),
}


all_item=[("luck",luck,0),("plus_minerais",plus_minerais,1)]


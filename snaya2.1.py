#CAMELET Alexandre et LECUTIEZ Simon 2015/2016, cours d'ISN - Lycée de la Plaine de l'Ain
#Snaya, notre version du célèbre jeu Snake.
#V2.1.0
#Ce programme, aussi modeste qu'il soit, est proposé librement. Vous pouvez le redistribuer et/ou le modifier selon les termes de la GNU General Public License telle que publiée par la Free Software Foundation, en version 3 ou plus récente (à votre guise).
#Vous pouvez trouver les termes de la GNU GPLv3 dans le fichier LICENSE fourni avec le programme, ou à l'adresse http://www.gnu.org/licenses/gpl.html .
#Rejoignez nous sur la page Github du projet! https://github.com/Rbird0/snaya/


	#*************** CLASSE PRINCIPALE ***************#


class Snaya :
	"""
	Classe principale du programme. C'est ici que tout commence, et c'est ici que tout est structuré. Un objet Snaya est créé dès le lancement du programme et appelle lui même les autres objets.
	"""

	def __init__(self) :
		"""
		Première fonction executée par le programme. Celle-ci initialise la fenêtre, définit les classes de sauvegarde et de chemins d'accès, ... C'est une fonction "structurante", c'est à dire qu'elle indique dans quel ordre les différentes fonction "executantes" seront appellées plutôt que d'effectuer elle-même les actions. 
		"""

		self.root = Tk() #On crée une fenêtre ayant pour titre "Snaya"
		self.root.title("Snaya")

		self.save = Save() #On définit un objet Save et un objet Paths attributs de snaya
		self.paths = Paths()

		self.save_load() #On execute la fonction chargeant la sauvegarde
		self.root.deiconify() #On remet le focus du clavier sur la fenêtre principale
		self.initialize() #On execute la fonction initialisant certaines variables et objets attributs

		self.dansMenu = True #On indique qu'on se trouve dans le menu
		self.dansJeu = False #On indique qu'on n'est pas en train de jouer
		self.can = Canvas(self.root, width = 800, height = 600) #On définit un canevas avec la taille de la fenêtre pour le menu et on le charge
		self.can.pack()
		self.menu_init() #On lance l'initialisation du menu
		self.menu() #On lance le menu

		self.root.mainloop() #On indique à tkinter qu'il doit s'attendre à recevoir des instructions au clavier et à la souris pour la fenêtre pricipale

	def save_load(self) :
		"""
		Fonction permettant de charger la sauvegarde. Elle executera les fonctions de l'objet save dans le bon ordre.
		"""

		self.save.open_dialog() #On demande à l'attribut save d'ouvrir une fenêtre de dialogue permettant de sélectionner le fichier de sauvegarde
		if self.save.isFileSelected == True : #Si un fichier a été sélectionné,
			self.save.check_integrity() #on demande à l'attribut save de vérifier rapidement si le fichier est au bon format,
			if self.save.integrity == True : #et si c'est le cas,
				self.paths.set_path("save", self.save.path) #on demande à l'attribut paths de "se souvenir" que le chemin de la sauvegarde est celui indiqué par la fenêtre de dialogue,
				self.save.proceed() #et on charge le fichier
			else : #Si le fichier n'a pas passé le test de format,
				print("Le fichier sélectionné n'est pas valide. Une sauvegarde vierge sera utilisée.") #on indique à l'utilisateur via la console que le fichier n'est pas valide et qu'une sauvegarde vide sera utilisée,
				self.save.use_default() #et on indique à l'attribut save d'utiliser la sauvegarde (vide) par défaut
		else : #Si aucun fichier n'a été sélectionné,
			print("Vous n'avez séléctionné aucun fichier. Une sauvegarde vierge sera utilisée.") #on indique à l'utilisateur via la console qu'aucun fichier a été sélectionné et qu'une sauvegarde vide sera utilisée,
			self.save.use_default() #et on indique à l'attribut save d'utiliser la sauvegarde (vide) par défaut

	def initialize(self) :
		"""
		Fonction initialisant certains attributs essentiels au programme.
		"""

		self.name = self.save.playerName #On indique qu'il faut aller chercher le nom du joueur dans l'attribut playerName de save
		self.playerName = {"name" : self.name, 0 : self.name[0], 1 : self.name[1], 2 : self.name[2]} #On définit un dictionnaire playerName attribut de snaya et contenant la string définissant le nom du joueur ainsi que les trois lettres qui le constituent, séparément

		self.paths.set_path("resources", self.save.resourcesPath) #On demande à l'attribut paths de "se souvenir" que le chemin du dossier de ressources est celui indiqué par le fichier de sauvegarde

		self.hs = Highscores(self.save.highscores) #On définit des objets Highscores, Achievements, Skins, Comptes et Parametres tous attributs de snaya
		self.ach = Achievements(self.save.achievements)
		self.skins = Skins(self.save.skins)
		self.comptes = Comptes(self.save.comptes)
		self.param = Parametres(self.save.parametres)

	def menu_init(self) :
		"""
		Fonction initialisant certains attributs essentiels au menu.
		"""

		parametres = self.param.get_parametres() #On demande à param de nous indiquer les différents paramètres et à skins de nous donner les différentes informations relatives aux skins
		skins = self.skins.get_skins()

		if parametres["graph mode"] == "sprite" : #Si l'on est en mode sprite,
			self.images = Images(self.root, self.paths.get_path("resources"), skins["selected skin"]) #on définit un objet Image attribut de snaya en lui indiquant le chemin des images à l'aide du chemin de ressources indiqué dans paths
		else : #Sinon,
			self.images = Images() #on définit un objet Image attribut de snaya sans indiquer de chemin

		self.menuRender = {"background" : [], "highlight line" : [], "title texts" : [], "sélection texts" : [], "highscores texts" : [], "achievements texts" : [], "achievements elements" : [], "paramètres texts" : []} #On définit un attribut de snaya menuRender dictionnaire contenant les listes des choses affichées dans le menu
		self.menuMechanics = {"current menu" : "title", "highlight" : 0} #On définit un attribut de snaya menuMechanics dictionnaire contenant les mécaniques du menu tels que le menu actuel et la sélection actuelle dans le menu
		
		self.bind() #On execute la fonction affectant des actions aux touches

	def menu(self) :
		"""
		Fonction permettant de gérer l'affichage et les mécaniques du menu. Celle-ci tournera en boucle tant que l'utilisateur sera dans le menu.
		"""

		highscores = self.hs.get_highscores() #On va chercher les highscores, les achievements et les paramètres dans leurs attributs respectifs
		achievements = self.ach.get_achievements()
		parametres = self.param.get_parametres()

		if parametres["graph mode"] == "sprite" : #Si l'on est en mode sprite,
			for j in self.menuRender["background"] : #On supprime l'arrière-plan du menu
				self.can.delete(j)
		for j in self.menuRender["highlight line"] : #On supprime les éléments de toutes les sections du rendu du menu
			self.can.delete(j)
		for j in self.menuRender["title texts"] :
			self.can.delete(j)
		for j in self.menuRender["sélection texts"] :
			self.can.delete(j)
		for j in self.menuRender["highscores texts"] :
			self.can.delete(j)
		for j in self.menuRender["achievements texts"] :
			self.can.delete(j)
		for j in self.menuRender["achievements elements"] :
			self.can.delete(j)
		for j in self.menuRender["paramètres texts"] :
			self.can.delete(j)

		if self.menuMechanics["current menu"] == "title" and parametres["graph mode"] == "sprite" : #Si le menu actuel est le menu principal et si l'on est en mode sprite,
			images = self.images.get_images() #on affiche l'"image de titre" du jeu
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_image(0, 0, anchor = NW, image = images["menu title"])]
		elif parametres["graph mode"] == "sprite" : #Sinon si l'on est en mode sprite mais pas dans le menu principal,
			images = self.images.get_images() #on affiche l'image d'arrière plan du menu
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_image(0, 0, anchor = NW, image = images["menu"])]
		else : #Sinon,
			images = 0 #on affiche des rectangles grossiers en arrière-plan,
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(0, 0, 124, 600, width = 0, fill = "#547e25")]
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(124, 0, 676, 600, width = 0, fill = "#8c5918")]
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(676, 0, 800, 600, width = 0, fill = "#547e25")]
			if self.menuMechanics["current menu"] == "title" : #et si le menu actuel est le menu principal, on affiche un texte en haut en guise de titre
				self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 30, anchor = N, text = "SNAYA", font = ("Mayan", -130), fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "title" : #Si l'on est dans le menu de titre,
			self.menu_title() #on execute la fonction affichant le menu de titre

		if self.menuMechanics["current menu"] == "sélection nom" : #Si l'on est dans le menu de sélection de nom,
			self.menu_selection() #on execute la fonction affichant le menu de sélection de nom

		if self.menuMechanics["current menu"] == "highscores" : #Si l'on est dans le menu de highscores,
			self.menu_highscores(highscores) #on execute la fonction affichant le menu de highscores

		if self.menuMechanics["current menu"] == "achievements" : #Si l'on est dans le menu d'achievements,
			self.menu_achievements(images, achievements, parametres) #on execute la fonction affichant le menu d'achievements

		if self.menuMechanics["current menu"] == "paramètres" : #Si l'on est dans le menu de paramètres,
			self.menu_parametres(parametres) #on execute la fonction affichant le menu de paramètres

		if self.dansMenu == True : #On rafraîchit le menu toutes les 10 millisecondes
			self.root.after(10, self.menu)
		else :
			self.launch() #Et si le jeu a été lancé, on execute la fonction d'initialisation du jeu

	def menu_title(self) :
		"""
		Fonction affichant les textes et la barre de sélection du menu principal.
		"""

		#On affiche les textes "Jouer", "Highscores", "Achievements", et "Paramètres"
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 275, anchor = S, text = "Jouer", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 337.5, anchor = S, text = "Highscores", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 400, anchor = S, text = "Achievements", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 462.5, anchor = S, text = "Paramètres", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 525, anchor = S, text = "Quitter", font = ("Mayan", 25), fill = "#f0cc00")]

		#On affiche la barre de sélection suivant sa position gérée par l'attribut menuMechanics
		self.menuRender["highlight line"] = [self.can.create_line(375, 270 + self.menuMechanics["highlight"]*62.5, 425, 270 + self.menuMechanics["highlight"]*62.5, width = 2, fill = "#f0cc00")]

	def menu_selection(self) :
		"""
		Fonction affichant les textes et la barre de sélection du menu de sélection de nom.
		"""

		#On affiche le titre de la section
		self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(400, 30, anchor = N, text = "ENTREZ VOTRE NOM", font = ("Mayan", 35), fill = "#f0cc00")]

		#On affiche les trois lettres sélectionnées suivant leur valeur donnée par l'attribut playerName[position de la lettre]
		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(325, 375, anchor = SE, text = self.playerName[0], font = ("Mayan", 75), fill = "#f0cc00")]
		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(400, 375, anchor = S, text = self.playerName[1], font = ("Mayan", 75), fill = "#f0cc00")]
		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(475, 375, anchor = SW, text = self.playerName[2], font = ("Mayan", 75), fill = "#f0cc00")]

		#On affiche la barre de sélection suivant sa position gérée par l'attribut menuMechanics
		self.menuRender["highlight line"] = [self.can.create_line(273 + self.menuMechanics["highlight"]*102, 370, 323 + self.menuMechanics["highlight"]*102, 370, width = 2, fill = "#f0cc00")]

	def menu_highscores(self, highscores) :
		"""
		Fonction affichant les textes du menu de highscores.
		"""

		#On affiche le titre de la section
		self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(400, 30, anchor = N, text = "HIGHSCORES", font = ("Mayan", 35), fill = "#f0cc00")]

		#Pour j dans les clés du dictionnaire de highscores,
		#on affiche les lignes dans l'ordre et en utilisant les valeurs renvoyées par le dictionnaire pour la clé en question
		for j in highscores.keys() :
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(245, 160 + 40*(j - 1), anchor = NW, text = highscores[j]["name"], font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(350, 160 + 40*(j - 1), anchor = NW, text = " . . . . . . . . . . . ", font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(600, 160 + 40*(j - 1), anchor = NE, text = highscores[j]["score"], font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(245, 160 + 40*(j - 1), anchor = NE, text = str(j) + ". ", font = ("Mayan", 20), fill = "#f0cc00")]

	def menu_achievements(self, images, achievements, parametres) :
		"""
		Menu affichant les textes et les éléments du menu d'achievements.
		"""

		if parametres["graph mode"] == "sprite" : #Si l'on est en mode sprite,
			self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(201, 171, anchor = NW, image = images["ach bg"])] #on affiche une image avec de la transparence pour le fond
		else : #Sinon,
			for j in range(0,5) : #on crée des rectangles ayant la même fonction
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_rectangle(201, 171 + 70*j, 601, 231 + 70*j, width = 0, fill = "#6f4811")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_rectangle(206, 176 + 70*j, 256, 226 + 70*j, width = 0, fill = "#463b2b")]

		#On affiche le titre de la section
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(400, 30, anchor = N, text = "ACHIEVEMENTS", font = ("Mayan", 35), fill = "#f0cc00")]

		nbAch = 0 #On initialise le nombre d'achievements à 0

		#On affiche les titres des achievements
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 176, anchor = NW, text = "Adam & Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 246, anchor = NW, text = "Mécanique newtonienne", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 316, anchor = NW, text = "Jeunesse dorée", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 386, anchor = NW, text = "Super Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 456, anchor = NW, text = "Globetrotter", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]

		if parametres["graph mode"] == "sprite" : #Si l'on est en mode sprite,
			if achievements[1] == True : #pour chaque achievement débloqué, on affiche l'image correspondante et sa description, et on augmente le comtpe d'achievements d'1,
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 176, anchor = NW, image = images["ach1"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 201, anchor = NW, text = "Manger 10 pommes classiques en une partie.", font = ("Mayan", 10), fill = "#f0cc00")]
			else : #et pour chaque achievement non débloqué, on affiche une image grisée
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(207, 176, anchor = NW, image = images["no ach"])]
			if achievements[2] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 246, anchor = NW, image = images["ach2"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 271, anchor = NW, text = "Manger 100 pommes classiques au total.", font = ("Mayan", 10), fill = "#f0cc00")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(207, 246, anchor = NW, image = images["no ach"])]
			if achievements[3] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 316, anchor = NW, image = images["ach3"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 341, anchor = NW, text = "Manger 150 pommes en or au total.", font = ("Mayan", 10), fill = "#f0cc00")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(207, 316, anchor = NW, image = images["no ach"])]
			if achievements[4] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 386, anchor = NW, image = images["ach4"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 411, anchor = NW, text = "Manger 100 pommes spéciales au total.", font = ("Mayan", 10), fill = "#f0cc00")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(207, 386, anchor = NW, image = images["no ach"])]
			if achievements[5] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 456, anchor = NW, image = images["ach5"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 481, anchor = NW, text = "Parcourir toute la grille en une seule partie.", font = ("Mayan", 10), fill = "#f0cc00")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(207, 456, anchor = NW, image = images["no ach"])]

		else : #Sinon,
			if achievements[1] == True : #pour chaque achievement débloqué, on affiche un "V" vert et sa description, et on augmente le comtpe d'achievements d'1,
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 200, 230, 220, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 220, 252, 180, width = 2, fill = "#76cb3d")]
			else : #et pour chaque achievement non débloqué, on affiche une croix rouge
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 180, 252, 222, width = 2, fill = "#f8320b")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 222, 252, 180, width = 2, fill = "#f8320b")]
			if achievements[2] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 270, 230, 290, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 290, 252, 250, width = 2, fill = "#76cb3d")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 250, 252, 292, width = 2, fill = "#f8320b")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 292, 252, 250, width = 2, fill = "#f8320b")]
			if achievements[3] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 340, 230, 360, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 360, 252, 320, width = 2, fill = "#76cb3d")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 320, 252, 362, width = 2, fill = "#f8320b")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 362, 252, 320, width = 2, fill = "#f8320b")]
			if achievements[4] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 410, 230, 430, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 430, 252, 390, width = 2, fill = "#76cb3d")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 390, 252, 432, width = 2, fill = "#f8320b")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 432, 252, 390, width = 2, fill = "#f8320b")]
			if achievements[5] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 480, 230, 500, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 500, 252, 460, width = 2, fill = "#76cb3d")]
			else :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 460, 252, 502, width = 2, fill = "#f8320b")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 502, 252, 460, width = 2, fill = "#f8320b")]
		
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(546, 65, anchor = NW, text = str(nbAch), font = ("Mayan", 30), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(592, 136, anchor = SE, text = "5", font = ("Mayan", 30), fill = "#f0cc00")]
		self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(556, 119, 590, 85, width = 2, fill = "#f0cc00")]

	def menu_parametres(self, parametres) :
		"""
		Fonction affichant les textes et la barre de sélection du menu de paramètres.
		"""

		#On affiche le titre de la section
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(400, 30, anchor = N, text = "PARAMÈTRES", font = ("Mayan", 35), fill = "#f0cc00")]

		#Pour chaque paramètre, on va venir afficher le nom et l'état actuel
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 200, anchor = SW, text = "Dossier ressources", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 240, anchor = SW, text = "Sauvegarder", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 280, anchor = SW, text = "Mode graphique: " + parametres["graph mode"], font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 320, anchor = SW, text = "Taille de la grille: " + str(parametres["largeur"]) + " x " + str(parametres["hauteur"]), font = ("Mayan", 20), fill = "#f0cc00")]
		if parametres["bonus"] == True :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 360, anchor = SW, text = "Bonus: avec", font = ("Mayan", 20), fill = "#f0cc00")]
		else :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 360, anchor = SW, text = "Bonus: sans", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 400, anchor = SW, text = "Vitesse: " + str(parametres["vitesse"]), font = ("Mayan", 20), fill = "#f0cc00")]
		if parametres["graph mode"] == "sprite" : #Si l'on est en mode sprite, on ajoute un paramètre de sélection de la skin
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 440, anchor = SW, text = "Skin: " + self.skins.get_skins()["selected skin"], font = ("Mayan", 20), fill = "#f0cc00")]

		#On affiche la barre de sélection suivant sa position gérée par l'attribut menuMechanics
		if self.menuMechanics["highlight"] <= 2 :
			self.menuRender["highlight line"] = [self.can.create_line(220, 198 + self.menuMechanics["highlight"]*40, 270, 198 + self.menuMechanics["highlight"]*40, width = 2, fill = "#f0cc00")]
		elif self.menuMechanics["highlight"] >= 5 :
			self.menuRender["highlight line"] = [self.can.create_line(220, 198 + (self.menuMechanics["highlight"] - 1)*40, 270, 198 + (self.menuMechanics["highlight"] - 1)*40, width = 2, fill = "#f0cc00")]
		elif self.menuMechanics["highlight"] == 3 :
			self.menuRender["highlight line"] = [self.can.create_line(419, 198 + self.menuMechanics["highlight"]*40, 439, 198 + self.menuMechanics["highlight"]*40, width = 2, fill = "#f0cc00")]
		elif self.menuMechanics["highlight"] == 4 :
			self.menuRender["highlight line"] = [self.can.create_line(472, 198 + (self.menuMechanics["highlight"] - 1)*40, 492, 198 + (self.menuMechanics["highlight"] - 1)*40, width = 2, fill = "#f0cc00")]

	def bind(self) :
		"""
		Fonction affectant les fonctions aux différentes touches.
		"""

		#Pour chaque touche, on affecte la fonction correspondant:
		#Haut et Z permettent d'aller vers le haut, Bas et S permettent d'aller vers le bas, etc...
		self.can.bind_all('<Up>', self.haut)
		self.can.bind_all('z', self.haut)
		self.can.bind_all('<Down>', self.bas)
		self.can.bind_all('s', self.bas)
		self.can.bind_all('<Left>', self.gauche)
		self.can.bind_all('q', self.gauche)
		self.can.bind_all('<Right>', self.droite)
		self.can.bind_all('d', self.droite)
		self.can.bind_all('<Return>', self.suivant)
		self.can.bind_all('<space>', self.suivant)
		self.can.bind_all('<Escape>', self.precedent)
		self.can.bind_all('p', self.precedent)

	def haut(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Haut.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" : #si l'on est dans le menu principal ou le menu de paramètres, on enlève 1 à la position de la barre de sélection
				self.menuMechanics["highlight"] -= 1
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == -1 : #Ensuite, si l'on est dans le menu principal et que la barre de sélection se trouve en position -1, on la ramène sur la position 4
				self.menuMechanics["highlight"] = 4
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 0 : #Si l'on se trouve sur l'écran de sélection de nom et suivant la position de la lettre modifiée, on execute la fonction permettant de passer à la lettre suivante
				self.name_plus_one(0)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 1 :
				self.name_plus_one(1)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 2 :
				self.name_plus_one(2)
			if self.menuMechanics["current menu"] == "paramètres" and self.param.get_graph_mode() != "sprite" and self.menuMechanics["highlight"] == -1 : #Si l'on est dans le menu de paramètres, que l'on est en mode simplifié et que la barre de sélection se trouve en position -1, on la ramène sur la position 6
				self.menuMechanics["highlight"] = 6
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == -1 : #Si l'on est dans le menu de paramètres, que l'on est en mode sprite et que la barre de sélection se trouve en position -1, on la ramène sur la position 7
				self.menuMechanics["highlight"] = 7

		elif self.dansJeu == True and self.direction != "south" : #Sinon, si l'on est en jeu,
			self.direction = "north" #on passe la direction actuelle à "nord"
	
	def bas(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Bas.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" : #si l'on est dans le menu principal ou le menu de paramètres, on ajoute 1 à la position de la barre de sélection
				self.menuMechanics["highlight"] += 1
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 5 : #Ensuite, si l'on est dans le menu principal et que la barre de sélection se trouve en position 5, on la ramène sur la position 0
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 0 : #Si l'on se trouve sur l'écran de sélection de nom et suivant la position de la lettre modifiée, on execute la fonction permettant de passer à la lettre précédente
				self.name_minus_one(0)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 1 :
				self.name_minus_one(1)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 2 :
				self.name_minus_one(2)
			if self.menuMechanics["current menu"] == "paramètres" and self.param.get_graph_mode() != "sprite" and self.menuMechanics["highlight"] == 7 : #Si l'on est dans le menu de paramètres, que l'on est en mode simplifié et que la barre de sélection se trouve en position 7, on la ramène sur la position 0
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 8 : #Si l'on est dans le menu de paramètres, que l'on est en mode sprite et que la barre de sélection se trouve en position 8, on la ramène sur la position 0
				self.menuMechanics["highlight"] = 0
		elif self.dansJeu == True and self.direction != "north" : #Sinon, si l'on est en jeu,
			self.direction = "south" #on passe la direction actuelle à "sud"

	def droite(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Droite.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "sélection nom" : #Si l'on se trouve sur l'écran de sélection de nom, on passe à la lettre à la position suivante
				self.menuMechanics["highlight"] += 1
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 3 : #Puis si la position devient 3, on la ramène à 0
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 2 and self.paths.get_path("resources") != "" : #Si l'on se trouve dans le menu de paramètres, que c'est la troisième ligne qui est sélectionnée, et qu'un chemin pour le dossier de ressources est bien sélectionné, on passe à l'autre mode graphique (sprite si l'on était sur simple et simple si l'on était sur sprite)
				self.param.switch_graph_mode()
				if self.param.get_parametres()["graph mode"] == "sprite" : #Si c'est en mode sprite qu'on est passé, on définit l'attribut images
					self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 : #Sinon si c'est la partie gauche de la quatrième ligne qui est sélectionnée, on ajoute un à la largeur du tableau
				self.param.plus_one_largeur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 : #Sinon si c'est la partie droite quatrième ligne qui est sélectionnée, on ajoute un à la hauteur du tableau
				self.param.plus_one_hauteur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 5 : #Sinon si c'est la cinquième ligne qui est sélectionnée, on inverse l'activation ou non des bonus
				self.param.switch_bonus()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 : #Sinon si c'est la sixième ligne qui est sélectionnée, on ajoute un à la vitesse
				self.param.plus_one_vitesse()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 7 : #Sinon si c'est la septième ligne qui est sélectionnée, on sélectionne la skin suivante,
				j = 0
				while self.skins.get_skins()["unlocked"][j] != self.skins.get_skins()["selected skin"] :
					j += 1
				if self.skins.get_skins()["unlocked"][j] is not self.skins.get_skins()["unlocked"][-1] :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][j+1])
				else :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][0])
				self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"]) #et on rafraîchit le dictionnaire d'images
		elif self.dansJeu == True and self.direction != "west" : #Sinon, si l'on est en jeu,
			self.direction = "east" #on passe la direction actuelle à "est"

	def gauche(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Gauche.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "sélection nom" : #Si l'on se trouve sur l'écran de sélection de nom, on passe à la lettre à la position précédente
				self.menuMechanics["highlight"] -= 1
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == -1 : #Puis si la position devient -1, on la ramène à 2
				self.menuMechanics["highlight"] = 2
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 2 and self.paths.get_path("resources") != "" : #Si l'on se trouve dans le menu de paramètres, que c'est la troisième ligne qui est sélectionnée, et qu'un chemin pour le dossier de ressources est bien sélectionné, on passe à l'autre mode graphique (sprite si l'on était sur simple et simple si l'on était sur sprite)
				self.param.switch_graph_mode()
				if self.param.get_parametres()["graph mode"] == "sprite" : #Si c'est en mode sprite qu'on est passé, on définit l'attribut images
					self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 : #Sinon si c'est la partie gauche de la quatrième ligne qui est sélectionnée, on retire un à la largeur du tableau
				self.param.minus_one_largeur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 : #Sinon si c'est la partie droite quatrième ligne qui est sélectionnée, on retire un à la hauteur du tableau
				self.param.minus_one_hauteur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 5 : #Sinon si c'est la cinquième ligne qui est sélectionnée, on inverse l'activation ou non des bonus
				self.param.switch_bonus()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 : #Sinon si c'est la sixième ligne qui est sélectionnée, on retire un à la vitesse
				self.param.minus_one_vitesse()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 7 : #Sinon si c'est la septième ligne qui est sélectionnée, on sélectionne la skin précédente,
				j = 0
				while self.skins.get_skins()["unlocked"][j] != self.skins.get_skins()["selected skin"] :
					j += 1
				if self.skins.get_skins()["unlocked"][j] is not self.skins.get_skins()["unlocked"][0] :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][j-1])
				else :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][-1])
				self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"]) #et on rafraîchit le dictionnaire d'images
		elif self.dansJeu == True and self.direction != "east" : #Sinon, si l'on est en jeu,
			self.direction = "west" #on passe la direction actuelle à "ouest"

	def suivant(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Suivant.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 0 : #Si l'on se trouve dans le menu principal et que la ligne active est la première, on passe à l'écran de sélection du nom
				self.menuMechanics["current menu"] = "sélection nom"
				self.menuMechanics["highlight"] = 0
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 1 : #Si l'on se trouve dans le menu principal et que la ligne active est la deuxième, on passe à l'écran de highscores
				self.menuMechanics["current menu"] = "highscores"
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 2 : #Si l'on se trouve dans le menu principal et que la ligne active est la troisième, on passe à l'écran d'achievements
				self.menuMechanics["current menu"] = "achievements"
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 3 : #Si l'on se trouve dans le menu principal et que la ligne active est la quatrième, on passe au menu des paramètres
				self.menuMechanics["current menu"] = "paramètres"
				self.menuMechanics["highlight"] = 0
			elif self.menuMechanics["current menu"] == "sélection nom" : #Si l'on se trouve dans l'écran de sélection du nom, on lance la partie
				self.dansMenu = False
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 4 : #Si l'on se trouve dans le menu principal et que la ligne active est la cinquième, on quitte le jeu
				self.quitter()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 0 : #Si l'on se trouve dans le menu des paramètres et que la ligne active est la première, on affiche un dialogue permettant à l'utilisateur de choisir son dossier de ressources
				path = filedialog.askdirectory(title = "Choisir le dossier de ressources")
				if path != "" :
					self.paths.set_path("resources", path)
					if self.param.get_parametres()["graph mode"] == "sprite" :
						self.images.update(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
				else :
					print("Vous n'avez sélectionné aucun dossier! Rien ne sera fait.")
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 1 : #Si l'on se trouve dans le menu des paramètres et que la ligne active est la deuxième, on sauvegarde, c'est à dire qu'on écrase le fichier de sauvegarde avec les données actuelles
				self.save.write_to_file(self.playerName["name"], self.paths.get_path("resources"), self.hs.get_highscores(), self.ach.get_achievements(), self.skins.get_skins(), self.comptes.get_comptes(), self.param.get_parametres())
		elif self.isOver == True : #Si l'on se trouve sur l'écran de game over, on retourne au menu pricipal
			self.isOver = False
			self.retour_menu()
		if self.dansJeu == True : #Si l'on est en jeu, on met la pause ou on la retire si elle est déjà active
			self.pause = not self.pause

	def precedent(self, event) :
		"""
		Fonction gérant les actions lorsque l'utilisateur appuie sur la touche Précédent.
		"""

		if self.dansMenu == True : #Si l'on se trouve dans le menu,
			if self.menuMechanics["current menu"] == "title" : #Si l'on se trouve sur le menu principal, on quitte le jeu
				self.quitter()
			if self.menuMechanics["current menu"] == "sélection nom" : #Si l'on se trouve sur l'écran de sélection de nom, l'écran de highscores, l'écran d'achievements ou le menu de paramètres, on retourne au menu principal
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "highscores" :
				self.menuMechanics["highlight"] = 1
			if self.menuMechanics["current menu"] == "achievements" :
				self.menuMechanics["highlight"] = 2
			if self.menuMechanics["current menu"] == "paramètres" :
				self.menuMechanics["highlight"] = 3
			self.menuMechanics["current menu"] = "title"
		elif self.isOver == True : #Si l'on se trouve sur l'écran de game over, on retourne au menu pricipal
			self.isOver = False
			self.retour_menu()
		if self.dansJeu == True : #Si l'on est en jeu, on met la pause ou on la retire si elle est déjà active
			self.pause = not self.pause

	def name_plus_one(self, position) :
		"""
		Fonction prenant en entrée une position de lettre et passant la lettre correspondante dans le nom du joueur à la suivante dans l'ordre alphabétique.
		"""

		lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		for j in range(len(lettres)) :
			if lettres[j] == self.playerName[position] and lettres[j] != "Z" :
				let = lettres[j+1]
			elif lettres[j] == self.playerName[position] and lettres[j] == "Z" :
				let = "A"
		self.playerName[position] = let
		self.name_build()

	def name_minus_one(self, position) :
		"""
		Fonction prenant en entrée une position de lettre et passant la lettre correspondante dans le nom du joueur à la précédente dans l'ordre alphabétique.
		"""

		lettres = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
		for j in range(len(lettres)) :
			if lettres[j] == self.playerName[position] and lettres[j] != "A" :
				let = lettres[j+1]
			elif lettres[j] == self.playerName[position] and lettres[j] == "A" :
				let = "Z"
		self.playerName[position] = let
		self.name_build()

	def name_build(self) :
		"""
		Fonction refraîchissant le nom du joueur avec les trois lettres qui le définissent.
		"""

		self.playerName["name"] = self.playerName[0] + self.playerName[1] + self.playerName[2]

	def launch(self) :
		"""
		Fonction initialisant divers attributs nécessaires au lancement du jeu.
		"""

		self.score = 0 #On initialise le score et le temps de la boucle précédente à 0
		self.oldTemps = 0
		self.direction = "east" #On initialise les deux dernières directions à "est"
		self.oldDirection = "east"

		self.dansJeu = True #On indique qu'on est en jeu et on passe la pause et le game over à faux
		self.pause = False
		self.isOver = False
		self.bonus = self.param.get_parametres()["bonus"] #On va chercher dans les paramètres l'activation ou non des bonus (pommes dorées et spéciales)

		self.grilleParcours = [] #On initialise une liste utilisée pour déterminer si le joueur obtient un certain achievement

		self.pommesPartie = 0 #On initialise le nombre de pommes normales mangées depuis le début de la partie à 0

		self.snake = Snake() #On crée un objet Snake attribut de snaya
		interdit = self.snake.get_coords() #Les pommes ne peuvent pas apparaître sur une case où se trouve le serpent: ici on crée une variable qui va contenir toutes les cases où les pommes ne peuvent pas apparître
		self.pomme = Pomme(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"]) #On fait apparaître une pomme (objet Pomme attribut de snaya)
		if self.bonus == True : #Si les bonus sont activés
			interdit = interdit + [self.pomme.get_coords()] #Les pommes ne peuvent également pas apparître sur une case où il y a déjà une pomme
			self.pommeGold = PommeRand(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"]) #On crée un objet PommeRand attribut de snaya, qui nous permettra de gérer le comportement de la pomme en or
			interdit = interdit + [self.pommeGold.get_coords()]
			self.pommeSpec = PommeSpec(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"]) #On crée un objet PommeSpec attribut de snaya, qui nous permettra de gérer le comportement de la pomme spéciale
			self.pommes = {"pomme" : self.pomme.get_coords(), "pomme or" : self.pommeGold.get_coords(), "pomme spec" : self.pommeSpec.get_coords()} #Et on stocke toutes leurs coordonnées dans un dictionnaire
		else : #Sinon, on ne stocke que les coordonnées de la pomme normale
			self.pommes = {"pomme" : self.pomme.get_coords()}

		self.can.delete(ALL) #On supprime tout l'affichage existant
		self.can.config(width = 16*self.param.get_parametres()["largeur"]+32, height = 16*self.param.get_parametres()["hauteur"]+48, bg = "#050505") #On redimensionne le canevas afin qu'il s'adapte à la taille de grille choisie

		self.gameRender = {"score" : [], "score line" : [], "grid" : [], "tete" : [], "snake" : [], "pomme" : [], "pomme or" : [], "pomme spec" : [], "game over" : [], "pause" : []} #On initialise un dictionnaire contenant les différents éléments qui seront affichés (vides pour l'instant)
		self.afficher_init() #On execute la fonction qui affiche les éléments fixes du jeu, comme la grille de fond
		self.move() #On lance la fonction qui tourne en boucle pendant le jeu et qui permet de gérer le déroulement du jeu ainsi que les actions du joueur

	def afficher_init(self) :
		"""
		Fonction qui va afficher les éléments fixes lorsque l'on est en jeu, c'est à dire la grille et la barre en dessous de l'affichage du score.
		"""

		self.gameRender["score line"] = [self.can.create_line(0, 14, 16*self.param.get_parametres()["largeur"]+32, 14, fill = "#E0E0E0")] #On crée une ligne qui se trouve en dessous du score

		for i in range(0, self.param.get_parametres()["largeur"]) : #On crée un certain nombre de rectangles qui vont constituer la grille sur laquelle se déplace le serpent
			for j in range(0, self.param.get_parametres()["hauteur"]) :
				self.gameRender["grid"] = self.gameRender["grid"] + [self.can.create_rectangle(i*16+18, j*16+30, (i+1)*16+18, (j+1)*16+30, outline = "#404040", fill = "#1B1B1B")]

	def move(self) :
		"""
		Fonction qui s'appelle automatiquement sous certaines conditions afin de créer la boucle de jeu, et qui va gérer l'ordre dans lequel les différentes opérations sont effectuées.
		"""

		if self.bonus == True : #Si les bonus sont activés, on crée un dictionnaire qui contiendra les coordonnées des pommes normales, dorées et spéciales
			self.pommes = {"pomme" : self.pomme.get_coords(), "pomme or" : self.pommeGold.get_coords(), "pomme spec" : self.pommeSpec.get_coords()}
		else : #Sinon, ce dictionnaire contiendra seulement les coordonnées de la pomme normale
			self.pommes = {"pomme" : self.pomme.get_coords()}

		if self.pause != True : #Si le jeu n'est pas en pause, on exécute la commande qui gère les déplacements du serpent
			self.deplacer()

		snake = self.snake.get_coords_and_directions() #On va chercher les valeurs des coordonnées et directions du serpent, de la largeur et de la hauteur de la grille dans leurs attributs respectifs, afin d'éviter d'appeler leurs fonctions souvent
		snakeCoords = self.snake.get_coords()
		largeur = self.param.get_largeur()
		hauteur = self.param.get_hauteur()

		if snakeCoords[0] not in self.grilleParcours : #Pour l'achievement numéro 5, si le serpent n'est pas déjà passé sur cette case, elle est ajotuée à la liste des cases parcourues
			self.grilleParcours += [snakeCoords[0]]

		if self.bonus == True and snake[0][1] != snake[1][1] : #Si les bonus sont activés et si la direction du serpent a changé, on execute la fonction qui compte le nombre de déplacements et qui gère la disparition des pommes spéciales suivant celui-ci
			self.pommeGold.deplacement()
			self.pommeSpec.deplacement()

		if self.pause != True : #Si le jeu n'est pas en pause,
			if self.bonus == True : #Si les bonus sont activés,
				if self.snake.isEat() == True : #Si le serpent a mangée une pomme normale,
					self.score += 100 #on augmente le score de 100 points,
					self.comptes.plus_one_pomme() #on incrémente le compteur de pommes total...
					self.pommesPartie += 1 #... ainsi que celui de la partie en cours,
					self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur) #et on fait apparaître une nouvelle pomme
					if self.pommes["pomme or"] == () : #Si il n'y pas encore de pomme d'or sur la grille, on en fait peut-être apparaître une également
						self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
					if self.pommes["pomme spec"] == () : #Si il n'y pas encore de pomme spéciale sur la grille, on en fait peut-être apparaître une également
						self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur)
				if self.snake.goldEat == True : #Si le serpent a mangée une pomme dorée,
					self.score = self.score + 500 #on augmente le score de 500 points,
					self.comptes.plus_one_pomme_gold() #on incrémente le compteur de pommes dorées total,
					self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur) #on fait peut-être apparaître une nouvelle pomme d'or,
					self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur) #on fait apparaître une nouvelle pomme
					if self.pommes["pomme spec"] == () : #Si il n'y pas encore de pomme spéciale sur la grille, on en fait peut-être apparaître une également
						self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur)
				if self.snake.specEat == True : #Si le serpent a mangée une pomme spéciale,
					self.score = self.score + 100 #on augmente le score de 100 points,
					self.comptes.plus_one_pomme_spec() #on incrémente le compteur de pommes spéciales total,
					self.pommeSpec.mange() #on execute la fonction qui indique à quel moment la pomme spéciale a été mangée
					self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur) #on fait peut-être apparaître une nouvelle pomme spéciale,
					self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur) #on fait apparaître une nouvelle pomme
					if self.pommes["pomme or"] == () : #Si il n'y pas encore de pomme spéciale sur la grille, on en fait peut-être apparaître une également
						self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
			else : #Sinon,
				if self.snake.isEat == True : #Si le serpent a mangée une pomme normale,
					self.score += 100 #on augmente le score de 100 points,
					self.comptes.plus_one_pomme() #on incrémente le compteur de pommes total...
					self.pommesPartie += 1 #... ainsi que celui de la partie en cours,
					self.pomme.spawn_pomme(snakeCoords, largeur, hauteur) #et on fait apparaître une nouvelle pomme

		self.nettoyer_aff() #On execute la fonction qui retire tous les éléments de l'affichage afin de le rafraîchir

		self.gameRender["score"] += [self.can.create_text(5, 0, text = "Score : " + str(self.score), font = ("Courier", 10), anchor = NW, fill = "#E0E0E0")] #On affiche le score

		if self.param.get_parametres()["graph mode"] == "sprite" : #Si l'on est en mode sprite,
			self.afficher() #on affiche les différents éléments sous forme d'images
		else : #Sinon,
			self.afficher_simple() #on affiche les différents éléments sous forme de rectangles

		if self.pause == True : #Si le jeu est en pause,
			self.afficher_pause() #on execute la fonction qui affiche l'écran de pause

		if self.snake.isOver() != True : #Si la partie n'a pas été perdue,
			isOk = False
			while isOk != True : #on attend que le temps entre deux rafraîchissements se soit écoulé (en ajoutant éventuellement celui de la pomme spéciale),
				self.temps = time.time()*1000
				if self.bonus == True :
					if self.temps > self.oldTemps + self.param.get_parametres()["step"] + self.pommeSpec.get_step() :
						isOk = True
						self.oldTemps = self.temps
						self.root.after(10, self.move) #et une fois que c'est le cas, on execute à nouveau cette fonction
				else :
					if self.temps > self.oldTemps + self.param.get_parametres()["step"] :
						isOk = True
						self.oldTemps = self.temps
						self.root.after(10, self.move)
		else : #Sinon, on execute la fonction qui gère la perte de la partie
			self.game_over()

	def deplacer(self) :
		"""
		"""

		largeur = self.param.get_largeur()
		hauteur = self.param.get_hauteur()

		if self.direction == "west" and self.oldDirection != "east" :
			self.snake.go_west(self.pommes, largeur, hauteur)
			self.oldDirection = "west"
		elif self.direction == "north" and self.oldDirection != "south" :
			self.snake.go_north(self.pommes, largeur, hauteur)
			self.oldDirection = "north"
		elif self.direction == "east" and self.oldDirection != "west" :
			self.snake.go_east(self.pommes, largeur, hauteur)
			self.oldDirection = "east"
		elif self.direction == "south" and self.oldDirection != "north" :
			self.snake.go_south(self.pommes, largeur, hauteur)
			self.oldDirection = "south"
		elif self.oldDirection == "west" :
			self.snake.go_west(self.pommes, largeur, hauteur)
		elif self.oldDirection == "north" :
			self.snake.go_north(self.pommes, largeur, hauteur)
		elif self.oldDirection == "east" :
			self.snake.go_east(self.pommes, largeur, hauteur)
		elif self.oldDirection == "south" :
			self.snake.go_south(self.pommes, largeur, hauteur)

	def nettoyer_aff(self) :
		"""
		"""

		for j in self.gameRender["score"] :
			self.can.delete(j)
		for j in self.gameRender["tete"] :
			self.can.delete(j)
		for j in self.gameRender["snake"] :
			self.can.delete(j)
		for j in self.gameRender["pomme"] :
			self.can.delete(j)
		for j in self.gameRender["pomme or"] :
			self.can.delete(j)
		for j in self.gameRender["pomme spec"] :
			self.can.delete(j)
		for j in self.gameRender["pause"] :
			self.can.delete(j)

	def afficher(self) :
		"""
		"""

		snake = self.snake.get_coords_and_directions()
		images = self.images.get_images()


		if snake[0][1] == "west" :
			self.gameRender["tete"] = self.gameRender["tete"] + [self.can.create_image(snake[0][0][0]*16+18, snake[0][0][1]*16+30, anchor = N, image = images["snake head left"])]
		elif snake[0][1] == "north" :
			self.gameRender["tete"] = self.gameRender["tete"] + [self.can.create_image(snake[0][0][0]*16+18, snake[0][0][1]*16+30, anchor = W, image = images["snake head top"])]
		elif snake[0][1] == "east" :
			self.gameRender["tete"] = self.gameRender["tete"] + [self.can.create_image(snake[0][0][0]*16+18, snake[0][0][1]*16+30, anchor = NW, image = images["snake head right"])]
		else :
			self.gameRender["tete"] = self.gameRender["tete"] + [self.can.create_image(snake[0][0][0]*16+18, snake[0][0][1]*16+30, anchor = NW, image = images["snake head bot"])]

		tour = 0
		for j in snake[1:] :
			direction = j[1]
			if snake[tour][1] == "east" :
				if snake[tour+1][1] == "east" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body horizontal"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "north" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body firstangle"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "south" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body thirdangle"])] #on dessine le corps du serpent
				else :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body"])] #on dessine le corps du serpent
			elif snake[tour][1] == "north" :
				if snake[tour+1][1] == "east" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body fthangle"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "north" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body vertical"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "west" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body thirdangle"])] #on dessine le corps du serpent
				else :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body"])] #on dessine le corps du serpent
			elif snake[tour][1] == "west" :
				if snake[tour+1][1] == "south" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body fthangle"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "north" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body secangle"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "west" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body horizontal"])] #on dessine le corps du serpent
				else :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body"])] #on dessine le corps du serpent
			elif snake[tour][1] == "south" :
				if snake[tour+1][1] == "east" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body secangle"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "south" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body vertical"])] #on dessine le corps du serpent
				elif snake[tour+1][1] == "west" :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body firstangle"])] #on dessine le corps du serpent
				else :
					self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body"])] #on dessine le corps du serpent
			else :
				self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_image(j[0][0]*16+18, j[0][1]*16+30, anchor = NW, image = images["snake body"])] #on dessine le corps du serpent
			tour = tour+1

		self.gameRender["pomme"] = self.gameRender["pomme"] + [self.can.create_image(self.pomme.get_coords()[0]*16+18, self.pomme.get_coords()[1]*16+30, anchor = NW, image = images["apple"])]
		if self.pommeGold.get_coords() != () :
			self.gameRender["pomme or"] = self.gameRender["pomme or"] + [self.can.create_image(self.pommeGold.get_coords()[0]*16+18, self.pommeGold.get_coords()[1]*16+30, anchor = NW, image = images["apple gold"])]
		if self.pommeSpec.get_coords() != () :
			self.gameRender["pomme spec"] = self.gameRender["pomme spec"] + [self.can.create_image(self.pommeSpec.get_coords()[0]*16+18, self.pommeSpec.get_coords()[1]*16+30, anchor = NW, image = images["apple spec"])]

	def afficher_simple(self) :
		"""
		"""

		snake = self.snake.get_coords_and_directions()
		pomme = self.pomme.get_coords()
		pommeGold = self.pommeGold.get_coords()
		pommeSpec = self.pommeSpec.get_coords()

		self.gameRender["tete"] = self.gameRender["tete"] + [self.can.create_rectangle(snake[0][0][0]*16+18, snake[0][0][1]*16+30, (snake[0][0][0]+1)*16+18, (snake[0][0][1]+1)*16+30, outline = "#E0E0E0", fill = "#FFAA00")]

		for j in snake[1:] :
			self.gameRender["snake"] = self.gameRender["snake"] + [self.can.create_rectangle(j[0][0]*16+18, j[0][1]*16+30, (j[0][0]+1)*16+18, (j[0][1]+1)*16+30, outline = "#E0E0E0", fill = "#FF7000")]

		self.gameRender["pomme"] = self.gameRender["pomme"] + [self.can.create_rectangle(pomme[0]*16+18, pomme[1]*16+30, (pomme[0]+1)*16+18, (pomme[1]+1)*16+30, outline = "#E0E0E0", fill = "#FF0000")]
		if self.pommeGold.get_coords() != () :
			self.gameRender["pomme or"] = self.gameRender["pomme or"] + [self.can.create_rectangle(pommeGold[0]*16+18, pommeGold[1]*16+30, (pommeGold[0]+1)*16+18, (pommeGold[1]+1)*16+30, outline = "#E0E0E0", fill = "#FFE600")]
		if self.pommeSpec.get_coords() != () :
			self.gameRender["pomme spec"] = self.gameRender["pomme spec"] + [self.can.create_rectangle(pommeSpec[0]*16+18, pommeSpec[1]*16+30, (pommeSpec[0]+1)*16+18, (pommeSpec[1]+1)*16+30, outline = "#E0E0E0", fill = "#0000FF")]

	def afficher_pause(self) :
		"""
		"""

		self.gameRender["pause"] = self.gameRender["pause"] + [self.can.create_rectangle(42, 54, 16*self.param.get_parametres()["largeur"]-6, 16*self.param.get_parametres()["hauteur"]+6, stipple = "gray50", fill = "#424242", width = 0)]
		self.gameRender["pause"] = self.gameRender["pause"] + [self.can.create_text(8*self.param.get_parametres()["largeur"]+16, 60, anchor = N, text = "Pause", font = ("Mayan", 12), fill = "#E0E0E0")]

	def game_over(self) :
		"""
		"""

		if self.bonus == True :
			self.pommeGold.despawn()
			self.pommeSpec.despawn()

		self.isOver = True

		self.comptes.plus_one_partie()
		self.comptes.add_score(self.score)

		if self.comptes.get_comptes()["score total"] >= 100000 and self.skins.get_skins()["bleu_jaune"] != True :
			self.skins.unlock_skin("bleu_jaune")

		if self.pommesPartie >= 10 :
			self.ach.ach_unlock(1)

		if self.comptes.get_comptes()["nombre pommes"] >= 100 :
			self.ach.ach_unlock(2)

		if self.comptes.get_comptes()["nombre pommes or"] >= 150 :
			self.ach.ach_unlock(3)

		if self.comptes.get_comptes()["nombre pommes spec"] >= 100 :
			self.ach.ach_unlock(4)

		if len(self.grilleParcours) == self.param.get_largeur()*self.param.get_hauteur() :
			self.ach.ach_unlock(5)

		if self.save.isFileSelected == True :
			self.save.write_to_file(self.playerName["name"], self.paths.get_path("resources"), self.hs.get_highscores(), self.ach.get_achievements(), self.skins.get_skins(), self.comptes.get_comptes(), self.param.get_parametres())

		self.gameRender["game over"] = self.gameRender["game over"] + [self.can.create_rectangle(42, 54, 16*self.param.get_parametres()["largeur"]-6, 16*self.param.get_parametres()["hauteur"]+6, stipple = "gray50", fill = "#424242", width = 0)]
		self.gameRender["game over"] = self.gameRender["game over"] + [self.can.create_text(8*self.param.get_parametres()["largeur"]+16, 60, anchor = N, text = "Game Over", font = ("Mayan", 12), fill = "#E0E0E0")]
		self.gameRender["game over"] = self.gameRender["game over"] + [self.can.create_text(8*self.param.get_parametres()["largeur"]+16, 16*self.param.get_parametres()["hauteur"]-12, anchor = S, text = "Retour au", font = ("Mayan", 12), fill = "#E0E0E0")]
		self.gameRender["game over"] = self.gameRender["game over"] + [self.can.create_text(8*self.param.get_parametres()["largeur"]+16, 16*self.param.get_parametres()["hauteur"], anchor = S, text = "menu", font = ("Mayan", 12), fill = "#E0E0E0")]

	def retour_menu(self) :
		"""
		"""

		self.can.delete(ALL)
		self.can.config(width = 800, height = 600)

		self.dansMenu = True
		self.dansJeu = False

		self.hs.add_score(self.score, self.playerName["name"])

		self.menuRender = {"background" : [], "highlight line" : [], "title texts" : [], "sélection texts" : [], "highscores texts" : [], "achievements texts" : [], "achievements elements" : [], "paramètres texts" : []}
		self.menuMechanics = {"current menu" : "title", "highlight" : 0}

		self.menu()

	def quitter(self) :
		"""
		"""

		if (messagebox.askyesno(title = "Quitter", message = "Voulez-vous vraiment quitter? :(")) :
			self.root.destroy()
		else :
			return 0
#

	#*************** CLASSES SECONDAIRES ***************#


class Save :
	"""
	"""

	def __init__(self) :
		"""
		"""

		self.path = ""
		self.isFileSelected = False
		self.integrity = True
		self.saveFile = []
		self.save = []

	def open_dialog(self) :
		"""
		"""

		self.path = filedialog.askopenfilename(title = "Ouvrir le fichier de sauvegarde", filetypes = [("sauvegarde Snaya",".sav"),("tous les fichiers","*")], initialfile = "snaya.sav")
		if self.path != "" :
			self.isFileSelected = True

	def check_integrity(self) :
		"""
		"""

		try :
			self.file = open(self.path, 'r')
		except Exception :
			self.integrity = False
			return 0

		for j in self.file :
			self.saveFile.append(j.rstrip('\n'))

		self.file.close()

		for j in self.saveFile :
			if j != "" and "#" not in j :
				self.save.append(j)

		nameS = False
		cheminsS = False
		highscoresS = False
		achievementsS = False
		skinsS = False
		comptesS = False
		parametresS = False
		nameE = False
		cheminsE = False
		highscoresE = False
		achievementsE = False
		skinsE = False
		comptesE = False
		parametresE = False

		for j in self.save :
			if "/name_start" in j :
				nameS = True
			if "/name_end" in j :
				nameE = True
			if "/chemins_start" in j :
				cheminsS = True
			if "/chemins_end" in j :
				cheminsE = True
			if "/highscores_start" in j :
				highscoresS = True
			if "/highscores_end" in j :
				highscoresE = True
			if "/achievements_start" in j :
				achievementsS = True
			if "/achievements_end" in j :
				achievementsE = True
			if "/skins_start" in j :
				skinsS = True
			if "/skins_end" in j :
				skinsE = True
			if "/comptes_start" in j :
				comptesS = True
			if "/comptes_end" in j :
				comptesE = True
			if "/parametres_start" in j :
				parametresS = True
			if "/parametres_end" in j :
				parametresE = True

		if not nameS or not nameE or not cheminsS or not cheminsE or not highscoresS or not highscoresE or not achievementsS or not achievementsE or not skinsS or not skinsE or not comptesS or not comptesE or not parametresS or not parametresE :
			self.integrity = False

	def use_default(self) :
		"""
		"""

		self.isFileSelected = False
		self.integrity = True
		self.save = ['/name_start', 'name = "AAA"', '/name_end', '/chemins_start', 'resources path = ""', '/chemins_end', '/highscores_start', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '/highscores_end', '/achievements_start', 'achievement1 = False', 'achievement2 = False', 'achievement3 = False', 'achievement4 = False', 'achievement5 = False', '/achievements_end', '/skins_start', 'jaune_vert = True', 'bleu_jaune = False', 'selected skin = "jaune_vert"', '/skins_end', '/comptes_start', 'nombre pommes norm = "0"', 'nombre pommes gold = "0"', 'nombre pommes spec = "0"', 'score total = "0"', 'nombre parties = "0"', '/comptes_end', '/parametres_start', 'graph mode = "simple"', 'grille taille = "20,20"', 'bonus = True', 'vitesse = "2"', '/parametres_end']
		self.proceed()

	def proceed(self) :
		"""
		"""

		self.ranger()
		self.assigner()

	def ranger(self) :
		"""
		"""

		nameRead = []
		cheminsRead = []
		highscoresRead = []
		achievementsRead = []
		skinsRead = []
		comptesRead = []
		parametresRead = []

		name = False
		chemins = False
		highscores = False
		achievements = False
		skins = False
		comptes = False
		parametres = False

		for j in self.save :
			if '/name_start' in j :
				name = True
			if '/chemins_start' in j :
				chemins = True
			if '/highscores_start' in j :
				highscores = True
			if '/achievements_start' in j :
				achievements = True
			if '/skins_start' in j :
				skins = True
			if '/comptes_start' in j :
				comptes = True
			if '/parametres_start' in j :
				parametres = True

			if '/name_end' in j :
				name = False
			if '/chemins_end' in j :
				chemins = False
			if '/highscores_end' in j :
				highscores = False
			if '/achievements_end' in j :
				achievements = False
			if '/skins_end' in j :
				skins = False
			if '/comptes_end' in j :
				comptes = False
			if '/parametres_end' in j :
				parametres = False

			if name == True :
				nameRead.append(j)
			if chemins == True :
				cheminsRead.append(j)
			if highscores == True :
				highscoresRead.append(j)
			if achievements == True :
				achievementsRead.append(j)
			if skins == True :
				skinsRead.append(j)
			if comptes == True :
				comptesRead.append(j)
			if parametres == True :
				parametresRead.append(j)

		for j in range(len(nameRead)-1) :
			if nameRead[j] == '' or '/' in nameRead[j] :
				nameRead = nameRead[0:j] + nameRead[j+1:]
		for j in range(len(cheminsRead)-1) :
			if cheminsRead[j] == '' or '/' in cheminsRead[j] :
				cheminsRead = cheminsRead[0:j] + cheminsRead[j+1:]
		for j in range(len(highscoresRead)-1) :
			if highscoresRead[j] == '' or '/' in highscoresRead[j] :
				highscoresRead = highscoresRead[0:j] + highscoresRead[j+1:]
		for j in range(len(achievementsRead)-1) :
			if achievementsRead[j] == '' or '/' in achievementsRead[j] :
				achievementsRead = achievementsRead[0:j] + achievementsRead[j+1:]
		for j in range(len(skinsRead)-1) :
			if skinsRead[j] == '' or '/' in skinsRead[j] :
				skinsRead = skinsRead[0:j] + skinsRead[j+1:]
		for j in range(len(comptesRead)-1) :
			if comptesRead[j] == '' or '/' in comptesRead[j] :
				comptesRead = comptesRead[0:j] + comptesRead[j+1:]
		for j in range(len(parametresRead)-1) :
			if parametresRead[j] == '' or '/' in parametresRead[j] :
				parametresRead = parametresRead[0:j] + parametresRead[j+1:]

		self.rawName = nameRead
		self.rawChemins = cheminsRead
		self.rawHighscores = highscoresRead
		self.rawAchievements = achievementsRead
		self.rawSkins = skinsRead
		self.rawComptes = comptesRead
		self.rawParametres = parametresRead

	def assigner(self) :
		"""
		"""

		lecture = False
		playerName = ""

		for j in self.rawName :
			if 'name' in j and '=' in j :
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						playerName = playerName+k
				self.playerName = playerName[1:]

		lecture = False
		resourcesPath = ""

		for j in self.rawChemins :
			if 'resources path' in j and '=' in j :
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						resourcesPath = resourcesPath+k
				self.resourcesPath = resourcesPath[1:]

		highscores = {}
		compteur = 0

		for j in self.rawHighscores :
			compteur += 1
			highscores[compteur] = j

		self.highscores = highscores

		achievements = {}

		for j in self.rawAchievements :
			if 'achievement1' in j and '=' in j and 'True' in j :
				achievements["ach1"] = True
			elif 'achievement1' in j and '=' in j and 'False' in j :
				achievements["ach1"] = False
			if 'achievement2' in j and '=' in j and 'True' in j :
				achievements["ach2"] = True
			elif 'achievement2' in j and '=' in j and 'False' in j :
				achievements["ach2"] = False
			if 'achievement3' in j and '=' in j and 'True' in j :
				achievements["ach3"] = True
			elif 'achievement3' in j and '=' in j and 'False' in j :
				achievements["ach3"] = False
			if 'achievement4' in j and '=' in j and 'True' in j :
				achievements["ach4"] = True
			elif 'achievement4' in j and '=' in j and 'False' in j :
				achievements["ach4"] = False
			if 'achievement5' in j and '=' in j and 'True' in j :
				achievements["ach5"] = True
			elif 'achievement5' in j and '=' in j and 'False' in j :
				achievements["ach5"] = False

		self.achievements = achievements

		lecture = False
		skins = {}

		for j in self.rawSkins :
			if 'jaune_vert' in j and '=' in j and 'True' in j :
				skins["jaune_vert"] = True
			if 'jaune_vert' in j and '=' in j and 'False' in j :
				skins["jaune_vert"] = False
			if 'bleu_jaune' in j and '=' in j and 'True' in j :
				skins["bleu_jaune"] = True
			if 'bleu_jaune' in j and '=' in j and 'False' in j :
				skins["bleu_jaune"] = False
			if 'selected skin' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				skins["selected skin"] = texte[1:]

		self.skins = skins

		lecture = False
		comptes = {}

		for j in self.rawComptes :
			if 'nombre pommes norm' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				comptes["nombre pommes"] = int(texte)
			if 'nombre pommes gold' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				comptes["nombre pommes or"] = int(texte)
			if 'nombre pommes spec' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				comptes["nombre pommes spec"] = int(texte)
			if 'score total' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				comptes["score total"] = int(texte)
			if 'nombre parties' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				comptes["nombre parties"] = int(texte)

		self.comptes = comptes

		lecture = False
		param = {}

		for j in self.rawParametres :
			if 'graph mode' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				param["graph mode"] = texte
			if 'grille taille' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				coordX, coordY = texte.split(',')
				param["taille grille"] = [int(coordX), int(coordY)]
			if 'bonus' in j and '=' in j and 'True' in j :
				param["bonus"] = True
			elif 'bonus' in j and '=' in j and 'False' in j :
				param["bonus"] = False
			if 'vitesse' in j and '=' in j :
				texte = ""
				for k in j :
					if k == '"' :
						lecture = not lecture
					if lecture == True :
						texte = texte+k
				texte = texte[1:]
				param["vitesse"] = int(texte)

		self.parametres = param

	def write_to_file(self, name, resourcesPath, highscores, achievements, skins, comptes, parametres) :
		"""
		"""

		try :
			self.file = open(self.path, 'w')
		except Exception :
			print("Erreur lors de l'ouverture du fichier.")
			return 0

		highscoresFin = str(highscores[1]["score"]) + ',"' + highscores[1]["name"] + '"\n' + str(highscores[2]["score"]) + ',"' + highscores[2]["name"] + '"\n' + str(highscores[3]["score"]) + ',"' + highscores[3]["name"] + '"\n' + str(highscores[4]["score"]) + ',"' + highscores[4]["name"] + '"\n' + str(highscores[5]["score"]) + ',"' + highscores[5]["name"] + '"\n' + str(highscores[6]["score"]) + ',"' + highscores[6]["name"] + '"\n' + str(highscores[7]["score"]) + ',"' + highscores[7]["name"] + '"\n' + str(highscores[8]["score"]) + ',"' + highscores[8]["name"] + '"\n' + str(highscores[9]["score"]) + ',"' + highscores[9]["name"] + '"\n' + str(highscores[10]["score"]) + ',"' + highscores[10]["name"] + '"'
		achievementsFin = "achievement1 = " + str(achievements[1]) + "\n" + "achievement2 = " + str(achievements[2]) + "\n" + "achievement3 = " + str(achievements[3]) + "\n" + "achievement4 = " + str(achievements[4]) + "\n" + "achievement5 = " + str(achievements[5])
		skinsFin = "jaune_vert = " + str(skins["jaune_vert"]) + "\n" + "bleu_jaune = " + str(skins["bleu_jaune"]) + "\n" + 'selected skin = "' + skins["selected skin"] + '"'
		comptesFin = 'nombre pommes norm = "' + str(comptes["nombre pommes"]) + '"\n' + 'nombre pommes gold = "' + str(comptes["nombre pommes or"]) + '"\n' + 'nombre pommes spec = "' + str(comptes["nombre pommes spec"]) + '"\n' + 'score total = "' + str(comptes["score total"]) + '"\n' + 'nombre parties = "' + str(comptes["nombre parties"]) + '"'
		parametresFin = 'graph mode = "' + parametres["graph mode"] + '"\n' + 'grille taille = "' + str(parametres["largeur"]) + "," + str(parametres["hauteur"]) + '"\n' + "bonus = " + str(parametres["bonus"]) + "\n" + 'vitesse = "' + str(parametres["vitesse"]) + '"'

		sequence = "###NOM###\n\n/name_start\n\nname = " + '"' + name + '"' + "\n\n/name_end\n\n\n###CHEMINS###\n\n/chemins_start\n\nresources path = " + '"' + resourcesPath + '"' + "\n\n/chemins_end\n\n\n###HIGHSCORES###\n\n/highscores_start\n\n" + highscoresFin + "\n\n/highscores_end\n\n\n###ACHIEVEMENTS###\n\n/achievements_start\n\n" + achievementsFin + "\n\n/achievements_end\n\n\n###SKINS###\n\n/skins_start\n\n" + skinsFin + "\n\n/skins_end\n\n\n###COMPTES###\n\n/comptes_start\n\n" + comptesFin + "\n\n/comptes_end\n\n\n###PARAMETRES###\n\n/parametres_start\n\n" + parametresFin + "\n\n/parametres_end"
		self.file.write(sequence)

		self.file.close()

class Paths :
	"""
	"""

	def __init__(self) :
		"""
		"""

		self.save = ""
		self.resources = ""

	def set_path(self, asking, path) :
		"""
		"""

		if asking == "save" :
			self.save = path
		elif asking == "resources" :
			self.resources = path

	def get_path(self, asking) :
		"""
		"""

		if asking == "save" :
			return self.save
		elif asking == "resources" :
			return self.resources

class Highscores :
	"""
	"""

	def __init__(self, save) :
		"""
		"""

		self.highscores = save
		self.order()

	def order(self) :
		"""
		"""

		for j in self.highscores.keys() :
			score, nom = self.highscores[j].split(",")
			score = int(score)
			name = ""
			for k in nom :
				if k != '"' :
					name = name + k
			self.highscores[j] = {"name" : name, "score" : score}

	def add_score(self, newScore, name) :
		"""
		"""

		old = {0 : {"name" : "XXX", "score" : 0}}

		for j in range(1, 11) :
			old[j] = self.highscores[j]

		for j in range(1,11) :
			if newScore > self.highscores[j]["score"] :
				self.highscores[j+1] = old[j]
			if newScore > old[j]["score"] and (newScore <= old[j-1]["score"] or old[j-1] is old[0]) :
				self.highscores[j] = {"name" : name, "score" : newScore}

		self.highscores[11] = 0
		del self.highscores[11]

	def get_highscores(self) :
		"""
		"""

		return self.highscores

class Achievements :
	"""
	"""

	def __init__(self, save) :
		"""
		"""

		self.achievements = save
		self.order()

	def order(self) :
		"""
		"""

		self.numbers = {}
		for j in self.achievements.keys() :
			self.numbers[int(j[3])] = self.achievements[j]

	def ach_unlock(self, ach) :
		"""
		"""

		self.numbers[ach] = True

	def get_achievements(self) :
		"""
		"""

		return self.numbers

class Skins :
	"""
	"""

	def __init__(self, save) :
		"""
		"""

		self.skins = save
		self.skins["unlocked"] = ["jaune_vert"]
		if self.skins["bleu_jaune"] == True :
			self.skins["unlocked"] += ["bleu_jaune"]

	def select_skin(self, skin) :
		"""
		"""

		self.skins["selected skin"] = skin

	def unlock_skin(self, skin) :
		"""
		"""

		self.skins[skin] = True
		self.skins["unlocked"] += [skin]

	def get_skins(self) :
		"""
		"""

		return self.skins

class Comptes :
	"""
	"""

	def __init__(self, save) :
		"""
		"""

		self.comptes = save

	def plus_one_pomme(self) :
		"""
		"""

		self.comptes["nombre pommes"] += 1

	def plus_one_pomme_gold(self) :
		"""
		"""

		self.comptes["nombre pommes or"] += 1

	def plus_one_pomme_spec(self) :
		"""
		"""

		self.comptes["nombre pommes spec"] += 1

	def plus_one_partie(self) :
		"""
		"""

		self.comptes["nombre parties"] += 1

	def add_score(self, score) :
		"""
		"""

		self.comptes["score total"] += score

	def get_comptes(self) :
		"""
		"""

		return self.comptes

class Parametres :
	"""
	"""

	def __init__(self, save) :
		"""
		"""

		self.param = save
		self.speed()
		self.largeur_hauteur()

	def speed(self) :
		"""
		"""

		if self.param["vitesse"] < 2 :
			self.param["step"] = 140
		elif self.param["vitesse"] == 2 :
			self.param["step"] = 110
		elif self.param["vitesse"] == 3 :
			self.param["step"] = 90
		elif self.param["vitesse"] == 4 :
			self.param["step"] = 70
		else :
			self.param["step"] = 50

	def largeur_hauteur(self) :
		"""
		"""

		self.param["largeur"] = self.param["taille grille"][0]
		self.param["hauteur"] = self.param["taille grille"][1]

	def switch_graph_mode(self) :
		"""
		"""

		if self.param["graph mode"] == "sprite" :
			self.param["graph mode"] = "simple"
		else :
			self.param["graph mode"] = "sprite"

	def switch_bonus(self) :
		"""
		"""

		if self.param["bonus"] == True :
			self.param["bonus"] = False
		else :
			self.param["bonus"] = True

	def plus_one_largeur(self) :
		"""
		"""

		if self.param["largeur"] < 99 :
			self.param["taille grille"] = [self.param["largeur"] + 1, self.param["hauteur"]]
			self.largeur_hauteur()

	def plus_one_hauteur(self) :
		"""
		"""

		if self.param["hauteur"] < 99 :
			self.param["taille grille"] = [self.param["largeur"], self.param["hauteur"] + 1]
			self.largeur_hauteur()

	def minus_one_largeur(self) :
		"""
		"""

		if self.param["largeur"] > 10 :
			self.param["taille grille"] = [self.param["largeur"] - 1, self.param["hauteur"]]
			self.largeur_hauteur()

	def minus_one_hauteur(self) :
		"""
		"""

		if self.param["hauteur"] > 10 :
			self.param["taille grille"] = [self.param["largeur"], self.param["hauteur"] - 1]
			self.largeur_hauteur()

	def plus_one_vitesse(self) :
		"""
		"""

		if self.param["vitesse"] < 5 :
			self.param["vitesse"] += 1
			self.speed()

	def minus_one_vitesse(self) :
		"""
		"""

		if self.param["vitesse"] > 1 :
			self.param["vitesse"] -= 1
			self.speed()

	def get_parametres(self) :
		"""
		"""

		return self.param

	def get_largeur(self) :
		"""
		"""

		return self.param["largeur"]

	def get_hauteur(self) :
		"""
		"""

		return self.param["hauteur"]

	def get_step(self) :
		"""
		"""

		return self.param["step"]

	def get_graph_mode(self) :
		"""
		"""

		return self.param["graph mode"]

class Images :
	"""
	"""

	def __init__(self, root = 0, path = 0, skin = 0) :
		"""
		"""

		self.images = {}
		if (root, path, skin) != (0, 0, 0) :
			self.init2(root, path, skin)

	def init2(self, root, path, skin) :
		"""
		"""

		self.chemins(path, skin)
		self.window_icon(root)
		self.dico()

	def update(self, root, path, skin) :
		"""
		"""

		self.chemins(path, skin)
		self.window_icon(root)
		self.dico()

	def chemins(self, path, skin) :
		"""
		"""

		self.paths = {}
		self.paths['window icon'] = path + r"/menu/snayalogolittle.png"
		self.paths['snake head right'] = path + r"/" + skin + r"/snake_head_right.png"
		self.paths['snake head top'] = path + r"/" + skin + r"/snake_head_top.png"
		self.paths['snake head left'] = path + r"/" + skin + r"/snake_head_left.png"
		self.paths['snake head bot'] = path + r"/" + skin + r"/snake_head_bot.png"
		self.paths['snake body'] = path + r"/" + skin + r"/snake_body.png"
		self.paths['snake body vertical'] = path + r"/" + skin + r"/snake_body_vertical.png"
		self.paths['snake body horizontal'] = path + r"/" + skin + r"/snake_body_horizontal.png"
		self.paths['snake body firstangle'] = path + r"/" + skin + r"/snake_body_firstangle.png"
		self.paths['snake body secangle'] = path + r"/" + skin + r"/snake_body_secangle.png"
		self.paths['snake body thirdangle'] = path + r"/" + skin + r"/snake_body_thirdangle.png"
		self.paths['snake body fthangle'] = path + r"/" + skin + r"/snake_body_fthangle.png"
		self.paths['apple'] = path + r"/" + skin + r"/pomme.png"
		self.paths['apple gold'] = path + r"/" + skin + r"/pomme_gold.png"
		self.paths['apple spec'] = path + r"/" + skin + r"/pomme_spec.png"
		self.paths['menu title'] = path + r"/menu/snayatitle.png"
		self.paths['menu'] = path + r"/menu/snayamenu.png"
		self.paths['ach1'] = path + r"/" + skin + r"/ach1.png"
		self.paths['ach2'] = path + r"/" + skin + r"/ach2.png"
		self.paths['ach3'] = path + r"/" + skin + r"/ach3.png"
		self.paths['ach4'] = path + r"/" + skin + r"/ach4.png"
		self.paths['ach5'] = path + r"/" + skin + r"/ach5.png"
		self.paths['no ach'] = path + r"/" + skin + r"/noach.png"
		self.paths['ach bg'] = self.achBg = path + r"/menu/achievements_background.png"

	def window_icon(self, root) :
		"""
		"""

		root.iconphoto(root, PhotoImage(file = self.paths['window icon']))

	def dico(self) :
		"""
		"""

		self.images["snake head right"] = PhotoImage(file = self.paths['snake head right'])
		self.images["snake head top"] = PhotoImage(file = self.paths['snake head top'])
		self.images["snake head left"] = PhotoImage(file = self.paths['snake head left'])
		self.images["snake head bot"] = PhotoImage(file = self.paths['snake head bot'])
		self.images["snake body"] = PhotoImage(file = self.paths['snake body'])
		self.images["snake body vertical"] = PhotoImage(file = self.paths['snake body vertical'])
		self.images["snake body horizontal"] = PhotoImage(file = self.paths['snake body horizontal'])
		self.images["snake body firstangle"] = PhotoImage(file = self.paths['snake body firstangle'])
		self.images["snake body secangle"] = PhotoImage(file = self.paths['snake body secangle'])
		self.images["snake body thirdangle"] = PhotoImage(file = self.paths['snake body thirdangle'])
		self.images["snake body fthangle"] = PhotoImage(file = self.paths['snake body fthangle'])
		self.images["apple"] = PhotoImage(file = self.paths['apple'])
		self.images["apple gold"] = PhotoImage(file = self.paths['apple gold'])
		self.images["apple spec"] = PhotoImage(file = self.paths['apple spec'])
		self.images["menu title"] = PhotoImage(file = self.paths['menu title'])
		self.images["menu"] = PhotoImage(file = self.paths['menu'])
		self.images["ach1"] = PhotoImage(file = self.paths['ach1'])
		self.images["ach2"] = PhotoImage(file = self.paths['ach2'])
		self.images["ach3"] = PhotoImage(file = self.paths['ach3'])
		self.images["ach4"] = PhotoImage(file = self.paths['ach4'])
		self.images["ach5"] = PhotoImage(file = self.paths['ach5'])
		self.images["no ach"] = PhotoImage(file = self.paths['no ach'])
		self.images["ach bg"] = PhotoImage(file = self.paths['ach bg'])

	def get_images(self) :
		"""
		"""

		return self.images
#

	#*************** CLASSES DE JEU ***************#


class Snake :
	"""
	"""

	def __init__(self) :
		"""
		"""

		self.coords = [((2, 0), "east"), ((1, 0), "east"), ((0, 0), "east")]
		self.gameOver = False

	def go_north(self, pommes, largeur, hauteur) :
		"""
		"""

		suppl = self.coords[-1]
		body = self.coords[:-1]

		self.eat = False
		self.goldEat = False
		self.specEat = False

		tete = self.coords[0]
		self.coords = [((tete[0][0], tete[0][1]-1), "north")] + body

		tete = self.coords[0]

		if tete[0][1] == -1 :
			self.coords = [((tete[0][0], hauteur-1), tete[1])] + self.coords[1:]

		tete = self.coords[0]

		self.eating(tete, pommes, suppl)

	def go_south(self, pommes, largeur, hauteur) :
		"""
		"""

		suppl = self.coords[-1]
		body = self.coords[:-1]

		self.eat = False
		self.goldEat = False
		self.specEat = False

		tete = self.coords[0]
		self.coords = [((tete[0][0], tete[0][1]+1), "south")] + body

		tete = self.coords[0]

		if tete[0][1] == hauteur :
			self.coords = [((tete[0][0], 0), tete[1])] + self.coords[1:]

		tete = self.coords[0]

		self.eating(tete, pommes, suppl)

	def go_west(self, pommes, largeur, hauteur) :
		"""
		"""

		suppl = self.coords[-1]
		body = self.coords[:-1]

		self.eat = False
		self.goldEat = False
		self.specEat = False

		tete = self.coords[0]
		self.coords = [((tete[0][0]-1, tete[0][1]), "west")] + body

		tete = self.coords[0]

		if tete[0][0] == -1 :
			self.coords = [((largeur-1, tete[0][1]), tete[1])] + self.coords[1:]

		tete = self.coords[0]

		self.eating(tete, pommes, suppl)

	def go_east(self, pommes, largeur, hauteur) :
		"""
		"""

		suppl = self.coords[-1]
		body = self.coords[:-1]

		self.eat = False
		self.goldEat = False
		self.specEat = False

		tete = self.coords[0]
		self.coords = [((tete[0][0]+1, tete[0][1]), "east")] + body

		tete = self.coords[0]

		if tete[0][0] == largeur :
			self.coords = [((0, tete[0][1]), tete[1])] + self.coords[1:]

		tete = self.coords[0]

		self.eating(tete, pommes, suppl)

	def eating(self, tete, pommes, suppl) :
		"""
		"""

		for j in pommes :
			if tete[0] == pommes[j] :
				self.coords = self.coords + [suppl]
				if j == "pomme" :
					self.eat = True
				if j == "pomme or" :
					self.goldEat = True
				if j == "pomme spec" :
					self.specEat = True

		self.game_over()

	def game_over(self) :
		"""
		"""

		coords = []
		for j in range(len(self.coords)) :
			coords = coords + [self.coords[j][0]]
		if coords[0] in coords[1:] :
			self.gameOver = True

	def get_coords(self) :
		"""
		"""

		coords = []
		for j in range(len(self.coords)-1) :
			coords.append(self.coords[j][0])
		return coords

	def get_coords_and_directions(self) :
		"""
		"""

		return self.coords

	def isOver(self) :
		"""
		"""

		return self.gameOver

	def isEat(self) :
		"""
		"""

		return self.eat

class Pomme :
	"""
	"""

	def __init__(self, interdit, largeur, hauteur) :
		"""
		"""

		self.spawn_pomme(interdit, largeur, hauteur)

	def spawn_pomme(self, interdit, largeur, hauteur) :
		"""
		"""

		grid = []
		for i in range(0, largeur) :
			for j in range(0, hauteur) :
				if (i, j) not in interdit :
					grid = grid + [(i, j)]
		pos = random.randint(0, len(grid))
		self.coords = grid[pos-1]

	def get_coords(self) :
		"""
		"""

		return self.coords

	def despawn(self) :
		"""
		"""

		self.coords = ()

class PommeRand(Pomme) :
	"""
	"""

	def __init__(self, interdit, largeur, hauteur) :
		"""
		"""

		self.depl = 0
		self.choose(interdit, largeur, hauteur)
		self.date = 0

	def choose(self, interdit, largeur, hauteur) :
		"""
		"""

		if random.randint(0, 3) == 1 :
			self.spawn_pomme(interdit, largeur, hauteur)
			self.depl = 5
		else :
			self.coords = ()

	def deplacement(self) :
		"""
		"""

		if self.depl != 0 :
			self.depl -= 1
		else :
			self.coords = ()

class PommeSpec(PommeRand) :
	"""
	"""

	def mange(self) :
		"""
		"""

		self.date = time.time()*1000

	def get_step(self) :
		"""
		"""

		if self.temps() <= 5000 :
			return 100
		else :
			return 0

	def temps(self) :
		"""
		"""

		return time.time()*1000 - self.date
#

	#*************** IMPORTATION DES BIBLIOTHEQUES ***************#


from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random
import time

	#*************** PROGRAMME PRINCIPAL ***************#

snaya = Snaya()
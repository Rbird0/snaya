#CAMELET Alexandre et LECUTIEZ Simon 2015/2016, cours d'ISN - Lycée de la Plaine de l'Ain
#Snaya, notre version du célèbre jeu Snake.
#V2.1.0
#Ce programme, aussi modeste qu'il soit, est proposé librement. Vous pouvez le redistribuer et/ou le modifier selon les termes de la GNU General Public License telle que publiée par la Free Software Foundation, en version 3 ou plus récente (à votre guise).
#Vous pouvez trouver les termes de la GNU GPLv3 dans le fichier LICENSE fourni avec le programme, ou à l'adresse http://www.gnu.org/licenses/gpl.html .
#Rejoignez nous sur la page Github du projet! https://github.com/Rbird0/snaya/


	#*************** CLASSE PRINCIPALE ***************#


class Snaya :
	"""
	"""

	def __init__(self) :
		"""
		"""

		self.root = Tk()
		self.root.title("Snaya")

		self.save = Save()
		self.paths = Paths()

		self.save_load()
		self.root.deiconify()
		self.initialize()

		self.dansMenu = True
		self.dansJeu = False
		self.can = Canvas(self.root, width = 800, height = 600)
		self.can.pack()
		self.menu_init()
		self.menu()

		self.root.mainloop()

	def save_load(self) :
		"""
		"""

		self.save.open_dialog()
		if self.save.isFileSelected == True :
			self.save.check_integrity()
			if self.save.integrity == True :
				self.paths.set_path("save", self.save.path)
				self.save.proceed()
			else :
				print("Le fichier sélectionné n'est pas valide. Une sauvegarde vierge sera utilisée.")
				self.save.use_default()
		else :
			print("Vous n'avez séléctionné aucun fichier. Une sauvegarde vierge sera utilisée.")
			self.save.use_default()

	def initialize(self) :
		"""
		"""

		self.name = self.save.playerName
		self.playerName = {"name" : self.name, 0 : self.name[0], 1 : self.name[1], 2 : self.name[2]}

		self.paths.set_path("resources", self.save.resourcesPath)
		self.hs = Highscores(self.save.highscores)
		self.ach = Achievements(self.save.achievements)
		self.skins = Skins(self.save.skins)
		self.comptes = Comptes(self.save.comptes)
		self.param = Parametres(self.save.parametres)

	def menu_init(self) :
		"""
		"""

		parametres = self.param.get_parametres()
		skins = self.skins.get_skins()

		if parametres["graph mode"] == "sprite" :
			self.images = Images(self.root, self.paths.get_path("resources"), skins["selected skin"])
		else :
			self.images = Images()

		self.menuRender = {"background" : [], "highlight line" : [], "title texts" : [], "sélection texts" : [], "highscores texts" : [], "achievements texts" : [], "achievements elements" : [], "paramètres texts" : []}
		self.menuMechanics = {"current menu" : "title", "highlight" : 0}
		

		self.bind()

	def menu(self) :
		"""
		"""

		highscores = self.hs.get_highscores()
		achievements = self.ach.get_achievements()
		parametres = self.param.get_parametres()

		if parametres["graph mode"] == "sprite" :
			for j in self.menuRender["background"] :
				self.can.delete(j)
		for j in self.menuRender["highlight line"] :
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

		if self.menuMechanics["current menu"] == "title" and parametres["graph mode"] == "sprite" :
			images = self.images.get_images()
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_image(0, 0, anchor = NW, image = images["menu title"])]
		elif parametres["graph mode"] == "sprite" :
			images = self.images.get_images()
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_image(0, 0, anchor = NW, image = images["menu"])]
		else :
			images = 0
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(0, 0, 124, 600, width = 0, fill = "#547e25")]
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(124, 0, 676, 600, width = 0, fill = "#8c5918")]
			self.menuRender["background"] = self.menuRender["background"] + [self.can.create_rectangle(676, 0, 800, 600, width = 0, fill = "#547e25")]
			if self.menuMechanics["current menu"] == "title" :
				self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 30, anchor = N, text = "SNAYA", font = ("Mayan", -130), fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "title" :
			self.menu_title()

		if self.menuMechanics["current menu"] == "sélection nom" :
			self.menu_selection()

		if self.menuMechanics["current menu"] == "highscores" :
			self.menu_highscores(highscores)

		if self.menuMechanics["current menu"] == "achievements" :
			self.menu_achievements(images, achievements, parametres)

		if self.menuMechanics["current menu"] == "paramètres" :
			self.menu_parametres(parametres)

		if self.dansMenu == True :
			self.root.after(10, self.menu)
		else :
			self.launch()

	def menu_title(self) :
		"""
		"""

		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 275, anchor = S, text = "Jouer", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 337.5, anchor = S, text = "Highscores", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 400, anchor = S, text = "Achievements", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 462.5, anchor = S, text = "Paramètres", font = ("Mayan", 25), fill = "#f0cc00")]
		self.menuRender["title texts"] = self.menuRender["title texts"] + [self.can.create_text(400, 525, anchor = S, text = "Quitter", font = ("Mayan", 25), fill = "#f0cc00")]

		self.menuRender["highlight line"] = [self.can.create_line(375, 270 + self.menuMechanics["highlight"]*62.5, 425, 270 + self.menuMechanics["highlight"]*62.5, width = 2, fill = "#f0cc00")]

	def menu_selection(self) :
		"""
		"""

		self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(400, 30, anchor = N, text = "ENTREZ VOTRE NOM", font = ("Mayan", 35), fill = "#f0cc00")]

		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(325, 375, anchor = SE, text = self.playerName[0], font = ("Mayan", 75), fill = "#f0cc00")]
		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(400, 375, anchor = S, text = self.playerName[1], font = ("Mayan", 75), fill = "#f0cc00")]
		self.menuRender["sélection texts"] = self.menuRender["sélection texts"] + [self.can.create_text(475, 375, anchor = SW, text = self.playerName[2], font = ("Mayan", 75), fill = "#f0cc00")]

		self.menuRender["highlight line"] = [self.can.create_line(273 + self.menuMechanics["highlight"]*102, 370, 323 + self.menuMechanics["highlight"]*102, 370, width = 2, fill = "#f0cc00")]

	def menu_highscores(self, highscores) :
		"""
		"""

		self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(400, 30, anchor = N, text = "HIGHSCORES", font = ("Mayan", 35), fill = "#f0cc00")]

		for j in highscores.keys() :
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(245, 160 + 40*(j - 1), anchor = NW, text = highscores[j]["name"], font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(350, 160 + 40*(j - 1), anchor = NW, text = " . . . . . . . . . . . ", font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(600, 160 + 40*(j - 1), anchor = NE, text = highscores[j]["score"], font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.can.create_text(245, 160 + 40*(j - 1), anchor = NE, text = str(j) + ". ", font = ("Mayan", 20), fill = "#f0cc00")]

	def menu_achievements(self, images, achievements, parametres) :
		"""
		"""

		if parametres["graph mode"] == "sprite" :
			self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(201, 171, anchor = NW, image = images["ach bg"])]
		else :
			for j in range(0,5) :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_rectangle(201, 171 + 70*j, 601, 231 + 70*j, width = 0, fill = "#6f4811")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_rectangle(206, 176 + 70*j, 256, 226 + 70*j, width = 0, fill = "#463b2b")]

		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(400, 30, anchor = N, text = "ACHIEVEMENTS", font = ("Mayan", 35), fill = "#f0cc00")]

		nbAch = 0

		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 176, anchor = NW, text = "Adam & Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 246, anchor = NW, text = "Mécanique newtonienne", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 316, anchor = NW, text = "Jeunesse dorée", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 386, anchor = NW, text = "Super Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
		self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 456, anchor = NW, text = "Globetrotter", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]

		if parametres["graph mode"] == "sprite" :
			if achievements[1] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_image(206, 176, anchor = NW, image = images["ach1"])]
				self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.can.create_text(266, 201, anchor = NW, text = "Manger 10 pommes classiques en une partie.", font = ("Mayan", 10), fill = "#f0cc00")]
			else :
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

		else :
			if achievements[1] == True :
				nbAch += 1
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(210, 200, 230, 220, width = 2, fill = "#76cb3d")]
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.can.create_line(230, 220, 252, 180, width = 2, fill = "#76cb3d")]
			else :
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
		"""

		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(400, 30, anchor = N, text = "PARAMÈTRES", font = ("Mayan", 35), fill = "#f0cc00")]

		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 200, anchor = SW, text = "Dossier ressources", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 240, anchor = SW, text = "Sauvegarder", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 280, anchor = SW, text = "Mode graphique: " + parametres["graph mode"], font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 320, anchor = SW, text = "Taille de la grille: " + str(parametres["largeur"]) + " x " + str(parametres["hauteur"]), font = ("Mayan", 20), fill = "#f0cc00")]
		if parametres["bonus"] == True :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 360, anchor = SW, text = "Bonus: avec", font = ("Mayan", 20), fill = "#f0cc00")]
		else :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 360, anchor = SW, text = "Bonus: sans", font = ("Mayan", 20), fill = "#f0cc00")]
		self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 400, anchor = SW, text = "Vitesse: " + str(parametres["vitesse"]), font = ("Mayan", 20), fill = "#f0cc00")]
		if parametres["graph mode"] == "sprite" :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.can.create_text(200, 440, anchor = SW, text = "Skin: " + self.skins.get_skins()["selected skin"], font = ("Mayan", 20), fill = "#f0cc00")]

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
		"""

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
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" :
				self.menuMechanics["highlight"] -= 1
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == -1 :
				self.menuMechanics["highlight"] = 4
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 0 :
				self.name_plus_one(0)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 1 :
				self.name_plus_one(1)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 2 :
				self.name_plus_one(2)
			if self.menuMechanics["current menu"] == "paramètres" and self.param.get_graph_mode() != "sprite" and self.menuMechanics["highlight"] == -1 :
				self.menuMechanics["highlight"] = 6
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == -1 :
				self.menuMechanics["highlight"] = 7
		elif self.dansJeu == True and self.direction != "south" :
			self.direction = "north"
	
	def bas(self, event) :
		"""
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" :
				self.menuMechanics["highlight"] += 1
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 5 :
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 0 :
				self.name_minus_one(0)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 1 :
				self.name_minus_one(1)
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 2 :
				self.name_minus_one(2)
			if self.menuMechanics["current menu"] == "paramètres" and self.param.get_graph_mode() != "sprite" and self.menuMechanics["highlight"] == 7 :
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 8 :
				self.menuMechanics["highlight"] = 0
		elif self.dansJeu == True and self.direction != "north" :
			self.direction = "south"

	def droite(self, event) :
		"""
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "sélection nom" :
				self.menuMechanics["highlight"] += 1
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == 3 :
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 2 and self.paths.get_path("resources") != "" :
				self.param.switch_graph_mode()
				if self.param.get_parametres()["graph mode"] == "sprite" :
					self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 :
				self.param.plus_one_largeur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 :
				self.param.plus_one_hauteur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 5 :
				self.param.switch_bonus()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 :
				self.param.plus_one_vitesse()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 7 :
				j = 0
				while self.skins.get_skins()["unlocked"][j] != self.skins.get_skins()["selected skin"] :
					j += 1
				if self.skins.get_skins()["unlocked"][j] is not self.skins.get_skins()["unlocked"][-1] :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][j+1])
				else :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][0])
				self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
		elif self.dansJeu == True and self.direction != "west" :
			self.direction = "east"

	def gauche(self, event) :
		"""
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "sélection nom" :
				self.menuMechanics["highlight"] -= 1
			if self.menuMechanics["current menu"] == "sélection nom" and self.menuMechanics["highlight"] == -1 :
				self.menuMechanics["highlight"] = 2
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 2 and self.paths.get_path("resources") != "" :
				self.param.switch_graph_mode()
				if self.param.get_parametres()["graph mode"] == "sprite" :
					self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
			if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 :
				self.param.minus_one_largeur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 :
				self.param.minus_one_hauteur()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 5 :
				self.param.switch_bonus()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 :
				self.param.minus_one_vitesse()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 7 :
				j = 0
				while self.skins.get_skins()["unlocked"][j] != self.skins.get_skins()["selected skin"] :
					j += 1
				if self.skins.get_skins()["unlocked"][j] is not self.skins.get_skins()["unlocked"][0] :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][j-1])
				else :
					self.skins.select_skin(self.skins.get_skins()["unlocked"][-1])
				self.images = Images(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
		elif self.dansJeu == True and self.direction != "east" :
			self.direction = "west"

	def suivant(self, event) :
		"""
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 0 :
				self.menuMechanics["current menu"] = "sélection nom"
				self.menuMechanics["highlight"] = 0
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 1 :
				self.menuMechanics["current menu"] = "highscores"
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 2 :
				self.menuMechanics["current menu"] = "achievements"
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 3 :
				self.menuMechanics["current menu"] = "paramètres"
				self.menuMechanics["highlight"] = 0
			elif self.menuMechanics["current menu"] == "sélection nom" :
				self.dansMenu = False
			elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 4 :
				self.quitter()
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 0 :
				path = filedialog.askdirectory(title = "Choisir le dossier de ressources")
				if path != "" :
					self.paths.set_path("resources", path)
					if self.param.get_parametres()["graph mode"] == "sprite" :
						self.images.update(self.root, self.paths.get_path("resources"), self.skins.get_skins()["selected skin"])
				else :
					print("Vous n'avez sélectionné aucun dossier! Rien ne sera fait.")
			elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 1 :
				self.save.write_to_file(self.playerName["name"], self.paths.get_path("resources"), self.hs.get_highscores(), self.ach.get_achievements(), self.skins.get_skins(), self.comptes.get_comptes(), self.param.get_parametres())
		elif self.isOver == True :
			self.isOver = False
			self.retour_menu()

	def precedent(self, event) :
		"""
		"""

		if self.dansMenu == True :
			if self.menuMechanics["current menu"] == "title" :
				self.quitter()
			if self.menuMechanics["current menu"] == "sélection nom" :
				self.menuMechanics["highlight"] = 0
			if self.menuMechanics["current menu"] == "highscores" :
				self.menuMechanics["highlight"] = 1
			if self.menuMechanics["current menu"] == "achievements" :
				self.menuMechanics["highlight"] = 2
			if self.menuMechanics["current menu"] == "paramètres" :
				self.menuMechanics["highlight"] = 3
			self.menuMechanics["current menu"] = "title"

	def name_plus_one(self, position) :
		"""
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
		"""

		self.playerName["name"] = self.playerName[0] + self.playerName[1] + self.playerName[2]

	def launch(self) :
		"""
		"""

		self.score = 0
		self.oldTemps = 0
		self.direction = "east"
		self.oldDirection = "east"

		self.dansJeu = True
		self.bonus = self.param.get_parametres()["bonus"]

		self.grilleParcours = []

		self.pommesPartie = 0

		self.snake = Snake()
		interdit = self.snake.get_coords()
		self.pomme = Pomme(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"])
		if self.bonus == True :
			interdit = interdit + [self.pomme.get_coords()]
			self.pommeGold = PommeRand(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"])
			interdit = interdit + [self.pommeGold.get_coords()]
			self.pommeSpec = PommeSpec(interdit, self.param.get_parametres()["largeur"], self.param.get_parametres()["hauteur"])
			self.pommes = {"pomme" : self.pomme.get_coords(), "pomme or" : self.pommeGold.get_coords(), "pomme spec" : self.pommeSpec.get_coords()}
		else :
			self.pommes = {"pomme" : self.pomme.get_coords()}

		self.can.delete(ALL)
		self.can.config(width = 16*self.param.get_parametres()["largeur"]+32, height = 16*self.param.get_parametres()["hauteur"]+48, bg = "#050505")

		self.gameRender = {"score" : [], "score line" : [], "grid" : [], "tete" : [], "snake" : [], "pomme" : [], "pomme or" : [], "pomme spec" : [], "game over" : []}
		self.afficher_init()
		self.move()

	def afficher_init(self) :
		"""
		"""

		self.gameRender["score line"] = [self.can.create_line(0, 14, 16*self.param.get_parametres()["largeur"]+32, 14, fill = "#E0E0E0")]

		for i in range(0, self.param.get_parametres()["largeur"]) :
			for j in range(0, self.param.get_parametres()["hauteur"]) :
				self.gameRender["grid"] = self.gameRender["grid"] + [self.can.create_rectangle(i*16+18, j*16+30, (i+1)*16+18, (j+1)*16+30, outline = "#404040", fill = "#1B1B1B")]

	def move(self) :
		"""
		"""

		if self.bonus == True :
			self.pommes = {"pomme" : self.pomme.get_coords(), "pomme or" : self.pommeGold.get_coords(), "pomme spec" : self.pommeSpec.get_coords()}
		else :
			self.pommes = {"pomme" : self.pomme.get_coords()}

		self.deplacer()

		snake = self.snake.get_coords_and_directions()
		snakeCoords = self.snake.get_coords()
		largeur = self.param.get_largeur()
		hauteur = self.param.get_hauteur()

		if snakeCoords[0] not in self.grilleParcours :
			self.grilleParcours += [snakeCoords[0]]

		if self.bonus == True :
			if snake[0][1] != snake[1][1] :
				self.pommeGold.deplacement()
				self.pommeSpec.deplacement()

		if self.bonus == True :
			if self.snake.eat == True :
				self.score = self.score + 100
				self.comptes.plus_one_pomme()
				self.pommesPartie += 1
				self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
				if self.pommes["pomme or"] == () :
					self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
				if self.pommes["pomme spec"] == () :
					self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur)
			if self.snake.goldEat == True :
				self.score = self.score + 500
				self.comptes.plus_one_pomme_gold()
				self.pommeGold.mange()
				self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
				self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
				if self.pommes["pomme spec"] == () :
					self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur)
			if self.snake.specEat == True :
				self.score = self.score + 100
				self.comptes.plus_one_pomme_spec()
				self.pommeSpec.mange()
				self.pommeSpec.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeGold.get_coords()], largeur, hauteur)
				self.pomme.spawn_pomme(snakeCoords + [self.pommeGold.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
				if self.pommes["pomme or"] == () :
					self.pommeGold.choose(snakeCoords + [self.pomme.get_coords()] + [self.pommeSpec.get_coords()], largeur, hauteur)
		else :
			if self.snake.eat == True :
				self.score = self.score + 100
				self.comptes.plus_one_pomme()
				self.pommesPartie += 1
				self.pomme.spawn_pomme(snakeCoords, largeur, hauteur)

		self.nettoyer_aff()

		self.gameRender["score"] = self.gameRender["score"] + [self.can.create_text(5, 0, text = "Score : " + str(self.score), font = ("Courier", 10), anchor = NW, fill = "#E0E0E0")]

		if self.param.get_parametres()["graph mode"] == "sprite" :
			self.afficher()
		else :
			self.afficher_simple()

		if self.snake.isOver() != True :
			isOk = False
			while isOk != True :
				self.temps = time.time()*1000
				if self.bonus == True :
					if self.temps > self.oldTemps + self.param.get_parametres()["step"] + self.pommeSpec.get_step() :
						isOk = True
						self.oldTemps = self.temps
						self.root.after(10, self.move)
				else :
					if self.temps > self.oldTemps + self.param.get_parametres()["step"] :
						isOk = True
						self.oldTemps = self.temps
						self.root.after(10, self.move)
		else :
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

	def mange(self) :
		"""
		"""

		self.date = time.time()*1000

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
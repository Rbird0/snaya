#CAMELET Alexandre et LECUTIEZ Simon 2015/2016, cours d'ISN - Lycée de la Plaine de l'Ain
#Snaya, notre version du célèbre jeu Snake.
#V2.1.0


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

		self.menuRender = {"background" : [], "highlight line" : [], "title texts" : [], "highscores texts" : [], "achievements texts" : [], "achievements elements" : [], "paramètres texts" : []}
		self.menuMechanics = {"current menu" : "title", "highlight" : 0, "value" : 0}
		self.menuCan = Canvas(self.root, width = 800, height = 600)
		self.menuCan.pack()

		self.bind()

	def menu(self) :
		"""
		"""

		highscores = self.hs.get_highscores()
		achievements = self.ach.get_achievements()
		parametres = self.param.get_parametres()

		if parametres["graph mode"] == "sprite" :
			for j in self.menuRender["background"] :
				self.menuCan.delete(j)
		for j in self.menuRender["highlight line"] :
			self.menuCan.delete(j)
		for j in self.menuRender["title texts"] :
			self.menuCan.delete(j)
		for j in self.menuRender["highscores texts"] :
			self.menuCan.delete(j)
		for j in self.menuRender["achievements texts"] :
			self.menuCan.delete(j)
		for j in self.menuRender["achievements elements"] :
			self.menuCan.delete(j)
		for j in self.menuRender["paramètres texts"] :
			self.menuCan.delete(j)

		if self.menuMechanics["current menu"] == "title" and parametres["graph mode"] == "sprite" :
			images = self.images.get_images()
			self.menuRender["background"] = self.menuRender["background"] + [self.menuCan.create_image(0, 0, anchor = NW, image = images["menu title"])]
		elif parametres["graph mode"] == "sprite" :
			images = self.images.get_images()
			self.menuRender["background"] = self.menuRender["background"] + [self.menuCan.create_image(0, 0, anchor = NW, image = images["menu"])]
		else :
			self.menuRender["background"] = self.menuRender["background"] + [self.menuCan.create_rectangle(0, 0, 124, 600, width = 0, fill = "#547e25")]
			self.menuRender["background"] = self.menuRender["background"] + [self.menuCan.create_rectangle(124, 0, 676, 600, width = 0, fill = "#8c5918")]
			self.menuRender["background"] = self.menuRender["background"] + [self.menuCan.create_rectangle(676, 0, 800, 600, width = 0, fill = "#547e25")]
			if self.menuMechanics["current menu"] == "title" :
				self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 30, anchor = N, text = "SNAYA", font = ("Mayan", -130), fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "title" :

			self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 275, anchor = S, text = "Jouer", font = ("Mayan", 25), fill = "#f0cc00")]
			self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 337.5, anchor = S, text = "Highscores", font = ("Mayan", 25), fill = "#f0cc00")]
			self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 400, anchor = S, text = "Achievements", font = ("Mayan", 25), fill = "#f0cc00")]
			self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 462.5, anchor = S, text = "Paramètres", font = ("Mayan", 25), fill = "#f0cc00")]
			self.menuRender["title texts"] = self.menuRender["title texts"] + [self.menuCan.create_text(400, 525, anchor = S, text = "Quitter", font = ("Mayan", 25), fill = "#f0cc00")]

			self.menuRender["highlight line"] = [self.menuCan.create_line(375, 270 + self.menuMechanics["highlight"]*62.5, 425, 270 + self.menuMechanics["highlight"]*62.5, width = 2, fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "highscores" :

			self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.menuCan.create_text(400, 30, anchor = N, text = "HIGHSCORES", font = ("Mayan", 35), fill = "#f0cc00")]

			for j in highscores.keys() :
				self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.menuCan.create_text(245, 160 + 40*(j - 1), anchor = NW, text = highscores[j]["name"], font = ("Mayan", 20), fill = "#f0cc00")]
				self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.menuCan.create_text(350, 160 + 40*(j - 1), anchor = NW, text = " . . . . . . . . . . . ", font = ("Mayan", 20), fill = "#f0cc00")]
				self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.menuCan.create_text(600, 160 + 40*(j - 1), anchor = NE, text = highscores[j]["score"], font = ("Mayan", 20), fill = "#f0cc00")]
				self.menuRender["highscores texts"] = self.menuRender["highscores texts"] + [self.menuCan.create_text(245, 160 + 40*(j - 1), anchor = NE, text = str(j) + ". ", font = ("Mayan", 20), fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "achievements" :
			if parametres["graph mode"] == "sprite" :
				self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(201, 171, anchor = NW, image = images["ach bg"])]
			else :
				for j in range(0,5) :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_rectangle(201, 171 + 70*j, 601, 231 + 70*j, width = 0, fill = "#6f4811")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_rectangle(206, 176 + 70*j, 256, 226 + 70*j, width = 0, fill = "#463b2b")]

			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(400, 30, anchor = N, text = "ACHIEVEMENTS", font = ("Mayan", 35), fill = "#f0cc00")]

			nbAch = 0

			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 176, anchor = NW, text = "Adam & Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 246, anchor = NW, text = "Mécanique newtonienne", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 316, anchor = NW, text = "Jeunesse dorée", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 386, anchor = NW, text = "Super Snake", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 456, anchor = NW, text = "Globetrotter", font = ("Mayan", 15, "bold"), fill = "#f0cc00")]

			if parametres["graph mode"] == "sprite" :
				if achievements[1] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(206, 176, anchor = NW, image = images["ach1"])]
					self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 201, anchor = NW, text = "Manger 10 pommes classiques en une partie.", font = ("Mayan", 10), fill = "#f0cc00")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(207, 176, anchor = NW, image = images["no ach"])]
				if achievements[2] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(206, 246, anchor = NW, image = images["ach2"])]
					self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 271, anchor = NW, text = "Manger 100 pommes classiques au total.", font = ("Mayan", 10), fill = "#f0cc00")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(207, 246, anchor = NW, image = images["no ach"])]
				if achievements[3] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(206, 316, anchor = NW, image = images["ach3"])]
					self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 341, anchor = NW, text = "Manger 150 pommes en or au total.", font = ("Mayan", 10), fill = "#f0cc00")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(207, 316, anchor = NW, image = images["no ach"])]
				if achievements[4] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(206, 386, anchor = NW, image = images["ach4"])]
					self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 411, anchor = NW, text = "Manger 100 pommes spéciales au total.", font = ("Mayan", 10), fill = "#f0cc00")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(207, 386, anchor = NW, image = images["no ach"])]
				if achievements[5] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(206, 456, anchor = NW, image = images["ach5"])]
					self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(266, 481, anchor = NW, text = "Parcourir toute la grille en une seule partie.", font = ("Mayan", 10), fill = "#f0cc00")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_image(207, 456, anchor = NW, image = images["no ach"])]

			else :
				if achievements[1] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 200, 230, 220, width = 2, fill = "#76cb3d")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(230, 220, 252, 180, width = 2, fill = "#76cb3d")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 180, 252, 222, width = 2, fill = "#f8320b")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 222, 252, 180, width = 2, fill = "#f8320b")]
				if achievements[2] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 270, 230, 290, width = 2, fill = "#76cb3d")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(230, 290, 252, 250, width = 2, fill = "#76cb3d")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 250, 252, 292, width = 2, fill = "#f8320b")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 292, 252, 250, width = 2, fill = "#f8320b")]
				if achievements[3] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 340, 230, 360, width = 2, fill = "#76cb3d")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(230, 360, 252, 320, width = 2, fill = "#76cb3d")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 320, 252, 362, width = 2, fill = "#f8320b")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 362, 252, 320, width = 2, fill = "#f8320b")]
				if achievements[4] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 410, 230, 430, width = 2, fill = "#76cb3d")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(230, 430, 252, 390, width = 2, fill = "#76cb3d")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 390, 252, 432, width = 2, fill = "#f8320b")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 432, 252, 390, width = 2, fill = "#f8320b")]
				if achievements[5] == True :
					nbAch += 1
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 480, 230, 500, width = 2, fill = "#76cb3d")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(230, 500, 252, 460, width = 2, fill = "#76cb3d")]
				else :
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 460, 252, 502, width = 2, fill = "#f8320b")]
					self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(210, 502, 252, 460, width = 2, fill = "#f8320b")]
			
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(546, 65, anchor = NW, text = str(nbAch), font = ("Mayan", 30), fill = "#f0cc00")]
			self.menuRender["achievements texts"] = self.menuRender["achievements texts"] + [self.menuCan.create_text(592, 136, anchor = SE, text = "5", font = ("Mayan", 30), fill = "#f0cc00")]
			self.menuRender["achievements elements"] = self.menuRender["achievements elements"] + [self.menuCan.create_line(556, 119, 590, 85, width = 2, fill = "#f0cc00")]

		if self.menuMechanics["current menu"] == "paramètres" :
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(400, 30, anchor = N, text = "PARAMÈTRES", font = ("Mayan", 35), fill = "#f0cc00")]

			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 200, anchor = SW, text = "Dossier ressources", font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 240, anchor = SW, text = "Fichier de sauvegarde", font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 280, anchor = SW, text = "Mode graphique: " + parametres["graph mode"], font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 320, anchor = SW, text = "Taille de la grille: " + str(parametres["largeur"]) + " x " + str(parametres["hauteur"]), font = ("Mayan", 20), fill = "#f0cc00")]
			if parametres["bonus"] == True :
				self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 360, anchor = SW, text = "Bonus: avec", font = ("Mayan", 20), fill = "#f0cc00")]
			else :
				self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 360, anchor = SW, text = "Bonus: sans", font = ("Mayan", 20), fill = "#f0cc00")]
			self.menuRender["paramètres texts"] = self.menuRender["paramètres texts"] + [self.menuCan.create_text(200, 400, anchor = SW, text = "Vitesse: " + str(parametres["vitesse"]), font = ("Mayan", 20), fill = "#f0cc00")]

			if self.menuMechanics["highlight"] <= 2 :
				self.menuRender["highlight line"] = [self.menuCan.create_line(220, 198 + self.menuMechanics["highlight"]*40, 270, 198 + self.menuMechanics["highlight"]*40, width = 2, fill = "#f0cc00")]
			elif self.menuMechanics["highlight"] >= 5 :
				self.menuRender["highlight line"] = [self.menuCan.create_line(220, 198 + (self.menuMechanics["highlight"] - 1)*40, 270, 198 + (self.menuMechanics["highlight"] - 1)*40, width = 2, fill = "#f0cc00")]
			elif self.menuMechanics["highlight"] == 3 :
				self.menuRender["highlight line"] = [self.menuCan.create_line(419, 198 + self.menuMechanics["highlight"]*40, 439, 198 + self.menuMechanics["highlight"]*40, width = 2, fill = "#f0cc00")]
			elif self.menuMechanics["highlight"] == 4 :
				self.menuRender["highlight line"] = [self.menuCan.create_line(472, 198 + (self.menuMechanics["highlight"] - 1)*40, 492, 198 + (self.menuMechanics["highlight"] - 1)*40, width = 2, fill = "#f0cc00")]

		self.root.after(10, self.menu)

	def bind(self) :
		"""
		"""

		self.menuCan.bind_all('<Up>', self.menu_haut)
		self.menuCan.bind_all('z', self.menu_haut)
		self.menuCan.bind_all('<Down>', self.menu_bas)
		self.menuCan.bind_all('s', self.menu_bas)
		self.menuCan.bind_all('<Left>', self.menu_gauche)
		self.menuCan.bind_all('q', self.menu_gauche)
		self.menuCan.bind_all('<Right>', self.menu_droite)
		self.menuCan.bind_all('d', self.menu_droite)
		self.menuCan.bind_all('<Return>', self.menu_suivant)
		self.menuCan.bind_all('<space>', self.menu_suivant)
		self.menuCan.bind_all('<Escape>', self.menu_precedent)
		self.menuCan.bind_all('p', self.menu_precedent)

	def menu_haut(self, event) :
		"""
		"""

		print("haut")
		if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" :
			self.menuMechanics["highlight"] -= 1
		if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == -1 :
			self.menuMechanics["highlight"] = 4
		if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == -1 :
			self.menuMechanics["highlight"] = 6
	
	def menu_bas(self, event) :
		"""
		"""

		if self.menuMechanics["current menu"] == "title" or self.menuMechanics["current menu"] == "paramètres" :
			self.menuMechanics["highlight"] += 1
		if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 5 :
			self.menuMechanics["highlight"] = 0
		if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 7 :
			self.menuMechanics["highlight"] = 0

	def menu_droite(self, event) :
		"""
		"""

		if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 2 :
			self.param.modifier("graph mode", 0)
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 :
			self.param.modifier("taille grille", [self.param.largeur + 1, self.param.hauteur])
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 :
			self.param.modifier("taille grille", [self.param.largeur, self.param.hauteur + 1])
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 5 :
			self.param.modifier("bonus", 0)
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 :
			self.param.modifier("vitesse", self.param.vitesseAff + 1)

	def menu_gauche(self, event) :
		"""
		"""

		if self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 3 :
			self.param.modifier("taille grille", [self.param.largeur - 1, self.param.hauteur])
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 4 :
			self.param.modifier("taille grille", [self.param.largeur, self.param.hauteur - 1])
		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 6 :
			if self.param.vitesseAff > 0 :
				self.param.modifier("vitesse", self.param.vitesseAff - 1)

	def menu_suivant(self, event) :
		"""
		"""

		if self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 0 :
			# self.selection_nom()
			return 0
		elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 1 :
			self.menuMechanics["current menu"] = "highscores"
		elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 2 :
			self.menuMechanics["current menu"] = "achievements"
		elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 3 :
			self.menuMechanics["current menu"] = "paramètres"
			self.menuMechanics["highlight"] = 0
		elif self.menuMechanics["current menu"] == "title" and self.menuMechanics["highlight"] == 4 :
			self.quitter()

		elif self.menuMechanics["current menu"] == "paramètres" and self.menuMechanics["highlight"] == 0 :
			#hhh
			return 0

	def menu_precedent(self, event) :
		"""
		"""

		if self.menuMechanics["current menu"] == "title" :
			self.quitter()
		if self.menuMechanics["current menu"] == "highscores" :
			self.menuMechanics["highlight"] = 1
		if self.menuMechanics["current menu"] == "achievements" :
			self.menuMechanics["highlight"] = 2
		if self.menuMechanics["current menu"] == "paramètres" :
			self.menuMechanics["highlight"] = 3
		self.menuMechanics["current menu"] = "title"

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

		for j in self.saveFile :
			if j != "" and "#" not in j :
				self.save.append(j)

		cheminsS = False
		highscoresS = False
		achievementsS = False
		skinsS = False
		comptesS = False
		parametresS = False
		cheminsE = False
		highscoresE = False
		achievementsE = False
		skinsE = False
		comptesE = False
		parametresE = False

		for j in self.save :
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

		if not cheminsS or not cheminsE or not highscoresS or not highscoresE or not achievementsS or not achievementsE or not skinsS or not skinsE or not comptesS or not comptesE or not parametresS or not parametresE :
			self.integrity = False

	def use_default(self) :
		"""
		"""

		self.isFileSelected = False
		self.integrity = True
		self.save = ['###CHEMINS###', '', '/chemins_start', '', 'resourcesPath = ""', '', '/chemins_end', '', '', '###HIGHSCORES###', '', '/highscores_start', '', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '0,"---"', '', '/highscores_end', '', '', '###ACHIEVEMENTS###', '', '/achievements_start', '', 'achievement1 = False', 'achievement2 = False', 'achievement3 = False', 'achievement4 = False', 'achievement5 = False', '', '/achievements_end', '', '', '###SKINS###', '', '/skins_start', '', 'jaune_vert = True', 'bleu_jaune = False', 'selectedSkin = "jaune_vert"', '', '/skins_end', '', '', '###COMPTES###', '', '/comptes_start', '', 'nombrePommesNorm = "0"', 'nombrePommesGold = "0"', 'nombrePommesSpec = "0"', 'scoreTotal = "0"', 'nombreParties = "0"', '', '/comptes_end', '', '', '###PARAMETRES###', '', '/parametres_start', '', 'graphMode = "simple"', 'grilleTaille = "20,20"', 'bonus = True', 'vitesse = "2"', '', '/parametres_end']
		self.proceed()

	def proceed(self) :
		"""
		"""

		self.ranger()
		self.assigner()

	def ranger(self) :
		"""
		"""

		cheminsRead = []
		highscoresRead = []
		achievementsRead = []
		skinsRead = []
		comptesRead = []
		parametresRead = []

		chemins = False
		highscores = False
		achievements = False
		skins = False
		comptes = False
		parametres = False

		for j in self.save :
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

	def get_parametres(self) :
		"""
		"""

		return self.param

class Images :
	"""
	"""

	def __init__(self, root, path, skin) :
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

		self.images = {}
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


	#*************** IMPORTATION DES BIBLIOTHEQUES ***************#


from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random

	#*************** PROGRAMME PRINCIPAL ***************#

snaya = Snaya()

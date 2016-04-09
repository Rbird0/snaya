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

		self.save = Save(self.root)
		self.paths = Paths()

		self.save_load()
		self.initialize()

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

		resources = self.paths.get_path("resources")
		parametres = self.param.get_parametres()
		skins = self.skins.get_skins()

		if parametres["graph mode"] == "sprite" :
			self.menu = Menu(self.root, resources, skins["selected skin"])
		else :
			self.menu = Menu(self.root)

		self.root.mainloop()

class Save :
	"""
	"""

	def __init__(self, root) :
		"""
		"""

		self.path = ""
		self.window = root
		self.isFileSelected = False
		self.integrity = True
		self.saveFile = []
		self.save = []

	def open_dialog(self) :
		"""
		"""

		self.path = filedialog.askopenfilename(title = "Ouvrir le fichier de sauvegarde", filetypes = [("sauvegarde Snaya",".sav"),("tous les fichiers","*")], initialfile = "snaya.sav", parent = self.window)
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
			highscores[str(compteur)] = j

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

class Menu :
	"""
	"""

	def __init__(self, root, resources = 0, skin = 0) :
		"""
		"""

		self.can = Canvas(self.root, width = 800, height = 600)

		self.background = []

		if resources != 0 :
			self.images = Images(self.root, resources, skins["selected skin"])
			images = self.images.get_images()
			self.sprite(images)
		else :
			self.simple()

	def simple(self) :
		"""
		"""

		self.background = self.background + [self.can.create_rectangle(0, 0, 124, 600, width = 0, fill = "#547e25")]
		self.background = self.background + [self.can.create_rectangle(124, 0, 676, 600, width = 0, fill = "#8c5918")]
		self.background = self.background + [self.can.create_rectangle(676, 0, 800, 600, width = 0, fill = "#547e25")]

		self.menu()

	def sprite(self, images) :
		"""
		"""

		self.background = self.background + [self.can.create_image(0, 0, anchor = NW, image = images["menu title"])]

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

	def get_achievements(self) :
		"""
		"""

		return self.achievements

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

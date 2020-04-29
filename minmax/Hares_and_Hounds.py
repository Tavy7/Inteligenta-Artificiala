#Hares and Hounds
#Python 3.6.9

import time
from copy import deepcopy
import random

def firstIndex(lista, x):#functie care returneaza indexu unui caracter
	
	for i in range(len(lista)):
		if lista[i] == x:
			return int(i)
	return -1

def getPozCaini(matr):#functie care returneaza pozitile tuturor dulai
	lista = []

	for i in range (len(matr)):
		if matr[i] == "c":
			lista.append(i)

	return lista

class Joc:
	"""
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
	JMIN = None
	JMAX = None
	GOL = '#'
	def __init__(self, tabla=None):
		self.matr = [Joc.GOL] * 11# poz 0 este stanga, iar poz -1 este dreapta
		self.matr[-1] = 'i'
		self.matr[0] = 'c'
		self.matr[1] = 'c'
		self.matr[7] = 'c'
		#locatile dulailor si a iepurelui

	def final(self):
		rez = False
		pozIepure = firstIndex(self.matr, "i")#gasim pozitia iepurelui

		pozFinale = {1:[2, 4, 5], 3:[2, 5, 6], 7:[4, 5, 8], 9:[5, 6, 8], 0:[3, 6, 9]}#cheia reprezinta pozitia iepurelui
		#iar valorile reprezinta pozitile in ordine crescatoare necesare pentru ca dulaii sa l blocheze pe iepure

		pozCaini = getPozCaini(self.matr)

		if pozIepure in pozFinale:
			if pozFinale[pozIepure] == pozCaini:#daca dulaii sunt pe pozitile care inchid iepurele
				rez = "c"

		if pozIepure == 0 or (pozIepure in [1, 4, 7] and self.matr[0] == "#"):#daca iepurele intr o mutare poate ajunge pe poz 0
			return "i"

		c = 0

		for i in pozCaini:
			if i == 10:
				i = 9
			if pozIepure % 3 == 1 and i % 3 != 1:#x % 3 == 1 inseamna prima coloana
				c += 1#iepurele e in stanga cainelui curent

		if c == 3:#iepurele e in stanga dulailor
			rez = "i"

		return rez

	def mutariCaini(self):

		l_mutari = []
		mutari = {"sus": -3, "jos": 3, "dreapta": 1}#mutari posibile

		caini = []

		for i in range(len(self.matr)):
			if self.matr[i] == "c":
				caini.append(i)

		for ind in caini:
			if ind == 0:
				aux = deepcopy(self)
				aux.matr[4], aux.matr[0] = "c", "#"

				l_mutari.append(aux)
				continue
			if ind == 10:
				continue

			mutari["dreapta"] = 1
			if ind % 3 == 0:
				mutari["dreapta"] = 4
			#^^ cazuri speciale

			for i in mutari.values():#iteram prin toate mutarile si le memoram pe cele valabile
				if ind + i > 0 and ind + i < 10 and self.matr[ind + i] == '#':
					aux = deepcopy(self)
					aux.matr[ind + i], aux.matr[ind] = "c", "#"

					l_mutari.append(aux)

		return l_mutari

	def mutari_joc(self, jucator):
		"""
		Pentru configuratia curenta de joc "self.matr" (de tip lista, cu 11 elemente),
		trebuie sa returnati o lista "l_mutari" cu elemente de tip Joc,
		corespunzatoare tuturor configuratiilor-succesor posibile.

		"jucator" este simbolul jucatorului care face mutarea
		"""
		l_mutari = []

		if jucator == "c":
			return self.mutariCaini()

		if jucator == 'i':
			jucatorCurent = firstIndex(self.matr, jucator)#index iepure
			mutari = {"stanga" : -1, "dreapta": 1, "sus": -3, "jos": 3, "diagNV": -4, "diagNE": -2, "diagSW": 2, "diagSE": 4}#mutari iepure

		if jucatorCurent == -1:
			print("Nu s-a gasit caracterul")
			return l_mutari

		if jucatorCurent == 0:#poz de finala
			if jucator == 'i':
				l_mutari.append(self.matr)
				return l_mutari

		if jucatorCurent == 10 and jucator == 'i':#poz initiala
				mutari = {"NW": -7, "W": -4, "SW": -1}

		for i in mutari.values():#iteram in mutari si le memoram pe cele valide
			if validareMiscareIepure(jucatorCurent, jucatorCurent + i):
					if jucatorCurent + i > 0 and jucatorCurent + i < 10 and self.matr[jucatorCurent + i] == '#':
						aux = deepcopy(self)
						aux.matr[jucatorCurent + i] = jucator
						aux.matr[jucatorCurent] = "#"

						l_mutari.append(aux)

		return l_mutari
	

	#euristica1
	def spatiiLibere(self, jucator):
	#returneaza nr de spatii libere (sau media lor) pe fiecare jucator

		if jucator == 'c':
			countSpatiiCaini = 0
			
			countSpatiiCaini += len(self.mutariCaini())

			return countSpatiiCaini / 3

		if jucator == 'i':
			countSpatiiIepure = len(self.mutari_joc("i"))
			return countSpatiiIepure

	#euristica2
	def distantaManhatten(self):
		#distanta Manhatten
		pozIepure = firstIndex(self.matr, "i")
		pozCaini = getPozCaini(self.matr)

		total = 0

		for x in pozCaini:
			total += (abs(x - pozIepure))

		return total
		
	#euristica3
	def disantaChebyshev(self):
		#distanta Chebyshev
		pozIepure = firstIndex(self.matr, "i")
		pozCaini = getPozCaini(self.matr)

		total = 0

		for x in pozCaini:
			total += (max(x, pozIepure))

		return total			
		
	def estimeaza_scor(self, adancime):
		t_final = self.final()
		if t_final == Joc.JMAX :
			return (99 + adancime)
		elif t_final == Joc.JMIN:
			return (-99 -adancime)
		else:
			if euristica == 1:
				return self.spatiiLibere(Joc.JMAX) - self.spatiiLibere(Joc.JMIN)
			elif euristica == 2:
				return self.distantaManhatten()
			else:
				return self.disantaChebyshev()


	def __str__(self):
		string = "  " 
		for i in range (1, len(self.matr) - 1):

			string += str(self.matr[i] + " ")
			if i % 3 == 0 and i != 9:

				if i == 6:
					string += str(self.matr[-1])
					string += "\n  "
					continue
				
				string += "\n"

				if i == 3:
					string += str(self.matr[0] + " ")

		return string

	def stringIndici(self):
		#afisarea indicilor pe pozitii 
		string = "\nTabla indici\n  " 
		for i in range (1, len(self.matr) - 1):
			c = i
			if self.matr[i] != "#":
				c = i

			string += str(c) + " "
			if i % 3 == 0 and i != 9:

				if i == 6:
					string += str(10) + " "
					string += "\n  "
					continue
				
				string += "\n"

				if i == 3:
					string += str(0) + " "
		string+= "\nScrieti \'exit\' pentru a parasi programul(sau Ctrl + D sau Ctrl + C).\n"
		return string

class Stare:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
	configuratiile posibile in urma mutarii unui jucator
	"""

	ADANCIME_MAX = None

	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
		self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
		self.j_curent = j_curent  # simbolul jucatorului curent

		# adancimea in arborele de stari
		#	(scade cu cate o unitate din „tata” in „fiu”)
		self.adancime = adancime

		# scorul starii (daca e finala, adica frunza a arborelui)
		# sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
		self.scor = scor

		# lista de mutari posibile din starea curenta
		self.mutari_posibile = [] # lista va contine obiecte de tip Stare

		# cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa = None


	def jucator_opus(self):
		if self.j_curent == Joc.JMIN:
			return Joc.JMAX
		else:
			return Joc.JMIN

	def mutari_stare(self):

		l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
		#mutarile posibile pentru j_curent

		juc_opus = self.jucator_opus()

		l_stari_mutari = []

		for mutare in l_mutari:
			aux = Stare(tabla_joc = mutare, j_curent = juc_opus, adancime = self.adancime - 1, parinte = self)
			l_stari_mutari.append(aux)

		#memoram mutarile posibile de tipul Stare


		return l_stari_mutari
		
	
	def __str__(self):
		sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent+")\n"
		return sir
	
""" Algoritmul MinMax """

def min_max(stare):

	# Daca am ajuns la o frunza a arborelui, adica:
	# - daca am expandat arborele pana la adancimea maxima permisa
	# - sau daca am ajuns intr-o configuratie finala de joc
	if stare.adancime==0 or stare.tabla_joc.final():
		# calculam scorul frunzei apeland "estimeaza_scor"
		stare.scor=stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare
		
	#Altfel, calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile = stare.mutari_stare()

	#aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
	mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]
	

	if stare.j_curent==Joc.JMAX :
		#daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
		stare.stare_aleasa=max(mutari_scor, key=lambda x: x.scor)
	else:
		#daca jucatorul e JMIN aleg starea-fiica cu scorul minim
		stare.stare_aleasa=min(mutari_scor, key=lambda x: x.scor)

	# actualizez scorul „tatalui” = scorul „fiului” ales
	stare.scor=stare.stare_aleasa.scor
	return stare


def alpha_beta(alpha, beta, stare):
	# Daca am ajuns la o frunza a arborelui, adica:
	# - daca am expandat arborele pana la adancimea maxima permisa
	# - sau daca am ajuns intr-o configuratie finala de joc
	if stare.adancime == 0 or stare.tabla_joc.final():
		# calculam scorul frunzei apeland "estimeaza_scor"
		stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare

	# Conditia de retezare:
	if alpha >= beta:
		return stare  # este intr-un interval invalid, deci nu o mai procesez

	# Calculez toate mutarile posibile din starea curenta (toti „fiii”)
	stare.mutari_posibile = stare.mutari_stare()

	if stare.j_curent == Joc.JMAX:
		scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

		# pentru fiecare „fiu” de tip MIN:
		for mutare in stare.mutari_posibile:
			# calculeaza scorul fiului curent
			stare_noua = alpha_beta(alpha, beta, mutare)

			# incerc sa imbunatatesc (cresc) scorul si alfa
			# „tatalui” de tip MAX, folosind scorul fiului curent
			if scor_curent < stare_noua.scor:
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor

			if alpha < stare_noua.scor:
				alpha = stare_noua.scor
				if alpha >= beta:  # verific conditia de retezare
					break  # NU se mai extind ceilalti fii de tip MIN


	elif stare.j_curent == Joc.JMIN:
		scor_curent = float('inf')  # scorul „tatalui” de tip MIN

		# pentru fiecare „fiu” de tip MAX:
		for mutare in stare.mutari_posibile:
			stare_noua = alpha_beta(alpha, beta, mutare)

			# incerc sa imbunatatesc (scad) scorul si beta
			# „tatalui” de tip MIN, folosind scorul fiului curent
			if scor_curent > stare_noua.scor:
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor

			if beta > stare_noua.scor:
				beta = stare_noua.scor
				if alpha >= beta:  # verific conditia de retezare
					break  # NU se mai extind ceilalti fii de tip MAX

	# actualizez scorul „tatalui” = scorul „fiului” ales
	stare.scor = stare.stare_aleasa.scor

	return stare


def afis_daca_final(stare_curenta):
	final=stare_curenta.tabla_joc.final()
	if final == 'i':
		print("A castigat iepurele!")
		return True	

	if final == 'c':
		print("Au castiga dulaii!")
		return True

	return False
		
def validareMiscareCaine(poz1, poz2):
	if poz1 == 0 and poz2 == 4:
		return True

	if poz1 == 6 and poz2 == 10:
		return True
	#^^^ cazuri speciale

	mutari = {"sus": -3, "jos": 3, "dreapta": 1}	

	for i in mutari.values():#verificam daca pentru mutarile posibile exista combinatia de care avem nevoie
		if poz1 + i == poz2:
			return True

	return False


def validareMiscareIepure(poz1, poz2):
	if poz1 == 10 and poz2 % 3 == 0 and poz2 != 0:
		return True

	if poz2 == 0 and poz1 % 3 == 1 and poz1 != 10:
		return True

	if poz1 % 3 == 0 and poz2 == 10:
		return True

	if (poz1 % 3 == 1 and poz2 % 3 == 0 and poz2 != 0):
		return False
	if (poz1 % 3 == 0 and poz2 % 3 == 1 and poz1 != 0):
		return False

	#^^^cazuri speciale

	mutari = {"stanga" : -1, "dreapta": 1, "sus": -3, "jos": 3, "diagNE": -4, "diagNW": -2, "diagSW": 4, "diagSE": 2}

	if poz1 % 3 == 0:
		mutari = {"stanga" : -1, "sus": -3, "jos": 3, "diagNE": -4, "diagSE": 2}

	for i in mutari.values():#verificam daca pentru mutarile posibile exista combinatia de care avem nevoie
		if poz1 + i == poz2:
			return True

	return False 

def dogTurnCounter(dogCounter, poz):
	if abs(poz[0] - poz[1]) == 3:#daca dulaul s-a miscat doar sus sau jos 
		dogCounter += 1	#incrementam
	else:
		dogCounter = 0	#resetam counterul

	return dogCounter


def main():
	#initializare algoritm
	raspuns_valid=False
	while not raspuns_valid:
		tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
		if tip_algoritm in ['1','2']:
			raspuns_valid=True
		else:
			print("Nu ati ales o varianta corecta.")

	raspuns_valid = False
	global euristica
	while not raspuns_valid:
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")#euristicile sunt la linia 145
		euristica = int(input("Selectati euristica pe care doriti sa o folositi.\n 1 - Numar spatii libere \n 2 - Distanta Manhatten\n 3 - Disanta Chebyshev\n "))
		if euristica in [1, 2, 3]:
			raspuns_valid = True
		else:
			print("Trebuie sa introduceti o valoare egala cu 1, 2 sau 3!")

	# initializare ADANCIME_MAX
	raspuns_valid = False
	while not raspuns_valid:
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print(" 1 - Usor\n 2 - Mediu\n 3 - Greu")
		n = input("Alegeti dificultate: ")
		if n in ['1', '2', '3']:
			Stare.ADANCIME_MAX = int(n) * 2
			raspuns_valid = True
		else:
			print("Trebuie sa introduceti un numar de la 1 la 3.")

	#initializare jucatori
	raspuns_valid=False
	while not raspuns_valid:
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		Joc.JMIN=input("Doriti sa jucati cu i(epure) sau cu c(aini)?\n ").lower()
		if (Joc.JMIN in ['i', 'c']):
			raspuns_valid=True
		else:
			print("Raspunsul trebuie sa fie i sau c.")
	Joc.JMAX = 'c' if Joc.JMIN == 'i' else 'i'
	
	
	#initializare tabla
	tabla_curenta=Joc()
	
	print("Tabla initiala")
	print(str(tabla_curenta))
	
	#creare stare initiala
	stare_curenta=Stare(tabla_curenta, 'c', Stare.ADANCIME_MAX)#catelusii muta primii

	if Joc.JMIN == 'c':
		print(stare_curenta.tabla_joc.stringIndici())
	dogCounter = 0

	while True :
		if (stare_curenta.j_curent==Joc.JMIN):
		#muta jucatorul
			raspuns_valid=False
			while not raspuns_valid:

				t_inainte=int(round(time.time() * 1000))
				try:
					if Joc.JMIN == 'c':
						#utilizatoru lintroduce cainele pe care vrea sa il mute, iar daca mutarea e valida, se efectueaza
						#de aseamanea poate scrie exit pentru a iesi din program

						inpu = input("Selectati pozitia cainelui pe care doriti sa il mutati: ")

						if inpu == "exit":#daca utilizatorul a introdus exit
							print("\nAti iesit cu succes din program!")
							exit()
						
						if 	int(inpu) < 11:
							caine = int(inpu)
						else:
							print("Input gresit!")
							continue

						if stare_curenta.tabla_joc.matr[caine] == 'c':

							inpu = input("Selectati pozitia pe care sa efectuati mutarea: ")

							if inpu == "exit":#daca utilizatorul a introdus exit
								print("\nAti iesit cu succes din program!")
								exit()


							if 	int(inpu) < 11:
								mutare = int(inpu)
							else:
								print("Input gresit!")
								continue

							if stare_curenta.tabla_joc.matr[mutare] == "#" and validareMiscareCaine(caine, mutare):
								raspuns_valid = True
								dogCounter = dogTurnCounter(dogCounter, (caine, mutare))

								if dogCounter == 10:
									print(str(stare_curenta.tabla_joc.matr))
									print("Dulaii s-au miscat 10 runde doar sus si jos.\nIepurele castiga!")
									exit()

								stare_curenta.tabla_joc.matr[mutare], stare_curenta.tabla_joc.matr[caine] = Joc.JMIN, "#"
							else:

								print("Mutare invalida!")
				
					elif Joc.JMIN == 'i':
						indexIepure = firstIndex(stare_curenta.tabla_joc.matr, "i")
						#gasim index-ul iepurelui

						inpu = input("Selectati pozitia pe care sa efectuati mutarea: ")#il mutam

						if inpu == "exit":#daca utilizatorul a introdus exit
							print("\nAti iesit cu succes din program!")
							exit()

						if 	int(inpu) < 11:
							mutare = int(inpu)
						else:
							print("Input gresit!")
							continue

						if stare_curenta.tabla_joc.matr[mutare] == "#" and validareMiscareIepure(indexIepure, mutare):

							stare_curenta.tabla_joc.matr[mutare], stare_curenta.tabla_joc.matr[indexIepure] = Joc.JMIN, "#"
							raspuns_valid = True
						else:

							print("Mutare invalida!")


				except ValueError:
					print("Input gresit")

			t_dupa=int(round(time.time() * 1000))
			print("User a gandit mutarea timp de "+str(t_dupa-t_inainte) + " milisecunde.")

			#afisarea starii jocului in urma mutarii utilizatorului
			
			print("\nTabla dupa mutarea jucatorului")
			print(str(stare_curenta))
			print(stare_curenta.tabla_joc.stringIndici())
			
			#testez daca jocul a ajuns intr-o stare finala
			#si afisez un mesaj corespunzator in caz ca da
			if (afis_daca_final(stare_curenta)):
				break
				
				
			#S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent=stare_curenta.jucator_opus()
		#--------------------------------
		else: #jucatorul e JMAX (calculatorul)
			#Mutare calculator
			
			#preiau timpul in milisecunde de dinainte de mutare
			t_inainte=int(round(time.time() * 1000))

			if tip_algoritm=='1':
				stare_actualizata=min_max(stare_curenta)
			else: #tip_algoritm==2
				stare_actualizata=alpha_beta(-500, 500, stare_curenta)
			
			stare_curenta.tabla_joc=stare_actualizata.stare_aleasa.tabla_joc

			print("Tabla dupa mutarea calculatorului")
			print(str(stare_curenta))
			
			#preiau timpul in milisecunde de dupa mutare
			t_dupa=int(round(time.time() * 1000))
			print("Calculatorul a \"gandit\" timp de " + str(t_dupa-t_inainte) + " milisecunde.")
			
			if (afis_daca_final(stare_curenta)):
				break
				
			#S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent=stare_curenta.jucator_opus()
	
if __name__ == "__main__" :
	main()

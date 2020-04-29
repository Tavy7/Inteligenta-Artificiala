#Problema 7 - Evadarea lui mormocel
#Python 3.6.9

from math import sqrt
from copy import deepcopy
import time
import random


#clasa frunza pentru a memora datele
class Frunza:
    def __init__(self, ident, pozitie, nrInsecte, gMax):
        self.ident = ident
        self.poz = pozitie
        self.nrInsecte = nrInsecte
        self.gMax = gMax

    def __str__(self):
    	return "{} la pozitia {}, avand {} insecte o greutate maxima de {}".format(self.ident, self.poz, self.nrInsecte, self.gMax)

centru = (0, 0)
frunze = {}

#functie pentru alegerea euristicii
def alegeEuristica():
	global euristica
	print("Alegeti euristica:\n 1 - Disanta euclidiana intre doua puncte")
	print(" 2 - Disanta Manhattan intre doua puncte\n 3 - Distanta euclidiana cu o marja de eroare de 5\n")

	euristica = int (input())
	if euristica not in [1, 2, 3]:
		print("Valoarea aleasa trebuie sa fie 1, 2 sau 3!")
		alegeEuristica()
	

def citire():
	path = "inputs/input"#locatia fisierului
	print ("Selectati inputul dorit:")

	tipuriInput = {
		1: "fara solutii", 2:"stare intiala = stare finala", 
		3: "drum de cost minim lungime 3-5",
		4: "drum cost minim lungime > 5"
	}
	for i in range(1, 5):
		print (str(i) + " - " + path + str(i) + ".txt" + " - " + tipuriInput[i])
	
	i = input()#selectare fisierul de input

	if 	i.isdigit() and int(i) < 1 or int(i) > 4:#verificare input
		print("Input incorect!")
		citire()
		return  

	path += str(i) + ".txt"
	print (path)
	file = open(path)#deschidere fisier

	global raza, masaInitialaBroasca, frunzaStart#declarare variabile
	
	raza = float(next(file))
	masaInitialaBroasca = float(next(file))
	frunzaStart = next(file).strip()

	alegeEuristica()

	for line in file:
	    ident, x, y, nrInsecte, gMax = line.split()
	    frunze[ident] = Frunza (ident, (int(x), int(y)), int(nrInsecte), float(gMax))
	    #print (str(frunze[ident]))
	file.close()#citire^^^^

	scriere("Raza lacului: {}\nGreutate initiala: {}\nFrunza start: {}\nFisier input: {}".format(str(raza), str(masaInitialaBroasca), frunzaStart, path))
	#scriere in fisier 

def scriere(string):

	file = open("output.txt", "a")
	file.write(string)



#distanta euclidiana intre doua puncte
def distantaEuclidiana(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#distanta intre un punct si marginea lacului (admisibila)
def distantaLac(p):
    return abs(raza - distantaEuclidiana(p, centru))

#distantaManhattan
def distantaManhattan(p1, p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] + p2[1])

def disantaLacManhattan(p):#distanta Chebyshev (admisibila)
    return raza - distantaManhattan(centru, p)

def distantaEronata(p):
	#distanta intre punct si marginea lacului
	#dar cu o marja de eroare de 5 (neadmisibila)
	return distantaLac(p) + random.randint(-5, 5)



""" definirea problemei """
class Nod:
	def __init__(self, frunze, identitateFrunzaCurenta, masa):
		self.frunze = frunze#lista de frunze
		self.ident = identitateFrunzaCurenta#string
		self.masa = masa#gReuTaTEa

		if euristica == 1:
			self.h = distantaLac(self.frunze[self.ident].poz)#distanta euclidiana

		if euristica == 2:
			self.h = disantaLacManhattan(self.frunze[self.ident].poz)#distanta Chebyshev
		
		if euristica == 3:
			self.h = distantaEronata(self.frunze[self.ident].poz)#distanta euclidiana eronata
		
		self.info = (self.frunze, self.ident, self.masa)

	def __str__ (self):
		return "Ne aflam pe frunza {}, cu coordonatele {}, h = {}.".format(self.ident, self.frunze[self.ident].poz, self.h)
	def __repr__ (self):
		return f"({self.info}, h={self.h})"

""" Sfarsit definire problema """	
""" Clase folosite in algoritmul A* """
		
class NodParcurgere:
	"""O clasa care cuprinde informatiile asociate unui nod din listele open/closed
		Cuprinde o referinta catre nodul in sine (din graf)
		dar are ca proprietati si valorile specifice algoritmului A* (f si g). 
		Se presupune ca h este proprietate a nodului din graf
	"""
	def __init__(self, nod_graf, parinte=None, g=0, f=None):
		self.nod_graf = nod_graf	# obiect de tip Nod
		self.parinte = parinte		# obiect de tip NodParcurgere
		self.g = g					# costul drumului de la radacina pana la nodul curent
		if f is None :
			self.f = self.g + self.nod_graf.h
		else:
			self.f = f


	def drum_arbore(self):
		"""
			Functie care calculeaza drumul asociat unui nod din arborele de cautare.
			Functia merge din parinte in parinte pana ajunge la radacina
		"""
		nod_c = self
		drum = [nod_c]
		while nod_c.parinte is not None :
			drum = [nod_c.parinte] + drum
			nod_c = nod_c.parinte
		return drum


	def contine_in_drum(self, nod):
		"""
			Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
			Verificarea se face mergand din parinte in parinte pana la radacina
			Se compara doar informatiile nodurilor (proprietatea info)
			Returnati True sau False.

			"nod" este obiect de tip Nod (are atributul "nod.info")
			"self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
		"""
		nodCurent = self
		while nodCurent:
			if nodCurent.nod_graf.ident == nod.ident:
				return True
			nod_curent = nod_curent.parinte#trecem la urmatorul nod
		return False

    #lungimeSaritura = masa / 3 #la fiecare saritura broscuta pierde o unitate de energie *in timpul sariturii*
	#masa 0 inseamna ca moare
	#cand ajung pe o frunza, tr sa simulez ca broscuta mananca 0, dupa 1, dupa ... n insecte de pe frunza si generez lista de noduri posibile dupa


	#se modifica in functie de problema
	def expandeaza(self):
		"""Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
		si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
		sau lista vida, daca nu exista niciunul.
		(Fiecare tuplu contine un obiect de tip Nod si un numar.)
		"""
		lista = []#lista de returnat
		frunze, identCurenta, masa = self.nod_graf.info
		frunzaActuala = frunze[identCurenta]#frunza din nodul curent (self)

		for frunzaNoua in frunze.values():
			if frunzaActuala.ident == frunzaNoua.ident:#frunza identica
				continue

			for insecteMancate in range (0, frunzaActuala.nrInsecte + 1):#verificam cate insecte sa fie mancate
				masaNoua = masa + insecteMancate

				if distantaEuclidiana(frunzaActuala.poz, frunzaNoua.poz) > masaNoua / 3:
					continue#saritura depaseste conditia din cerinta

				masaNoua -= 1 #efectuam saritura

				if masaNoua > frunzaNoua.gMax or masaNoua == 0:#daca a ajuns pe o frunza care nu o suporta sau daca moare broasca
					continue

				frunzeAux = deepcopy(frunze)#copiem lista de frunze
				insecteRamase = frunzaActuala.nrInsecte - insecteMancate#updatam nr de insecte
				frunzeAux[frunzaActuala.ident] = Frunza(frunzaActuala.ident, frunzaActuala.poz, insecteRamase, frunzaActuala.gMax) #modificam frunza pe care am sarit in lista

				nod = Nod(frunzeAux, frunzaNoua.ident, masaNoua)#nod nou
				lista.append((nod, 1))#il punem in lista impreuna cu costul
		return lista


	#se modifica in functie de problema
	def test_scop(self):
		ident = self.nod_graf.ident
		poz = self.nod_graf.frunze[ident].poz
		greutate = self.nod_graf.masa
		
		#daca nu poate sari sau daca unul din puncte e in afara razei
		if euristica == 1:
			return distantaLac(poz) <= greutate / 3 or poz[0] > raza or poz[1] > raza

		if euristica == 2:
			return disantaLacManhattan(poz) <= greutate / 3 or poz[0] > raza or poz[1] > raza

		if euristica == 3:
			return distantaEronata(poz) <= greutate / 3 or poz[0] > raza or poz[1] > raza

	def __str__ (self):
		parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
		return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"



""" Algoritmul A* """


def str_info_noduri(l):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = "["
	for x in l:
		sir += str(x)+"  "
	sir += "]"
	return sir


def afis_succesori_cost(l):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = ""
	for (x, cost) in l:
		sir += "\nnod: "+str(x) + ", cost arc:" + str(cost)
	
	return sir


def in_lista(l, nod):
	"""
	lista "l" contine obiecte de tip NodParcurgere
	"nod" este de tip Nod
	"""
	for i in range(len(l)):
		if l[i].nod_graf == nod:
			return l[i]
	return None


def a_star():
    nodStart = Nod (frunze, frunzaStart, masaInitialaBroasca)
    radArbore = NodParcurgere(nodStart)
    open = [radArbore]		# open va contine elemente de tip NodParcurgere
    closed = []				# closed va contine elemente de tip NodParcurgere

    while open: #cat timp exista noduri neexplorate

    	nodCurent = open.pop(0)#scoatem primul nod din open

    	if nodCurent.test_scop():#s-a termiant
    		open.append(nodCurent)
    		break

    	closed.append(nodCurent)
    	#scoatem nodul curent din lista open si il introducem in closed

    	drum = nodCurent.drum_arbore()

    	for succesor, cost in nodCurent.expandeaza():#testam toti succesorii nodului
    		if in_lista(drum, succesor):
    			continue

    		nodOpen = in_lista(open, succesor)
    		nodClosed = in_lista(closed, succesor)

    		gNou = nodCurent.g + cost

    		if nodOpen:#daca nu e None, atunci verific daca il pot actualiza
    			if gNou < nodOpen.g:#daca exista o distanta mai buna
    				nodOpen.g = gNou
    				nodOpen.f = nodOpen.g + nodOpen.nod_graf.h#actualizam f
    				nodOpen.parinte = nodCurent
    			

    		elif nodClosed:#daca nu e None
    			fNou = gNou + nodClosed.nod_graf.h

    			if fNou < nodClosed.f:# verific daca il pot actualiza
    				nodClosed.g = gNou
    				nodClosed.f = fNou + nodClosed.nod_graf.h
    				nodClosed.parinte = nodCurent

    				#daca l am modificat, il adaugam inapoi in open
    				open.append(nodClosed)
    		else:#daca nu exista nici in open, nici in closed, il pun in open
    			open.append(NodParcurgere(nod_graf = succesor, parinte = nodCurent, g = gNou))

    	open.sort(key=lambda nod: nod.f)#la final sortam lista in fuctie de f
    	#pentru ca sa putem lua nodul cu cea mai mica f in urmatoarea iteratie

    print("\n------------------ Concluzie -----------------------")
    if(len(open)==0):
    	print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
    	drum = nodCurent.drum_arbore()
    	for nod in drum:#pentru afisare
    		ident, masa = nod.nod_graf.ident, nod.nod_graf.masa
    		coord = nod.nod_graf.frunze[ident].poz
    		string = "Broscuta a sarit la {}{}. Greutate: {}\n".format(ident, coord, masa)
    		scriere(string)#apelam functia de scriere in fisier
    		print(string)

	
if __name__ == "__main__":
	citire()
	t_inainte=int(round(time.time() * 1000))
	a_star()
	t_dupa=int(round(time.time() * 1000))
	print("Calculatorul a \"gandit\" timp de " + str(t_dupa-t_inainte) + " milisecunde.")
	scriere("\nCalculatorul a \"gandit\" timp de " + str(t_dupa-t_inainte) + " milisecunde.")#scriere in fisier
	scriere("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n")
			
import time

class Joc:
    """
    Clasa care defineste Jocul. Se va schimba de la un Joc la altul.
    """
    NR_COLOANE = 7
    NR_LINII = 6
    NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
    SIMBOLURI_JUC = ['X', '0']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'
    def __init__(self, tabla=None):
        self.matr = tabla or [Joc.GOL]*(Joc.NR_COLOANE * Joc.NR_LINII)

    def verifica(self, lista):
        simbol = lista[0]
        lung = 1

        for i in lista[1:]:
            if i != simbol:
                simbol = i
                lung = 1
            else:
                lung += 1
                if lung == Joc.NR_CONNECT and simbol != self.GOL:
                    return simbol
        return False


    def final(self):
        # returnam simbolul jucatorului castigator daca are 4 piese adiacente
        #	pe linie, coloana, diagonala \ sau diagonala /
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat Jocul
        rez = False

        for i in range(self.NR_LINII):
            linie = [
                self.matr[i * self.NR_COLOANE + j]
                for j in range(self.NR_COLOANE)
            ]

            rez = self.verifica(linie)
            if rez:
                return rez
       
        # verificam coloane
        for j in range(self.NR_COLOANE):
            coloana = [
                self.matr[i * self.NR_COLOANE + j]
                for i in range(self.NR_LINII)
            ]

            rez = self.verifica(coloana)
            if rez:
                return rez

        # verificam diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                diag = [
                    self.matr[(i + k) * self.NR_COLOANE + (j + k)]
                    for k in range(self.NR_CONNECT)
                ]
            rez = self.verifica(diag)
            if rez:
                return rez
                
        # verificam diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                 diag = [
                    self.matr[(i + k) * self.NR_COLOANE + (j + self.NR_CONNECT - k - 1)]
                    for k in range(self.NR_CONNECT)
                ]
            rez = self.verifica(diag)
            if rez:
                return rez

        if rez==False  and  Joc.GOL not in self.matr:
            return 'remiza'
        else:
            return False


    def mutari(self, jucator_opus):
        l_mutari=[]

        for i in range (self.NR_COLOANE):
            if self.matr[i] != self.GOL:
                continue
        
            newMatr = self.matr[:]
            for j in range (self.NR_LINII - 1, -1, -1):
                if newMatr[j * self.NR_COLOANE + i] == self.GOL:
                    break
            newMatr[j * self.NR_COLOANE + i] = jucator_opus
            l_mutari.append(Joc(newMatr))

        return l_mutari

    def intervale_deschise (self, lista, jucator_opus):
        nr = 0

        for i in range (len(lista) - self.NR_CONNECT):
            if jucator_opus in lista[i:i + self.NR_CONNECT]:
                continue
            nr += 1
        return nr 


    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "juc_opus"

        juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0

        for i in range(self.NR_LINII):
            linie = [
                self.matr[i * self.NR_COLOANE + j]
                for j in range(self.NR_COLOANE)
            ]

            rez += self.intervale_deschise(linie, juc_opus)

        # verificam coloane
        for j in range(self.NR_COLOANE):
            coloana = [
                self.matr[i * self.NR_COLOANE + j]
                for i in range(self.NR_LINII)
            ]

            rez += self.intervale_deschise(coloana, juc_opus)

        # verificam diagonale \
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                diag = [
                    self.matr[(i + k) * self.NR_COLOANE + (j + k)]
                    for k in range(self.NR_CONNECT)
                ]
            
            rez += self.intervale_deschise(linie, juc_opus)
                
        # verificam diagonale /
        for i in range(self.NR_LINII - self.NR_CONNECT):
            for j in range(self.NR_COLOANE - self.NR_CONNECT):
                 diag = [
                    self.matr[(i + k) * self.NR_COLOANE + (j + self.NR_CONNECT - k - 1)]
                    for k in range(self.NR_CONNECT)
                ]
            
            rez += self.intervale_deschise(linie, juc_opus)

        return rez


    def fct_euristica(self):
        # intervale_deschisa(juc) = cate intervale de 4 pozitii
        # (pe linii, coloane, diagonale) nu contin juc_opus
        return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)



    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX :
            return (999+adancime)
        elif t_final == Joc.JMIN:
            return (-999-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()


    def __str__(self):
        sir = ''
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            k = lin * self.NR_COLOANE
            sir += (" ".join([str(x) for x in self.matr[k : k+self.NR_COLOANE]])+"\n")
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de Joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_Joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_Joc = tabla_Joc
        self.j_curent = j_curent

        #adancimea in arborele de stari
        self.adancime=adancime

        #scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor=scor

        #lista de mutari posibile din starea curenta
        self.mutari_posibile=[]

        #cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa=None

    def jucator_opus(self):
        if self.j_curent==Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari=self.tabla_Joc.mutari(self.j_curent)
        juc_opus=self.jucator_opus()
        l_stari_mutari=[Stare(mutare, juc_opus, self.adancime-1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari


    def __str__(self):
        sir= str(self.tabla_Joc) + "(Juc curent: "+self.j_curent+")\n"
        return sir



""" Algoritmul MinMax """

def min_max(stare):

    if stare.adancime==0 or stare.tabla_Joc.final() :
        stare.scor=stare.tabla_Joc.estimeaza_scor(stare.adancime)
        return stare

    #calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile=stare.mutari()

    #aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor=[min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent==Joc.JMAX :
        #daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        #daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor=stare.stare_aleasa.scor
    return stare



def alpha_beta(alpha, beta, stare):
    if stare.adancime==0 or stare.tabla_Joc.final() :
        stare.scor = stare.tabla_Joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare #este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX :
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            #calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN :
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare



def afis_daca_final(stare_curenta, pozitie = -1):
    # de adagat parametru "pozitie", ca sa nu verifice mereu toata tabla,
    # ci doar linia, coloana, 2 diagonale pt elementul nou, de pe "pozitie"

    if pozitie == -1:
        final = stare_curenta.tabla_Joc.final()
        if(final):
            if (final=="remiza"):
                print("Remiza!")
            else:
                print("A castigat "+final)

            return True

        return False
    
    max = stare_curenta.tabla_Joc.NR_COLOANE * stare_curenta.tabla_Joc.NR_LINII
    winco = stare_curenta.tabla_Joc.NR_CONNECT 

    #jos
    if pozitie +  winco * stare_curenta.tabla_Joc.NR_COLOANE < max:
        lista = [
            stare_curenta.tabla_Joc.matr[pozitie + i * stare_curenta.tabla_Joc.NR_COLOANE] 
            for i in range (winco)
        ]
        x = stare_curenta.tabla_Joc.verifica(lista)
        if x:
            print (x, "a castigat!")
            return True

    #stanga
    if pozitie - winco > 0:
        lista = [
            stare_curenta.tabla_Joc.matr[pozitie - i] 
            for i in range (winco)
        ]
        x = stare_curenta.tabla_Joc.verifica(lista)
        if x:
            print (x, "a castigat!")
            return True
       

    #dreapta
    if pozitie + winco < max:
        lista = [
            stare_curenta.tabla_Joc.matr[pozitie - i] 
            for i in range (winco)
        ]
        x = stare_curenta.tabla_Joc.verifica(lista)
        if x:
            print (x, "a castigat!")
            return True 
    #/
    if pozitie + winco * stare_curenta.tabla_Joc.NR_COLOANE + winco < max:
        lista = [
            stare_curenta.tabla_Joc.matr[pozitie + winco * i + j] 
            for i, j in zip (range(stare_curenta.tabla_Joc.NR_COLOANE), range(winco))
        ]
        x = stare_curenta.tabla_Joc.verifica(lista)
        if x:
            print (x, "a castigat!")
            return True   

    #\
    if pozitie + winco * stare_curenta.tabla_Joc.NR_COLOANE - winco < max:
        lista = [
            stare_curenta.tabla_Joc.matr[pozitie + winco * i - j] 
            for i, j in zip (range(stare_curenta.tabla_Joc.NR_COLOANE), range(winco))
        ]
        x = stare_curenta.tabla_Joc.verifica(lista)
        if x:
            print (x, "a castigat!")
            return True   
 
        
    return False


def main():
    #initializare algoritm
    raspuns_valid=False
    while not raspuns_valid:
        tip_algoritm=input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1','2']:
            raspuns_valid=True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit() and int(n) > 0:
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")


    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    #initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    #creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True :
        if (stare_curenta.j_curent == Joc.JMIN):
            #muta jucatorul
            raspuns_valid=False
            while not raspuns_valid:
                try:
                    coloana = int(input("coloana = "))
                    if 0 <= coloana < Joc.NR_COLOANE:
                        if stare_curenta.tabla_Joc.matr[coloana] != Joc.GOL:
                            print ("Coloana ocupata.")
                        else:
                            for linie in range (Joc.NR_LINII - 1, -1, -1):
                                if stare_curenta.tabla_Joc.matr[linie * Joc.NR_COLOANE + coloana] == Joc.GOL:
                                    break
                            raspuns_valid = True
                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            #dupa iesirea din while sigur am valida coloana
            #deci pot plasa simbolul pe "tabla de Joc"
            pozitie = linie * Joc.NR_COLOANE + coloana
            stare_curenta.tabla_Joc.matr[pozitie] = Joc.JMIN

            #afisarea starii Jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            #testez daca Jocul a ajuns intr-o stare finala
            #si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta, pozitie)):
                break


            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        #--------------------------------
        else: #jucatorul e JMAX (calculatorul)
        #Mutare calculator

            #preiau timpul in milisecunde de dinainte de mutare
            t_inainte=int(round(time.time() * 1000))
            if tip_algoritm=='1':
                stare_actualizata = min_max(stare_curenta)
            else: #tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            stare_curenta.tabla_Joc = stare_actualizata.stare_aleasa.tabla_Joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            #preiau timpul in milisecunde de dupa mutare
            t_dupa=int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de "+str(t_dupa-t_inainte)+" milisecunde.")
        
            if (afis_daca_final(stare_curenta)):
                break

            #S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__" :
        main()
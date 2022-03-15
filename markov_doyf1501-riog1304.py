
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, Ã  utiliser pour solutionner la problÃ©matique.
    C'est un gabarit pour l'application de traitement des frÃ©quences de mots dans les oeuvres d'auteurs divers.

    Les mÃ©thodes aparaissant dans ce fichier dÃ©finissent une API qui est utilisÃ©e par l'application
    de test testmarkov.py
    Les paramÃ¨tres d'entrÃ©e et de sortie (Application Programming Interface, API) sont dÃ©finis,
    mais le code est Ã  Ã©crire au complet.
    Vous pouvez ajouter toutes les mÃ©thodes et toutes les variables nÃ©cessaires au bon fonctionnement du systÃ¨me

    La classe markov est invoquÃ©e par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont prÃ©sents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
"""
import argparse
import os
import glob
import ntpath
import string
import re
import sys
import math
import random

class objet_unigramme:
    """Classe des objet du unigramme. Chaque objet sert à contenir un mot ainsi que sa fréquence utilisé.
        - Contient le mot de l'objet pour faciliter la recherche
        - Contient la fréquence de l'objet"""

    def __init__(self, mot, frequence):
        self.mot = mot
        self.frequence = frequence
        return
    def __init__(self,mot):
        self.mot = mot
        self.frequence=1
        return
    def setFrequence(self, frequence):
        self.frequence = frequence
        return
    def getFrequence(self):
        return self.frequence
    def getMot(self):
        return self.mot
    def augmenter(self):
        self.frequence += 1
        return
    def getResultat(self):
        return str("Le mot " + str(self.mot) + " revient " + str(self.frequence))
    def afficher(self):
        print(self.getResultat())
        return

class objet_ngramme:
    """Classe des objet du bigramme. Chaque objet sert à contenir un mot, le vecteur des mots qui peuvent le suivre et la fréquence du mot ainsi que chaqu'un des mots du vecteur.
     - Contient le mot de l'objet pour faciliter la recherche
     - Contient la fréquence de ce mot
     - Contient le vecteur des mots qui peuvent le suivre
     - Chaque mot du vecteur sont des objet objet_unigramme, contenant un mot et une fréquence"""

    def __init__(self, mot):
        self.mot = mot
        self.frequence = 0
        self.secondMot = {}
        return
    def ajouterMot(self, mot):
        if self.secondMot.get(mot) == None:
            self.secondMot[mot] = objet_unigramme(mot)
        else:
            self.secondMot[mot].augmenter()
        self.frequence+=1
        return
    def setFrequence(self, frequence):
        self.frequence = frequence
        return


    def getFrequence(self):
        return self.frequence


    def setFrequence(self, mot, frequence):
        self.secondMot[mot].setFrequence(frequence)
        return
    def getSecondMot(self):
        return self.secondMot
    def afficher(self):
        print("Le mot " + self.mot + " reveint " + str(self.frequence) + " et précede " + str(self.secondMot.__len__()))
        return
    def mergesort(self, list):
        if len(list) > 1:
            mid = len(list) // 2
            left_half = list[:mid]
            right_half = list[mid:]

            self.mergesort(left_half)
            self.mergesort(right_half)

            i, j, k = 0, 0, 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i].getFrequence() <= right_half[j].getFrequence():
                    list[k] = left_half[i]
                    i = i + 1
                else:
                    list[k] = right_half[j]
                    j = j + 1
                k = k + 1

            while i < len(left_half):
                list[k] = left_half[i]
                i = i + 1
                k = k + 1

            while j < len(right_half):
                list[k] = right_half[j]
                j = j + 1
                k = k + 1

class markov():
    """Classe Ã  utiliser pour coder la solution Ã  la problÃ©matique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code Ã  dÃ©velopper sont prÃ©sentes, mais tout le code est Ã  Ã©crire
        - En particulier, il faut complÃ©ter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas Ã  Ãªtre modifiÃ©
    # Signes de ponctuation Ã  retirer (complÃ©ter la liste qui ne comprend que "!" et "," au dÃ©part)
    PONC = ["!",",",".","'","\"",]

    def set_ponc(self, value):
        """DÃ©termine si les signes de ponctuation sont conservÃ©s (True) ou Ã©liminÃ©s (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou Ã©limine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation Ã  retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, Ã  partir du rÃ©pertoire qui les contient tous

        Note: le champs self.rep_aut doit Ãªtre prÃ©dÃ©fini:
            - Par dÃ©faut, il contient le rÃ©pertoire d'exÃ©cution du script
            - Peut Ãªtre redÃ©fini par la mÃ©thode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des rÃ©pertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accÃ©der)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """DÃ©finit le nom du rÃ©pertoire qui contient l'ensemble des rÃ©pertoires d'auteurs

        Note: L'appel Ã  cette mÃ©thode extrait la liste des rÃ©pertoires d'auteurs et les ajoute Ã  self.auteurs

        Args (string) : Nom du rÃ©pertoire en question (peut Ãªtre absolu ou bien relatif au rÃ©pertoire d'exÃ©cution)

        Returns:
            void : ne fait que dÃ©finir le nom du rÃ©pertoire qui contient les rÃ©pertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return


    def set_ngram(self, ngram):
        """Indique que l'analyse et la gÃ©nÃ©ration de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre Ã  jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        """Initialize l'objet de type markov lorsqu'il est crÃ©Ã©

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        # Initialisation des champs nÃ©cessaires aux fonctions fournies
        self.keep_ponc = False
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 2
        self.liste = {}

        # Au besoin, ajouter votre code d'initialisation de l'objet de type markov lors de sa crÃ©ation

        return

    # Ajouter les structures de donnÃ©es et les fonctions nÃ©cessaires Ã  l'analyse des textes,
    #   la production de textes alÃ©atoires, la dÃ©tection d'oeuvres inconnues,
    #   l'identification des n-iÃ¨mes mots les plus frÃ©quents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelÃ©e en premier par testmarkov.py
    # Ensuite, selon ce qui est demandÃ©, les fonctions find_author(), gen_text() ou get_nth_element() sont appelÃ©es

    def find_author(self, oeuvre):
        #étape 1, ouvrir et lire le fichier inconu (string oeuvre)
        #self.set_aut_dir("TextesPourAutoValidation")
        frequence_inconnu = {}
        texteInconnu = open(oeuvre, 'r')
        lecturInconnu = texteInconnu.read().lower()

        match_pattern = re.findall(r'\b[a-z]{3,50}\b', lecturInconnu)

        frequence_inconnu=extractionNGramme(self.ngram,match_pattern,frequence_inconnu)
        texteInconnu.close()
        #2 convertir l'objet en nombre ({mot: frq}


        for word in frequence_inconnu:
            frequence_inconnu[word]= frequence_inconnu[word].getFrequence()

        print(frequence_inconnu)

        #On lit tous les textes de tous les auteurs, on en fait des dict dans une liste
        self.analyze()
        #on change les objets pour les freq de chaque mot
        for auteur in self.auteurs:
            for word in self.liste[auteur]:
                self.liste[auteur][word] = self.liste[auteur][word].getFrequence()

        #Calculs, on commence par calculer la taille des deux vecteurs

        tailleAuteur = 0
        tailleInconnu =0


        sommeInconnu = 0
        sommeAuteur = 0
        produitScalaire = 0

        for word in frequence_inconnu:
            sommeInconnu += (frequence_inconnu[word])*(frequence_inconnu[word])

        tailleInconnu = math.sqrt(sommeInconnu)

        for auteur in self.auteurs:
            for word in self.liste[auteur]:
                if word in self.liste[auteur] and word in frequence_inconnu:
                    sommeAuteur += (self.liste[auteur][word]) * (self.liste[auteur][word])
                    produitScalaire += self.liste[auteur][word] * frequence_inconnu[word]
                else:
                    sommeAuteur+= 0
                    produitScalaire+=0
            tailleAuteur = math.sqrt(sommeAuteur)
            indiceRessemblance =  produitScalaire/(tailleAuteur*tailleInconnu)
            print(auteur,"-->",indiceRessemblance)










        resultats = [("balzac", 0.1234), ("voltaire", 0.1123)]   # Exemple du format des sorties


        # Ajouter votre code pour dÃ©terminer la proximitÃ© du fichier passÃ© en paramÃ¨tre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximitÃ© au fichier inconnu
        # Plus la proximitÃ© est grande, plus proche l'oeuvre inconnue est des autres Ã©crits d'un auteur
        #   Le produit scalaire entre le vecteur reprÃ©sentant les oeuvres d'un auteur
        #       et celui associÃ© au texte inconnu pourrait s'avÃ©rer intÃ©ressant...
        #   Le produit scalaire devrait Ãªtre normalisÃ© avec la taille du vecteur associÃ© au texte inconnu:
        #   proximitÃ© = (A . B) / (|A| |B|)   oÃ¹ A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           . est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def gen_text(self, auteur, taille, textname):
        self.analyze()
        print("--------------jhg------")

        if self.ngram ==1:
            i =0
            listeMot = []
            listePoids = []

            for word in self.liste[auteur]:
                self.liste[auteur][word].aficher()
                self.liste[auteur][word] = self.liste[auteur][word].getFrequence()


            #print(self.liste["Hugo"])

            listeMot = list(self.liste[auteur].keys())

            listePoids = list(self.liste[auteur].values())


            textGen = open(textname,'w')



            randomizer= (random.choices(listeMot,listePoids,k=taille))

            for word in randomizer:
                textGen.write(word)
                textGen.write(" ")

            textGen.close()
        if self.ngram > 1:
            self.analyze()
            listDesMots = []
            listPoids = []
            for ngram in self.liste[auteur]:
                self.liste[auteur][ngram] = self.liste[auteur][ngram].getFrequence()
            listDesMots = list(self.liste[auteur].keys())
            listPoids = list(self.liste[auteur].values())

            premierMot = random.choices(listDesMots,listPoids,k=1)
            mot= str(premierMot)
            text_Gen = open(textname,'w')

            for word in self.liste[auteur]:
                secondMot= random.choices(list(self.liste[auteur][word][ngram].getSecondMot(mot)))















        """AprÃ¨s analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            taille (int): Taille du texte Ã  gÃ©nÃ©rer
            textname (string): Nom du fichier texte Ã  gÃ©nÃ©rer.

        Returns:
            void : ne retourne rien, le texte produit doit Ãªtre Ã©crit dans le fichier "textname"
        """

        return

    def mergesort(self, list):
        if len(list) > 1:
            mid = len(list) // 2
            left_half = list[:mid]
            right_half = list[mid:]

            self.mergesort(left_half)
            self.mergesort(right_half)

            i, j, k = 0, 0, 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i].getFrequence() <= right_half[j].getFrequence():
                    list[k] = left_half[i]
                    i = i + 1
                else:
                    list[k] = right_half[j]
                    j = j + 1
                k = k + 1

            while i < len(left_half):
                list[k] = left_half[i]
                i = i + 1
                k = k + 1

            while j < len(right_half):
                list[k] = right_half[j]
                j = j + 1
                k = k + 1

    def get_nth_element(self, auteur, n):
        """AprÃ¨s analyse des textes d'auteurs connus, retourner le n-iÃ¨me plus frÃ©quent n-gramme de l'auteur indiquÃ©

        Args:
            auteur (string): Nom de l'auteur Ã  utiliser
            n (int): Indice du n-gramme Ã  retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherchÃ© (il est possible qu'il y ait plus d'un n-gramme au mÃªme rang)
        """
        listeTriage = []
        i = 0
        for word in self.liste[auteur]:
            listeTriage.append(self.liste[auteur][word])
            i+=1
        sys.setrecursionlimit(len(listeTriage)*len(listeTriage))
        self.mergesort(listeTriage)
        for j in range(int(len(listeTriage)/2)):
            listeTriage[j], listeTriage[len(listeTriage)-(j+1)]=(listeTriage[len(listeTriage)-(j+1)],listeTriage[j])
        ngram = listeTriage[n]
        return ngram

    def analyze(self):
        self.set_aut_dir("TextesPourEtudiants")
        for auteur in self.auteurs:
            frequency = {}
            listeOeuvres=self.get_aut_files(auteur)
            for oeuvre in listeOeuvres:
                texte = open(oeuvre, 'r', encoding='utf8')
                lecture = texte.read().lower()
                match_pattern = re.findall(r'\b[a-z]{3,50}\b', lecture)
                frequency=extractionNGramme(self.ngram,match_pattern,frequency)
            self.liste[auteur]=frequency



        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservÃ©e dans des strutures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse:  faire le calcul des frÃ©quences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procÃ©dant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur
        # Il serait possible de considÃ©rer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de frÃ©quence pour chacune des oeuvres
        #       de faÃ§on indÃ©pendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant des les additionner pour obtenir le vecteur global d'un auteur
        #   De cette faÃ§on, les mots d'un court poÃ¨me auraient une importance beaucoup plus grande que
        #   les mots d'une trÃ¨s longue oeuvre du mÃªme auteur. Ce n'est PAS ce qui vous est demandÃ© ici.

        return
def extractionNGramme(n,match_pattern,frequency):
    if n == 1:
        for word in match_pattern:
            if frequency.get(word)==None:
                frequency[word]=objet_unigramme(word)
            else:
                frequency[word].augmenter()

        for word in frequency:
            pass
            #print(frequency[word].getResultat())
    else:
        i=0
        for word in match_pattern:
            i+=1
            key = word
            for wordAfter in range(n-2):
                if i+wordAfter < match_pattern.__len__():
                    key+=(" " + match_pattern[i+wordAfter])
            if key not in frequency:
                frequency[key]=objet_ngramme(key)
            if i+n-1 < match_pattern.__len__() :
                wordSuivant = match_pattern[i+n-1]
                frequency[key].ajouterMot(wordSuivant)
                #frequency[key].afficher()
    return frequency

if __name__ == "__main__":

    t= markov()
    t.ngram=2
    t.analyze()
    temp = t.get_nth_element("Balzac",0)
    temp.afficher()



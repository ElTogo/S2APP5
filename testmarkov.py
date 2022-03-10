#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour l'Ã©valuation du code de dÃ©tection des auteurs et de gÃ©nÃ©ration de textes
#
#
#  Copyright 2018-2022 F. Mailhot et UniversitÃ© de Sherbrooke
#

import argparse
import importlib
import sys

import markov_CIP1_CIP2 as markov


class TestMarkov():
    """Classe Ã  utiliser pour valider la rÃ©solution de la problÃ©matique :

        - Contient tout le nÃ©cessaire pour tester la problÃ©matique.

    Pour valider la solution de la problÃ©matique, effectuer :
        - python testmarkov.py -help
            + Indique tous les arguments et options disponibles

    Copyright 2018-2022, F. Mailhot et UniversitÃ© de Sherbrooke
    """

    # Si mode verbose, reflÃ©ter les valeurs des paramÃ¨tres passÃ©s sur la ligne de commande
    def print_verbose(self):
        """Mode verbose, imprime l'ensemble des paramÃ¨tres utilisÃ©s pour ce test:
            - Valeur des paramÃ¨tres par dÃ©faut s'ils n'ont pas Ã©tÃ© modifiÃ©s sur la ligne de commande
            - Ensemble des tests demandÃ©s

        Returns:
            void: Ne fait qu'imprimer les valeurs contenues dans self
        """
        if self.args.v:
            print("Mode verbose:")

            if self.args.f:
                print("Fichier inconnu Ã  Ã©tudier: " + self.args.f)

            print("Calcul avec des " + str(self.args.m) + "-grammes")
            if self.args.F:
                print(str(self.args.F) + "e mot (ou digramme) le plus frÃ©quent sera calculÃ©")

            if self.args.a:
                print("Auteur Ã©tudiÃ©: " + self.args.a)

            if self.args.noPonc:
                print("Retirer les signes de ponctuation")
                self.markov.print_ponc()
            else:
                print("Conserver les signes de ponctuation")

            if self.args.G:
                print("GÃ©nÃ©ration d'un texte de " + str(self.args.G) + " mots, pour l'auteur: ", self.auteur)
                print("Le nom du fichier gÃ©nÃ©rÃ© sera: " + self.get_gen_file_name())

            if self.args.R:
                print("Nom du fichier de statistiques destinÃ© Ã  R: " + str(self.args.R))

            print("Calcul avec les auteurs du rÃ©pertoire: " + self.args.d)
            print("Liste des auteurs: ")
            for a in self.auteurs:
                aut = a.split("/")
                print("    " + aut[-1])

            print("")
        return

    def get_gen_file_name(self):
        name = self.gen_basename
        if self.g_cip :
            name = name + self.g_sep + self.cip
        if self.g_aut :
            name = name + self.g_sep + self.auteur
        if self.g_ext :
            name = name + self.g_ext

        return name

    def setup_and_parse_cli(self):
        """Utilise le module argparse pour:
            - Enregistrer les commandes Ã  reconnaÃ®tre
            - Lire la ligne de commande et crÃ©er le champ self.args qui rÃ©cupÃ¨re la structure produite

        Returns:
            void: Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog='markov_CIP1_CIP2.py')
        parser.add_argument('-d', default='.',
                            help='Repertoire contenant les sous-repertoires des auteurs (. par dÃ©faut)')
        parser.add_argument('-a', help='RÃ©sultats Ã  produire pour cet auteur spÃ©cifique')
        parser.add_argument('-f', help='Fichier inconnu pour lequel on recherche un auteur')
        parser.add_argument('-m', default=1, type=int, choices=range(1, 20),
                            help='Mode (1 ou 2 ou 3 ou ... 20) - unigrammes ou digrammes ou trigrammes ou ...')
        parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
        parser.add_argument('-G', default=1000, type=int, help='Taille du texte a generer')
        parser.add_argument('-g', default='Gen_text', help='Nom de base du fichier de texte Ã  gÃ©nÃ©rer')
        parser.add_argument('-g_ext', default='.txt', help='Extension utilisÃ©e pour le fichier gÃ©nÃ©rÃ©, .txt par dÃ©faut')
        parser.add_argument('-g_nocip', action='store_true', help='Ne pas utiliser les CIPs dans le nom du fichier gÃ©nÃ©rÃ©')
        parser.add_argument('-g_noaut', action='store_true', help='Ne pas utiliser le nom de l\'auteur dans le nom du fichier gÃ©nÃ©rÃ©')
        parser.add_argument('-g_sep', default="_", help='Utiliser cette chaine de caractÃ¨res comme sÃ©parateur dans le nom de fichier gÃ©nÃ©reÃ©')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        parser.add_argument('-noPonc', action='store_true', help='Retirer la ponctuation')
        parser.add_argument('-rep_code', default='.', help='RÃ©pertoire contenant la liste des CIPs et le code markov_CIP1_CIP2.py')
        parser.add_argument('-R', help='Nom du fichier de statistiques destinÃ© Ã  R')
        self.args = parser.parse_args()

        if self.args.d:
            self.dir = self.args.d
        if self.args.noPonc:
            self.keep_punc = False
        if self.args.m:
            self.ngram = self.args.m
        if self.args.G:
            self.gen_size = self.args.G
            self.gen_text = True
        if self.args.a :
            self.auteur = self.args.a
        if self.args.g:
            self.gen_basename = self.args.g
            self.gen_text = True
        if self.args.rep_code:
            self.rep_code = self.args.rep_code
        if self.args.g_ext:
            self.g_ext = self.args.g_ext
        if self.args.g_nocip:
            self.g_cip = False
        if self.args.g_noaut:
            self.g_aut = False
        if self.args.g_sep:
            self.g_sep = self.args.g_sep
        if self.args.f :
            self.oeuvre = self.args.f
            self.do_analyze = True
        if self.args.F:
            self.do_get_nth_ngram = True
            self.nth_ngram = self.args.F

        return

    def list_cips(self):
        """Lit le fichier etudiants.txt, trouve les CIPs, et retourne la liste

        Args:
            void: Le CIP est obtenu du fichier etudiants.txt, dans le rÃ©pertoire courant,
            ou tel qu'indiquÃ© en paramÃ¨tre (option -rep_code)

        Returns:
            void: void: Au retour, tous les cips sont inclus dans la liste self.cips
        """
        cip_file = self.rep_code + "/etudiants.txt"
        cip_list = open(cip_file,"r")
        Lines = cip_list.readlines()
        for line in Lines:
            for cip in line.split():
                self.cips.append(cip)

        return

    def import_markov_cip(self, cip):
        """Importe le fichier markov_CIP1_CIP2.py, oÃ¹ "CIP1_CIP2" est passÃ© dans le paramÃ¨tre cip

        Args:
            cip (string): Contient "CIP1_CIP2", les cips pour le code Ã  tester

        Returns:
            void: Au retour, le module markov_CIP1_CIP2 est importÃ© et remplace le prÃ©cÃ©dent
        """

        if "init_module" in self.init_modules:
            # DeuxiÃ¨me appel (ou subsÃ©quents): enlever tous les modules supplÃ©mentaires
            for m in sys.modules.keys():
                if m not in self.init_modules:
                    del(sys.modules[m])
        else:
            # Premier appel: identifier tous les modules dÃ©jÃ  prÃ©sents
            self.init_modules = sys.modules.keys()

        self.cip = cip
        markov_name = "markov_" + cip
        self.markov_module = importlib.import_module(markov_name)
        getattr(self.markov_module, "markov")

        return

    def __init__(self):
        """Constructeur pour la classe testmarkov.  Initialisation de l'ensemble des Ã©lÃ©ments requis

        Args:
            void: Le constructeur lit la ligne de commande et ajuste l'Ã©tat de l'objet testmarkov en consÃ©quence

        Returns:
            void: Au retour, la nouvelle instance de test est prÃªte Ã  Ãªtre utilisÃ©e
        """
        self.dir = "."
        self.ngram = 1
        self.keep_punc = True
        self.gen_text = False
        self.gen_size = 100
        self.gen_basename = "Gen_text"
        self.g_ext = ".txt"
        self.g_cip = True
        self.g_aut = True
        self.auteur = ""
        self.tests = []
        self.do_analyze = False
        self.do_get_nth_ngram = False
        self.setup_and_parse_cli()

        self.cips = []
        self.list_cips()
        self.init_modules = {}


if __name__ == "__main__":
    tm = TestMarkov()       # Initialisation de l'instance de test


    for cip in tm.cips:   # Permet de tester le code d'une ou plusieurs Ã©quipes, Ã  tour de rÃ´le
        tm.import_markov_cip(cip)
        tm.markov = tm.markov_module.markov()

        # Ajout de l'information nÃ©cessaire dans l'instance Ã  tester de la classe markov sous Ã©tude:
        #   Utilisation de la ponctuation (ou non), taille des n-grammes, rÃ©pertoire des auteurs
        if tm.args.noPonc :
            tm.markov.set_ponc(False)
        else:
            tm.markov.set_ponc(True)

        tm.markov.set_ngram(tm.ngram)
        tm.markov.set_aut_dir(tm.dir)

        tm.auteurs = tm.markov.auteurs
        tm.print_verbose()  # Imprime l'Ã©tat de l'instance (si le mode verbose a Ã©tÃ© utilisÃ© sur la ligne de commande)

        tm.markov.analyze()

        if tm.gen_text:
            filename = tm.get_gen_file_name()
            tm.markov.gen_text(tm.auteur, tm.gen_size, filename)

        if tm.do_analyze:
            tm.analysis_result = tm.markov.find_author(tm.oeuvre)
            print('cip: ', cip, " - FrÃ©quences: ", tm.analysis_result)

        if tm.do_get_nth_ngram:
            nth_ngram = tm.markov.get_nth_element(tm.auteur, tm.nth_ngram)
            print("cip: ", cip, " - Auteur: ", tm.auteur, ", ", tm.nth_ngram, "e ngram de ", tm.ngram, "mots: ", nth_ngram)

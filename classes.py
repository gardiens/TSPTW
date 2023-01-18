# *
# * Ensembles de classes utilisés dans nos algorithmes un peu générique
from score import *
from random import sample, random
import networkx as nx
import matplotlib.pyplot as plt
from numpy import Inf


class instance:
    '''C'est le modele de travail, il contient toutes les informations sur l'instance
    inputname: c'est la localisation relative de l'instance étudié '''

    def __init__(self, inputname='') -> None:
        self.name_instance = inputname
        if inputname == '':
            print(' ATTENTION INPUTNAME PAS CHARGE ')
        # un truc du genre  {int: {x,y,wstart,wend},...}
        self.travail = load_instance(inputname)

        self.dist_mat = compute_dist_mat(self.travail)  # Matrice de distance
        # liste de tous les points
        self.touslespoints = list(self.travail.keys())

    def compute_score_with_mat(self, sol_list, tolerance=False, debug=False, listecomplete=False, nbviola=False):
        '''compute the score using the distance matrix,
        sol_list is an instance that you want to comput 
        Tolerance, if True then raise error if nb_violation > 0
        if debug, print the distance, duree and nb_violation
        listecomplete is a boolean, if True, return the list of all the distance between the points+ the duration'''
        distance = 0
        duree = 0
        nb_violation = 0  # ! débuggage, calcul le nombre de violation dans la fenêtre de temps
        # print(sol_list)
        l = []  # the list complete of all distance+ duration...
        for i in range(len(sol_list)-1):
            distance += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]
            # ! la durée est la somme des distances entre les points
            duree += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]

            next_start = self.travail[sol_list[i+1]]["wstart"]
            end_window = self.travail[sol_list[i+1]]["wend"]
            if (duree < next_start):
                duree = next_start
            if (duree > end_window):
                nb_violation += 1
            l.append((distance, duree))

        # cas de la distance du dernier point au premier
        distance += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]
        # cas de la durée du dernier point au premier point...
        duree += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]
        l.append((distance, duree))
        next_start = self.travail[sol_list[0]]["wstart"]
        end_window = self.travail[sol_list[0]]["wend"]
        if (duree < next_start):
            duree = next_start
        if (duree > end_window):
            nb_violation += 1
        # * Debug lines:
        if debug:
            print(distance)
            print(duree)
            print(nb_violation)
        if tolerance and nb_violation > 0:
            raise Exception("nb_violation > 0")
        # print(distance)
        # print(duree)
        # print(nb_violation)
        if not listecomplete:
            return (distance, nb_violation) if nbviola else distance
        else:
            return (distance, nb_violation, l) if nbviola else (distance, l)

    def compute_score(self, sol_list, tolerance=False, debug=False, listecomplete=False, nbviola=False):
        # sourcery skip: inline-immediately-returned-variable
        ''' compute the score from the instance and the solution given in argument'''

        score = self.compute_score_with_mat(
            sol_list, tolerance, debug, listecomplete, nbviola)
        return score

    def compute_score_somme_retards(self, sol_list, demarrage=0, listedistanceduree=None, debug=False, listecomplete=False, tolerance=False):
        '''Calcule le score étant la somme des retards des individus
        Reprend la fonction compute_score_apartir mais en renvoyant le retard au lieu de la distance'''
        #! il faut que l'agencement dans sol_list soit le même que dans listedsitanceduree !!!

        # * Copiage de compute_score avec modification pour ne pas recalculer les distances déjà calculées
        retard_tot = 0
        if demarrage == 0 or demarrage == 1:  # ! Ici , il faut se placer à un endroit où le calcul n'a pas d'importance!!
            distance = 0
            duree = 0
            demarrage = 1  # c'est pour que la boucle démarre au bon endroit :)))

        nb_violation = 0
        if isinstance(sol_list, solution):
            sol_list = sol_list.get_ordre()
        for i in range(demarrage-1, len(sol_list)-1):
            distance += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]
            # ! la durée est la somme des distances entre les points
            duree += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]
            next_start = self.travail[sol_list[i+1]]["wstart"]
            end_window = self.travail[sol_list[i+1]]["wend"]
            if (duree < next_start):
                duree = next_start
            if (duree > end_window):
                nb_violation += 1
                retard_tot += duree - end_window
            #listedistanceduree[i] = (distance, duree)
        # cas de la distance du dernier point au premier
        distance += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]
        # cas de la durée du dernier point au premier point...
        duree += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]

        next_start = self.travail[sol_list[0]]["wstart"]
        end_window = self.travail[sol_list[0]]["wend"]
        if (duree < next_start):
            duree = next_start
        if (duree > end_window):
            nb_violation += 1

        return retard_tot

    def compute_score_apartir(self, sol_list, demarrage=0, listedistanceduree=None, debug=False, listecomplete=False, tolerance=False):
        '''Compute the score and update the liste of distance and duration of a given sol_list.
        demarrage: the index of the point where we start to compute the score, c'est celui à partir de laquelle on a travailler
        sol_list: la liste des points solutions, obtenu par sol.get_sol()
        La subtilité ici c'est qu'on ne CALCULE PAS NECESSAIREMENT TOUS LES CALCULS DEJA FAITS  DANS LA LISTE'''
        #! il faut que l'agencement dans sol_list soit le même que dans listedsitanceduree !!!
        if listedistanceduree is None:
            listedistanceduree = []
        # * Copiage de compute_score avec modification pour ne pas recalculer les distances déjà calculées
        if demarrage == 0 or demarrage == 1:  # ! Ici , il faut se placer à un endroit où le calcul n'a pas d'importance!!
            distance = 0
            duree = 0
            demarrage = 1  # c'est pour que la boucle démarre au bon endroit :)))
        else:

            distance = listedistanceduree[demarrage-2][0]
            duree = listedistanceduree[demarrage-2][1]
        nb_violation = 0  # ! débuggage, calcul le nombre de violation dans la fenêtre de temps
        # * Je sais pas coder, si jamais on confond sol_list avec l'instance solution, on la convertit naturellemnt :)
        if isinstance(sol_list, solution):
            sol_list = sol_list.get_ordre()

        for i in range(demarrage-1, len(sol_list)-1):
            distance += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]
            # ! la durée est la somme des distances entre les points
            duree += self.dist_mat[int(sol_list[i]), int(sol_list[i+1])]

            next_start = self.travail[sol_list[i+1]]["wstart"]
            end_window = self.travail[sol_list[i+1]]["wend"]
            if (duree < next_start):
                duree = next_start
            if (duree > end_window):
                nb_violation += 1
            listedistanceduree[i] = (distance, duree)

        # cas de la distance du dernier point au premier
        distance += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]
        # cas de la durée du dernier point au premier point...
        duree += self.dist_mat[int(sol_list[-1]), int(sol_list[0])]

        next_start = self.travail[sol_list[0]]["wstart"]
        end_window = self.travail[sol_list[0]]["wend"]
        if (duree < next_start):
            duree = next_start
        if (duree > end_window):
            nb_violation += 1

        listedistanceduree[-1] = (distance, duree)
        # * Debug lines:
        if debug:
            print(distance)
            print(duree)
            print(nb_violation)
        if tolerance and nb_violation > 0:
            raise Exception("nb_violation > 0")
        # print(distance)
        # print(duree)
        # print(nb_violation)
        if not listecomplete:
            return distance
        else:
            return distance, l

    def verif_sol_inst(self, inst_name, sol_name):
        # sourcery skip: de-morgan, use-fstring-for-concatenation
        '''
        compute the score of an instance for a given solution
        instance and solution are given by the name of their file
        if a score is given in the solution file, check if it matches the computed score
        vraiment une fonction 100% débug '''

        instance = load_instance(inst_name)
        sol_list, sol_score_f = load_solution(sol_name)
        sol_score_c = compute_score(instance, sol_list)

        for node in instance:
            if (not node in sol_list):
                print("a city is not in solution: " + node)

        if (sol_score_f is None):
            print("no score in file")
            print("computed score:" + str(sol_score_c))
            return

        if (sol_score_f != sol_score_c):
            print("Score in file different from computed score:")
            print(str(sol_score_f) + " != " + str(sol_score_c))
            return

        print("Score in file corresponds to computed score: " + str(sol_score_c))
        return

    def display(self, sol_list):
        '''Affichage de la solution graphiquement avec networkx'''
        G = nx.DiGraph()

        for key in self.travail:
            # print(key)
            G.add_node(
                key, pos=(self.travail[key]['x'], self.travail[key]['y']))
        # On rajoute une arête
        for i in range(len(sol_list)-1):
            G.add_edge(sol_list[i], sol_list[i+1])
        G.add_edge(sol_list[-1], sol_list[0])
        '''color_map=[] # Calcul pour colorer les couleurs des noeuds 
        for node in G:
            if node < 10:
                color_map.append('blue')
            else: 
                color_map.append('green')  '''

        pos = nx.get_node_attributes(G, 'pos')
        nx.draw(G, pos, with_labels=True)
        plt.show()
        #print(' ON EST LA ')

    def get_name_instance(self):
        return self.name_instance


class solution(instance):
    """_summary_ : class solution
    value:
    self.value le core du programme 
    value: la liste de solution qu'on va faire rentrer
    le score de la solution et sa liste distance/durée est inféré. 
    inputname: le nom de l'instance regardé 
    """

    def __init__(self, modele: instance, value=[], score=+Inf, calculscore=True, listedistanceduree=[]) -> None:
        self.modele = modele  # On garde en mémoire le modèle
        self.name_instance = modele.get_name_instance()
        self.ordrevisite = value

        self.score = score
        if value != []:
            self.listedistanceduree = [0 for k in range(len(value))]
            if calculscore:
                self.score = modele.compute_score_apartir(
                    value, 0, self.listedistanceduree)
            else:
                self.listedistanceduree = listedistanceduree

    def get_sol(self):
        return self.ordrevisite

    def get_listedistanceduree(self):
        return self.listedistanceduree

    def get_len(self):
        return len(self.get_ordre())

    def get_random_points(self, k=2):
        '''Renvoie une liste de k points dans [0,len(self)] aléatoires,
        la liste sortie est triée!'''
        # n=self.get_ordre().len()
        t = sample(range(self.get_len()), k)
        t.sort()

        return t   # merci copilot

    def swap(self, i, j):
        '''Echange le i-ième et j-ième lieux visités dans la solution
        i: int
        j:int'''
        if i == j:
            print(' le swap na pas eût lieu on a eût deux fois les mêmes indices')
        self.ordrevisite[i], self.ordrevisite[j] = self.ordrevisite[j], self.ordrevisite[i]
        # L'arrangement entre les deux est importants, on change donc les deux
        self.listedistanceduree[i], self.listedistanceduree[j] = self.listedistanceduree[j], self.listedistanceduree[i]
        #! on pourrait renvoyer une nouvelle liste si on veut être plus propre?

    def get_score(self):
        return self.score

    def set_score(self, val):
        self.score = val

    def get_ordre(self):
        return self.ordrevisite

    def set_ordre(self, nvordre):
        self.ordrevisite = nvordre

    def set_elem_ordre(self, i, val):
        self.ordrevisite[i] = val

    def get_elem_ordre(self, i):
        return self.ordrevisite[i]

    def __str__(self) -> str:
        return 'Ordre visité:'+str(self.ordrevisite)+'liste distance duree ( le premier cest la distance):'+str(self.listedistanceduree)+'score:'+str(self.score)

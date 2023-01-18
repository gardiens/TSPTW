'''Version évolué de 2-OPT: ici on faitl e choix de se déplacer uniquement dans le cas des osolutions faisables (pas de violation de fenêtre de temps)'''
''' Il faudrait voir si on peut ne pas évoluer dans les solutions faisables, mais je pense que y'aurait un problème'''




from itertools import permutations # Très utile pour calculer les permutations
from score import *
from random import sample
from classes import *
from math import exp
from random import random
from matplotlib import pyplot as plt
def upate_T_SA(T, alpha=0.99):
    ''' Choisis comment on modifie la température en fonction de l'itération dans le simulated annealing'''

    return alpha*T


def random_solution(modele):
    '''initialise une solution aléatoire, NI + doit donner des solutions valides...'''
    arr = sample(modele.touslespoints, len(modele.touslespoints))

    return solution(modele, arr)


def apportsolution(modele, sol, nvplacement, listref):
    '''
    NON UTILISER EN PRATIQUE. CE SERAIT UNE OPTIMISATION DU CALCUL DU SCORE DANS LE CAS DE 2OPT 
    return oldscore, nvscore ( l'ancien score si on a pas fait la permutation, et le même pour nvscore)
    modele:modele où on bosse
    sol: solution regardé
    nvplacement: permutation de listref,

    listref: [int] liste des indices des villes qu'on va placé. Le suppose trié!!! '''

    ordre = self.get_ordre()
    #! Bug si kopt=n !!
    n = len(listeref)
    nvscore = 0
    oldscore = 0
    for k in range(n):
        ancienproprio = ordre[listref[k]]
        nvproprio = ordre[nvplacement[k]]
        voisin1 = ordre[listeref[k]-1]  # voisin gauche
        voisin2 = ordre[listeref[k]+1]  # voisin droit
        # On vérifie si dans la permutation l'élément de droite est dans les objets à regarder ou non, si oui on le calcule pas , sinon non
        if voisin2 != ordre[listref[k+1 % len(listref)]]:
            nvscore += modele.dist_mat[voisin2, nvproprio]
            oldscore = modele.dist_mat[voisin2, ancienproprio]

        nvscore += sol.dist_mat[voisin1, nvproprio]
        oldscore += sol.dist_mat[voisin1, ancienproprio]
        #! Ici, il faut faire gaffe si les indices sont à côté où non

    return nvscore, oldscore
    # * Important, pointavaluer est supposé TRIER


def kopt(modele, sol: solution, perm, ind_a_changer):
    ''' Renvoie une nouvelle solution où l'ordre des points à été changé selon perm
    perm[int]: liste des indices des points à changer dans la solution'''
    oordre = sol.get_ordre()[:]  # deepcopy car on va le modifier
    # la seul chose importante c'est de pas calculer le SCORE pour améliorr la compléxité
    nvsol = solution(modele, oordre, 10**6, False,
                     sol.get_listedistanceduree()[:])
    p1 = sol.get_elem_ordre(perm[0])
    for k in range(len(ind_a_changer)-1):

        ancien_coeff = sol.get_elem_ordre(perm[k])

        nv_coeff = sol.get_elem_ordre(perm[k+1])
        nvsol.set_elem_ordre(perm[k], nv_coeff)
    # Ne pas oublier le dernier
    nvsol.set_elem_ordre(perm[-1], p1)

    return nvsol


def verif_valide(modele, sol: solution, ind_a_changer, demarrage=0):
    ''' Renvoie True si la solution est valide, False sinon
    si la valeur est True, il mets à jour automatique sol.listedistanceduree et son score
    A améliorer: si on garde la listedistanceduree d'avant, on pourrait faire un calcul plus rapide'''
    #! SUPPOSE QUE A SOLUTION EST FAISABLE AVANT
    # * Copiage de compute_score avec modification pour ne pas recalculer les distances déjà calculées
    listedistanceduree = sol.get_listedistanceduree()

    # ! Ici , il faut se placer à un endroit où le calcul n'a pas d'importance!!
    if demarrage in [0, 1]:
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
        distance += sol.dist_mat[int(sol_list[i]), int(sol_list[i+1])]
        # ! la durée est la somme des distances entre les points
        duree += sol.dist_mat[int(sol_list[i]), int(sol_list[i+1])]

        next_start = sol.travail[sol_list[i+1]]["wstart"]
        end_window = sol.travail[sol_list[i+1]]["wend"]
        if (duree < next_start):
            duree = next_start
        if (duree > end_window):
            nb_violation += 1
            return False
        listedistanceduree[i] = (distance, duree)

    # cas de la distance du dernier point au premier
    distance += sol.dist_mat[int(sol_list[-1]), int(sol_list[0])]
    # cas de la durée du dernier point au premier point...
    duree += sol.dist_mat[int(sol_list[-1]), int(sol_list[0])]

    next_start = sol.travail[sol_list[0]]["wstart"]
    end_window = sol.travail[sol_list[0]]["wend"]
    if (duree < next_start):
        duree = next_start
    if (duree > end_window):
        nb_violation += 1
        return False

    listedistanceduree[-1] = (distance, duree)
    # * Debug lines:

    sol.set_score(distance)
    # ? A la fin, il doit avoir modifier listedistanceduree et le score de la solution. Comme set_ renvoie une donnée mutable, on peut faire ces opérations comme ça :)
    return True
    # print(distance)
    # print(duree)
    # print(nb_violation)


def simulated_annealing_kopt_naif(k: int, modele: instance, score, listsol1=False, T_init=100, T_final=1, alpha=0.99, sol_init=None, listTT=False, nb_iter_max=-1, expo_global=4):
    """
    _summary_ : fonction qui permet de trouver une solution optimale par recuit simulé
    2OPT car spécialement fit pour 2OPT
    modele: class de l'instance étudié
    k: de quelle k on regarde?
    score: la fonction de score a utiliser (ex: compute_score)
    T_init: température initiale
    T_final: température finale
    alpha: coefficient de refroidissement
    nb_iter: nombre d'itération
    sol_init: solution initiale
    voisinage: fonction qui permet de trouver une solution voisine
    listsol: True on renvoie aussi la liste des oslutions utilisés
    """
    #! Assert the solution is feasible
    nbiter = 1
    listsol = []
    listT = []
    ecart = []
    if sol_init is None:
        # ! ICI IL FAUT UNE RANDOM SOLUTION FAISABLE !!!!!
        sol = random_solution(modele)
        # la solution est bien random
    else:

        sol = sol_init
    T = T_init
    moy_diff = 0
    while T > T_final or nbiter < nb_iter_max:
        '''if nbiter % 100 == 0:
            print('on est à la température', T)'''

        # Selection des voisins, ça revient à choisir quelles indices ont veut changer
        # Liste d'indice qu'on va changer  de la forme ( sa place dans la première liste, son nom) #TODO: WIP
        ind_a_changer = sol.get_random_points(k)
        for perm in permutations(ind_a_changer, k):
            nvsol = kopt(modele, sol, perm, ind_a_changer)
            score1, score2 = score(
                modele, sol), score(modele, nvsol)

            if score2 < score1:
                # On verifie si la nouvelle solution est valide
                # TODO: WIP, c'est l'opération de changement de la permutation des indices
                # Applique l'opération sur sol de kopt
                sol = nvsol
                sol.set_score(score2)

                break

            elif random() < exp(-(score2 - score1) / T):
                # On garde le changement
                sol = nvsol
                '''listsol.append(nvsol)'''
                break
            else:
                del nvsol  # On supprime la solution qu'on a créé
        moy_diff += abs(score2-score1)
        listT.append(sol)
        listsol.append(sol)
        T = upate_T_SA(T, alpha)
        nbiter += 1
    print('en tous, on a fait pour le simulated annealing',
          nbiter, ' itérations', 'le score final est', score(modele, sol))
    print('la moyenne des différences de score est', moy_diff/nbiter)
    '''if score2 == 0:
        print('on a trouvé la solution optimale')
        return sol, listsol'''

    if listsol1:
        if listTT:
            return sol, listsol, listT
        else:
            return sol, listsol
    else:
        if listTT:
            return sol, listT
        else:
            return sol,

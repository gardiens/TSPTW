''' Fichier pour compute des scores '''

from classes import *


def score_naif(modele: instance, sol: solution, exposant=3):
    if isinstance(sol, list):
        score, nbviol = modele.compute_score(sol, False, False, False, True)
    else:
        (score, nbviol) = modele.compute_score(
            sol.get_sol(), False, False, False, True)

    return score+10**exposant*nbviol


def score_retard(modele: instance, sol: solution):
    if isinstance(sol, list):
        retard = modele.compute_score_somme_retards(sol, 0)
    else:
        retard = modele.compute_score_somme_retards(sol, 0)

    return retard

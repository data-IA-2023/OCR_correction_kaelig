def fusionner_valeurs_similaires(dictionnaire):
    valeurs_a_fusionner = {}
    resultat = {}

    for cle, valeur in dictionnaire.items():
        if cle in valeurs_a_fusionner:
            resultat[cle] = valeurs_a_fusionner[cle] + valeur
        else:
            valeurs_a_fusionner[cle] = valeur

    return resultat

# Exemple d'utilisation
dico = {'a': 100, 'b': 200, 'c': 300, 'd': 200, 'e': 100}
resultat = fusionner_valeurs_similaires(dico)
print(resultat)  # {'a': 100, 'b': 200, 'c': 300, 'd': 200, 'e': 100}

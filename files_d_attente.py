from random import random
from math import log
import matplotlib.pyplot as mat

def tri(l,k):#trie l (liste de listes) sur la composante de rang k de chaque sous-liste
    n = len(l)
    for i in range(1,n):
        j = i
        while j > 0 and l[j-1][0] > l[j][0]:
            l[j-1], l[j] = l[j], l[j-1]
            j -= 1
    return l

def sous_liste(l,k):#l : liste de listes. sous_liste extrait la liste des composantes de rang k des sous-listes de l
    return [l[i][k] for i in range(len(l))]

#arrange_liste_abscisse et arrange_liste_ordonnee dédoublent les éléments d'une liste pour permettre un affichage convenable
def arrange_liste_abscisse(l):
    n = len(l)
    if n <= 2:
        return []
    g = [l[0]]+[l[(i//2)+1] for i in range(2*n-2)]
    return g

def arrange_liste_ordonnee(l):
    n = len(l)
    if n <= 2:
        return []
    g = [l[i//2] for i in range(2*n-2)]+[l[-1]]
    return g

def vider_serveur(serveurs, t):#serveurs[fi] = [numéro du client servi au serveur numéro fi, instant de fin de service du client]. vider serveur met à jour la liste serveurs en enlevant les clients dont le service est terminé avant l'instant t
    nombre_de_serveurs = len(serveurs)-1
    for i in range(1, nombre_de_serveurs+1):
        if serveurs[i][1] < t:
            serveurs[i] = [0,0]

def premier_serveur_libre(serveurs):#serveurs[fi] = [client en train d'être servi au serveur numéro fi, instant de départ du client]
#renvoie le numéro du premier serveur qui va être libéré et l'instant de libération du serveur correspondant (l'instant pour lequel le client servi va finir son service)
    Nombre_de_serveurs = len(serveurs)-1
    rang = 0
    instant_liberation = float("infinity")
    for i in range(1,Nombre_de_serveurs+1):
        if serveurs[i][1] < instant_liberation:
            rang, instant_liberation = i, serveurs[i][1]
            if instant_liberation == 0:
                break
    return (rang, instant_liberation)

def somme(l,i):#renvoie la somme des éléments de l à partir du rang i
    n = len(l)-i
    compteur = 0
    for index in range(i,i+n):
        compteur += l[index]
    return compteur

def moyenne(l,i):#renvoie la moyenne des éléments de l à partir du rang i
    nb_clients = len(l)-i
    if nb_clients == 0:
        return 0
    cumul = 0
    for clientent in range(i,i+nb_clients):
        cumul += l[clientent]
    return cumul / nb_clients

def moyenne_ponderee(instants,valeurs):#renvoie la moyenne des éléments de la liste valeurs, pondérée par les durées instants[i+1] - instants[i]
    n = len(valeurs)
    if n <= 1:
        return 0
    cumul = 0
    for index in range(n-1):
        cumul += valeurs[index]*(instants[index+1]-instants[index])#valeur * poids
    moy =  cumul/instants[-1]
    return moy

#A partir du taux d'arrivée (nombre de personnes qui arrivent dans la file par unité de temps) et du taux de service (nombre de personnes servies par unité de temps), on construit temps_inter_arrivees (liste des durées séparant deux arrivées consécutives) et temps_service (liste des temps de service)
#On construit ensuite la liste des temps d'attente avec la formule de Lindley, puis la liste des instants de fin de service
#La deuxième composante de chaque élément des listes instant_arrivee et fin_service (qui valent 1 ou -1) permet de savoir si l'instant associé correspond à une arrivée dans la file (composante valant 1) où à un départ du sytème, c'est-à-dire lorsqu'un client a fini d'être servi (composante valant -1)
#On construit ensuite la liste instant_arrivee_depart qui est la liste triée selon la première composante de (instant_arrivee + fin_service[1:]). Cette liste permet par opérations d'obtenir les arrivées cumulées et les départs cumulés à chaque instant
def une_file_un_serveur(taux_arrivee,taux_service,nombre_de_clients):
    temps_inter_arrivees = [((-1)/taux_arrivee)*log(random()) for i in range(nombre_de_clients+1)]#liste des durées séparant deux arrivées consécutives
    temps_inter_arrivees[0] = 0
    instant_arrivee = [[0,1] for i in range(nombre_de_clients+1)]#le "1" permet de savoir que l'instant correspondant est un instant où une personne arrive dans la file
    for i in range(1,nombre_de_clients+1):
        instant_arrivee[i][0] = instant_arrivee[i-1][0] + temps_inter_arrivees[i]
    temps_service = [((-1)/taux_service)*log(random()) for i in range(nombre_de_clients+1)]
    temps_service[0] = 0
    temps_attente = [0 for i in range(nombre_de_clients+1)]
    for i in range(1,nombre_de_clients+1):
        temps_attente[i] = max(temps_attente[i-1] + temps_service[i-1] - temps_inter_arrivees[i],0)#formule de Lindley
    fin_service = [[instant_arrivee[i][0] + temps_attente[i] + temps_service[i], -1] for i in range(nombre_de_clients+1)]#le "-1" permet de savoir que l'instant correspondant est un instant où une personne sort du système
    fin_service[0][0] = 0

    instant_arrivee_depart = tri(instant_arrivee + fin_service[1:], 0)#liste des instants où un client entre ou sort du sytème
    arrivees_cumulees = [0 for i in range(2*nombre_de_clients+1)]#cumul du nombre de personnes arrivées dans la file
    departs_cumules = [0 for i in range(2*nombre_de_clients+1)]#cumul du nombre de personnes sorties du système
    longueur_file = [0 for i in range(2*nombre_de_clients+1)]#longueur de la file à chaque instant
    for i in range(1,2*nombre_de_clients+1):
        arrivees_cumulees[i] = arrivees_cumulees[i-1] + (1 + instant_arrivee_depart[i][1])/2#il y a une personne de plus arrivée dans la file si et seulement si l'instant associé correspond à une arrivée dans la file (c'est-à-dire pour instant_arrivee_depart[i][1] == 1)
        departs_cumules[i] = departs_cumules[i-1] + (1 - instant_arrivee_depart[i][1])/2#il y a une personne de plus sortie du système si et seulement si l'instant associé correspond à une sortie du système (c'est-à-dire instant_arrivee_depart[i][1] == -1)
        longueur_file[i] = arrivees_cumulees[i] - departs_cumules[i]

    #modification des listes pour améliorer les représentations graphiques
    instant_arrivee_depart = arrange_liste_abscisse(sous_liste(instant_arrivee_depart,0))
    arrivees_cumulees = arrange_liste_ordonnee(arrivees_cumulees)
    departs_cumules = arrange_liste_ordonnee(departs_cumules)
    longueur_file = arrange_liste_ordonnee(longueur_file)

    #représentations graphiques
    mat.plot(instant_arrivee_depart,arrivees_cumulees,instant_arrivee_depart,departs_cumules)#arrivees_cumulees en fonction du temps et departs_cumules en fonction du temps
    mat.show()
    mat.plot(instant_arrivee_depart,longueur_file)#longueur de la file en fonction du temps
    mat.show()

#A partir des listes des instants d'arrivee et des temps de service, on détermine pour chaque client le temps d'attente, l'instant de début de service, le temps de séjour dans le système et l'instant de fin de service.
#Pour cela, on utilise une liste serveurs, avec serveurs[fi] = [client en train d'être servi au serveur numéro fi, instant de départ du client], qui permet de récupérer le numéro du client sur lequel le client actuel attend (dernier client qui a pris le même serveur que le client actuel)
#Cela va permettre ensuite de procéder de la même manière que pour une file avec un seul serveur, puisque le client "précédent" est connu
def une_file_N_serveurs(instant_arrivee,temps_service,nombre_de_serveurs,nombre_de_clients):
    temps_attente = [0 for i in range(nombre_de_clients+1)]
    debut_service = [0 for i in range(nombre_de_clients+1)]
    temps_sejour = [0 for i in range(nombre_de_clients+1)]
    fin_service = [[0, -1] for i in range(nombre_de_clients+1)]
    serveurs = [[0,0] for i in range(nombre_de_serveurs+1)]#serveurs[fi] = [client en train d'être servi au serveur numéro fi, instant de départ du client]
    for client in range(1,nombre_de_clients+1):
        numero_serveur_libre, instant_serveur_libre = premier_serveur_libre(serveurs)
        debut_service[client] = max(instant_serveur_libre, instant_arrivee[client][0])
        temps_attente[client] = debut_service[client] - instant_arrivee[client][0]
        fin_service[client][0] = debut_service[client] + temps_service[client]
        temps_sejour[client] = temps_attente[client] + temps_service[client]
        serveurs[numero_serveur_libre] = [client, fin_service[client][0]]#le serveur qui se libère en premier change d'état
    instant_arrivee_depart = tri(instant_arrivee + tri(fin_service[1:],0),0)#liste des instants où un client entre ou sort du sytème
    arrivees_cumulees = [0 for i in range(2*nombre_de_clients+1)]#cumul du nombre de personnes arrivées dans le système
    departs_cumules = [0 for i in range(2*nombre_de_clients+1)]#cumul du nombre de personnes sorties du système
    longueur_file = [0 for i in range(2*nombre_de_clients+1)]#longueur de la file à chaque instant
    for i in range(1,2*nombre_de_clients+1):
        arrivees_cumulees[i] = arrivees_cumulees[i-1] + (1 + instant_arrivee_depart[i][1])/2
        departs_cumules[i] = departs_cumules[i-1] + (1 - instant_arrivee_depart[i][1])/2
        longueur_file[i] = longueur_file[i-1] + instant_arrivee_depart[i][1]

    #modification des listes pour améliorer les représentations graphiques
    instant_arrivee_depart = sous_liste(instant_arrivee_depart,0)
    moyenne_longueur_file = moyenne_ponderee(instant_arrivee_depart,longueur_file)
    instant_arrivee_depart = arrange_liste_abscisse(instant_arrivee_depart)
    arrivees_cumulees = arrange_liste_ordonnee(arrivees_cumulees)
    departs_cumules = arrange_liste_ordonnee(departs_cumules)
    longueur_file = arrange_liste_ordonnee(longueur_file)

    return ((instant_arrivee_depart, arrivees_cumulees, departs_cumules, longueur_file), (moyenne_longueur_file, moyenne(temps_attente,1), moyenne(temps_sejour,1)))

#Chaque client arrivant dans le système va entrer dans la file la plus courte (choisie avec la fonction auxiliaire plus_courte_file)
def N_files_N_serveurs(temps_inter_arrivees,instant_arrivee,temps_service,nombre_de_serveurs,nombre_de_clients):
    def recherche_client_precedent(files,numero_file,client_servi):
        nombre_de_clients = len(files)
        i = client_servi -1
        while files[i][0] != numero_file and i >= 0:
            i -= 1
        if i == -1:
            return 0
        return i
    def maj_longueur_des_files(files_serveurs, t, nb_files):
        longueur_des_files = [0 for i in range(nb_files + 1)]
        for client in files_serveurs:
            if client[1] > t:
                longueur_des_files[client[0]] += 1
        return longueur_des_files
    def plus_courte_file(longueur_des_files):#renvoie le numéro de la file la plus courte
        numero_file = 0
        long = float("infinity")
        nombre_de_files = len(longueur_des_files)-1
        for fi in range(1,nombre_de_files+1):
            if longueur_des_files[fi] < long:
                numero_file = fi
                long = longueur_des_files[fi]
        return numero_file
    def partition_clients_par_file(files_serveurs,nb_files):#renvoie la liste dont l'élément de rang k est la liste des clients ayant pris la file k
        g = [[] for i in range(nb_files+1)]
        nb_clients = len(files_serveurs)-1
        for client in range(1,nb_clients+1):
            g[files_serveurs[client][0]].append(client)
        return(g)
    temps_attente = [0 for i in range(nombre_de_clients+1)]
    debut_service = [0 for i in range(nombre_de_clients+1)]
    fin_service = [[0, -1] for i in range(nombre_de_clients+1)]
    temps_sejour = [0 for i in range(nombre_de_clients+1)]
    longueur_des_files = [0 for i in range(nombre_de_serveurs+1)]#longueur_des_files[i] = longueur de la file i
    files_serveurs = [[0,0]]#files_serveurs[i] = [numéro de file prise par le client i,fin de service du client i]
    for client in range(1,nombre_de_clients+1):
        t = instant_arrivee[client][0]
        longueur_des_files = maj_longueur_des_files(files_serveurs, t, nombre_de_serveurs)
        numero_file = plus_courte_file(longueur_des_files)
        client_precedent = recherche_client_precedent(files_serveurs, numero_file, client)
        temps_attente[client] = max(temps_attente[client_precedent] + temps_service[client_precedent] - temps_inter_arrivees[client],0)#formule de Lindley
        fin_service[client][0] = instant_arrivee[client][0] + temps_attente[client] + temps_service[client]
        temps_sejour[client] = temps_attente[client] + temps_service[client]
        files_serveurs.append([numero_file, fin_service[client][0]])

    clients_par_files = partition_clients_par_file(files_serveurs, nombre_de_serveurs)#renvoie la liste dont l'élément de rang k est la liste des clients ayant pris la file k
    instant_arrivee_par_files = [[] for i in range(nombre_de_serveurs+1)]#instant_arrivee_par_files[fi] est la liste des instants d'arrivées des pris ayant pris la file fi
    temps_attente_par_files = [[] for i in range(nombre_de_serveurs+1)]#temps_attente_par_files[fi] = liste des temps d'attente des clients ayant pris la file fi
    fin_service_par_files = [[] for i in range(nombre_de_serveurs+1)]#fin_service_par_files[fi] = liste des instants de fin de service des clients ayant pris la file fi
    for fi in range(1,nombre_de_serveurs+1):
        for client in clients_par_files[fi]:#pour chaque client ayant pris la file fi
            instant_arrivee_par_files[fi].append(instant_arrivee[client])
            fin_service_par_files[fi].append(fin_service[client])
    instant_arrivee_depart_par_files = [[[0,0]] for i in range(nombre_de_serveurs+1)]#instant_arrivee_depart_par_files[fi] = liste des instant correspondant à une arrivée dans la file fi où à un départ du serveur fi
    arrivees_cumulees_par_files = [[] for i in range(nombre_de_serveurs+1)]#arrivees_cumulees_par_files[fi] = liste des arrivées cumulées dans la file fi
    departs_cumules_par_files = [[] for i in range(nombre_de_serveurs+1)]#departs_cumules_par_files[fi] = liste des départs cumulés du serveur fi
    longueur_file_par_files = [[] for i in range(nombre_de_serveurs+1)]#longueur_file_par_files[fi] = liste des longueurs successives de la file fi
    for fi in range(1,nombre_de_serveurs+1):
        instant_arrivee_depart_par_files[fi] = [[0,0]] + tri(instant_arrivee_par_files[fi]+fin_service_par_files[fi],0)
        if len(instant_arrivee_depart_par_files[fi]) > 1:
            arrivees_cumulees_par_files[fi].append(0)
            arrivees_cumulees_par_files[fi].append(0)
            longueur_file_par_files[fi].append(0)
            indice = 0
            for tp in instant_arrivee_depart_par_files[fi][1:]:
                indice += 1
                arrivees_cumulees_par_files[fi].append(arrivees_cumulees_par_files[fi][-1] + (1 + tp[1])/2)
                arrivees_cumulees_par_files[fi].append(arrivees_cumulees_par_files[fi][-1] + (1 - tp[1])/2)
                longueur_file_par_files[fi].append(longueur_file_par_files[fi][-1] + tp[1])
    instant_arrivee_depart_par_files0 = [sous_liste(instant_arrivee_depart_par_files[fi],0) for fi in range(nombre_de_serveurs+1)]
    instant_arrivee_depart = tri(instant_arrivee + fin_service[1:], 0)
    departs_cumules = [0 for i in range(2*nombre_de_clients+1)]
    longueur_file = [0 for i in range(2*nombre_de_clients+1)]
    for i in range(1,2*nombre_de_clients+1):
        departs_cumules[i] = departs_cumules[i-1] + (1 - instant_arrivee_depart[i][1])/2
        longueur_file[i] = longueur_file[i-1] + instant_arrivee_depart[i][1]

    #modification des listes pour améliorer les représentations graphiques
    instant_arrivee_depart = arrange_liste_abscisse(sous_liste(instant_arrivee_depart,0))
    departs_cumules = arrange_liste_ordonnee(departs_cumules)
    longueur_file = arrange_liste_ordonnee(longueur_file)
    return (instant_arrivee_depart, departs_cumules,longueur_file),(somme([moyenne_ponderee(sous_liste(instant_arrivee_depart_par_files[fi],0),longueur_file_par_files[fi]) for fi in range(1,nombre_de_serveurs+1)],0),moyenne(temps_attente,1),moyenne(temps_sejour,1)))

def affichage(taux_arrivee,taux_service,nombre_de_serveurs,nombre_de_clients):#affiche la représentation graphique des arrivées cumulées, des départs cumules et des longueurs des files en fonction du temps, pour un système à une file et N serveurs et un système à N files et N serveurs
    temps_inter_arrivees = [((-1)/taux_arrivee)*log(random()) for client in range(nombre_de_clients+1)]
    temps_inter_arrivees[0] = 0
    instant_arrivee = [[0,1] for client in range(nombre_de_clients+1)]
    instant_arrivee[0][1] = 0
    for client in range(1,nombre_de_clients+1):
        instant_arrivee[client][0] = instant_arrivee[client-1][0] + temps_inter_arrivees[client]
    temps_service = [((-1)/taux_service)*log(random()) for client in range(nombre_de_clients+1)]
    (temps0,arrivees_cumulees0,departs_cumules0,longueur_file0) = une_file_N_serveurs(instant_arrivee,temps_service,nombre_de_serveurs,nombre_de_clients)[0]
    (temps1,departs_cumules1,longueur_file1) = N_files_N_serveurs(temps_inter_arrivees,instant_arrivee,temps_service,nombre_de_serveurs,nombre_de_clients)[0]
    mat.plot(temps0,arrivees_cumulees0)
    mat.xlabel(r'Temps')
    mat.ylabel(r'Arrivées cumulées')
    mat.show()
    mat.plot(temps0,departs_cumules0,temps1,departs_cumules1)
    mat.xlabel(r'Temps')
    mat.ylabel(r'Départs cumulés')
    mat.show()
    mat.plot(temps0,longueur_file0,temps1,longueur_file1)
    mat.xlabel(r'Temps')
    mat.ylabel(r'Personnes en attente')
    mat.show()

#On fait varier le taux d'arrivée de "pas" à "taux_arrivees_max" avec un pas "pas", d'une part avec un taux de service qui vaut k1*taux_arrivee, d'autre part, taux_service = taux_arrivee + k2
#Cela permet d'en déduire les variations de E(Q∞) en fonction du taux d'arrivée
def resultats(nombre_de_serveurs,nombre_de_clients,taux_arrivee_max,pas,k1,k2):
    resultat = [[] for i in range(6)]
    nombre_iterations = int(taux_arrivee_max/pas)
    for taux_arrivee in range(1,nombre_iterations):
        taux_arrivees_0 =  taux_arrivee*pas
        temps_inter_arrivees = [(-1)/(taux_arrivees_0)*log(random()) for i in range(nombre_de_clients+1)]
        temps_inter_arrivees[0] = 0
        instant_arrivee = [[0,1] for i in range(nombre_de_clients+1)]
        instant_arrivee[0][1] = 0
        for client in range(1,nombre_de_clients+1):
            instant_arrivee[client][0] = instant_arrivee[client-1][0] + temps_inter_arrivees[client]
        temps_service1 = [(-1)/(k1*taux_arrivees_0)*log(random()) for client in range(nombre_de_clients+1)]
        temps_service2 = [(-1)/(taux_arrivees_0+k2)*log(random()) for client in range(nombre_de_clients+1)]

        l = [une_file_N_serveurs(instant_arrivee,temps_service1,nombre_de_serveurs,nombre_de_clients)[1],une_file_N_serveurs(instant_arrivee,temps_service2,nombre_de_serveurs,nombre_de_clients)[1]]
        for i in range(2):
            for j in range(3):
                resultat[3*i+j].append(l[i][j])

    x0 = [taux_arrivee*pas for taux_arrivee in range(1,nombre_iterations)]
    ylongueur_file_0 = [1/(k1-1) for taux_arrivee in range(1,nombre_iterations)]
    ylongueur_file_1 = [taux_arrivee*pas/(k2) for taux_arrivee in range(1,nombre_iterations)]
    mat.plot(x0,resultat[0],x0,ylongueur_file_0)
    mat.xlabel(r'λ')
    mat.ylabel(r'E(Q∞)')
    mat.show()
    mat.plot(x0,resultat[3],x0,ylongueur_file_1)
    mat.xlabel(r'λ')
    mat.ylabel(r'E(Q∞)')
    mat.show()
    print('valeurs moyenne de l\'espérance du temps d\'attente =', moyenne(resultat[1],0), moyenne(resultat[4],0))
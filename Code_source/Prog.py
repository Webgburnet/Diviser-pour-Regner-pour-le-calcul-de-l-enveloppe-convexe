import random
import timeit
import math
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['figure.dpi'] = 120

#Creation d'une liste de points à aleatoire
def points_aleatoires(n=2000, xmin=-1000, xmax=1000, ymin=-1000, ymax=1000):
    return [(random.randint(xmin, xmax), random.randint(ymin, ymax)) for _ in range(n)]

def Sauvegarde_liste_point_aleatoire(nomfichier,points):
    file = open(nomfichier, "w")
    t=len(points)
    file.write(str(t))
    for i in range (t):
        file.write("\n")
        file.write(str(points[i][0]))
        file.write(",") 
        file.write(str(points[i][1]))         
    file.close()

def lirePoints(nomfichier):
    L = []
    with open(nomfichier, 'r') as file:
        n = int(file.readline().rstrip())
        for line in file.readlines():
            x,y = line.rstrip().split(',')
            if (type(x)==int and type(y)==int):
                L.append((int(x),int(y)))
            else:
                L.append((float(x),float(y)))
    return L

#Affichae du nuage de points sans l'enveloppe convexe
def affichage (L,nomfichier):
    plt.figure()
    plt.scatter([x for x,y in L], [y for x,y in L])
    plt.xlabel("Axe X")
    plt.ylabel("Axe Y")
    plt.title("Affichage des points")
    labels = ['$P_{0}$'.format(i) for i in range(len(L))]
    for label, x, y in zip(labels, [p[0] for p in L], [p[1] for p in L]):
        plt.annotate(label, xy=(x, y),  va='bottom', ha='right', size='x-small', color='black')
    plt.grid(True)
    plt.savefig(nomfichier, format="svg")
    plt.show()

# Définitions des fonctions pour trier le nuage par un tri fusion : fusion_points et tri_fusion_points

# méthode récursive
def fusion_bis(L1, L2):
    if not L1:
        # si la liste L1 est vide on retourne directement L2
        return L2
    if not L2:
        # idem mais avec L2
        return L1
    if L1[0] <= L2[0]:
        return [L1[0]] + fusion_bis(L1[1:], L2)
    else:
        return [L2[0]] + fusion_bis(L1, L2[1:])

# méthode récursive de fusion de listes de points
def fusion_points(L1, L2):
    if not L1:
        # si la liste L1 est vide on retourne directement L2
        return L2
    if not L2:
        # idem mais avec L2
        return L1
    # on tri selon l'abscisse
    if L1[0][0] < L2[0][0]:
        return [L1[0]] + fusion_bis(L1[1:], L2)
    if L1[0][0] > L2[0][0]:
        return [L2[0]] + fusion_bis(L1, L2[1:])
    # cas en plus du fait qu'il faut ensuite trier selon l'ordonnée si il y a égalité
    if L1[0][1] <= L2[0][1]:
        return [L1[0]] + fusion_bis(L1[1:], L2)
    else:
        return [L2[0]] + fusion_bis(L1, L2[1:])
		
# tri fusion aves des points
def tri_fusion_points(L):
    """ Fonction qui prend en argument une liste L de points du plan
    et qui trie cette liste
    """
    n = len(L)
    if n <= 1:
        return L
    else:
        m = n // 2
        return fusion_points(tri_fusion_points(L[:m]), tri_fusion_points(L[m:]))

def tri_nuage(L):
    """ Renvoie la liste des points du nuage de points, triée par abscisse puis ordonnée croissante. """
    return tri_fusion_points(L)

def orientation(p, q ,r):
    """ Renvoie 1 si le triplet (P, Q, R) est en sens direct,
    0 si le triplet (P, Q, R) est un alignement,
    et -1 si le triplet (P, Q, R) est en sens indirect. """
    vecteur_pq = (q[0] - p[0], q[1] - p[1])  # vecteur PQ
    vecteur_pr = (r[0] - p[0], r[1] - p[1])  # vecteur PR
    determinant = vecteur_pq[0]*vecteur_pr[1] - vecteur_pq[1]*vecteur_pr[0]  # le déterminant des deux vecteurs
    if determinant > 0:
        return 1
    if determinant < 0:
        return -1
    return 0

# on défini une fonction pour afficher le nuage de points et son enveloppe convexe
def fonction_enveloppe_convexe(L_origin, debug=False):
    L = tri_nuage(L_origin)
    if debug:
        print(L_origin)
        print(L)
    # on va créer un tableau d'association entre les indices des deux listes
    association = {i: L_origin.index(L[i]) for i in range(len(L))}
    EnvSup = []
    EnvInf = []
    for i in range(len(L)):
        if debug:
            if len(EnvSup) >= 2:
                o = orientation(L[i], L[EnvSup[-1]], L[EnvSup[-2]])
                print('Sup : ' + str(o))
        while len(EnvSup) >= 2 and orientation(L[i], L[EnvSup[-1]], L[EnvSup[-2]]) <= 0:
            EnvSup.pop()
        EnvSup.append(i)
        if debug:
            if len(EnvInf) >= 2:
                o = orientation(L[EnvInf[-2]], L[EnvInf[-1]], L[i])
                print('Inf : ' + str(o))
        while len(EnvInf) >= 2 and orientation(L[EnvInf[-2]], L[EnvInf[-1]], L[i]) <= 0:
            EnvInf.pop()
        EnvInf.append(i)
        if debug:
            print(EnvSup, EnvInf)
    sommets = EnvInf[:-1] + EnvSup[::-1]
    # on convertit les indices
    return [association[i] for i in sommets]

#on définit la taille maximal de l'ensemble convexe
def taille_ensembles(L):
    t=len(L)
    return t

#on affiche l'ensembles des couples x et y de l'enveloppe convexe ainsi sue la postion dans le fichier +1
def affichage_couple_enveloppe(L,G):
    t=int(taille_ensembles(G))
    X=0
    Y=0
    P=[]
    Cx=[]
    Cy=[]
    for i in range (t):
        #print (i)
        position=G[i]
        X=L[position][0]
        Y=L[position][1]
        P.append(position)
        Cx.append(X)
        Cy.append(Y)
        #print (position,X,Y)
        print(f"Position dans le tableau : {position} ; avec pour coordonnee X={X} et Y={Y}")
    return P,Cx,Cy


# on défini une fonction pour afficher re nuage de points et son enveloppe convexe
def affiche_enveloppe(L, algorithme,nomfichier):
    """ Affiche l'enveloppe convexe du nuage de points selon l'algorithme sélectionné. """
    Enveloppe = algorithme(L)

    X = [L[i][0] for i in Enveloppe]
    X.append(L[Enveloppe[0]][0])
    Y = [L[i][1] for i in Enveloppe]
    Y.append(L[Enveloppe[0]][1])

    #plt.xlim((-1, 7))
    #plt.ylim((0, 5))
    plt.scatter([x for x,y in L], [y for x,y in L])
    plt.xlabel("Axe X")
    plt.ylabel("Axe Y")
    plt.title("Affichage de l'enveloppe")

    plt.plot(X, Y)

    labels = ['$P_{0}$'.format(i) for i in range(len(L))]
    for label, x, y in zip(labels, [p[0] for p in L], [p[1] for p in L]):
        plt.annotate(label, xy=(x, y),  va='bottom', ha='right', size='xx-small', color='black')
    plt.grid(True)
    plt.savefig(nomfichier, format="svg")
    plt.show()

def AffichagePropreFichier (nomfichier):
    L = lirePoints(nomfichier)
    nomfichier_nuage=nomfichier.replace('.txt','_nuage.svg')
    nomfichier_svg=nomfichier.replace('.txt','.svg')
    
    print(f"La liste des points est la suivantes pour le fichier {nomfichier} : \n",L)
    Grandeur_ensembles=fonction_enveloppe_convexe(L)
    print("Emplacement des points de l'enveloppe convexe dans le Tableau est\n",Grandeur_ensembles)
    
    print("Les coordonnées de chaqu'un des points de l'enveloppe convexe est")
    affichage_couple_enveloppe(L,Grandeur_ensembles)
    
    print("Le nombre de point de l'enveloppe convexe est de",taille_ensembles(Grandeur_ensembles))
    
    affichage(L,nomfichier_nuage)
    affiche_enveloppe(L, fonction_enveloppe_convexe,nomfichier_svg)


#Calcul du temps d'excution
def tempsExecution (L,algo):
    t = timeit.Timer(lambda:algo(L))
    l=t.timeit(1)
    return l

def complexite_temporelle(debug=False):
    
    print("Grace au jeu de donnée")
    ListeFichier=['data_a.txt','data0.txt','data_b.txt','data_c.txt','data1.txt','data_d.txt','data2.txt','data_e.txt','data_f.txt','data_.txt']
    l=len(ListeFichier)
    n=[]
    t=[]
    logx=[]
    racine=[]
    x=[]
    xlogx=[]
    x2=[]
    x3=[]

    for i in range(l):
        listePoint=lirePoints(ListeFichier[i])
        n.append(len(listePoint))
        """
        if(debug==True):
            logx.append(math.log(n[i]))
            racine.append(math.sqrt(n[i]))
            x.append(n[i])
            xlogx.append(n[i]*math.log(n[i]))
            x2.append((n[i])**2)
            x3.append((n[i])**3)
        #"""
        print(f"Taille de la lsite pour {ListeFichier[i]} :",n[i])
        print(f"Le temps d'execution pour {ListeFichier[i]} :")
        #%timeit -r 3 -n 10 fonction_enveloppe_convexe(listePoint)
        t.append(tempsExecution(listePoint,fonction_enveloppe_convexe))
        print(t[i])


    if debug==True :
        plt.figure()
        plt.xlabel("taille n")
        plt.ylabel("temps")
        plt.title("Courbes")

        plt.plot(n,t,'r',label="Courbes")
        plt.legend()
        plt.grid(True)
        plt.savefig("temps.png", format="png")
        plt.show()

        """
        plt.grid(True)
        plt.plot(n,logx,'b',label="log x")
        plt.legend()
        plt.savefig("logx.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n,racine,'g',label="racine²")
        plt.legend()
        plt.savefig("racine.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n,x,'c',label="x")
        plt.legend()
        plt.savefig("x.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n,xlogx,'m',label="x log x")
        plt.legend()
        plt.savefig("xlogx.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n,x2,'y',label="x^2")
        plt.legend()
        plt.savefig("x2.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n,x3,'k',label="x^3")
        plt.legend()
        plt.savefig("x3.png", format="png")
        plt.show()
        #"""

def complexite_temporelle_alea(m,debug=False):
    
    n2=[]
    t2=[]
    logx=[]
    racine=[]
    x=[]
    xlogx=[]
    x2=[]
    x3=[]
        
    for j in range(1,m+1):
        aleatoire=points_aleatoires(j)
        #print(aleatoire)
        n2.append(len(aleatoire))
       
        """
        logx.append(math.log(n2[j-1]))
        racine.append(math.sqrt(n2[j-1]))
        x.append(n2[j-1])
        xlogx.append(n2[j-1]*math.log(n2[j-1]))
        x2.append((n2[j-1])**2)
        x3.append((n2[j-1])**3)
        #""" 
        #print("Taille de la lsite pour :",n2[j-1])
        #print(f"Le temps d'execution pour {j-1} :")
        #%timeit -r 3 -n 10 fonction_enveloppe_convexe(aleatoire)
        t2.append(tempsExecution(aleatoire,fonction_enveloppe_convexe))
        #print(t2[j-1])
     
    if debug==True :
        plt.figure()
        plt.xlabel("taille n")
        plt.ylabel("temps")
        plt.title("Courbes")

        plt.plot(n2,t2,'r',label="Courbes")
        plt.legend()
        plt.grid(True)
        plt.savefig("temps.png", format="png")
        plt.show()

""" 
        plt.grid(True)
        plt.plot(n2,logx,'b',label="log x")
        plt.legend()
        plt.savefig("logx.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n2,racine,'g',label="racine²")
        plt.legend()
        plt.savefig("racine.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n2,x,'c',label="x")
        plt.legend()
        plt.savefig("x.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n2,xlogx,'m',label="x log x")
        plt.legend()
        plt.savefig("xlogx.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n2,x2,'y',label="x^2")
        plt.legend()
        plt.savefig("x2.png", format="png")
        plt.show()

        plt.grid(True)
        plt.plot(n2,x3,'k',label="x^3")
        plt.legend()
        plt.savefig("x3.png", format="png")
        plt.show()
 #"""

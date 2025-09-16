import numpy as np 
import matplotlib.pyplot as plt


#1
P = np.array( [[0.5,0.5,0],
               [0.5,0,0.5],
               [0,0.5,0.5]] )


n=50
P_n = np.linalg.matrix_power(P, n) # ou on peut faire une boucle est faire 50x np.dot(p,p)
print(P_n,'=P_n')

N=[1,1,1]  # pour le trouver on fait pi*P = pi avec pi la mesure de proba invariante

print("mesure invariante théorique : ", N)
print("mesure de proba invariante théorique :", [ N[i]/sum(N) for i in range(len(N)) ] ) # pour le trouver on fait pi*P = pi avec la condition que la somme des élément de pi =1 se qui revient a diviser la mesure invariante par sa somme cummulées
print("mesure de proba invariante numerique :", P_n[0])  # On regarde la convergence de P_n quand P est grand

#2

def processus(x,n):
    X = [0 for k in range(3)]  # On initialise un vecteur remplie de 0
    X[x] = 1       # On définie notre loi initiale X0
    traj = [x]    # On définit un vecteur qui représente notre marche 
    for k in range(n):
        Xsuivant = np.dot(X,P)  # On calcule Xk+1
        somme = np.cumsum(Xsuivant) #On calcule la somme cummulée de notre vecteur Xk+1
        u = np.random.random()  # on tire une uniforme entre 0 et 1
        i=0
        while somme[i]<u: #tant que l'uniforme est supérieur a la somme cummulée en rajoute +1 à i
            i=i+1
        X = [0 for k in range(3)]   # on réinitialise X 
        X[i] = 1            # on ajoute 1 à l'indice où notre uniforme est tombé
        traj.append(i)      # on ajoute  notre Xk+1 à la trajectoire
    return traj

print(processus(2,10))

#3  

for x in range(3):  # On fait une boucle pour la réalisation de la trajectoire pour chaque sommet de départ
    X = processus(x,50)
    plt.step([k for k in range(len(X))],X,label=f'Marche de X_n pour X0={x}') # On trace notre marche aléatoire avec comme sommet de épart x

plt.ylabel('Etat de la chaine')  #on nomme juste l'axe x, y et la légend et on l'affiche
plt.xlabel('n')
plt.legend()
plt.show()


#4

n = 10000
X = processus(1, n)  # On génere une marche aléatoire commencant du sommet 1 (remarque: le choix du sommet ne change rien à la fréquence )
plt.bar([0,1,2],[X.count(x)/n for x in range(3)], width=0.3 ,label=f'Trajectoire de X_n pour n = {n}') # on utilise la fct plt.bar car la fct plt.hist n'affiche pas bien les densité

N = [2,2,2]
pi = [ N[i]/sum(N) for i in range(len(N)) ]
plt.plot(pi,'o', color='r',label='densité de la proba invariante')   # On fait juste de l'affichage
plt.xlabel("Les chaines de transition")
plt.ylabel("probabilitÈ")
plt.legend()
plt.show()


#5
def markov_gen(x): 
    X0 = [0 for k in range(3)] # On initialise un vecteur remplie de 0
    X0[x] = 1        # On définie notre loi initiale X0
    X1 = np.dot(X0,P)  # On multiple X0 par la matrice de transition P pour avoir X1
    somme = np.cumsum(X1) # On calcule la somme cummulée de notre vecteur X1
    u = np.random.random()  # On tire une v.a uniforme sur [0,1]
    i=0 
    while somme[i]<u:   
        i=i+1
    return i     # On retourne l'indice représentant l'intervalle où est tombé notre uniforme qui représente l'état à laquel se trouve la CM



def T(x,y):
    i = 0  #pas
    while x != y :
        x = markov_gen(x)
        y = markov_gen(y)
        i+=1
    return i

#Nombre d'échantillon à simuler
R = 1000


#On fixe d(x,y) = (0,2)

x,y = 0,2

T2 = [T(x,y) for _ in range(R)]


moyempi = sum(T2)/R
plt.axvline(moyempi,  color='r', label=f'moy empirique = {moyempi}')   # On fait juste de l'affichage
plt.xlabel("T")
plt.ylabel("Frequence d'apparation")
plt.legend()

plt.hist( T2, bins = [-0.5+k/2 for k in range(2*max(T2)+1 )],label=f'(x,y) = ({x},{y})' )
print(f'pour (x,y) = ({x},{y})')
print("proba que T = 1 numériquement :",T2.count(1)/R , 'alors que la proba théorique = ',1/4) #On trouve la proba theorique 1-4 car l'ona qu'une possibilité d'avoir T=1 c'est a dire de faire 1/2*1/2
print("proba que T = 2 numériquement :",T2.count(2)/R ,'alors que la proba théorique = ',3/16)
plt.show()


#6

# on a une chaine de markov car la proba de passage entre 2 instant ne dépend pas du passser


def couplage_annexe(x, y, z, t, P):  # On écrit la matrice de transition de Q
    if x != y and z == t:
        return P[x, z] * P[y, t]
    elif x == y and z == t:
        return P[x, z]
    else:
        return 0

def couplage(x, y, n, P):
    x_trajectoire = [x]
    y_trajectoire = [y]
    for _ in range(n):
        A = [(i, j) for i in range(len(P)) for j in range(len(P))]   # Effectuer une transition de la chaîne de Markov pour chaque trajectoire
        B = [couplage_annexe(x, y, z, t, P) for (z, t) in A]
        B =B/np.sum(B)  # Normaliser les probabilités de transition
        C = np.random.choice(range(len(A)), p=B)    # On choisie une transition en utilisant les probabilités calculées 
        (x_next, y_next) =A[C]
        x_trajectoire.append(x_next)   # On ajoute les états suivants aux trajectoires
        y_trajectoire.append(y_next)
        x = x_next # On modifie les états actuels
        y = y_next

    return x_trajectoire, y_trajectoire

# Matrice de transition P
P = np.array([[0.5, 0.5, 0],
              [0.5, 0, 0.5],
              [0, 0.5, 0.5]])

#on définie les états initiaux x et y
x_initial = 0
y_initial = 1

# Nombre d'itérations
n = 10

# on definie les trajectoires couplées
x_trajectoire , y_trajectoire = couplage(x_initial, y_initial, n, P)

# On trace les trajectoires couplées
plt.step([k for k in range(len(x_trajectoire))],x_trajectoire, label='Trajectoire X')
plt.step([k for k in range(len(y_trajectoire))],y_trajectoire, label='Trajectoire Y')
plt.xlabel('n')
plt.ylabel('États')
plt.title('Couplage de deux trajectoires de la chaîne de Markov')
plt.legend()
plt.show()

# Je ne comprend pas pourquoi sa affiche que la trajectoire de y


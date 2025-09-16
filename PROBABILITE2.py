import numpy as np
import matplotlib.pyplot as plt
import random


#%% Exercice 2.1

#1
P = np.array( [[0,0.5,0,0.5,0,0],
               [0.25,0,0,0.25,0.25,0.25],
               [0,0,0,0,0,1],
               [0.5,0.5,0,0,0,0],
               [0,0.5,0,0,0,0.5],
               [0,1/3,1/3,0,1/3,0]] )

#2

def markov_gen(x): 
    X0 = [0 for k in range(6)] # On initialise un vecteur remplie de 0
    X0[x] = 1        # On définie notre loi initiale X0
    X1 = np.dot(X0,P)  # On multiple X0 par la matrice de transition P pour avoir X1
    somme = np.cumsum(X1) # On calcule la somme cummulée de notre vecteur X1
    u = random.random()  # On tire une v.a uniforme sur [0,1]
    i=0 
    while somme[i]<u:   
        i=i+1
    return i     # On retourne l'indice représentant l'intervalle où est tombé notre uniforme qui représente l'état à laquel se trouve la CM


#3

def markov(x,n):
    X = [0 for k in range(6)]
    X[x] = 1       # On définie notre loi initiale X0
    traj = [x]   # On définit un vecteur qui représente notre marche 
    for k in range(n):
        X = [0 for k in range(6)]
        X[markov_gen(traj[k])] = 1  # On applique la fonction markov_gen à l'étape ou l'on est pour trouver l'étape suivant de notre marche aléatoire
        traj.append(markov_gen(traj[k])) # on rajoute l'état trouver dans le vecteur représentant notre marche
    return traj

print(markov(2,10))


#4

X = markov(0,50)
plt.step([k for k in range(len(X))],X,label='Marche de X_n')

plt.ylabel('Etat de la chaÓne')

plt.xlabel('n')

plt.legend()
plt.show()

#5)

n = 10000

X = markov(0, n)


plt.hist(X,density=True,bins=[-0.5+k for k in range(7)],label=f'Trajectoire de X_n pour n = {n}')

N = [2,4,1,2,2,3]
pi = [ N[i]/sum(N) for i in range(len(N)) ]

plt.plot(pi,'o',color='r',label='densitÈ de la proba invariante')
plt.xlabel("Les chaÓnes de transition")
plt.ylabel("probabilitÈ")
plt.legend()
plt.show()

#6 et 7)

ech = 10000
Retour = []
moy=[]
for k in range(6): # on fait une boucle pour chaque X0=k
    X = markov(k, ech)   #On simule une marche aléatoire de longeur ech commencant de k
    i=0
    while i< len(X):    # on fait tourner le programme en sorte de parcourir tout la marche aléatoire
        if X[i] == k:   # si commencant de l'état k l'état où l'on se trouve est l'état k alors on à un premier temps de retour
            compte = 1  # on réinitialise le compteur à chaque fois qu'on passe par k
            i=i+1
        while  i<len(X) and X[i] != k:
            compte += 1
            i=i+1
        moy.append(compte)
    Retour.append(moy[:-1])
    moy = []
    

for k in range(6):
    moy = sum( Retour[k] )/len(Retour[k])
    plt.title(f'Temps de retour en {k}')
    plt.hist(Retour[k],bins=[-0.25+k/2 for k in range(2*max(Retour[k])+1)] )
    plt.xlabel("Temps de retour")
    plt.ylabel(f'Nbr dÈchantillon pour n = {ech}')
    plt.axvline(x=moy,color='r',label=f'Esperence num temps de retour en {k}' )
    plt.axvline(x=1/pi[k],color='g',label=f'Esperence théorique du tps de retour en {k}')
    plt.legend()
    plt.show()


#%% Exercice 2.2
#1)
    
def ehrenfest_gen(N,x):
    
    if np.random.binomial(1, x/N) == 1:  #Si je tire une molécule à gauche
        return x-1
    else:
        return x+1
        
    
#2)

def ehrenfest(N,x,n):
    X = [x]
    for k in range(n):
        x = ehrenfest_gen(N, x)
        X.append(x)
    return X

#3)

N=10
for x in [2,5,7]:
    X = ehrenfest(N,x,50)
    plt.step([k for k in range(len(X))],X,label=f'x ={x}')

plt.title(f'N = {N}')
plt.ylabel('Etat de la chaine')

plt.xlabel('n')

plt.legend()
plt.show()


#4)



n = 1000
x=3
    
X = ehrenfest(N,x,n)
plt.hist(X,density=True,bins=[-0.5+k for k in range(N+1)],label=f'Trajectoire de X_n pour n = {n}')
plt.title(f'x = {x} pour N = {N}')
plt.xlabel("Les chaines de transition")
plt.ylabel("probabilite ")
plt.legend()
plt.show()

    



    

    



    
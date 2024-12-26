# G = {
#     1: {6: 5},
#     2: {1: 3, 4: 10, 5: 3, 6: 11},
#     3: {2: 1, 4: 7},
#     4: {},
#     5: {4: 4},
#     6: {1: 1},
#     7: {1: 5, 5: 4}
# }

def shortest_path(G, sd, sa):
    d = {}
    parent = {}

    def w(u, v):
        return G[u][v]

    def relachement(u, v):
        if d[v] > d[u] + w(u, v):
            d[v] = d[u] + w(u, v)
            parent[v] = u

    def extraire(F):
        u = F[0]
        for n in F:
            if d[n]<d[u]:
                u=n 
        F.remove(u)
        return u

    def initialisation(G, r):
        for u in G.keys():
            d[u] = float("inf")
            parent[u] = None
        d[r] = 0
        F = list(G) #G.keys()
        return F

    def dijekstra(G, r):
        F = initialisation(G, r)
        
        while len(F) > 0: # F non vide
            u = extraire(F) # Extraire de F le sommet u ayant le plus pertit d[.]
            for v in G[u].keys():
                relachement(u, v)

        return d, parent

    d, parent = dijekstra(G, sd)
    # print("d:", d)
    # print("parent:", parent)

    def plus_court_chemin(sd, sa): # sd: sommet départ, sa: sommet arrivé
        if d[sa] == float('inf') or parent[sa] is None:
            return []  # Pas de chemin possible
        
        path = []
        current = sa
        
        while current is not None:
            path.append(current)
            current = parent[current]
            
        if path[-1] != sd:
            return []  # Le point de départ n'est pas atteint
        
        return path[::-1]  # Retourne le chemin dans le bon ordre

    path = plus_court_chemin(sd, sa)
    return path
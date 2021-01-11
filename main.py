import argparse
import random

from src.aco.ant_colony import AntColonyOptimizer
from src.model.city import City
from src.model.network import Network

import datetime


def load_data():
    import xml.etree.ElementTree as ET
    root = ET.parse('data/janos-us--D-D-M-N-S-A-N-S/janos-us.xml').getroot()
    prefix = "{http://sndlib.zib.de/network}"
    city_name = ""
    city_list = []
    index_to_name = dict()
    adjacency_dict = dict()
    index = 0
    for type_tag in root.findall(f"{prefix}networkStructure/{prefix}links/{prefix}link"):
        source = type_tag.find(f"{prefix}source").text
        if source != city_name:
            index_to_name[index] = source
            city_name = source
            index += 1

    city_name = "Seattle"
    index = 0
    for type_tag in root.findall(f"{prefix}networkStructure/{prefix}links/{prefix}link"):
        source = type_tag.find(f"{prefix}source").text
        target = type_tag.find(f"{prefix}target").text
        cost = type_tag.find(f"{prefix}additionalModules/{prefix}addModule/{prefix}cost").text
        if source != city_name:
            city_list.append(City(index, city_name, adjacency_dict))
            adjacency_dict = dict()
            index += 1
            city_name = source
        adjacency_dict[next(key for key, value in index_to_name.items() if value == target)] = cost
    city_list.append(City(index, city_name, adjacency_dict))
    return Network(city_list), index_to_name


# def run_aco(start_city, finish_city, n_paths):
#     problem, index_to_name = load_data()
#     optimizer = AntColonyOptimizer(n_ants=15, rho=.05, pheromone_unit=300, best_route_p=0.2, elitist_weight=1,
#                                    distance_preference_factor=1)
#
#     start = next(key for key, value in index_to_name.items() if value == start_city)
#     finish = next(key for key, value in index_to_name.items() if value == finish_city)
#     best_distances, best_paths = optimizer.fit(problem, start, finish, iterations=20, n_paths=n_paths)
#     print("PATH ACO: ")
#     for i, path in enumerate(best_paths):
#         # print("PATH ACO: ")
#         # for city in path:
#         #     print(index_to_name[city])
#         print(best_distances[i])

def run_aco(arguments: vars):
    problem, index_to_name = load_data()
                                                            #n_ants = liczba mrowek
                                                            # rho = o ile feromony beda wyparowywac co iteracje
                                                            # pheromone unit = bazowa wartosc domyslna feromonow dla kazdej trasy
                                                            # best_route_p = prawdopodobienstwo tego ze z roboczego miasta przejdziemy do nastepnego miasta ktore jest na razie najlepsze
                                                            # elitist_weight = ile najlepsza trasa w iteracji danej bedzie zwiekszona feromonami
                                                            # distance_preference_factor = dzielone jest przez odleglosc do danego miasta, chyba moze byc jakiekolwiek, nie bedize mialo to znaczenia
    optimizer = AntColonyOptimizer(n_ants=arguments['ants'], rho=arguments['rho'], pheromone_unit=arguments['pheromone'], best_route_p=arguments['best'], elitist_weight=arguments['elitist'],
                                   distance_preference_factor=100)
    start = next(key for key, value in index_to_name.items() if value == arguments['starting'])
    finish = next(key for key, value in index_to_name.items() if value == arguments['finishing'])
    best_distances, best_paths,time = optimizer.fit(problem, start, finish, iterations=arguments['iterations'], n_paths=arguments['npaths'])

    print("\nACO ZNALAZL: " + str(min(len(best_distances),arguments['npaths'])) + " SCIEZEK")
    for i, path in enumerate(best_paths):
        print(f"{i+1}. PATH ACO: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tDLUGOSC TRASY = {best_distances[i]}")

    return time

#
# def run_dfs(start_city, finish_city, n_paths):
#     network, index_to_name = load_data()
#     start = next(key for key, value in index_to_name.items() if value == start_city)
#     finish = next(key for key, value in index_to_name.items() if value == finish_city)
#     best_distances, best_paths = network.dfs_solve(start, finish, n_routes=n_paths)
#     print("PATHDFS: ")
#     for i, path in enumerate(best_paths):
#         # print("PATHDFS: ")
#         # for city in path:
#         #     print(index_to_name[city])
#         print(best_distances[i])

def run_dfs(start_city, finish_city, n_paths):
    network, index_to_name = load_data()
    start = next(key for key, value in index_to_name.items() if value == start_city)
    finish = next(key for key, value in index_to_name.items() if value == finish_city)
    best_distances, best_paths = network.dfs_solve(start, finish, n_routes=n_paths)
    print("\nDFS ZNALAZL " + str(len(best_distances)) + " SCIEZEK")
    for i, path in enumerate(best_paths):
        print(f"{i+1}. PATH DFS: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tDLUGOSC TRASY = {best_distances[i]}")


    return best_paths[0], best_distances[0]

# Iteracje	RHO	    Feromony	P_najlepszej_sciezki	polepszanie najlepszej	roznica_srednia
#       20  0.17	    200	                     0.17	                    1	            1.27


def benchmark():
    #losujemy 10 roznych polaczen
    problem, index_to_name = load_data()
    pairs = set()
    while len(pairs) < 20:
        a=random.randint(0,len(index_to_name)-1)
        b=random.randint(0,len(index_to_name)-1)
        while b is a:
            b=random.randint(0,len(index_to_name)-1)
        pairs.add((a,b))
    best_routes = []
    aco_routes = []
    #wykonaj dla kazdego dfs zeby miec porownanie
    for a,b in pairs:
        pat,dis = run_dfs(index_to_name[a],index_to_name[b],5)
        best_routes.append(dis)
    #     pat,dis = run_aco(index_to_name[a],index_to_name[b],15)
    #     aco_routes.append(dis)
    #takie znaleziono najlepsze:
    for i,(a,b) in enumerate(pairs):
        print(index_to_name[a] + " -> " + index_to_name[b] + " dlugosc: "+ str(best_routes[i]))
    # print("\nDFS\t\tACO\t\tROZNICA")
    # for i in range(len(best_routes)):
    #     print(str(best_routes[i]))
    # print("\tACO:")
    # for rout in aco_routes:
    #     print(rout)


    bench_rho_value = [0.05,0.08,0.11,0.14,0.17,0.20]         #6
    bench_pherom_count = [100,150,200]              #3
    bench_best_route_p = [0.05,0.08,0.11,0.14,0.17,0.20]      #6
    bench_elitist = [1.00,1.05,1.10,1.15]                #4
    bench_iters = [10,20]                           #2      #lacznie 288

    print("TAKIE SA MIASTA:\n")
    for a,b in pairs:
        print(str(index_to_name[a])+" -> " + str(index_to_name[b]))


    bench_results_file = open("resultsadv.txt", 'a')
    bench_results_file.write("\nIteracje\tRHO\tFeromony\tP_najlepszej_sciezki\tpolepszanie najlepszej\troznica_srednia\n")
    bench_results_file.close()

                                    #2
    for rho_v in bench_rho_value:                           #6
        # curr_best = float("inf")
        settings = ""
        for pherom_c in bench_pherom_count:                 #3
            for route_p in bench_best_route_p:              #6
                for elits in bench_elitist:                 #4
                    differences = dict()
                    for i,(a,b) in enumerate(pairs):        #20
                        tmp = 0.0
                        for repeat in range(10):             #5
                            pat,dis = run_aco(index_to_name[a],index_to_name[b],5,15,rho_v,pherom_c,route_p,elits,100)
                            tmp += dis-best_routes[i]
                        differences[i]=tmp/10                        #jaka srednio wychodzi roznica miedzy najlpeszym

                    average = sum(differences.values())/len(differences.values())
                    # print(str(average))
                    settings = f'20\t{rho_v}\t{pherom_c}\t{route_p}\t{elits}\t{average}\n'
                    bench_results_file = open("resultsadv.txt", 'a')
                    bench_results_file.write(settings)
                    bench_results_file.close()



def parse_args() -> vars:
    ap = argparse.ArgumentParser()
    ap.add_argument('-r',"--rho",default=0.17, type=float,help="Value of Rho evaporation rate")
    ap.add_argument('-a', "--ants",default=20, type=int,help="number of ants working")
    ap.add_argument('-p','--pheromone',default=200, type=int, help="Number of pheromones left by each ant")
    ap.add_argument('-e','--elitist', default=1.0 ,type=float,help='improvement of best path yet')
    ap.add_argument('-s','--starting' ,type=str,help="starting city",required=True)
    ap.add_argument('-f','--finishing',type=str,help="finishing city",required=True)
    ap.add_argument('-i','--iterations',default=20,type=int,help='Number of iterations')
    ap.add_argument('-b', '--best',default=0.17,type=float,help='probabilty of choosing best existing path each iteration')
    ap.add_argument('-n', '--npaths',default=5,type=int,help="number of paths to be found")
    args = vars(ap.parse_args())
    return args




if __name__ == '__main__':
    arguments = parse_args()
    # benchmark()
    # print(arguments['ants'])
    a = datetime.datetime.now()
    run_dfs(arguments['starting'],arguments['finishing'],arguments['npaths'])
    b = datetime.datetime.now()
    delta = b - a
    time=run_aco(arguments)

    # print(f" aco: {time} ms")
    print(f"DFS duration =  {int(delta.total_seconds()*1000)} ms")
    print(f"ACO duration  = {time} ms")
    # print(network.graph)

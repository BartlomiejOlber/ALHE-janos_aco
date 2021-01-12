import argparse
import random

import numpy as np

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
    index_to_name   = dict()
    adjacency_dict  = dict()
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
        source  = type_tag.find(f"{prefix}source").text
        target  = type_tag.find(f"{prefix}target").text
        cost    = type_tag.find(f"{prefix}additionalModules/{prefix}addModule/{prefix}cost").text
        if source != city_name:
            city_list.append(City(index, city_name, adjacency_dict))
            adjacency_dict = dict()
            index += 1
            city_name = source
        adjacency_dict[next(key for key, value in index_to_name.items() if value == target)] = cost
    city_list.append(City(index, city_name, adjacency_dict))
    return Network(city_list), index_to_name

def run_aco(arguments: vars):
    problem, index_to_name = load_data()
                                                            #n_ants = liczba mrowek
                                                            # rho = o ile feromony beda wyparowywac co iteracje
                                                            # pheromone unit = bazowa wartosc domyslna feromonow dla kazdej trasy
                                                            # best_route_p = prawdopodobienstwo tego ze z roboczego miasta przejdziemy do nastepnego miasta ktore jest na razie najlepsze
                                                            # elitist_weight = ile najlepsza trasa w iteracji danej bedzie zwiekszona feromonami
                                                            # distance_preference_factor = dzielone jest przez odleglosc do danego miasta, chyba moze byc jakiekolwiek, nie bedize mialo to znaczenia
    optimizer = AntColonyOptimizer(n_ants=arguments['ants'], rho=arguments['rho'], pheromone_unit=arguments['pheromone'], elitist_weight=arguments['elitist'],
                                   distance_preference_factor=100)
    start   = next(key for key, value in index_to_name.items() if value == arguments['starting'])
    finish  = next(key for key, value in index_to_name.items() if value == arguments['finishing'])
    best_distances, best_paths,time = optimizer.fit(problem, start, finish, iterations=arguments['iterations'], n_paths=arguments['npaths'])

    print("\n\t\t\tACO ZNALAZL: " + str(min(len(best_distances),arguments['npaths'])) + " SCIEZEK")
    for i, path in enumerate(best_paths):
        print(f"{i+1}. PATH ACO: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tDLUGOSC TRASY = {best_distances[i]}")

    return time, best_distances

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
    start   = next(key for key, value in index_to_name.items() if value == start_city)
    finish  = next(key for key, value in index_to_name.items() if value == finish_city)
    best_distances, best_paths = network.dfs_solve(start, finish, n_routes=n_paths)

    print("\n\t\t\tDFS ZNALAZL " + str(len(best_distances)) + " SCIEZEK")
    for i, path in enumerate(best_paths):
        print(f"{i+1}. PATH DFS: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tDLUGOSC TRASY = {best_distances[i]}")
    return best_distances

def benchmark(arguments: vars):
        #losujemy 20 roznych polaczen
    problem, index_to_name = load_data()
    pairs = set()
    while len(pairs) < 20:
        a=random.randint(0,len(index_to_name)-1)
        b=random.randint(0,len(index_to_name)-1)
        while b is a:
            b=random.randint(0,len(index_to_name)-1)
        pairs.add((a,b))

    best_routes = []
        #wykonaj dla kazdego dfs zeby miec porownanie
    for a,b in pairs:
        dis = run_dfs(index_to_name[a],index_to_name[b],5)
        best_routes.append(dis)

        #takie znaleziono najlepsze:
    for i,(a,b) in enumerate(pairs):
        print(index_to_name[a] + " -> " + index_to_name[b] + " dlugosc: "+ str(best_routes[i]))


    bench_rho_value = np.arange(0.05,0.20,0.02)
    bench_pherom_count = np.arange(50,300,50)
    bench_elitist = np.arange(1,5,0.3)

    print("TAKIE SA MIASTA:\n")
    for a,b in pairs:
        print(str(index_to_name[a])+" -> " + str(index_to_name[b]))


    bench_results_file = open("results.txt", 'a')
    bench_results_file.write("Mrowki\tIteracje\tRHO\tFeromony\tpolepszanie najlepszej\troznica_srednia\n")
    bench_results_file.close()
    curr_best = float("inf")
    best_settings = ""
    for rho_v in bench_rho_value:                           #6
        settings = ""
        for pherom_c in bench_pherom_count:                 #3
            for elits in bench_elitist:              #6
                arguments['rho']=rho_v
                arguments['pheromone']=pherom_c
                arguments['elitist']=elits
                differences = dict()
                for i,(a,b) in enumerate(pairs):        #20
                    tmp = 0.0
                    for repeat in range(10):             #5
                        time,dis = run_aco(arguments)
                        tmp += dis[min(4,len(dis)-1)]-best_routes[i][min(4,len(dis)-1)]
                    differences[i]=tmp/10                        #jaka srednio wychodzi roznica

                average = sum(differences.values())/len(differences.values())
                # print(str(average))
                if(average<curr_best):
                    curr_best=average
                settings = f'15\t15\t{rho_v}\t{pherom_c}\t{elits}\t{average}\n'
                if (average < curr_best):
                    curr_best = average
                    best_settings=settings
                bench_results_file = open("results.txt", 'a')
                bench_results_file.write(settings)
                bench_results_file.close()
    print(f'\n\nBest settings = {best_settings}')



def parse_args() -> vars:
    ap = argparse.ArgumentParser()
    ap.add_argument('-r',"--rho",default=0.13, type=float,help="Value of Rho evaporation rate")
    ap.add_argument('-a', "--ants",default=15, type=int,help="number of ants working")
    ap.add_argument('-p','--pheromone',default=200, type=int, help="Number of pheromones left by each ant")
    ap.add_argument('-e','--elitist', default=4.6 ,type=float,help='improvement of best path yet')
    ap.add_argument('-s','--starting' ,type=str,default="Seattle",help="starting city")
    ap.add_argument('-f','--finishing',type=str,default='NewYork' ,help="finishing city")
    ap.add_argument('-i','--iterations',default=15,type=int,help='Number of iterations')
    ap.add_argument('-n', '--npaths',default=5,type=int,help="number of paths to be found")
    args = vars(ap.parse_args())
    return args




if __name__ == '__main__':
    arguments = parse_args()

        #tryb benchmark
    # benchmark(arguments)

        #tryb normalny
    a = datetime.datetime.now()
    dfs_dis = run_dfs(arguments['starting'],arguments['finishing'],arguments['npaths'])
    # print(dfs_dis)
    b = datetime.datetime.now()
    delta = b - a
    time,aco_dist=run_aco(arguments)
    # print(aco_dist)

    # print(f" aco: {time} ms")
    print(f"\n\nDFS duration =  {int(delta.total_seconds()*1000)} ms")
    print(f"ACO duration  = {time} ms")
    print(f'Path length difference: {aco_dist[0]-dfs_dis[0]}')



from src.util import load_data, parse_args
from main import run_dfs, run_aco
import datetime
import random
import numpy as np


def speed_test():
    arguments = parse_args()
    pairs = []
    problem, index_to_name = load_data()
    for i in range(100):
        a = random.randint(0, len(index_to_name) - 1)
        b = random.randint(0, len(index_to_name) - 1)
        while b is a:
            b = random.randint(0, len(index_to_name) - 1)
        pairs.append((a, b))
    bench_results_file = open("results.txt", 'w')
    for ants in range(1, 30):
        for iters in range(1, 30):
            dfs_faster = 0
            aco_faster = 0
            aco_worse_best = 0
            aco_worse_nth = 0
            for pair in pairs:
                arguments['starting'] = index_to_name[pair[0]]
                arguments['finishing'] = index_to_name[pair[1]]
                arguments['ants'] = ants
                arguments['iterations'] = iters
                a = datetime.datetime.now()
                dfs_dis = run_dfs(arguments['starting'], arguments['finishing'], arguments['npaths'])
                b = datetime.datetime.now()
                delta = b - a
                time, aco_dist = run_aco(arguments)
                if not aco_dist or int(aco_dist[0] - dfs_dis[0]) > 0:
                    aco_worse_best += 1
                if not aco_dist or int(aco_dist[-1] - dfs_dis[len(aco_dist) - 1]) > 0:
                    aco_worse_nth += 1
                if int(delta.total_seconds() * 1000) > int(time):
                    aco_faster += 1
                else:
                    dfs_faster += 1

            bench_results_file.write(f"ants: {ants} iters: {iters} \n")
            bench_results_file.write(f" acobestworse: {aco_worse_best}")
            bench_results_file.write(f" aconthworse: {aco_worse_nth}")
            bench_results_file.write(f" acofaster: {aco_faster}")
            bench_results_file.write(f" dfsfaster: {dfs_faster} \n")
    bench_results_file.close()


def benchmark(arguments: vars):
    # losujemy 20 roznych polaczen
    problem, index_to_name = load_data()
    pairs = set()
    while len(pairs) < 20:
        a = random.randint(0, len(index_to_name) - 1)
        b = random.randint(0, len(index_to_name) - 1)
        while b is a:
            b = random.randint(0, len(index_to_name) - 1)
        pairs.add((a, b))

    best_routes = []
    # wykonaj dla kazdego dfs zeby miec porownanie
    for a, b in pairs:
        dis = run_dfs(index_to_name[a], index_to_name[b], 5)
        best_routes.append(dis)

        # takie znaleziono najlepsze:
    for i, (a, b) in enumerate(pairs):
        print(index_to_name[a] + " -> " + index_to_name[b] + " dlugosc: " + str(best_routes[i]))

    bench_rho_value = np.arange(0.05, 0.20, 0.02)
    bench_pherom_count = np.arange(50, 300, 50)
    bench_elitist = np.arange(1, 5, 0.3)

    print("TAKIE SA MIASTA:\n")
    for a, b in pairs:
        print(str(index_to_name[a]) + " -> " + str(index_to_name[b]))

    bench_results_file = open("results.txt", 'a')
    bench_results_file.write("Mrowki\tIteracje\tRHO\tFeromony\tpolepszanie najlepszej\troznica_srednia\n")
    bench_results_file.close()
    curr_best = float("inf")
    best_settings = ""
    for rho_v in bench_rho_value:  # 6
        settings = ""
        for pherom_c in bench_pherom_count:  # 3
            for elits in bench_elitist:  # 6
                arguments['rho'] = rho_v
                arguments['pheromone'] = pherom_c
                arguments['elitist'] = elits
                differences = dict()
                for i, (a, b) in enumerate(pairs):  # 20
                    tmp = 0.0
                    for repeat in range(10):  # 5
                        time, dis = run_aco(arguments)
                        tmp += dis[min(4, len(dis) - 1)] - best_routes[i][min(4, len(dis) - 1)]
                    differences[i] = tmp / 10  # jaka srednio wychodzi roznica

                average = sum(differences.values()) / len(differences.values())
                # print(str(average))
                if (average < curr_best):
                    curr_best = average
                settings = f'15\t15\t{rho_v}\t{pherom_c}\t{elits}\t{average}\n'
                if (average < curr_best):
                    curr_best = average
                    best_settings = settings
                bench_results_file = open("results.txt", 'a')
                bench_results_file.write(settings)
                bench_results_file.close()
    print(f'\n\nBest settings = {best_settings}')

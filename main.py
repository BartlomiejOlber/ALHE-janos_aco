import datetime

from src.util import load_data, parse_args
from src.ant_colony import AntColonyOptimizer


def run_aco(arguments: vars):
    problem, index_to_name = load_data()
    optimizer = AntColonyOptimizer(n_ants=arguments['ants'], rho=arguments['rho'],
                                   pheromone_unit=arguments['pheromone'], elitist_weight=arguments['elitist'],
                                   distance_preference_factor=100)
    start = next(key for key, value in index_to_name.items() if value == arguments['starting'])
    finish = next(key for key, value in index_to_name.items() if value == arguments['finishing'])
    best_distances, best_paths, time = optimizer.fit(problem, start, finish, iterations=arguments['iterations'],
                                                     n_paths=arguments['npaths'])

    for i, path in enumerate(best_paths):
        print(f"{i + 1}. PATH ACO: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tLength = {best_distances[i]}")
    return time, best_distances


def run_dfs(start_city, finish_city, n_paths):
    network, index_to_name = load_data()
    start = next(key for key, value in index_to_name.items() if value == start_city)
    finish = next(key for key, value in index_to_name.items() if value == finish_city)
    best_distances, best_paths = network.dfs_solve(start, finish, n_routes=n_paths)

    for i, path in enumerate(best_paths):
        print(f"{i + 1}. PATH DFS: ")
        for city in path:
            print("\t" + str(index_to_name[city]))
        print(f"\t\tLength = {best_distances[i]}")
    return best_distances


if __name__ == '__main__':
    arguments = parse_args()

    # tryb benchmark
    # benchmark(arguments)
    a = datetime.datetime.now()
    dfs_dis = run_dfs(arguments['starting'], arguments['finishing'], arguments['npaths'])
    b = datetime.datetime.now()
    delta = b - a
    time, aco_dist = run_aco(arguments)


    print(f"\n\nDFS duration =  {int(delta.total_seconds() * 1000)} ms")
    print(f"ACO duration  = {time} ms")
    print(f'Best path length difference: {aco_dist[0] - dfs_dis[0]}')
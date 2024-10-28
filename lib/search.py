from random import shuffle

from lib.city import City

def get_total_distance(cities: list[City]) -> float:
    distance = 0
    for i in range(len(cities)):
        distance += cities[i].distance(cities[(i + 1) % len(cities)])  # wrap-around to the first city
    return distance

def search_this_map(cities: list[City]) -> list[list[City]]:
    """This function should return a list of city lists"""
    # states = []
    # for i in range(10):
    #     # Create a copy
    #     c = []
    #     for j in range(len(cities)):
    #         c.append(cities[j])
    #     # shuffle and add it to the array
    #     shuffle(c)
    #     states.append(c)
    #
    # return states
    return [hill_climbing_search(cities)]

def hill_climbing_search(cities: list[City]) -> list[City]:
    current_tour = cities[:]  # make a copy of the original tour
    current_distance = get_total_distance(current_tour)
    better = True

    while better:
        better = False
        for i in range(len(current_tour)):
            # Swap city i with the next city (or city 0 in the case of the last city)
            next_city_idx = (i + 1) % len(current_tour)
            new_tour = current_tour[:]
            # Swap adjacent cities
            new_tour[i], new_tour[next_city_idx] = new_tour[next_city_idx], new_tour[i]

            # get distance for new tour
            new_distance = get_total_distance(new_tour)

            # If the new tour is better, accept
            if new_distance < current_distance:
                current_tour = new_tour
                current_distance = new_distance
                better = True  # found a better tour, continue the loop
                break  # restart the loop from the first city

    return current_tour

def simulated_annealing(cities: list[City]) -> list[City]:
    pass

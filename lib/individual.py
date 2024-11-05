import random


def create_random_route(city_list):
    return random.sample(city_list, len(city_list))


def create_population(pop_size, city_list):
    population = []
    for i in range(pop_size):
        population.append(Individual(create_random_route(city_list)))
    return population


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)


def breed(p1, p2):
    return p1.breed(p2)


def breed_population(mating_pool, num_elite):
    children = []
    length = len(mating_pool) - num_elite
    pool = random.sample(mating_pool, len(mating_pool))

    for i in range(0, num_elite):
        children.append(mating_pool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(mating_pool) - i - 1])
        children.append(child)

    return children


def create_next_generation(population, num_elite):
    children = breed_population(population, num_elite)
    mutated_population = []
    for i in children:
        r = random.random()
        if r <= 0.1:
            i.mutate()
        mutated_population.append(i)

    return mutated_population


class Individual:
    """represents one route, or one member of a population"""
    def __init__(self, route):
        self.route = route
        self.distance = self.calculate_distance()
        self.desirability = self.calculate_desirability()

    def calculate_distance(self):
        distance = 0
        for i in range(len(self.route)):
            distance += self.route[i].distance(self.route[(i + 1) % len(self.route)])  # wrap-around to the first city
        return distance

    def calculate_desirability(self):
        return 1 / self.distance

    def breed(self, other):
        child = []
        child_p1 = []
        child_p2 = []

        gene_a = int(random.random() * len(self.route))
        gene_b = int(random.random() * len(self.route))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child_p1.append(self.route[i])

        child_p2 = [item for item in other.route if item not in child_p1]

        child = child_p1 + child_p2
        return Individual(child)

    def mutate(self):
        r1 = random.randint(0, len(self.route) - 1)
        r2 = random.randint(0, len(self.route) - 1)
        self.route[r1], self.route[r2] = self.route[r2], self.route[r1]

    def __eq__(self, other):
        return self.route == other.route

    def __gt__(self, other):
        return self.distance > other.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __ne__(self, other):
        return self.distance != other.distance


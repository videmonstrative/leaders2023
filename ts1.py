import random
import math

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0.0

    def calculate_fitness(self, points, obstacles):
        total_distance = 0.0
        for i in range(len(self.chromosome) - 1):
            point1 = points[self.chromosome[i]]
            point2 = points[self.chromosome[i + 1]]
            distance = distance_between_points(point1, point2)
            total_distance += distance
        self.fitness = 1 / total_distance

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def generate_initial_population(num_individuals, num_points):
    population = []
    for _ in range(num_individuals):
        chromosome = list(range(num_points))
        random.shuffle(chromosome)
        individual = Individual(chromosome)
        population.append(individual)
    return population

def select_parents(population, num_parents):
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    return sorted_population[:num_parents]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1.chromosome) - 1)
    child_chromosome = parent1.chromosome[:crossover_point]
    for gene in parent2.chromosome:
        if gene not in child_chromosome:
            child_chromosome.append(gene)
    return Individual(child_chromosome)

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        index1 = random.randint(0, len(individual.chromosome) - 1)
        index2 = random.randint(0, len(individual.chromosome) - 1)
        individual.chromosome[index1], individual.chromosome[index2] = individual.chromosome[index2], individual.chromosome[index1]

def calculate_shortest_path_genetic(points, obstacles, num_individuals, num_generations, num_parents, mutation_rate):
    population = generate_initial_population(num_individuals, len(points))

    for _ in range(num_generations):
        # Вычисляем приспособленность (fitness) для каждого индивида в популяции
        for individual in population:
            individual.calculate_fitness(points, obstacles)

        # Отбираем лучших родителей
        parents = select_parents(population, num_parents)

        offspring = []
        # Создаем новое поколение путем скрещивания и мутации
        while len(offspring) < num_individuals:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            offspring.append(child)

        population = offspring

    # Находим наилучшего индивида (с наибольшей приспособленностью)
    best_individual = max(population, key=lambda x: x.fitness)
    best_path = [points[gene] for gene in best_individual.chromosome]

    # Обход препятствий
    final_path = []
    for point in best_path:
        if not any(is_point_in_obstacle(point, obs) for obs in obstacles):
            final_path.append(point)

    return final_path

def is_point_in_obstacle(point, obstacle):
    # Проверка, находится ли точка внутри препятствия
    x, y = point
    obstacle_points = obstacle["points"]
    return is_point_inside_polygon(x, y, obstacle_points)

def is_point_inside_polygon(x, y, polygon):
    # Проверка, находится ли точка внутри многоугольника
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Пример использования

points = [(2, 2), (2, 4), (2, 10), (6, 2), (8, 11), (8, 7), (6, 5), (8, 13), (8, 5)]
obstacles = [
    {"points": [(3, 12), (3, 3), (5, 3), (5, 6), (7, 6), (7, 12)]},  # Препятствие 1
    {"points": [(4, 11), (6, 11), (6, 20), (4, 20)]},  # Препятствие 2
]
central_point = (6, 3)  # Центральная точка

path = calculate_shortest_path_genetic(points + [central_point], obstacles, num_individuals=100, num_generations=1000, num_parents=20, mutation_rate=0.01)

print("Путь:", path)


central_point = (6, 3)
points = [(2, 2), (2, 4), (2, 10), (6, 2), (8, 11), (8, 7), (6, 5), (8, 13), (8, 5)]
obstacles = [(3, 12), (3, 3), (5, 3), (5, 6), (7, 6), (7, 12)]

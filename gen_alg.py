# program to demonstrate working of a simple genetic algorithm
import random


# class for chromosome
class Chromosome:
    def __init__(self, _x):
        self.x = _x
        self.fitness = 0
        self.binary = self.get_binary()

    def calc_fitness(self, per):
        self.fitness = self.x * (per / 2 - self.x)

    def get_binary(self):
        binary_str = "{0:08b}".format(self.x)
        binary = [int(i) for i in binary_str]
        return binary


#the actual algorithm
class GeneticOptimizerAlgorithm:
    def __init__(self, _perimeter, _popu_size, _mutation, _generations):
        self.perimeter = _perimeter
        self.population_size = _popu_size
        self.mutation_rate = _mutation
        self.generations = _generations
        self.numbers = [n for n in range(0, 256)]
        self.population = self.initial_population()

    # generates the starting population
    def initial_population(self):
        init_population = []
        high = self.population_size + 1
        for _ in range(0, high):
            choice = random.randint(0, len(self.numbers) - 1)
            chromosome = Chromosome(self.numbers.pop(choice))
            init_population.append(chromosome)
        for chromo in init_population:
            chromo.calc_fitness(self.perimeter)
        fitness = lambda c: c.fitness
        init_population.sort(reverse=True, key=fitness)
        return init_population

    # generates a new population
    def select_cross_mutate(self):
        self.population_size = len(self.population)
        # SELECTION
        mating_pool = [self.population[i] for i in range(0, 16)]
        elite = mating_pool.copy()
        new_gen = []
        while len(mating_pool) > 0:
            p1 = mating_pool.pop(random.randint(0, len(mating_pool) - 1))
            p2 = mating_pool.pop(random.randint(0, len(mating_pool) - 1))
            crosspoints = [3, 4, 5]
            cross_point = random.choice(crosspoints)
            # CROSSING
            c1_bin, c2_bin = "", ""
            for i in range(0, cross_point):
                c1_bin = c1_bin + str(p1.binary[i])
                c2_bin = c2_bin + str(p2.binary[i])
            for i in range(cross_point, 8):
                c1_bin = c1_bin + str(p2.binary[i])
                c2_bin = c2_bin + str(p1.binary[i])
            # MUTATION
            if random.random() < self.mutation_rate:
                pos = random.randint(0, 7)
                if c1_bin[pos] == "0":
                    c1_bin[pos].replace("0", "1")
                else:
                    c1_bin[pos].replace("1", "0")
            if random.random() < self.mutation_rate:
                pos = random.randint(0, 7)
                if c2_bin[pos] == "0":
                    c2_bin[pos].replace("0", "1")
                else:
                    c2_bin[pos].replace("1", "0")
            c1 = Chromosome(int(c1_bin, 2))
            c2 = Chromosome(int(c2_bin, 2))
            new_gen.append(c1)
            new_gen.append(c2)
        # REPLACING UNFIT OLDER CHROMOSOMES WITH NEWLY CREATED CHROMOSOMES
        new_gen.extend(elite)
        for chromo in new_gen:
            chromo.calc_fitness(self.perimeter)
        fitness = lambda c: c.fitness
        new_gen.sort(reverse=True, key=fitness)
        return new_gen

    # "training" the algorithm
    def run(self):
        gen = self.generations
        print("Original population: ")
        for chromo in self.population:
            print(chromo.x, end=" ")
        print()
        print()
        while self.generations > 0:
            self.population = self.select_cross_mutate()
            fitness = lambda c: c.fitness
            self.population.sort(reverse=True, key=fitness)
            print("Generation ", gen - self.generations + 1)
            for chromo in self.population:
                print(chromo.x, end=" ")
            print()
            print()
            self.generations -= 1


if __name__ == "__main__":
    perimeter = int(input("What is the perimeter of the rectangle? "))
    while perimeter > 1021:
        perimeter = int(input("Perimeter must be b/w 0 and 1021: "))
    print()
    ga = GeneticOptimizerAlgorithm(perimeter, 32, 0.3, 8)
    ga.run()
    sol = ga.population[0].x
    print("Length:", sol, ", Breadth:", perimeter / 2 - sol)
    print("The area of a rectangle with the above dimensions is: ", sol * (perimeter / 2 - sol))

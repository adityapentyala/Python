import glob
import numpy as np
import os.path as path
import imageio
import time
import matplotlib.pyplot as plot
import random
import copy

'''starttime = time.time()
IMAGE_PATH = '/Users/sureshp/Downloads/planesnet/planesnet/planesnet'
file_paths = glob.glob(path.join(IMAGE_PATH, '*.png'))
images = [imageio.imread(path) for path in file_paths]
images = np.asarray(images)
currenttime = time.time()
print("Image aspects are: ", images.shape)
print("Time taken: ", currenttime - starttime)
images = np.around((images / 255), 3)

np.save("dataRGB", images)
'''

images = np.load("dataRGB.npy")
IMAGE_PATH = '/Users/sureshp/Downloads/planesnet/planesnet/planesnet'
file_paths = glob.glob(path.join(IMAGE_PATH, '*.png'))
n_images = images.shape[0]
labels = np.zeros(n_images)
for im in range(n_images):
    filename = path.basename(file_paths[im])[0]
    labels[im] = int(filename[0])

TRAIN_TEST_SPLIT = 0.9
split_index = int(TRAIN_TEST_SPLIT * n_images)
shuffled_indices = np.random.permutation(n_images)
train_indices = shuffled_indices[0:split_index]
test_indices = shuffled_indices[split_index:]

X_train_raw = images[train_indices, :, :]
y_train_raw = labels[train_indices]
# print(X_train_raw.shape, y_train_raw.shape)
X_test = images[test_indices, :, :]
y_test = labels[test_indices]

negatives = np.where(y_train_raw == 0)[0]
positives = np.where(y_train_raw == 1)[0]
indices = negatives[:int((negatives.shape[0] - positives.shape[0]) * 0.6)]
# print(positives.shape, negatives.shape, indices.shape)
X_train = np.delete(X_train_raw, indices, axis=0)
y_train = np.delete(y_train_raw, indices)

'''def visualize_data(positive_images, negative_images):
    
    figure = plot.figure()
    count = 0
    for i in range(positive_images.shape[0]):
        count += 1
        figure.add_subplot(2, positive_images.shape[0], count)
        plot.imshow(positive_images[i, :, :])
        plot.axis('off')
        plot.title("1")

        figure.add_subplot(1, negative_images.shape[0], count)
        plot.imshow(negative_images[i, :, :])
        plot.axis('off')
        plot.title("0")
    plot.show()

N_TO_VISUALIZE = 10

# Select the first N positive examples
positive_example_indices = (y_train == 1)
positive_examples = X_train[positive_example_indices, :, :]
positive_examples = positive_examples[0:N_TO_VISUALIZE, :, :]

# Select the first N negative examples
negative_example_indices = (y_train == 0)
negative_examples = X_train[negative_example_indices, :, :]
negative_examples = negative_examples[0:N_TO_VISUALIZE, :, :]

# Call the visualization function
visualize_data(positive_examples, negative_examples)
'''

n_pixels = X_train.shape[1] * X_train.shape[2] * X_train.shape[3]
X_train = X_train.reshape((X_train.shape[0], n_pixels)).astype('float32')
X_test = X_test.reshape((X_test.shape[0], n_pixels)).astype('float32')

n_targets = 2


# print(X_train.shape, y_train.shape)


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def relu(x):
    return np.maximum(x, 0)


class Chromosome:
    def __init__(self, weights):
        self.weights = weights
        self.w0, self.w1, self.w2, self.w3 = weights[0:480000].reshape(1200, 400), weights[480000:520000].reshape(400,
                                                                                                                  100),\
                                             weights[520000:521000].reshape(100, 10), weights[521000:521020].reshape(10,
                                                                                                                     2)
        self.nn = NeuralNetworkClassifier(self.w0, self.w1, self.w2, self.w3)
        self.fitness = 0
        self.calc_fitness()

    def calc_fitness(self):
        weights = self.weights
        self.w0, self.w1, self.w2, self.w3 = weights[0:480000].reshape(1200, 400), weights[480000:520000].reshape(400,
                                                                                                                  100),\
                                             weights[520000:521000].reshape(100, 10), weights[521000:521020].reshape(10,
                                                                                                                     2)
        self.nn = NeuralNetworkClassifier(self.w0, self.w1, self.w2, self.w3)
        true_rate = self.nn.measure_accuracy(X_train, y_train)
        self.fitness = round(true_rate, 2)


class GA_Optimizer:
    def __init__(self):
        self.population_size = 20
        self.mutation_rate = 0.35
        self.generations = 75
        self.species = 1
        self.population = self.init_population()
        self.population.sort(reverse=True, key=lambda c: c.fitness)
        self.accuracies = []
        self.avgaccuracies = []
        print(f"ORIGINAL POPULATION | Best: {self.population[0].fitness}")
        for chromo in self.population:
            print(chromo.fitness, end=" ")
        print()
        print()

    def init_population(self):
        print(f"Initialization begun at {time.ctime(time.time())}")
        population = []
        for _ in range(self.population_size):
            chromosome = Chromosome(np.random.randn(521020))
            population.append(chromosome)
        return population

    def select_cross_mutate(self):
        # select
        elites = [self.population[idx] for idx in range(0, 10)]
        selected = copy.deepcopy(elites)
        new_gen = []
        elites[8] = self.population[random.randint(10, 18)]
        elites[9] = self.population[random.randint(10, 18)]
        # cross
        while len(elites) != 0:
            p1 = elites.pop(random.randint(0, len(elites) - 1))
            p2 = elites.pop(random.randint(0, len(elites) - 1))
            # cross_points = [130255, 260510, 390765]
            c1, c2 = Chromosome(np.zeros(521020)), Chromosome(np.zeros(521020))
            for i in range(c1.weights.shape[0]):
                choice = random.random()
                #cross
                if choice < 0.5:
                    c1.weights[i] = p1.weights[i]
                    c2.weights[i] = p2.weights[i]
                else:
                    c1.weights[i] = p2.weights[i]
                    c2.weights[i] = p1.weights[i]
            new_gen.append(c1)
            new_gen.append(c2)
        # mutate
        for chromo in new_gen:
            if random.random() < self.mutation_rate:
                toReplace = [random.randint(0, 521019) for _ in range(150000)]
                while len(toReplace) > 0:
                    chromo.weights[toReplace.pop(0)] = np.random.random()
        # replace old population
        new_gen.extend(selected)
        self.population = new_gen
        for chromo in self.population:
            chromo.calc_fitness()
        self.population.sort(reverse=True, key=lambda c: c.fitness)

    def train_network(self):
        starttime = time.time()
        print(f"Training started at: {time.ctime(starttime)}")
        species = self.species
        while species > 0:
            print("SPECIES", self.species - species + 1)
            gen = self.generations
            while gen > 0:
                self.select_cross_mutate()
                print("Generation", self.generations - gen + 1, "| BEST:", self.population[0].fitness)
                self.accuracies.append(self.population[0].fitness)
                for chromo in self.population:
                    print(chromo.fitness, end=" ")
                print()
                print()
                n = 0
                for c in self.population[:10]:
                    n += c.fitness
                self.avgaccuracies.append(n/10)
                gen -= 1
            new_species = [self.population[i] for i in range(4)]
            while len(new_species) < self.population_size:
                chromosome = Chromosome(np.random.randn(521020))
                new_species.append(chromosome)
            self.population = new_species
            species -= 1
        self.population.sort(reverse=True, key=lambda c: c.fitness)
        print("Best Accuracy Possible:", self.population[0].fitness)
        print("Time Taken:", time.time() - starttime)


class NeuralNetworkClassifier:
    def __init__(self, w0, w1, w2, w3):
        self.weights0 = w0
        self.weights1 = w1
        self.weights2 = w2
        self.weights3 = w3

    def forward_propogate(self, Xi):
        layer1 = relu(np.dot(Xi, self.weights0))
        layer2 = relu(np.dot(layer1, self.weights1))
        layer3 = relu(np.dot(layer2, self.weights2))
        raw_output = softmax(np.dot(layer3, self.weights3))
        if raw_output[0] > raw_output[1]:
            output = 0
        else:
            output = 1
        return output

    def measure_accuracy(self, X_train, y):
        true_rate = 0
        total = 0
        preds = []
        for i in range(X_train.shape[0]):
            x = X_train[i]
            prediction = self.forward_propogate(x)
            preds.append(prediction)
            total += 1
            if round(prediction) == y[i]:
                true_rate += 1
        return round((true_rate / total) * 100, 2)

    def test(self, X_test, y_test):
        zeroes = 0
        ones = 0
        correct = 0
        total = 0
        incorrect = []
        for i in range(X_test.shape[0]):
            x = X_train[i]
            prediction = self.forward_propogate(x)
            if prediction == 0:
                zeroes += 1
            else:
                ones += 1
            total += 1
            if round(prediction) == y_test[i]:
                correct += 1
            else:
                incorrect.append((round(prediction), y_test[i]))
        print(f"The network was tested and got {round((correct / total) * 100, 2)}% of its predictions right.")
        print(f"zeroes:ones = {zeroes}:{ones}")
        print(f"INCORRECT VALUES: {incorrect}")
        print()


if __name__ == '__main__':
    ga = GA_Optimizer()
    ga.train_network()
    #testing
    for i in range(0, 7):
        weights = ga.population[i].weights
        w0, w1, w2, w3 = weights[0:480000].reshape(1200, 400), weights[480000:520000].reshape(400, 100), \
                         weights[520000:521000].reshape(100, 10), weights[521000:521020].reshape(10, 2)
        nn = NeuralNetworkClassifier(w0, w1, w2, w3)
        print(f"Accuracy: {ga.population[i].fitness}")
        nn.test(X_test, y_test)
    plot.figure()
    generations = [n for n in range(0, ga.generations*ga.species)]
    plot.title("Accuracy over generations")
    plot.plot(generations, ga.accuracies, label="Best accuracy")
    plot.plot(generations, ga.avgaccuracies, label="Average accuracy of elites")
    plot.xlabel("Generation")
    plot.ylabel("Accuracies")
    plot.legend()
    plot.show()

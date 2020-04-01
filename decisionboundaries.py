from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
import numpy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plot
from sklearn.model_selection import cross_val_score
from matplotlib.colors import ListedColormap

irisDataset = load_iris()
sepals = []
sepal_length = irisDataset.data[:, 0]
sepal_width = irisDataset.data[:, 1]
x_coords = []
y_coords = []
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

def listify(list1, list2):
    for i in range(0, len(list1)):
        temp = [list1[i], list2[i]]
        sepals.append(temp)

listify(sepal_length, sepal_width)
sepals = numpy.array(sepals)

Data_train, Data_test, Target_train, Target_test = train_test_split(sepals,
                                                                    irisDataset["target"], random_state=0)

formatterplot = plot.FuncFormatter(lambda index, *args: irisDataset.target_names[int(index)])

for k in range(1, 45):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(Data_train, Target_train)
    x_coords.append(k)
    y_coords.append(knn.score(Data_test, Target_test)*100)

plot.figure(1)
plot.plot(x_coords,y_coords)
plot.ylim(top = 100)
plot.xlabel("Value of k")
plot.ylabel("Accuracy")
plot.title("Accuracy for different values of k")

#calculating min and max lengths/widths of the features
length_min, length_max = min(sepal_length) - 0.1, max(sepal_length) + 0.1
width_min, width_max = min(sepal_width) - 0.1, max(sepal_width) + 0.1
#numpy.meshgrid() used to return coordinate matrices
xx, yy = numpy.meshgrid(numpy.linspace(length_min, length_max, 100), numpy.linspace(width_min, width_max, 100))
#training the dataset. change n_neighbours value to view the decision boundary change
knn_plotter = KNeighborsClassifier(n_neighbors=8)
knn_plotter.fit(Data_train, Target_train)
#predicting the decision boundaries relative to the dots
Z = knn_plotter.predict(numpy.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plot.figure(2)
plot.pcolormesh(xx, yy, Z, cmap = cmap_light)
plot.scatter(sepal_length, sepal_width, c=irisDataset.target, cmap=cmap_bold)
plot.xlabel("sepal length (cm)")
plot.ylabel("sepal width (cm)")
plot.colorbar(ticks=[0, 1, 2], format=formatterplot)
plot.show()

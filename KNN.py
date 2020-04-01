from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
import numpy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plot

irisDataset = load_iris()
Data_train, Data_test, Target_train, Target_test = train_test_split(irisDataset["data"], irisDataset["target"],
                                                                    random_state=0)
x_coords = []
y_coords = []

data_to_predict = numpy.array([[5, 2.9, 1, 0.2]])

for k in range(1, 100):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(Data_train, Target_train)
    x_coords.append(k)
    y_coords.append(knn.score(Data_test, Target_test)*100)

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(Data_train, Target_train)

predicted_species = knn.predict(data_to_predict)
print("The most probable species the sample will be is " + irisDataset["target_names"][predicted_species][0] + ". " +
      "The machine was tested and got {:.2f}% of its predictions right.".format(knn.score(Data_test, Target_test) * 100))

plot.figure()
plot.plot(x_coords, y_coords)
plot.xlabel("Value of k")
plot.ylabel("Accuracy (in %)")
plot.ylim(top = 100)
plot.title("Accuracy for different values of k")
plot.show()
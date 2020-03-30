import matplotlib.pyplot as plot
from sklearn.datasets import load_iris

irisDataset = load_iris()

#making individual lists for attributes
sepal_length = irisDataset.data[:, 0]
sepal_width = irisDataset.data[:, 1]
petal_length = irisDataset.data[:, 2]
petal_width = irisDataset.data[:, 3]

#this variable formats the colours to match the species
formatterplot = plot.FuncFormatter(lambda index, *args: irisDataset.target_names[int(index)])

#plotting first plot
plot.figure(1)
plot.scatter(sepal_length, sepal_width, c=irisDataset.target)
plot.xlabel("sepal length (cm)")
plot.ylabel("sepal width (cm)")
plot.colorbar(ticks=[0, 1, 2], format=formatterplot)

#plotting second plot
plot.figure(2)
plot.scatter(petal_length, petal_width, c=irisDataset.target)
plot.xlabel("petal length (cm)")
plot.ylabel("petal width (cm)")
plot.colorbar(ticks=[0, 1, 2], format=formatterplot)  #formats colours as per 'target' and 'target_names' keys of the dataset

#showing the plots
plot.show()





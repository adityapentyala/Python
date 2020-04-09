import pandas as pd
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plot
from sklearn.tree import export_graphviz
import pydotplus

maeList = []
depthList = []

boston = load_boston()
X = pd.DataFrame(boston.data, columns=boston.feature_names)
y = pd.DataFrame(boston.target, columns=["target"])
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

dtr_model = DecisionTreeRegressor(random_state=0, max_depth=6)
dtr_model.fit(X_train, y_train)
y_preds = dtr_model.predict(X_test)
print(mean_absolute_error(y_test, y_preds), dtr_model.get_depth())

dot_data = export_graphviz(dtr_model, feature_names=boston.feature_names, out_file=None,
                           filled=True,
                           rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png("boston.png")

for depths in range(1, 19):
    dtr_model = DecisionTreeRegressor(random_state=0, max_depth=depths)
    dtr_model.fit(X_train, y_train)
    preds = dtr_model.predict(X_test)
    this_mae = mean_absolute_error(y_test, preds)
    maeList.append(this_mae)
    depthList.append(depths)

plot.figure(1)
plot.plot(y_test, y_test)
plot.scatter(y_test, y_preds, s=10, c="red")
plot.title("Actual vs Predicted values")
plot.xlabel("Actual values")
plot.ylabel("Predicted values")

plot.figure(2)
plot.plot(depthList, maeList)
plot.title("Mean Absolute Error for different max depth values")
plot.xlabel("Depth")
plot.ylabel("MAE")

plot.show()

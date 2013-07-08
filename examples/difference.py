"""
Example Difference between Prediction and Naive Approach
--------------------------------------------------------
"""

from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data_aggregated_withdiff import get_feature_and_label_data_aggregated_withdiff
from windml.datasets.park_definitions import park_info
from sklearn import neighbors
import math
import matplotlib.pyplot as plt

name = 'tehachapi'
radius=30
k_neighbors = 50
feature_window = 3
horizon = 3

my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004, 2005)
X,Y = get_feature_and_label_data_aggregated_withdiff(my_windpark,feature_window,horizon)

knn = neighbors.KNeighborsRegressor(k_neighbors, 'uniform')
train_to=int(math.floor(len(X)*0.10))
test_to = train_to + 288
train_step=4

print "knn training"
reg = knn.fit(X[0:train_to:train_step],Y[0:train_to:train_step])
print "knn predicting"
y_ = reg.predict(X[train_to:test_to])
naive = []
times = []
for i in range(0, test_to-train_to):
    times.append(i)
    naive.append(Y[i+train_to-horizon])

sum_err_pred = 0.0
sum_err_naiv = 0.0

for i in range(0, test_to-train_to):
    sum_err_pred += (y_[i] - Y[i+train_to]) ** 2
    sum_err_naiv += (naive[i] - Y[i+train_to]) ** 2

print "sum of square err of prediction", sum_err_pred
print "sum of square err of naive approach", sum_err_naiv

plt.grid(True)
plt.xlabel("Timesteps")
plt.ylabel("Difference Prediction and Naive Corrected Score (MW)")
plt.plot(times, (y_ - naive), 'b-', label='difference')
plt.xlim([times[0], times[-1]])
plt.legend(loc='lower right')
plt.show()
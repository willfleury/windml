"""
Amount of Turbines
-------------------------------------------------------------

This plot shows the number of turbines with regard to various radii for
different wind parks Vantage, Palm Springs, Tehachapi and Cheyenne.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.util.distance import distance

import math
import matplotlib.pyplot as plt

from windml.datasets.nrel import NREL

parks = ['vantage', 'palmsprings', 'tehachapi', 'cheyenne']
radius_interval = [0.0, 8.0]
stepsize = 0.5

def amount_of_turbines(radius, park):
    target = NREL.park_id[park]
    ds = NREL()
    windpark = ds.get_windpark(target, radius, 2004, 2005)
    target = ds.get_turbine(target, 2004, 2005)
    turbines = windpark.get_turbines()
    return len(turbines)

results = {}
for park in parks:
    diff = radius_interval[1] - radius_interval[0]
    if(diff % stepsize > 0):
        raise Exception("Steps dont fit into interval")
    steps = int(diff / stepsize)

    values, results_park = [], {}
    for step in xrange(steps):
        value = radius_interval[0] + step * stepsize
        values.append(value)

    for value in values:
        k = amount_of_turbines(value, park)
        results_park[value] = k

    results[park] = results_park

# plot

labels = {'vantage':'Vantage', 'palmsprings':'Palm Springs', 'tehachapi': 'Tehachapi',\
          'cheyenne':'Cheyenne'}
colors = {'vantage':'k', 'palmsprings':'r', 'tehachapi':'b', 'cheyenne':'g'}
markers = {'vantage':'o', 'palmsprings':'x', 'tehachapi':'d', 'cheyenne':'^'}

for park in parks:
    items = results[park].items()
    X, Y = [], []
    for x,y in items:
        X.append(x)
        Y.append(y)

    plt.xlim([0, 8])
    plt.ylim([0, 80])

    plt.xlabel('Radius')
    plt.ylabel('Amount of Turbines')
    plt.scatter(X,Y, color=colors[park], marker=markers[park], label=labels[park])

plt.legend(loc='lower right')
plt.show()
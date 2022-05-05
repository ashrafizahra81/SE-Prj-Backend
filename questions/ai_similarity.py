import numpy as np
import pandas as pd
from math import *

# n equal to number of features
n = 5

# m equal to number of samples
m = 100
# Coefficients of each feature
values = [1, 1, 1, 1, 1]


class Similarity:

    def __init__(self, features):
        self.features = features

    def recommend(self, values, customer_feature1, customer_feature2, customer_feature3, customer_feature4, k1=6, k2=2,
                  k3=2, k4=2):
        # compute distances by one of the distance(distance_1, distance_2, ...) functions
        distances1 = np.array([self.distance_2(customer_feature1, f, values) for f in self.features])
        distances2 = np.array([self.distance_2(customer_feature2, f, values) for f in self.features])
        distances3 = np.array([self.distance_2(customer_feature3, f, values) for f in self.features])
        distances4 = np.array([self.distance_2(customer_feature4, f, values) for f in self.features])

        # get k nearest style indices
        k_indices1 = np.argsort(distances1)[:k1]
        k_indices2 = np.argsort(distances2)[:k2]
        k_indices3 = np.argsort(distances3)[:k3]
        k_indices4 = np.argsort(distances4)[:k4]

        # print(distances1[k_indices1])
        # print(self.features[k_indices1])

        # merge and unigue indices(union)
        k_indices = np.union1d(k_indices1, np.union1d(k_indices2, np.union1d(k_indices3, k_indices4)))
        # print(self.features[k_indices])

        # return the selected style indices
        return k_indices

    def distance_1(self, x, y, values):
        return np.sum(values * np.abs(x - y))

    def distance_2(self, x, y, values):
        return np.sqrt(np.sum(values * ((x - y) ** 2)))

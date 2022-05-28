import numpy as np
import pandas as pd
from math import *

# n equal to number of features
n = 5

# m equal to number of samples
m = 100
# Coefficients of each feature
values = [1, 1, 1, 1, 1]


class RecommendationSystem:

    def __init__(self, allClothes):
        self.allClothes = allClothes

    def recommend_based_on_questions(self, values, customer_feature1, customer_feature2, customer_feature3,
                                     customer_feature4, k1=4, k2=1, k3=1, k4=1):

        # k nearest neighbor
        k_indices1 = self.__one_recommend(customer_feature1, values, k1)
        k_indices2 = self.__one_recommend(customer_feature2, values, k2)
        k_indices3 = self.__one_recommend(customer_feature3, values, k3)
        k_indices4 = self.__one_recommend(customer_feature4, values, k4)

        # merge and unigue indices(union)
        k_indices = np.append(k_indices1, np.append(k_indices2, np.append(k_indices3, k_indices4)))

        # return the selected style indices
        return k_indices

    def recommend_based_on_clothes(self, selectedClothes, values, anomaly, k=5):

        # asume average of the each component for the as the customer vector of self.__oneRecommend little diffrent
        # with the ordinary averages
        average_of_multi_tags = self.__special_mean(selectedClothes, anomaly)
        k_indeces = self.__one_recommend(average_of_multi_tags, values, k)
        return k_indeces

    def recommend_based_on_cluster(self, cluster_taste, k=30):
        return 1

    def __one_recommend(self, customer, values, k):
        # compute distances by one of the distance(distance_1, distance_2, ...) functions
        distances = np.array([self.__similarity2(customer, f, values) for f in self.allClothes])

        # return k nearest style indices
        return np.argsort(distances)[:k]

    def update_cluster_taste(self, prev_cluster_taste, comment, clothesInd, alpha=0.1):
        # find the class number of clothes
        # clusterNumber = self.which_cluster(clothesInd)
        clusterNumber = 3

        # calculate the new replacement for selected cluster with weighted average
        weightedAverage = np.average([prev_cluster_taste[clusterNumber], comment], weights=[1, alpha])

        # update prev_Cluster_taste
        prev_cluster_taste[clusterNumber] = weightedAverage
        return prev_cluster_taste

    def __clustring(self, clothes):
        return 1

    def which_cluster(ClothesInd):
        return 1

    def __similarity1(self, customer, clothes, values):
        lowestMines = self.__lowest_mines(customer, clothes)
        return np.sum(values * np.abs(lowestMines))

    def __similarity2(self, customer, clothes, values):
        lowestMines = self.__lowest_mines(customer, clothes)
        return np.sqrt(np.sum(values * ((lowestMines) ** 2)))

    def __lowest_mines(self, customer, clothes):
        bestClothes = []
        tmpArray1 = []
        for i in range(len(customer)):
            for j in range(np.shape(clothes)[1]):
                tmpArray1.append(abs((customer[i] - clothes[i][j])))
            bestClothes.append(min(tmpArray1))
            tmpArray1 = []
        return np.array(bestClothes)

    def __special_mean(self, selectedClothes, anomaly):
        # we have to ignore anomaly values in each component to have access the real mean value
        meanVector = []
        for i in range(np.shape(selectedClothes)[0]):
            componentSum = 0
            count = 0
            for j in range(np.shape(selectedClothes)[1]):
                if (selectedClothes[i][j] != anomaly):
                    componentSum += selectedClothes[i][j]
                    count += 1
            meanVector.append(componentSum / count)

        return meanVector

    def extract_clothes(self, clothes):
        return 1

    def remove_duplicates(self, clothes):
        return 1

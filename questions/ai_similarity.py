import math
from random import random

import numpy as np
import pandas as pd
from math import *
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans



# n equal to number of features
n = 5

# m equal to number of samples
m = 100
# Coefficients of each feature
values = [1, 1, 1, 1, 1]


class Clustering:
    def __init__(self, path='accounts_style.csv'):
        self.path = path
        self.data = self.__preprecessing(path)
        self.data = self.__normalize_based_on_values([2, 2, 1.5, 1.25, 1.75])

    def getData(self):
        return self.data

    def fit_predict(self, n_clusters=6):
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
        self.kmeans = kmeans
        return kmeans.fit_predict(self.data)

    def cluster_centers(self):
        return self.kmeans.cluster_centers_

    def predict(self, input):
        return self.kmeans.predict(input)

    def __preprecessing(self, path):
        # select special part of the dataframe
        data = pd.read_csv(path)
        data = data.iloc[:, 2:]

        # spilit data and add new culomns
        data[['Age1', 'Age2', 'Age3']] = data["Age"].str.split(",", n=2, expand=True)
        data[['Color1', 'Color2', 'Color3']] = data["Color"].str.split(",", n=2, expand=True)
        data[['Pattern1', 'Pattern2', 'Pattern3']] = data["Pattern"].str.split(",", n=2, expand=True)
        data[['Size1', 'Size2', 'Size3']] = data["Size"].str.split(",", n=2, expand=True)
        data[['Formal1', 'Formal2', 'Formal3']] = data["Formal"].str.split(",", n=2, expand=True)

        # drop unusage columns
        data.drop(columns=['Age', 'Color', 'Pattern', 'Size', 'Formal'], inplace=True)

        # convert type from str to float64
        data = data.astype('float64')

        # calculate the average of each row specialy
        data['Age_avg'] = self.__special_mean(data[['Age1', 'Age2', 'Age3']].values, 20)
        data['Color-avg'] = self.__special_mean(data[['Color1', 'Color2', 'Color3']].values, 20)
        data['Pattern_avg'] = self.__special_mean(data[['Pattern1', 'Pattern2', 'Pattern3']].values, 20)
        data['Size-avg'] = self.__special_mean(data[['Size1', 'Size2', 'Size3']].values, 20)
        data['Formal_avg'] = self.__special_mean(data[['Formal1', 'Formal2', 'Formal3']].values, 20)

        # drop unusage columns
        data.drop(columns=['Age1', 'Age2', 'Age3', 'Color1', 'Color2', 'Color3', 'Pattern1',
                           'Pattern2', 'Pattern3', 'Size1', 'Size2', 'Size3', 'Formal1', 'Formal2', 'Formal3'],
                  inplace=True)

        return data

    def __normalize_based_on_values(self, values):
        # normalize data from 0 to 1
        normalized_data = pd.DataFrame(preprocessing.normalize(self.data), columns=self.data.columns)

        # put it in -1 to +1
        normalized_data = (normalized_data - 0.5) * 2

        # change the period for each component to change the influence
        normalized_data = normalized_data * values
        return normalized_data

    def __special_mean(self, selectedClothes, anomaly):
        # we have to ignore anomaly values in each component to have accessed the real mean value
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
class RecommendationSystem:

    def __init__(self, allClothes):
        self.allClothes = allClothes
        self.clustering = Clustering(path='accounts_style.csv')
        self.answers = self.clustering.fit_predict(n_clusters=6)
        self.preparedData = self.clustering.getData()
        self.preparedDataWithAnswers = self.preparedData
        self.preparedDataWithAnswers['Answers'] = self.answers

    def get_prepared_data(self):
        return self.preparedData

    def get_prepared_data_with_anwers(self):
        return self.preparedDataWithAnswers

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

    def recommend_based_on_clothes(self, selectedClothes, values, anomaly=20, k=5):

        # asume average of the each component for the as the customer vector of self.__oneRecommend little diffrent with the ordinary averages
        average_of_multi_tags = self.__special_mean(selectedClothes, anomaly)
        k_indeces = self.__one_recommend(average_of_multi_tags, values, k)
        return k_indeces

    def recommend_based_on_cluster(self, cluster_taste, k=30):
        tasteSum = sum(cluster_taste)
        selected_indices = []
        for i in range(len(cluster_taste)):
            selected_indices.append(
                self.__k_recommend_recommend_based_on_cluster(i, math.ceil(k * cluster_taste[i] / tasteSum)))
        selected_indices = self.__flatten(selected_indices)
        random.shuffle(selected_indices)
        return selected_indices

    def __k_recommend_recommend_based_on_cluster(self, index, k):
        indices = self.preparedDataWithAnswers[self.preparedDataWithAnswers['Answers'] == index].index
        rndIndices = random.choices(indices, k=2 * k)
        random.shuffle(rndIndices)
        return rndIndices[:k]

    def __one_recommend(self, customer, values, k):
        # compute distances by one of the distance(distance_1, distance_2, ...) functions
        distances = np.array([self.__similarity2(customer, f, values) for f in self.allClothes])

        # return k nearest style indices
        return np.argsort(distances)[: k]

    def __flatten(self, t):
        return [item for sublist in t for item in sublist]

    def update_cluster_taste(self, prev_cluster_taste, comment, clothesInd, alpha=0.1):
        # find the class number of clothes
        # clusterNumber = self.which_cluster(clothesInd)
        clusterNumber = 3

        # calculate the new replacement for selected cluster with weighted average
        weightedAverage = np.average([prev_cluster_taste[clusterNumber], comment], weights=[1, alpha])

        # update prev_Cluster_taste
        prev_cluster_taste[clusterNumber] = weightedAverage
        return prev_cluster_taste

    def get_data(self):
        return self.preparedData

    def favorite_items(inputmatrix):
        items = pd.DataFrame(inputmatrix, columns=['id', 'average', 'count'])
        items['average'] = 0.5 * (2 * items['average']).apply(np.ceil)
        items.sort_values(['average', 'count'], inplace=True, ascending=False)
        return items.values

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

# utils
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

# model
from sklearn.ensemble import IsolationForest
from hdbscan import HDBSCAN

# sklearn
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

#scipy
from scipy.spatial.distance import mahalanobis

class IsolationForestModel(BaseEstimator):
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.model = IsolationForest(**model_params)
    
    def fit(self, X, y=None):
        self.model.fit(X)
        return self
    
    def score_samples(self, X):
        return -self.model.score_samples(X)
    
class HDBScanModel(BaseEstimator):
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.model = HDBSCAN(**model_params)

    def fit(self, X, y=None):
        self.model.fit(X)
        self.train_scores_ = self.model.outlier_scores_
        return self
    
    def score_samples(self, X):
        if hasattr(self, "train_scores_") and len(X) == len(self.train_scores_):
            return self.train_scores_
        raise ValueError("X doesn't contain same length as train data.")

class MahalanobisModel(BaseEstimator):
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.kmeans_model_ = KMeans(**model_params)
        self.n_clusters = model_params.get("n_clusters", 7)
        self.cluster_stats_ = {}
        self.scalers_ = {}

    def fit(self, X, y=None):
        self.kmeans_model_.fit(X)
        labels = self.kmeans_model_.labels_
        for cluster in range(self.n_clusters):
            cluster_mask = labels == cluster
            X_cluster = X[cluster_mask]

            # Edge case: very small cluster size -> global stats
            if len(X_cluster) < 2:
                mu = np.mean(X, axis=0)
                cov = np.cov(X, rowvar=False)
            else:
                mu = np.mean(X_cluster, axis=0)
                cov = np.cov(X_cluster, rowvar=False)
            cov += np.eye(cov.shape[0]) * 1e-6
            cov_inv = np.linalg.pinv(cov)
            diff = X_cluster - mu
            distances = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1))
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaler.fit(distances.reshape(-1, 1))
            self.cluster_stats_[cluster] = {
                "mu": mu,
                "cov_inv": cov_inv
            }
            self.scalers_[cluster] = scaler
        return self
    
    def score_samples(self, X):
        if not hasattr(self, "kmeans_model_"):
            raise ValueError("You must call fit before score_samples.")
        X = np.asarray(X)
        clusters = self.kmeans_model_.predict(X)
        scores = np.zeros(X.shape[0])
        for cluster in range(self.n_clusters):
            cluster_mask = clusters == cluster
            if not np.any(cluster_mask):
                continue
            X_cluster = X[cluster_mask]
            stats = self.cluster_stats_[cluster]
            mu = stats["mu"]
            cov_inv = stats["cov_inv"]
            diff = X_cluster - mu
            distances = np.sqrt(np.sum(diff @ cov_inv * diff, axis=1))
            scaler = self.scalers_[cluster]
            distances_scaled = scaler.transform(distances.reshape(-1, 1)).ravel()
            scores[cluster_mask] = distances_scaled
        return scores

class AMLAnomalyEnsemble:
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = self._define_weights(weights)

    def _define_weights(self, weights):
        num_models = len(self.models)
        if weights is None:
            return [1/num_models] * num_models
        elif len(weights) != num_models:
            raise ValueError("Not enougth weights provided.")
        return weights
        
    def fit(self, X):
        self.fitted_ = True
        self.train_scores_ = []
        for i, model in enumerate(self.models):
            model.fit(X)
            scores = model.score_samples(X).reshape(-1, 1)
            self.train_scores_.append(scores)
        return self
    
    def score(self, X):
        if not hasattr(self, "fitted_"):
            raise ValueError("You must call fit before score.")
        all_scores = []
        for i, model in enumerate(self.models):
            scores = model.score_samples(X).reshape(-1, 1)
            all_scores.append(scores)
        stacked = np.hstack(all_scores)
        return np.dot(stacked, self.weights)
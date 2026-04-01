# utils
import numpy as np
from sklearn.base import BaseEstimator

# model
from sklearn.ensemble import IsolationForest
from hdbscan import HDBSCAN

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
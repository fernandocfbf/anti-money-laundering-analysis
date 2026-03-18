# utils
import pandas as pd
import numpy as np
from tqdm import tqdm

# model
from sklearn.ensemble import IsolationForest
from hdbscan import HDBSCAN
from sklearn.cluster import KMeans

from scipy.spatial.distance import mahalanobis

#scaler
from sklearn.preprocessing import MinMaxScaler

class IsolationForestModel:
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.model = IsolationForest(**model_params)
    
    def fit_predict(self, X):
        return (-1)*self.model.score_samples(X)
    
class HDBScanModel:
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.model = HDBSCAN(**model_params)

    def fit_predict(self, X):
        return self.model.fit_predict(X).outlier_scores_
    
class PeerDeviationModel:
    def __init__(self, model_params=None):
        if model_params is None:
            model_params = {}
        self.model = KMeans(**model_params)

    def fit_predict(self, X):
        cluster_columns = [f"col_{i}" for i in range(X.shape[1])]
        clustering_df = pd.DataFrame(X, cluster_columns)
        clustering_df["kmeans_cluster"] = self.model.fit_predict(X)

        progress_bar = tqdm(clustering_df["kmeans_cluster"].unique(), desc="Calculating Mahalanobis Distances")
        for cluster in clustering_df["kmeans_cluster"].unique():
            cluster_mask = clustering_df["kmeans_cluster"] == cluster
            cluster_idx = clustering_df[cluster_mask].index

            x_cluster = X[cluster_mask]
            x_cluster_df = pd.DataFrame(x_cluster, columns=cluster_columns, index=cluster_idx)

            mu = np.mean(x_cluster, axis=0)
            cov = np.cov(x_cluster, rowvar=False)
            cov += np.eye(cov.shape[0]) * 1e-6

            cov_inv = np.linalg.pinv(cov)
            
            x_cluster_df["mahalanobis_distance"] = x_cluster_df.apply(lambda row: mahalanobis(row, mu, cov_inv), axis=1)
            x_cluster_df["mahalanobis_risk_score"] = MinMaxScaler(feature_range=(0, 1)).fit_transform(x_cluster_df[["mahalanobis_distance"]])
            
            clustering_df.loc[cluster_mask, "mahalanobis_distance"] = x_cluster_df["mahalanobis_distance"]
            clustering_df.loc[cluster_mask, "mahalanobis_risk_score"] = x_cluster_df["mahalanobis_risk_score"]
            
            progress_bar.update(1)
        progress_bar.close()
        return np.array(clustering_df["mahalanobis_risk_score"])
    

    
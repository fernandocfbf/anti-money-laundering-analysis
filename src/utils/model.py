import os
import sys
ROOT_PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(ROOT_PATH)

import numpy as np
import streamlit as st

#model
from sklearn.pipeline import Pipeline
from src.unsupervised_model import AMLAnomalyEnsemble, IsolationForestModel, HDBScanModel, MahalanobisModel

#preprocess
from sklearn.preprocessing import FunctionTransformer, RobustScaler, StandardScaler

def get_model(random_state=42) -> AMLAnomalyEnsemble:
    log_transformer = FunctionTransformer(np.log1p, validate=False)
    identity_transformer = FunctionTransformer(lambda x: x, validate=False)

    iso_params = {
        "random_state": random_state,
        "contamination": 0.05
    }
    hdbscan_params = {
        'min_cluster_size': 1000,
        'min_samples': 120,
        'metric': 'manhattan',
        'cluster_selection_method': 'eom'
    }
    mahalanobis_params = {
        "n_clusters": 7,
        "random_state": random_state
    }
    pipeline_iforest = Pipeline([
        ("identity", identity_transformer),  # no log
        ("scaler", RobustScaler()),
        ("model", IsolationForestModel(iso_params))
    ])

    pipeline_hdbscan = Pipeline([
        ("log", log_transformer),
        ("scaler", RobustScaler()),
        ("model", HDBScanModel(hdbscan_params))
    ])

    pipeline_mahalanobis = Pipeline([
        ("log", log_transformer),
        ("scaler", StandardScaler()),
        ("model", MahalanobisModel(mahalanobis_params))
    ])

    models = [
        pipeline_iforest,
        pipeline_hdbscan,
        pipeline_mahalanobis
    ]

    return AMLAnomalyEnsemble(models=models, weights=[0.4, 0.3, 0.3])
# system
import time
import os
import sys
ROOT_PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(ROOT_PATH)

import pandas as pd

#machine learning
import shap

#model
from src.utils.model import get_surrogate_model

#constants
from src.constants import CATEGORY_TEMPALTES, FEATURE_METADATA

class SHAPExplainer:
    def __init__(self, threshold=0.8, random_state=42):
        self.threshold = threshold
        self.surrogate_model = get_surrogate_model(random_state=random_state)
        self.category_templates = CATEGORY_TEMPALTES
        self.feature_metadata = FEATURE_METADATA
    
    def _fit(self, X, y):
        self.surrogate_model.fit(X, y)
    
    def set_shap(self, X):
        explainer = shap.TreeExplainer(self.surrogate_model)
        shap_values = explainer.shap_values(X)
        return shap_values
    
    def _get_top_features(self, shap_values, feature_names, n=3):
        
        shap_df = pd.DataFrame({"feature": feature_names, "shap_value": shap_values})
        shap_df["abs_value"] = shap_df["shap_value"].abs()
        
        #TODO: add description to indentify direction
        top_features = (
            shap_df.sort_values(by="abs_value", ascending=False)
            .head(n)
        )

        #TODO: evaluate if this sort is needed
        top_features.sort()
        return top_features
    
    def _generate_text(self, top_features):
        explanations = {}
        for feature in top_features:
            metadata = self.feature_metadata.get(feature)
            if metadata:
                category = metadata.get("theme", "general")
                if category not in explanations:
                    explanations[category] = []             
                explanations[category].append(metadata["description"])
        return explanations

    def _generate_explanation(self, shap_values, feature_columns, n=3):
        top_features = self._get_top_features(shap_values, feature_columns, n)
        explanation_dict = self._generate_text(top_features)
        paragraphs = []
        for category, descriptions in explanation_dict.items():
            template = self.category_templates.get(category)
            if template: 
                joined_desc = ", ".join(descriptions)
                paragraphs.append(template.format(joined_desc))
        return " ".join(paragraphs)
    
    def explain(self, feature_df, target_column, n=3):
        top_offenders_df = (
            feature_df[feature_df[target_column] > self.threshold].copy()
            .reset_index(drop=True)
        )
        X = top_offenders_df.drop(columns=[target_column])
        y = top_offenders_df[target_column]
        self._fit(X, y)
        shap_values = self.set_shap(X)
        
        #TODO: this loop is slow, better approach is to vectorize it
        explanations = []
        for i in range(len(X)):
            explanation = self._generate_explanation(shap_values[i], X.columns, n)
            explanations.append(explanation)
        return explanations
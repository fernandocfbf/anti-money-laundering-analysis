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
from src.constants.explanability import CATEGORY_TEMPLATES, FEATURE_METADATA

class SHAPExplainer:
    def __init__(self, threshold=0.8, random_state=42):
        self.threshold = threshold
        self.surrogate_model = get_surrogate_model(random_state=random_state)
        self.category_templates = CATEGORY_TEMPLATES
        self.feature_metadata = FEATURE_METADATA
    
    def _fit(self, X, y):
        self.surrogate_model.fit(X, y)
    
    def _set_shap(self, X):
        explainer = shap.TreeExplainer(self.surrogate_model)
        shap_values = explainer.shap_values(X)
        return shap_values
    
    def _get_top_features(self, shap_values, feature_names, n=3):
        shap_df = pd.DataFrame({"feature": feature_names, "shap_value": shap_values})
        shap_df["abs_value"] = shap_df["shap_value"].abs()
        shap_df["direction"] = shap_df["shap_value"].apply(lambda x: "positive" if x > 0 else "negative")
        top_features = (
            shap_df.sort_values(by="abs_value", ascending=False)
            .head(n)
        )
        return top_features
    
    def _generate_text(self, top_features):
        explanations = {}
        for _, row in top_features.iterrows():
            feature = row["feature"]
            direction = row["direction"]
            metadata = self.feature_metadata.get(feature)
            if metadata:
                category = metadata.get("theme", "general")
                if category not in explanations:
                    explanations[category] = []
                explanations[category].append({
                    "description": metadata["description"],
                    "direction": direction
                })
        return explanations
    
    def _resolve_category_direction(self, items):
        directions = [item["direction"] for item in items]
        return "positive" if "positive" in directions else "negative"

    def _generate_explanation(self, shap_values, feature_columns, n=3):
        top_features = self._get_top_features(shap_values, feature_columns, n)
        explanation_dict = self._generate_text(top_features)
        paragraphs = []
        for category, items in explanation_dict.items():
            template_dict = self.category_templates.get(category)
            if not template_dict:
                continue
            direction = self._resolve_category_direction(items)
            template = template_dict.get(direction)
            if not template:
                continue
            descriptions = [item["description"] for item in items]
            if len(descriptions) == 1:
                joined_desc = descriptions[0]
            else:
                joined_desc = ", ".join(descriptions[:-1]) + " and " + descriptions[-1]
            paragraphs.append(template.format(joined_desc))
        return " ".join(paragraphs)
    
    def _remove_non_numeric_features(self, df):
        numeric_df = df.select_dtypes(include=["number"])
        return numeric_df

    def explain(self, feature_df, target_column, n=3):
        numeric_df = self._remove_non_numeric_features(feature_df)
        mask = numeric_df[target_column] > self.threshold
        top_offenders_df = numeric_df.loc[mask].copy()
        X = numeric_df.drop(columns=[target_column])
        X_explain = top_offenders_df.drop(columns=[target_column])
        y = numeric_df[target_column]
        self._fit(X, y)
        shap_values = self._set_shap(X_explain)
        explanations = []
        for i in range(len(X_explain)):
            explanation = self._generate_explanation(shap_values[i], X.columns, n)
            explanations.append(explanation)
        explanation_series = pd.Series(index=feature_df.index, dtype="object")
        explanation_series.loc[top_offenders_df.index] = explanations
        explanation_series = explanation_series.fillna("No explanation available. Score is under the threshold.")
        return explanation_series
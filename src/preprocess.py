import pandas as pd
import numpy as np

from sklearn.utils.validation import check_is_fitted
from sklearn.preprocessing import RobustScaler

class PreprocessTransactions:
    def __init__(self, 
        apply_log: bool = True,
        apply_scale: bool = True,
        skew_threshold: float = 1.0,
        scaler=None,
        numeric_only: bool = True
        ):
        self.apply_log = apply_log
        self.apply_scale = apply_scale
        self.skew_threshold = skew_threshold
        self.scaler = scaler if scaler is not None else RobustScaler()
        self.numeric_only = numeric_only
        self.skewed_cols_ = None
        self.numeric_cols_ = None

    def fit(self, X: pd.DataFrame):
        X_fit = X.copy()
        if self.numeric_only:
            self.numeric_cols_ = X_fit.select_dtypes(include=np.number).columns.tolist()
        else:
            self.numeric_cols_ = X_fit.columns.tolist()
        X_num = X_fit[self.numeric_cols_]
        if self.apply_log:
            skew = X_num.skew()
            self.skewed_cols_ = skew[skew > self.skew_threshold].index.tolist()
        else:
            self.skewed_cols_ = []
        if self.apply_scale:
            X_processed = self._apply_log(X_num)
            self.scaler.fit(X_processed)
        return self

    def _apply_log(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        for col in self.skewed_cols_:
            X_out[col] = np.log1p(X_out[col].clip(lower=0))
        return X_out
    
    def _apply_scaling(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = self.scaler.transform(X)
        return pd.DataFrame(
                X_out,
                columns=X.columns,
                index=X.index
            )

    def transform(self, X:pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(self, ["numeric_cols_", "skewed_cols_"])

        X_transformed = X.copy()
        X_num = X_transformed[self.numeric_cols_]

        if self.apply_log:
            X_num = self._apply_log(X_num)
        if self.apply_scale:
            X_num = self._apply_scaling(X_num)

        X_transformed[self.numeric_cols_] = X_num
        return X_transformed



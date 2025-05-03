import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
import re
import json
import pickle
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge

# 1.1 Load your collected data


from typing import List, Optional, Tuple, cast
from sklearn.base import RegressorMixin, BaseEstimator
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import FeatureUnion, FunctionTransformer, make_pipeline


def filter_columns(
    X: pd.DataFrame, columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """A function that filters the columns of the input data.

    Args:
        X (pd.DataFrame): The input data.
        columns (Optional[List[str]], optional): The columns that should be kept. Defaults to None.

    Returns:
        pd.DataFrame: The input data with only the specified columns.
    """

    if columns is not None:
        return X[columns]

    return X


def clean_short_open_numerical_cols(y: pd.Series) -> pd.Series:
    # replace digit-digit with mean of those ranges
    # set not-numeric values to NaN

    y = pd.to_numeric(y, errors="coerce")

    return y


def clean_data(X: pd.DataFrame) -> pd.DataFrame:
    r"""
        numeric_cols = ['age', 'height', 'weight', 'sleep_hours']
    for col in numeric_cols:
        # strip non‐digits (e.g. '90kg = bulking' → '90')
        df[col] = df[col].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)


    # 6. Helper to parse ranges like "3-4", "5 and more", "0-2"
    def parse_range(val):
        if pd.isna(val):
            return np.nan
        s = str(val)
        if 'and more' in s:
            return float(re.search(r'(\d+)', s).group(1))
        m = re.match(r'(\d+)-(\d+)', s)
        if m:
            return (float(m.group(1)) + float(m.group(2))) / 2
        # fallback: extract single number
        m2 = re.search(r'(\d+)', s)
        return float(m2.group(1)) if m2 else np.nan

    # 7. Apply range parser to these columns
    range_cols = [
        'smell_intensity', 'weekly_greasy_meals', 'processed_servings',
        'fv_servings', 'weekly_bms', 'wipes_per_bm'
    ]
    for col in range_cols:
        df[col] = df[col].apply(parse_range)

    # 1. Compute the mean of weekly bms excluding 100
    mean_bms = df.loc[df['weekly_bms'] != 100, 'weekly_bms'].mean()
    df.loc[df['weekly_bms'] == 100, 'weekly_bms'] = mean_bms

    # Map Male→0, Female→1, leave Other as NaN for now
    df['gender_encoded'] = df['gender'].map({'Male': 0, 'Female': 1})

    # Randomly assign 0 or 1 for the rows where gender == 'Other'
    mask_other = df['gender'] == 'Other'
    df.loc[mask_other, 'gender_encoded'] = np.random.randint(0, 2, size=mask_other.sum())

    # Drop the original gender column if you no longer need it
    df.drop(['gender', 'timestamp', 'meds_affecting_gut'], axis=1, inplace=True)

    # 2. One-hot encode the remaining categorical columns
    categorical_cols = [
        'hydration_level',
        'activity_level',
        'dairy_freq',
        'spiciness',
        'toilet_method',
        'stool_consistency',
        'stool_color',
        'caffeinated_beverages_per_day',
        'fat_grams',
        'fiber_grams'
    ]

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    """
    X.loc[:, "height"] = pd.to_numeric(
        X["height"].astype(str).str.replace(r"[,\.]", "", regex=True).astype(float)
    ).astype(int)
    # HOTFIX: set weight to 70 kg
    X.loc[:, "weight"] = (
        pd.to_numeric(X["weight"], errors="coerce").fillna(70).astype(float)
    )

    X.loc[:, "weekly_bms"] = (
        clean_short_open_numerical_cols(X["weekly_bms"]).fillna(5).astype(float)
    )
    # short_open_numerical_cols = [
    # 'weekly_bms',
    # 'wipes_per_bm'
    # ]

    # for col in short_open_numerical_cols:
    #     if col in X.columns:
    #         X.loc[:, col] = clean_short_open_numerical_cols(X[col])

    return X


def create_pipeline(
    estimator: RegressorMixin, features_in: List[str], pandas_output: bool = False
) -> Pipeline:
    """
    select faetures
    clean up (bugs and typos in the data)
    impute missing values
    standardize numerical
    encode categorical
    """
    main_pipeline_steps: List[Tuple[str, BaseEstimator]] = [
        (
            "data_cleaning",
            FunctionTransformer(
                clean_data,
                validate=False,
            ),
        ),
        (
            "column_selector",
            FunctionTransformer(
                filter_columns,
                kw_args={"columns": features_in},
                validate=False,
            ),
        ),
        (
            "feature_union",
            FeatureUnion(
                transformer_list=[
                    (
                        "numerical",
                        ColumnTransformer(
                            transformers=[
                                (
                                    "numerical_pipeline",
                                    make_pipeline(
                                        SimpleImputer(strategy="mean"),
                                        StandardScaler(),
                                    ),
                                    make_column_selector(dtype_include=np.number),  # type: ignore
                                ),
                            ],
                            remainder="drop",
                        ),
                    ),
                    (
                        "string",
                        ColumnTransformer(
                            transformers=[
                                (
                                    "string_pipeline",
                                    make_pipeline(
                                        SimpleImputer(
                                            strategy="constant", fill_value="dna"
                                        ),
                                        OneHotEncoder(
                                            drop="first",
                                            handle_unknown="infrequent_if_exist",
                                            sparse_output=not pandas_output,
                                        ),
                                    ),
                                    make_column_selector(dtype_include=object),  # type: ignore
                                ),
                            ],
                            remainder="drop",
                        ),
                    ),
                ]
            ),
        ),
    ]

    if estimator is not None:
        main_pipeline_steps.append(
            (
                "estimator",
                estimator,
            )
        )

    pipeline = cast(
        Pipeline,
        Pipeline(steps=main_pipeline_steps).set_output(
            transform="pandas" if pandas_output else "default"
        ),
    )
    return pipeline


class CreateYPipeline:
    def __init__(self, lower_bound: float, upper_bound: float):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.lower_value = None
        self.upper_value = None

    def fit(self, y: pd.Series) -> "CreateYPipeline":
        self.lower_value = np.percentile(y, self.lower_bound)
        self.upper_value = np.percentile(y, self.upper_bound)
        return self

    def transform(self, y: pd.Series) -> pd.Series:
        y = y.copy()
        y.loc[y < self.lower_value] = self.lower_value
        y.loc[y > self.upper_value] = self.upper_value
        return y

    def fit_transform(self, y: pd.Series) -> pd.Series:
        self.fit(y)
        return self.transform(y)

    def print(self):
        print(f"Lower bound: {self.lower_value}")
        print(f"Upper bound: {self.upper_value}")
        print(f"Lower bound percentile: {self.lower_bound}")
        print(f"Upper bound percentile: {self.upper_bound}")


from dataclasses import dataclass
from pathlib import Path
import optuna
import os
from typing import Callable, Dict, Any, TypedDict
from dataclasses import dataclass

from sklearn import clone
from sklearn.base import BaseEstimator

from dataclasses import dataclass
from typing import List

from sklearn.model_selection import KFold


@dataclass
class FeatureCombination:
    name: str
    features: List[str]

    def __post_init__(self):
        if "-" in self.name:
            raise ValueError("Name cannot contain '-'")


@dataclass
class FeatureSet(FeatureCombination):
    is_optional: bool = True
    is_exclusive: bool = False


@dataclass
class FeatureManager:
    feature_sets: List[FeatureSet]

    def verify_features_existence(self, X: pd.DataFrame) -> bool:
        columns: List[str] = X.columns.to_list()

        all_features: List[str] = [
            feature
            for feature_group in self.feature_sets
            for feature in feature_group.features
        ]

        diff_feats: List[str] = list(set(all_features) - set(columns))

        if len(diff_feats) > 0:
            print(f"WARNING: Missing features in the data: {diff_feats}")
            return False

        return True

    def get_all_possible_feature_combinations(self) -> List[FeatureCombination]:
        mandatory_feature_sets: List[FeatureSet] = [
            feat_set
            for feat_set in self.feature_sets
            if (feat_set.is_optional is False and feat_set.is_exclusive is False)
        ]
        optional_feature_set: List[FeatureSet] = [
            feat_set
            for feat_set in self.feature_sets
            if (feat_set.is_optional is True and feat_set.is_exclusive is False)
        ]
        exclusive_feature_sets: List[FeatureSet] = [
            feat_set for feat_set in self.feature_sets if feat_set.is_exclusive is True
        ]
        print(f"Detected {len(optional_feature_set)} optional feature sets.")
        print(f"Detected {len(mandatory_feature_sets)} mandatory feature sets.")
        print(f"Detected {len(exclusive_feature_sets)} exclusive feature sets.")

        if len(optional_feature_set) > 10:
            print(
                "WARNING: The number of optional feature sets is high: "
                + f"{len(optional_feature_set)}"
            )

        bitmap = 2 ** len(optional_feature_set) - 1
        possible_combinations: List[FeatureCombination] = []

        for i in range(bitmap + 1):
            if len(mandatory_feature_sets) == 0 and i == 0:
                continue
            combination_name: str = ""
            combination_features: List[str] = []

            for mandatory_set in mandatory_feature_sets:
                combination_name += f"{mandatory_set.name}_"
                combination_features.extend(mandatory_set.features)

            for j, optional_set in enumerate(optional_feature_set):
                if i & (1 << j):
                    combination_name += f"{optional_set.name}_"
                    combination_features.extend(optional_set.features)

            possible_combinations.append(
                FeatureCombination(
                    name=combination_name, features=list(set(combination_features))
                )
            )

        possible_combinations.extend(exclusive_feature_sets)

        print(f"Generated {len(possible_combinations)} possible feature combinations.")

        return possible_combinations


from dataclasses import dataclass
from typing import List, Literal, Optional
from sklearn.base import BaseEstimator
from sklearn.ensemble import (
    AdaBoostClassifier,
    AdaBoostRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import (
    LogisticRegression,
    PassiveAggressiveClassifier,
    PassiveAggressiveRegressor,
    Ridge,
    RidgeClassifier,
    SGDClassifier,
    SGDRegressor,
)
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC
from lightgbm import LGBMClassifier, LGBMRegressor
from xgboost import XGBClassifier, XGBRegressor
from catboost import CatBoostClassifier, CatBoostRegressor

RANDOM_STATE = 42


@dataclass
class ModelManager:
    task: Literal["classification", "regression"]

    def get_models(
        self,
        processes: int,
        use_models: Optional[List[str]] = None,
    ) -> List[BaseEstimator]:
        # --- TODO ---
        # Investigate the speed of the KNeighborsClassifier, it seems that it is incredibly slow or something is
        # wrong with the implementation.

        if use_models is None:
            use_models = ["ridge", "lgbm", "xgb"]

        job_count = processes if processes is not None else -1

        if self.task == "classification":
            models: List[BaseEstimator] = []

            all_models = [
                RidgeClassifier(random_state=RANDOM_STATE),
                LGBMClassifier(n_jobs=job_count, verbosity=-1, random_state=RANDOM_STATE),  # type: ignore
                XGBClassifier(n_jobs=job_count, random_state=RANDOM_STATE),
                AdaBoostClassifier(
                    algorithm="SAMME",
                    estimator=LGBMClassifier(n_jobs=job_count, verbosity=-1),
                    random_state=RANDOM_STATE,
                ),
                SVC(random_state=RANDOM_STATE),
                RandomForestClassifier(n_jobs=job_count, random_state=RANDOM_STATE),
                KNeighborsClassifier(
                    metric="cosine", n_jobs=1
                ),  # --- SUPPORTS MULTIPLE JOBS ---
                CatBoostClassifier(
                    verbose=False,
                    thread_count=job_count,
                    allow_writing_files=False,
                    random_state=RANDOM_STATE,
                ),
                SGDClassifier(
                    verbose=0,
                    random_state=RANDOM_STATE,
                    shuffle=False,
                    loss="modified_huber",
                ),
                PassiveAggressiveClassifier(random_state=RANDOM_STATE, shuffle=False),
                LogisticRegression(
                    random_state=RANDOM_STATE
                ),  # --- SUPPORTS MULTIPLE JOBS ---
                HistGradientBoostingClassifier(verbose=0, random_state=RANDOM_STATE),
            ]

            for model_name in use_models:
                for model in all_models:
                    if model_name.lower() in model.__class__.__name__.lower():
                        models.append(model)

            return models

        elif self.task == "regression":
            models: List[BaseEstimator] = []

            all_models = [
                Ridge(random_state=RANDOM_STATE),
                LGBMRegressor(n_jobs=job_count, verbosity=-1, random_state=RANDOM_STATE),  # type: ignore
                XGBRegressor(n_jobs=job_count, random_state=RANDOM_STATE),
                AdaBoostRegressor(
                    loss="linear",
                    estimator=LGBMClassifier(n_jobs=job_count, verbosity=-1),
                    random_state=RANDOM_STATE,
                ),
                RandomForestRegressor(n_jobs=job_count, random_state=RANDOM_STATE),
                KNeighborsRegressor(
                    metric="cosine", n_jobs=1
                ),  # --- SUPPORTS MULTIPLE JOBS ---
                CatBoostRegressor(
                    verbose=False,
                    thread_count=job_count,
                    allow_writing_files=False,
                    random_state=RANDOM_STATE,
                ),
                SGDRegressor(verbose=0, random_state=RANDOM_STATE, shuffle=False),
                PassiveAggressiveRegressor(random_state=RANDOM_STATE, shuffle=False),
                HistGradientBoostingRegressor(verbose=0, random_state=RANDOM_STATE),
            ]

            for model_name in use_models:
                for model in all_models:
                    if model_name.lower() in model.__class__.__name__.lower():
                        models.append(model)

            return models

        else:
            raise ValueError(
                "Bro. You had one job of selecting a proper task name and you failed..."
            )


@dataclass
class HyperOptCombination:
    name: str
    model: BaseEstimator
    feature_combination: FeatureCombination


@dataclass
class HyperOptManager:
    feature_manager: FeatureManager
    models: List[BaseEstimator]

    def get_model_combinations(self) -> List[HyperOptCombination]:
        all_feature_combinations: List[FeatureCombination] = (
            self.feature_manager.get_all_possible_feature_combinations()
        )

        hyper_opt_model_combinations: List[HyperOptCombination] = [
            HyperOptCombination(
                name=f"{model.__class__.__name__}" + f"_{combination.name}",
                model=clone(model),
                feature_combination=combination,
            )
            for model in self.models
            for combination in all_feature_combinations
        ]

        return hyper_opt_model_combinations


class HyperOptResultDict(TypedDict):
    name: str
    model: BaseEstimator
    features: List[str]
    params: Dict[str, Any]
    score: float
    n_trials: int
    metadata: Optional[Dict]


@dataclass
class TrialParamWrapper:
    """A class that is to help the creation of the trial parameters."""

    def _get_ridge_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "alpha": trial.suggest_float("alpha", 1e-3, 1000, log=True),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
        }

    def _get_random_forest_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 3, 20),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
            "max_features": trial.suggest_categorical(
                "max_features", [None, "sqrt", "log2"]
            ),
        }

    def _get_kneighbors_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_neighbors": trial.suggest_int("n_neighbors", 3, 50),
            "weights": trial.suggest_categorical("weights", ["uniform", "distance"]),
            "p": trial.suggest_int("p", 1, 5),
        }

    def _get_svc_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "C": trial.suggest_float("C", 1e-3, 10, log=True),
            "kernel": trial.suggest_categorical(
                "kernel", ["linear", "poly", "rbf", "sigmoid"]
            ),
            "gamma": trial.suggest_categorical("gamma", ["scale", "auto"]),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
        }

    def _get_lgbm_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "max_depth": trial.suggest_int("max_depth", 3, 20),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 50),
            "min_child_weight": trial.suggest_float(
                "min_child_weight", 1e-3, 100, log=True
            ),
            "subsample": trial.suggest_float("subsample", 0.1, 1),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.1, 1),
            "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 100, log=True),
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 100, log=True),
        }

    def _get_xgb_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int(
                "n_estimators", 100, 1200, step=50
            ),  # Number of trees in the ensemble
            "max_depth": trial.suggest_int(
                "max_depth", 3, 20
            ),  # Maximum depth of each tree
            "learning_rate": trial.suggest_float(
                "learning_rate", 0.01, 0.3, log=True
            ),  # Learning rate
            "subsample": trial.suggest_float(
                "subsample", 0.5, 1.0
            ),  # Subsample ratio of the training instances
            "colsample_bytree": trial.suggest_float(
                "colsample_bytree", 0.5, 1.0
            ),  # Subsample ratio of columns when constructing each tree
            "gamma": trial.suggest_float(
                "gamma", 0.01, 10.0, log=True
            ),  # Minimum loss reduction required to make a further partition on a leaf node of the tree
            "reg_alpha": trial.suggest_float(
                "reg_alpha", 1e-8, 100.0, log=True
            ),  # L1 regularization term on weights
            "reg_lambda": trial.suggest_float(
                "reg_lambda", 1e-8, 100.0, log=True
            ),  # L2 regularization term on weights
            "min_child_weight": trial.suggest_float(
                "min_child_weight", 1, 100, log=True
            ),  # Minimum sum of instance weight (hessian) needed in a child
        }

    def _get_catboost_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            # Number of boosting rounds
            "iterations": trial.suggest_int("iterations", 100, 1000),
            "depth": trial.suggest_int("depth", 4, 16),  # Depth of trees
            # Learning rate
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1.0, log=True),
            # L2 regularization term
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-3, 10.0, log=True),
            # Bagging temperature
            "bagging_temperature": trial.suggest_float("bagging_temperature", 0.0, 1.0),
            # Number of splits for numerical features
            "border_count": trial.suggest_int("border_count", 32, 255),
            # Balancing of positive and negative weights
            "scale_pos_weight": trial.suggest_float("scale_pos_weight", 0.0, 10.0),
            # Randomness in tree-building process
            "random_strength": trial.suggest_float("random_strength", 0.0, 10.0),
            # Use one-hot encoding for features with max size
            "one_hot_max_size": trial.suggest_int("one_hot_max_size", 2, 10),
            # Random subspace method for feature selection
            "rsm": trial.suggest_float("rsm", 0.5, 1.0),
            # Overfitting detector type
            "od_type": trial.suggest_categorical("od_type", ["IncToDec", "Iter"]),
            # Number of iterations to wait for the overfitting detector
            "od_wait": trial.suggest_int("od_wait", 10, 50),
        }

    def _get_adaboost_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1, log=True),
        }

    def _get_sgd_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "alpha": trial.suggest_float("alpha", 1e-3, 1.0, log=True),
            "l1_ratio": trial.suggest_float("l1_ratio", 0.0, 1.0),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
            "learning_rate": trial.suggest_categorical(
                "learning_rate", ["constant", "optimal", "invscaling", "adaptive"]
            ),
            "eta0": trial.suggest_float("eta0", 1e-6, 1e-1, log=True),
            "max_iter": trial.suggest_int("max_iter", 500, 10000),
            # "shuffle": trial.suggest_categorical("shuffle", [True, False]),
            "power_t": trial.suggest_float("power_t", 0.1, 1.0),
            "validation_fraction": trial.suggest_float("validation_fraction", 0.1, 0.5),
            "n_iter_no_change": trial.suggest_int("n_iter_no_change", 5, 50),
        }

    def _get_passive_agressive_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "C": trial.suggest_float("C", 1e-3, 1.0, log=True),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
            "validation_fraction": trial.suggest_float("validation_fraction", 0.1, 0.5),
            "n_iter_no_change": trial.suggest_int("n_iter_no_change", 5, 50),
            # "shuffle": trial.suggest_categorical("shuffle", [True, False]),
        }

    def _get_logistic_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "C": trial.suggest_float("C", 1e-3, 1.0, log=True),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
            "solver": trial.suggest_categorical(
                "solver", ["newton-cg", "lbfgs", "liblinear", "sag", "saga"]
            ),
            "max_iter": trial.suggest_int("max_iter", 100, 1000),
        }

    def _get_hist_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1, log=True),
            "max_iter": trial.suggest_int("max_iter", 100, 1000),
            "max_leaf_nodes": trial.suggest_int("max_leaf_nodes", 31, 255),
            "max_depth": trial.suggest_int("max_depth", 3, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
            "l2_regularization": trial.suggest_float("l2_regularization", 1e-3, 1.0),
            "max_bins": trial.suggest_int("max_bins", 2, 255),
            "tol": trial.suggest_float("tol", 1e-5, 1e-1, log=True),
        }

    def _get_nncm_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        return {
            "n_layers": trial.suggest_int("n_layers", 1, 10),
            "window": trial.suggest_int("window", 1, 20),
            "learning_rate": trial.suggest_float("learning_rate", 1e-3, 1, log=True),
            "n_epochs": trial.suggest_int("n_epochs", 10, 100),
            "batch_size": trial.suggest_int("batch_size", 1, 100),
            "dropout": trial.suggest_float("dropout", 0.0, 0.5),
            "activation": trial.suggest_categorical(
                "activation", ["relu", "tanh", "sigmoid"]
            ),
            "positive_class_threshold": trial.suggest_float(
                "positive_class_threshold", 0.5, 0.7
            ),
        }

    def get_params(self, model_name: str, trial: optuna.Trial) -> Dict[str, Any]:
        if "ridge" in model_name.lower():
            return self._get_ridge_params(trial)

        elif "randomforest" in model_name.lower():
            return self._get_random_forest_params(trial)

        elif "kneighbors" in model_name.lower():
            return self._get_kneighbors_params(trial)

        elif "svc" in model_name.lower():
            return self._get_svc_params(trial)

        elif "lgbm" in model_name.lower():
            return self._get_lgbm_params(trial)

        elif "xgb" in model_name.lower():
            return self._get_xgb_params(trial)

        elif "catboost" in model_name.lower():
            return self._get_catboost_params(trial)

        elif "adaboost" in model_name.lower():
            return self._get_adaboost_params(trial)

        elif "sgd" in model_name.lower():
            return self._get_sgd_params(trial)

        elif "minibatchsgd" in model_name.lower():
            return self._get_sgd_params(trial)

        elif "passive" in model_name.lower():
            return self._get_passive_agressive_params(trial)

        elif "logistic" in model_name.lower():
            return self._get_logistic_params(trial)

        elif "hist" in model_name.lower():
            return self._get_hist_params(trial)
        elif "neuralnetworkcustommodel" in model_name.lower():
            return self._get_nncm_params(trial)
        else:
            raise ValueError(f"Model {model_name} not supported.")


def calculate_metric(
    y_true: pd.Series, y_pred: pd.Series, metric: str = "rmse"
) -> float:
    if metric == "rmse":
        return np.sqrt(np.mean((y_true - y_pred) ** 2))
    elif metric == "mae":
        return np.mean(np.abs(y_true - y_pred))
    elif metric == "mse":
        return np.mean((y_true - y_pred) ** 2)
    else:
        raise ValueError(f"Metric {metric} not supported.")


CREATE_OBJECTIVE_TYPE = Callable[
    [pd.DataFrame, pd.DataFrame | pd.Series, HyperOptCombination],
    Callable[[optuna.Trial], float],
]


@dataclass
class EarlyStoppingCallback:
    name: str
    patience: int
    min_percentage_improvement: float = 0.0
    best_value: Optional[float] = None
    no_improvement_count: int = 0

    def __call__(self, study: optuna.Study, trial: optuna.Trial):
        # Get the current best value
        current_best_value = study.best_value

        # Check if the best value has improved
        if self.best_value is None or current_best_value > self.best_value * (
            1.0 + self.min_percentage_improvement
        ):
            self.best_value = current_best_value
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1

        # Stop study if there has been no improvement for `self.patience` trials
        if self.no_improvement_count >= self.patience:
            print(
                f"Early stopping the study: {self.name} due to "
                + f"no {self.min_percentage_improvement * 100}"
                + "% improvement for "
                + f"{self.patience} trials | on trial: {trial.number}"
            )
            study.stop()


def get_existing_trials_info(
    trials: List[optuna.trial.FrozenTrial], min_percentage_improvement: float
) -> Tuple[int, float | None]:
    no_improvement_count = 0
    best_value = None

    for trial in trials:

        if best_value is None or (
            trial.value is not None
            and trial.value > best_value * (1.0 + min_percentage_improvement)
        ):
            best_value = trial.value
            no_improvement_count = 0
        elif trial.value is not None:
            no_improvement_count += 1
        elif trial.value is None:
            print(f"WARNING: Trial {trial.number} has no value")

    return no_improvement_count, best_value


def save_hyper_result(
    trail: optuna.trial.FrozenTrial,
    model_combination: HyperOptCombination,
    output_dir_path: Path,
    hyper_opt_prefix: str,
    model_run: str,
    study: optuna.study.Study,
    metadata: Optional[Dict] = None,
    suffix: str = "",
) -> None:
    best_params = trail.params
    best_score = trail.value
    best_model = clone(model_combination.model).set_params(**best_params)

    result = HyperOptResultDict(
        name=model_combination.name,
        score=best_score,  # type: ignore
        params=best_params,
        model=best_model,
        features=model_combination.feature_combination.features,
        n_trials=len(study.trials),
        metadata=metadata,
    )

    os.makedirs(output_dir_path / f"{hyper_opt_prefix}{model_run}", exist_ok=True)

    try:
        results_path = Path(
            f"{output_dir_path}/{hyper_opt_prefix}{model_run}/{model_combination.name}{suffix}.pkl"
        )

        pickle.dump(result, open(results_path, "wb"))
    except Exception as e:
        print(
            f"ERROR: Error saving model combination {model_combination.name}{suffix}: {e}"
        )
        raise e


def optimize_model_and_save(
    model_run: str,
    direction: str,
    model_combination: HyperOptCombination,
    n_optimization_trials: int,
    n_patience: int,
    min_percentage_improvement: float,
    create_objective_func: CREATE_OBJECTIVE_TYPE,
    X: pd.DataFrame,
    y: pd.Series,
) -> None:
    X = X.copy()
    y = y.copy()

    combination_name = model_combination.name
    print(f"Optimizing model combination: {combination_name}")
    output_dir_path = Path(os.getcwd()) / "output"
    study_prefix = "study_"
    hyper_opt_prefix = "hyper_"
    os.makedirs(output_dir_path / f"{study_prefix}{model_run}", exist_ok=True)

    sql_path = Path(
        f"{output_dir_path}/{study_prefix}{model_run}/{combination_name}.db"
    )

    # Create an Optuna study for hyperparameter optimization
    study = optuna.create_study(
        direction=direction,
        study_name=f"{model_combination.name}",
        load_if_exists=True,
        storage=f"sqlite:///{sql_path}",
    )

    no_improvement_count, best_value = get_existing_trials_info(
        study.get_trials(), min_percentage_improvement
    )

    early_stopping = EarlyStoppingCallback(
        name=model_combination.name,
        patience=n_patience,
        min_percentage_improvement=min_percentage_improvement,
        best_value=best_value,
        no_improvement_count=no_improvement_count,
    )

    study.optimize(
        # func=create_objective_func(X, y, model_combination, n_cv),
        func=create_objective_func(X, y, model_combination),
        n_trials=n_optimization_trials,
        callbacks=[early_stopping],  # type: ignore
        # n_jobs=mp.cpu_count(),
    )

    trials = study.get_trials()
    completed_trails = [
        trial
        for trial in trials
        if trial.state == optuna.trial.TrialState.COMPLETE and trial.value is not None
    ]

    sorted_trials = sorted(
        completed_trails, key=lambda trial: trial.value, reverse=direction == "maximize"  # type: ignore
    )

    save_hyper_result(
        trail=sorted_trials[0],
        model_combination=model_combination,
        output_dir_path=output_dir_path,
        hyper_opt_prefix=hyper_opt_prefix,
        model_run=model_run,
        study=study,
        metadata={"score": sorted_trials[0].value},
    )


import multiprocessing as mp


def create_objective(
    X: pd.DataFrame, y: pd.Series, model_combination: HyperOptCombination
) -> Callable[[optuna.Trial], float]:

    model = model_combination.model

    def objective(trial: optuna.Trial) -> float:

        params = TrialParamWrapper().get_params(
            model_combination.model.__class__.__name__, trial=trial
        )

        X_pipeline = create_pipeline(
            estimator=clone(model).set_params(**params),
            features_in=model_combination.feature_combination.features,
            pandas_output=True,
        )
        y_pipeline = CreateYPipeline(
            lower_bound=10,
            upper_bound=90,
        )

        try:

            kfold = KFold(n_splits=5, shuffle=True, random_state=42)

            fold_scores = []

            for train_index, test_index in kfold.split(X):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]

                X_pipeline.fit(X_train, y_train)
                y_pipeline.fit_transform(y_train)

                y_pred = X_pipeline.predict(X_test)

                fold_score = calculate_metric(y_test, y_pred, metric="rmse")
                fold_scores.append(fold_score)

            score = np.mean(fold_scores)

        except Exception as e:
            print(f"Error in pipeline: {e}")
            score = np.inf

        return score

    return objective


def engineer_combinations_wrapper(
    use_models: Optional[List[str]] = None,
    processes: Optional[int] = None,
) -> List[FeatureCombination]:
    if processes is None:
        processes = mp.cpu_count()

    # THOSE FEATURES ARE NOT GONNA BE USED for X
    """
    [
    
        "timestamp",
        "wipes_per_bm"
    ]
    """

    feature_sets: List[FeatureSet] = [
        FeatureSet(
            name="toilet_features",
            features=[
                "stool_color",
                "stool_consistency",
                "toilet_method",
                "meds_affecting_gut",
                "smell_intensity",
            ],
            is_optional=True,
        ),
        FeatureSet(
            name="personal_features",
            features=[
                "age",
                "gender",
                "height",
                "weight",
                "sleep_hours",
                "activity_level",
            ],
            is_optional=True,
        ),
        FeatureSet(
            name="food_features",
            features=[
                "hydration_level",
                "fiber_grams",
                "fat_grams",
                "spiciness",
                "weekly_greasy_meals",
                "dairy_freq",
                "processed_servings",
                "fv_servings",
                "weekly_bms",
                "caffeinated_beverages_per_day",
            ],
            is_optional=True,
        ),
    ]

    feature_manager = FeatureManager(feature_sets=feature_sets)

    model_manager = ModelManager(task="regression")

    hyper_manager = HyperOptManager(
        feature_manager=feature_manager,
        models=model_manager.get_models(
            processes=processes,
            use_models=use_models,
        ),
    )

    return hyper_manager.get_model_combinations()


def hyperopt(
    model_run: str,
    processes: Optional[int] = None,
    n_optimization_trials: int = 40,
    n_patience: int = 10,
    min_percentage_improvement: float = 0.01,
) -> None:

    combinations = engineer_combinations_wrapper(
        processes=processes, use_models=["ridge"]
    )

    X_raw = df.drop(columns=["wipes_per_bm"]).copy()
    y_raw = df["wipes_per_bm"].copy()

    # NOTE: We decided to remove all "joke" submissions from our data
    y = pd.to_numeric(y_raw.copy().loc[~clean_short_open_numerical_cols(y_raw).isna()])
    X = X_raw.copy().loc[y.index]

    for i, model_combination in enumerate(combinations):
        print(f"Combination {i}: {model_combination.name}")
        optimize_model_and_save(
            model_run=model_run,
            direction="minimize",
            model_combination=model_combination,
            n_optimization_trials=n_optimization_trials,
            n_patience=n_patience,
            min_percentage_improvement=min_percentage_improvement,
            create_objective_func=create_objective,
            X=X,
            y=y,
        )


def load_hyper_opt_results(
    model_run: str,
    output_dir_path: Path,
    hyper_opt_prefix: str,
) -> List[HyperOptResultDict]:
    print(f"Loading hyper opt results for run {model_run}...")

    hyper_opt_results_dir_path = output_dir_path / f"{hyper_opt_prefix}{model_run}"

    if not hyper_opt_results_dir_path.exists():
        print(f"ERROR: Directory {hyper_opt_results_dir_path} does not exist.")
        return []

    print(f"Directory {hyper_opt_results_dir_path} exists.")

    hyper_opt_results = []

    for file_path in hyper_opt_results_dir_path.iterdir():
        if file_path.is_file() and file_path.suffix == ".pkl":
            print(f"Loading {file_path}...")
            result = cast(HyperOptResultDict, pickle.load(open(file_path, "rb")))
            result["name"] = file_path.stem
            hyper_opt_results.append(result)

    print(f"Loaded {len(hyper_opt_results)} hyper opt results.")

    return hyper_opt_results


def setup_analysis():
    hyper_opt_results = load_hyper_opt_results(
        model_run=model_run,
        output_dir_path=Path(os.getcwd()) / "output",
        hyper_opt_prefix="hyper_",
    )
    results_dict_list = [
        {**result, **result["metadata"]} for result in hyper_opt_results
    ]

    results_df = pd.DataFrame([result for result in results_dict_list])
    results_df = results_df.sort_values("score", ascending=True)
    results_df.to_csv(
        Path(os.getcwd()) / "output" / f"{model_run}_results.csv", index=False
    )

    return results_df, hyper_opt_results


import joblib
from pprint import pprint as pp
import pickle
import cloudpickle as cp


def save_singular_best():

    X_raw = df.drop(columns=["wipes_per_bm"]).copy()
    y_raw = df["wipes_per_bm"].copy()

    # NOTE: We decided to remove all "joke" submissions from our data
    y = pd.to_numeric(y_raw.copy().loc[~clean_short_open_numerical_cols(y_raw).isna()])
    X = X_raw.copy().loc[y.index]

    singular_best_hyper_opt_result = sorted(
        hyper_opt_results,
        key=lambda x: x["score"],
        reverse=False,
    )[0]
    singular_best_hyper_opt_result
    pp(singular_best_hyper_opt_result)

    hot_fix_features = [
        "stool_color",
        "stool_consistency",
        "toilet_method",
        "meds_affecting_gut",
        "smell_intensity",
        "age",
        "gender",
        "height",
        "weight",
        "sleep_hours",
        "activity_level",
        "hydration_level",
        "fiber_grams",
        "fat_grams",
        "spiciness",
        "weekly_greasy_meals",
        "dairy_freq",
        "processed_servings",
        "fv_servings",
        "weekly_bms",
        "caffeinated_beverages_per_day",
    ]

    singular_estimator_pipeline = create_pipeline(
        estimator=singular_best_hyper_opt_result["model"],
        features_in=hot_fix_features,
        pandas_output=True,
    )

    singular_estimator_pipeline.fit(X, y)

    joblib.dump(
        singular_estimator_pipeline,
        Path(os.getcwd()) / "estimator_joblib.pkl",
    )
    pickle.dump(
        singular_estimator_pipeline,
        open(Path(os.getcwd()) / "estimator_pickle.pkl", "wb"),
    )

    cp.dump(
        singular_estimator_pipeline,
        open(Path(os.getcwd()) / "estimator_cloudpickle.pkl", "wb"),
    )

    print(
        f"Singular best estimator pipeline saved to {Path(os.getcwd()) / 'estimator_joblib.pkl'}"
    )


if __name__ == "__main__":

    df = pd.read_csv("synthetic_bowel_movements.csv")
    df.head()

    column_mapping = {
        "What is your age?": "age",
        "How would you rate the typical smell intensity of your stool?": "smell_intensity",
        "On average, how many hours of sleep do you get per night?": "sleep_hours",
        "Timestamp": "timestamp",
        "What is your gender?": "gender",
        "Height (cm)": "height",
        "Weight (kg)": "weight",
        "Hydration Level": "hydration_level",
        "How active are you physically on average?": "activity_level",
        "Are you currently taking any medication that affects digestion or bowel movements?": "meds_affecting_gut",
        "How much dietary fibers do you eat daily?": "fiber_grams",
        "How much fat do you consume daily?": "fat_grams",
        "How spicy is your typical diet?": "spiciness",
        " How many meals with greasy or fried food do you eat per week?": "weekly_greasy_meals",
        "Do you regularly consume dairy products (milk, cheese, yogurt)?": "dairy_freq",
        "On average, how many servings of processed food do you eat per day?": "processed_servings",
        "On average, how many servings of fruits and vegetables do you eat per day?": "fv_servings",
        "What type of toilet paper or wiping method do you usually use?": "toilet_method",
        "How would you describe your typical stool consistency?": "stool_consistency",
        "What is the most common color of your stool?": "stool_color",
        'How many times do you go to the toilet for the number "2" in a week?': "weekly_bms",
        "How many caffeinated beverages (coffee, tea, energy drinks) do you consume per day?": "caffeinated_beverages_per_day",
        "On average, how many wipes or sheets of toilet paper do you use per bowel movement?": "wipes_per_bm",
    }

    # Apply the mapping
    df.rename(columns=column_mapping, inplace=True)
    df.head()

    # print(json.dumps(list(df.columns), indent=4))
    # model_run = "__initial_run__"

    # hyperopt(
    #     model_run=model_run,
    #     processes=None,
    #     n_optimization_trials=40,
    #     n_patience=10,
    #     min_percentage_improvement=0.01,
    # )
    model_run = "__initial_run__"
    results_df, hyper_opt_results = setup_analysis()
    save_singular_best()

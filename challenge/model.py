import logging
import os
import pickle
import warnings
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from challenge.enums import DayTime

DAY_MONTH_FMT = "%d-%b"
HOUR_MIN_FMT = "%H:%M"
FULL_DATE_FMT = "%Y-%m-%d %H:%M:%S"

DATE_O = "Fecha-O"
DATE_I = "Fecha-I"
PERIOD_DAY = "period_day"
HIGH_SEASON = "high_season"
MIN_DIFF = "min_diff"
DELAY = "delay"
OPERA = "OPERA"
FLIGHT_TYPE = "TIPOVUELO"
MONTH = "MES"

class DelayModel:
    def __init__(self):
        self.model_path = Path(os.getcwd(), "delay_model.pkl")
        self._model = self._load_model()
        self.unfiltered_features: pd.DataFrame = None
        self._target_column: str = None
        self.top_10_features: List[str] = [
            "OPERA_Latin American Wings", "MES_7", "MES_10", "OPERA_Grupo LATAM",
            "MES_12", "TIPOVUELO_I", "MES_4", "MES_11", "OPERA_Sky Airline",
            "OPERA_Copa Air",
        ]
        self.dataset_cols: List[str] = [
            "Fecha-I", "Vlo-I", "Ori-I", "Des-I", "Emp-I", "Fecha-O", "Vlo-O", "Ori-O",
            "Des-O", "Emp-O", "DIA", "MES", "AÑO", "DIANOM", "TIPOVUELO", "OPERA",
            "SIGLAORI", "SIGLADES",
        ]
        self.derived_cols: List[str] = ["period_day", "high_season", "min_diff", "delay"]

    @staticmethod
    def _get_high_season(date: str) -> int:
        year_date = int(date.split("-")[0])
        date = datetime.strptime(date, FULL_DATE_FMT)
        ranges = [
            ("15-Dec", "31-Dec"), ("1-Jan", "3-Mar"),
            ("15-Jul", "31-Jul"), ("11-Sep", "30-Sep"),
        ]

        for range_min, range_max in ranges:
            range_min = datetime.strptime(range_min, DAY_MONTH_FMT).replace(year=year_date)
            range_max = datetime.strptime(range_max, DAY_MONTH_FMT).replace(year=year_date)

            if range_min <= date <= range_max:
                return 1

        return 0

    @staticmethod
    def _get_period_day(date: str) -> str:
        date_time = datetime.strptime(date, FULL_DATE_FMT).time()
        intervals = [
            ("05:00", "11:59"), ("12:00", "18:59"),
            ("19:00", "23:59"), ("00:00", "4:59"),
        ]

        for interval_min, interval_max in intervals:
            interval_min = datetime.strptime(interval_min, HOUR_MIN_FMT).time()
            interval_max = datetime.strptime(interval_max, HOUR_MIN_FMT).time()

            if interval_min <= date_time <= interval_max:
                return DayTime.MORNING.value if interval_min <= date_time <= interval_max else DayTime.NIGHT.value

    @staticmethod
    def _get_min_diff(data: pd.DataFrame) -> int:
        date_o = datetime.strptime(data[DATE_O], FULL_DATE_FMT)
        date_i = datetime.strptime(data[DATE_I], FULL_DATE_FMT)
        min_diff = int((date_o - date_i).total_seconds() / 60)
        return min_diff

    def _check_columns_exists(self, data: pd.DataFrame) -> bool:
        return all(col in data.columns for col in self.dataset_cols)

    def _check_valid_target(self, target_column: str) -> bool:
        return target_column in [*self.dataset_cols, *self.derived_cols]

    def _generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        features = pd.get_dummies(data[OPERA], prefix=OPERA)
        features = pd.concat([features, pd.get_dummies(data[FLIGHT_TYPE], prefix=FLIGHT_TYPE)], axis=1)
        features = pd.concat([features, pd.get_dummies(data[MONTH], prefix=MONTH)], axis=1)
        return features.copy()

    def _generate_derived_features(self, data: pd.DataFrame) -> pd.DataFrame:
        threshold_in_minutes = 15
        data[PERIOD_DAY] = data[DATE_I].apply(self._get_period_day)
        data[HIGH_SEASON] = data[DATE_I].apply(self._get_high_season)
        data[MIN_DIFF] = data.apply(self._get_min_diff, axis=1)
        data[DELAY] = (data[MIN_DIFF] > threshold_in_minutes).astype(int)
        return data.copy()

    def _combine_features_to_top_format(self, data: pd.DataFrame) -> pd.DataFrame:
        top_features = pd.DataFrame(
            0, index=np.arange(data.shape[0]), columns=self.top_10_features
        )
        for col in data.columns:
            if col in top_features.columns:
                top_features[col] = top_features[col] | data[col]
        return top_features

    def _save_model(self, model: LogisticRegression) -> Path:
        with open(self.model_path, "wb") as model_file:
            pickle.dump(model, model_file)
        return self.model_path

    def _load_model(self) -> Union[LogisticRegression, None]:
        loaded_model = None
        if self.model_path.is_file():
            with open(self.model_path, "rb") as model_file:
                loaded_model = pickle.load(model_file)
        return loaded_model

    def preprocess(
        self, data: pd.DataFrame, target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        if self._check_columns_exists(data) and self._check_valid_target(
            target_column
        ):
            df_with_derived_feats = self._generate_derived_features(data)
            features = self._generate_features(df_with_derived_feats)
            self.unfiltered_features = features.copy()
            self._target_column = target_column
            return features[self.top_10_features], data[[target_column]]
        else:
            serving_features = self._generate_features(data)
            top_10_features_df = self._combine_features_to_top_format(
                serving_features
            )
            return top_10_features_df[self.top_10_features]

    def _returns_scale_values(self, target: pd.DataFrame) -> Tuple[int, int]:
        _, _, y_train, _ = train_test_split(
            self.unfiltered_features, target, test_size=0.33, random_state=42
        )
        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])
        return n_y0, n_y1

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        n_y0, n_y1 = self._returns_scale_values(target[self._target_column].copy())
        x_train, _, y_train, _ = train_test_split(
            features, target, test_size=0.33, random_state=42
        )
        reg_model = LogisticRegression(
            class_weight={1: n_y0 / len(y_train), 0: n_y1 / len(y_train)}
        )
        reg_model.fit(x_train, np.ravel(y_train))
        self._model = reg_model
        self._save_model(reg_model)

    def predict(self, features: pd.DataFrame) -> List[int]:
        preds = self._model.predict(features)
        return preds.tolist()

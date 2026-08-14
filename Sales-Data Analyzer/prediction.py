"""
prediction.py
Simple linear regression on monthly sales totals to forecast future
months, with standard evaluation metrics.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


def train_model(monthly_series):
    """
    Trains a linear regression model where X = month index (0, 1, 2, ...)
    and y = total sales for that month. Returns the fitted model plus
    the X/y arrays used, for evaluation.
    """
    X = np.arange(len(monthly_series)).reshape(-1, 1)
    y = monthly_series.values

    model = LinearRegression()
    model.fit(X, y)

    return model, X, y


def evaluate_model(model, X, y):
    """Returns R², MAE, and RMSE for the fitted model on the training data."""
    predictions = model.predict(X)
    r2 = r2_score(y, predictions)
    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))

    return {
        "r2_score": round(r2, 3),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
    }


def forecast_future_months(model, monthly_series, n_months=3):
    """
    Predicts the next n_months of sales beyond the last month in
    monthly_series. Returns (future_dates, predictions).
    """
    last_index = len(monthly_series) - 1
    future_X = np.arange(last_index + 1, last_index + 1 + n_months).reshape(-1, 1)
    predictions = model.predict(future_X)
    predictions = np.maximum(predictions, 0)  # sales can't be negative

    last_date = monthly_series.index[-1]
    future_dates = pd.date_range(
        start=last_date + pd.offsets.MonthEnd(1), periods=n_months, freq="ME"
    )

    return future_dates, predictions


def trend_direction(model):
    """Returns a simple human-readable trend label based on the model's slope."""
    slope = model.coef_[0]
    if slope > 50:
        return "Growing"
    elif slope < -50:
        return "Declining"
    else:
        return "Stable"

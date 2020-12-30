"""Strategies for deducing the relations between inputs and outputs in a dataset."""

from dataclasses import dataclass
from typing import Iterable, List

import pandas
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder


@dataclass
class LinearRegressionResult:
    """Result from running a linear regression model."""

    coefs: List[List[float]]
    intercept: List[float]
    score: float


def linear_regression(
    dataframe: pandas.DataFrame,
    inputs: Iterable[str],
    outputs: Iterable[str],
) -> LinearRegressionResult:
    """Extract the dataset variables columns and fit them in a linear regression model.

    Arguments:
        dataset: the dataset to run the linear regression against
        inputs: list of input variable names
        outputs: list of output variable names

    Returns:
        A result that contains the values of the coefiecients and intercepts
    """
    x = dataframe[inputs]
    y = dataframe[outputs]
    reg = LinearRegression().fit(x, y)
    coefs = reg.coef_.tolist()  # type: ignore
    intercept = reg.intercept_.tolist()  # type: ignore
    score = float(reg.score(x, y))
    return LinearRegressionResult(coefs=coefs, intercept=intercept, score=score)


@dataclass
class LogisticRegressionResult:
    """Result from running a logistic regression model."""

    outcomes: List[List[float]]
    coefs: List[List[List[float]]]
    intercepts: List[List[float]]
    score: float


def logistic_regression(
    dataframe: pandas.DataFrame,
    inputs: Iterable[str],
    outputs: Iterable[str],
) -> LogisticRegressionResult:
    """Extract the dataset variables columns and fit them in a logistic regression model.

    Arguments:
        dataset: the dataset to run the logistic regression against
        inputs: list of input variable names
        outputs: list of output variable names

    Returns:
        A result that contains the values of the coefiecients and intercepts
    """
    x = dataframe[inputs]
    y = dataframe[outputs].copy()
    encoders = [LabelEncoder() for _ in outputs]
    for encoder, output in zip(encoders, outputs):
        y[output] = encoder.fit_transform(y[output])

    reg = MultiOutputClassifier(LogisticRegression(max_iter=1000)).fit(x, y)  # type: ignore
    outcomes = [encoder.classes_.tolist() for encoder in encoders]
    coefs = [estimator.coef_.tolist() for estimator in reg.estimators_]
    intercepts = [estimator.intercept_.tolist() for estimator in reg.estimators_]
    score = float(reg.score(x, y))

    return LogisticRegressionResult(
        outcomes=outcomes,
        coefs=coefs,
        intercepts=intercepts,
        score=score,
    )

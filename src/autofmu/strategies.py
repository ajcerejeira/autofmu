"""Strategies for deducing the relations between inputs and outputs in a dataset."""

from dataclasses import dataclass
from typing import Iterable, List

import pandas
from sklearn.linear_model import LinearRegression


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
    score = reg.score(x, y)
    return LinearRegressionResult(coefs=coefs, intercept=intercept, score=score)

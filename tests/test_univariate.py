"""Tests for univariate analysis."""

import pandas as pd

from statqa.analysis.univariate import UnivariateAnalyzer
from statqa.metadata.schema import Variable


def test_numeric_univariate(sample_numeric_data: pd.Series, sample_variable: Variable):
    """Test univariate analysis on numeric data."""
    analyzer = UnivariateAnalyzer()
    result = analyzer.analyze(sample_numeric_data, sample_variable)

    assert "mean" in result
    assert "median" in result
    assert "std" in result
    assert result["n_valid"] > 0
    assert 40 < result["mean"] < 60  # Should be around 50


def test_categorical_univariate(
    sample_categorical_data: pd.Series, sample_categorical_variable: Variable
):
    """Test univariate analysis on categorical data."""
    analyzer = UnivariateAnalyzer()
    result = analyzer.analyze(sample_categorical_data, sample_categorical_variable)

    assert "mode" in result
    assert "frequencies" in result
    assert result["n_unique"] <= 3

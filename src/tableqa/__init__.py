"""
TableQA: Automatically extract structured facts from tabular datasets.

This package provides tools for:
- Parsing codebooks and metadata
- Running statistical analyses (univariate, bivariate, temporal, causal)
- Generating natural language insights
- Creating visualizations
- Generating Q/A pairs for LLM fine-tuning or RAG
"""

from tableqa.__version__ import __version__, __version_info__
from tableqa.analysis.bivariate import BivariateAnalyzer
from tableqa.analysis.causal import CausalAnalyzer
from tableqa.analysis.temporal import TemporalAnalyzer
from tableqa.analysis.univariate import UnivariateAnalyzer

# Import main public APIs
from tableqa.metadata.schema import Codebook, Variable, VariableType


__all__ = [
    "BivariateAnalyzer",
    "CausalAnalyzer",
    # Metadata
    "Codebook",
    "TemporalAnalyzer",
    # Analysis
    "UnivariateAnalyzer",
    "Variable",
    "VariableType",
    "__version__",
    "__version_info__",
]

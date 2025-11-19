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

# Import main public APIs
from tableqa.metadata.schema import Codebook, Variable, VariableType
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.analysis.bivariate import BivariateAnalyzer
from tableqa.analysis.temporal import TemporalAnalyzer
from tableqa.analysis.causal import CausalAnalyzer

__all__ = [
    "__version__",
    "__version_info__",
    # Metadata
    "Codebook",
    "Variable",
    "VariableType",
    # Analysis
    "UnivariateAnalyzer",
    "BivariateAnalyzer",
    "TemporalAnalyzer",
    "CausalAnalyzer",
]

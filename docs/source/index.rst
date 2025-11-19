StatQA Documentation
=====================

**StatQA** is a Python framework for automatically extracting structured facts, insights, and Q/A pairs from tabular datasets.

Features
--------

* **Metadata Understanding**: Parse codebooks and enrich with LLM
* **Statistical Analysis**: Univariate, bivariate, temporal, and causal analyses
* **Natural Language Insights**: Convert statistics to human-readable text
* **Q/A Generation**: Create training data for LLMs
* **Visualization**: Publication-quality plots

Quick Start
-----------

Installation::

    pip install statqa

Basic usage::

    from statqa import Codebook, UnivariateAnalyzer
    from statqa.metadata.parsers import TextParser

    # Parse codebook
    parser = TextParser()
    codebook = parser.parse("codebook.txt")

    # Run analysis
    analyzer = UnivariateAnalyzer()
    result = analyzer.analyze(data["age"], codebook.variables["age"])

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide/index
   api/index
   examples/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

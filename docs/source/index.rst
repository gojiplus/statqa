StatQA Documentation
=====================

**StatQA** is a Python framework for automatically extracting structured facts, insights, and **multimodal Q/A pairs** from tabular datasets with rich visual metadata and publication-quality plots.

Features
--------

* **Metadata Understanding**: Parse codebooks and enrich with LLM
* **Statistical Analysis**: Univariate, bivariate, temporal, and causal analyses
* **Natural Language Insights**: Convert statistics to human-readable text
* **Multimodal Q/A Generation**: Create CLIP-style visual-text pairs for AI training
* **Rich Visual Metadata**: Captions, alt-text, and visual elements for each plot
* **Publication-Quality Visualizations**: Automated plots with question-plot association mapping
* **Accessibility Support**: Full alt-text and captions for inclusive AI applications

Quick Start
-----------

Installation::

    pip install statqa

Basic usage with multimodal Q/A generation::

    from statqa import Codebook, UnivariateAnalyzer
    from statqa.metadata.parsers import TextParser
    from statqa.qa import QAGenerator

    # Parse codebook
    parser = TextParser()
    codebook = parser.parse("codebook.txt")

    # Run analysis with visualization
    analyzer = UnivariateAnalyzer()
    result = analyzer.analyze(data["age"], codebook.variables["age"])

    # Generate multimodal Q/A pairs
    qa_gen = QAGenerator()
    plot_data = {"data": data, "variables": codebook.variables, "output_path": "plots/age.png"}
    visual_metadata = qa_gen.generate_visual_metadata(result, variables=["age"], plot_data=plot_data)
    qa_pairs = qa_gen.generate_qa_pairs(result, insight, variables=["age"], visual_data=visual_metadata)

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

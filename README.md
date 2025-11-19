# StatQA

[![CI](https://github.com/gojiplus/statqa/actions/workflows/ci.yml/badge.svg)](https://github.com/gojiplus/statqa/actions/workflows/ci.yml)
[![Documentation](https://github.com/gojiplus/statqa/actions/workflows/docs.yml/badge.svg)](https://gojiplus.github.io/statqa)
[![PyPI version](https://badge.fury.io/py/statqa.svg)](https://pypi.org/project/statqa/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**StatQA** is a modern Python framework for automatically extracting structured facts, statistical insights, and Q/A pairs from tabular datasets. It converts raw columns and values into clear, human-readable statements, enabling rapid knowledge discovery, RAG corpus construction, and LLM training.

## 🎯 Key Features

- **📋 Flexible Metadata Parsing**: Parse codebooks from text, CSV, or PDF formats
- **🤖 LLM-Powered Enrichment**: Automatically infer variable types and relationships
- **📊 Comprehensive Statistical Analysis**:
  - Univariate: descriptive statistics, distribution tests, robust estimators
  - Bivariate: correlations, chi-square, group comparisons with effect sizes
  - Temporal: trend detection (Mann-Kendall), change points, year-over-year analysis
  - Causal: regression with confounding control, sensitivity analysis
- **💬 Natural Language Insights**: Convert statistics to publication-ready text
- **❓ Q/A Generation**: Create training data for LLMs with template-based and LLM-paraphrased questions
- **🔍 Provenance Tracking**: Full metadata for reproducibility (timestamps, tools, methods, analysis types)
- **📈 Publication-Quality Visualizations**: Automated plots for all analyses
- **🔬 Statistical Rigor**: Multiple testing correction, effect sizes, normality tests
- **⚡ Modern Python**: Type-safe (Pydantic), async-ready, fully typed

## 📦 Installation

### Basic Installation

```bash
pip install statqa
```

### With Optional Features

```bash
# Include LLM support (OpenAI/Anthropic)
pip install statqa[llm]

# Include PDF parsing
pip install statqa[pdf]

# Development installation
pip install statqa[dev]

# Complete installation
pip install statqa[all]
```

### From Source

```bash
git clone https://github.com/gojiplus/statqa.git
cd statqa
pip install -e ".[dev]"
```

## 🚀 Quick Start

### 1. Create a Codebook

```python
from statqa.metadata.parsers import TextParser

codebook_text = """
# Variable: age
Label: Respondent Age
Type: numeric_continuous
Units: years
Range: 18-99
Missing: -1, 999

# Variable: satisfaction
Label: Job Satisfaction
Type: categorical_ordinal
Values:
  1: Very Dissatisfied
  2: Dissatisfied
  3: Neutral
  4: Satisfied
  5: Very Satisfied
"""

parser = TextParser()
codebook = parser.parse(codebook_text)
```

### 2. Run Statistical Analyses

```python
import pandas as pd
from statqa.analysis import UnivariateAnalyzer, BivariateAnalyzer

# Load your data
data = pd.read_csv("survey_data.csv")

# Univariate analysis
analyzer = UnivariateAnalyzer()
result = analyzer.analyze(data["age"], codebook.variables["age"])

print(result)
# Output: {'mean': 42.5, 'median': 41.0, 'std': 12.3, ...}

# Bivariate analysis
biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(
    data,
    codebook.variables["age"],
    codebook.variables["satisfaction"]
)
```

### 3. Generate Natural Language Insights

```python
from statqa.interpretation import InsightFormatter

formatter = InsightFormatter()
insight = formatter.format_univariate(result)

print(insight)
# Output: "**Respondent Age**: mean=42.5, median=41.0, std=12.3, range=[18, 95]. N=1,000 [2.3% outliers]."
```

### 4. Create Q/A Pairs for LLM Training

```python
from statqa.qa import QAGenerator

qa_gen = QAGenerator(use_llm=False)  # Template-based
qa_pairs = qa_gen.generate_qa_pairs(result, insight)

for qa in qa_pairs:
    print(f"Q: {qa['question']}")
    print(f"A: {qa['answer']}")
    print(f"Provenance: {qa['provenance']}\n")
```

Each Q/A pair includes **provenance metadata** tracking:
- **When** the answer was generated (timestamp)
- **What tool** was used (statqa version)
- **What compute** was performed (analysis type, analyzer)
- **How** it was generated (template vs. LLM paraphrase)
- **Which LLM** was used (if applicable)

## 🎨 Complete Pipeline Example

```python
from statqa import Codebook, UnivariateAnalyzer
from statqa.metadata.parsers import CSVParser
from statqa.interpretation import InsightFormatter
from statqa.qa import QAGenerator
from statqa.utils.io import load_data, save_json

# 1. Parse codebook
parser = CSVParser()
codebook = parser.parse("codebook.csv")

# 2. Load data
data = load_data("data.csv")

# 3. Run analyses
analyzer = UnivariateAnalyzer()
results = analyzer.batch_analyze(data, codebook.variables)

# 4. Format insights
formatter = InsightFormatter()
for result in results:
    result["insight"] = formatter.format_insight(result)

# 5. Generate Q/A pairs
qa_gen = QAGenerator(use_llm=True, api_key="your-api-key")
qa_results = qa_gen.generate_batch(
    results,
    [r["insight"] for r in results]
)

# 6. Export for LLM fine-tuning
lines = qa_gen.export_qa_dataset(qa_results, format="openai")
with open("training_data.jsonl", "w") as f:
    f.write("\n".join(lines))
```

## 📝 Q/A Provenance Tracking

Every Q/A pair generated by StatQA includes detailed **provenance metadata** to ensure reproducibility and traceability:

```json
{
  "question": "What is the average Respondent Age?",
  "answer": "The mean age is 42.5 years (median=41.0, std=12.3).",
  "type": "descriptive",
  "provenance": {
    "generated_at": "2025-11-19T10:30:45.123456+00:00",
    "tool": "statqa",
    "tool_version": "0.1.0",
    "generation_method": "template",
    "analysis_type": "univariate",
    "analyzer": "UnivariateAnalyzer"
  }
}
```

### Provenance Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `generated_at` | ISO 8601 timestamp (UTC) | `2025-11-19T10:30:45+00:00` |
| `tool` | Software used for generation | `statqa` |
| `tool_version` | Version of statqa | `0.1.0` |
| `generation_method` | How the Q/A was created | `template`, `llm_paraphrase` |
| `analysis_type` | Statistical analysis performed | `univariate`, `bivariate`, `temporal`, `causal` |
| `analyzer` | Specific analyzer class used | `UnivariateAnalyzer`, `BivariateAnalyzer` |
| `llm_model` | LLM model (if applicable) | `gpt-4`, `claude-3-opus` |

This provenance tracking enables:
- **Reproducibility**: Recreate Q/A pairs from original data
- **Quality Control**: Filter by generation method or analysis type
- **Auditing**: Track when and how answers were computed
- **Citation**: Properly attribute computational methods in research

## 🖥️ Command-Line Interface

StatQA provides a powerful CLI for common workflows:

```bash
# Parse a codebook
statqa parse-codebook codebook.csv --output codebook.json --enrich

# Run full analysis pipeline
statqa analyze data.csv codebook.json --output-dir results/ --plots

# Generate Q/A pairs
statqa generate-qa results/all_insights.json --output qa_pairs.jsonl --llm

# Complete pipeline
statqa pipeline data.csv codebook.csv --output-dir output/ --enrich --qa
```

## 📊 Supported Analyses

### Univariate Statistics
- Central tendency: mean, median, mode
- Dispersion: std, IQR, MAD (robust)
- Distribution: skewness, kurtosis, normality tests
- Categorical: frequencies, entropy, diversity indices

### Bivariate Relationships
- **Numeric × Numeric**: Pearson/Spearman correlation, effect sizes
- **Categorical × Categorical**: Chi-square, Cramér's V
- **Categorical × Numeric**: t-tests, ANOVA, Cohen's d

### Temporal Analysis
- Trend detection: Mann-Kendall test, linear regression
- Change point detection
- Year-over-year comparisons
- Seasonal decomposition

### Causal Inference
- Regression with control variables
- Confounder identification
- Sensitivity analysis
- Treatment effect estimation

## 🔧 Advanced Features

### LLM-Powered Metadata Enrichment

```python
from statqa.metadata import MetadataEnricher

enricher = MetadataEnricher(provider="openai", api_key="your-key")
enriched_codebook = enricher.enrich_codebook(codebook)

# LLM infers variable types, suggests relationships, identifies confounders
```

### Multiple Testing Correction

```python
from statqa.utils.stats import correct_multiple_testing

p_values = [0.03, 0.01, 0.15, 0.002]
reject, corrected_p = correct_multiple_testing(p_values, method="fdr_bh")
```

### Custom Visualizations

```python
from statqa.visualization import PlotFactory

plotter = PlotFactory(style="publication", figsize=(10, 6))
fig = plotter.plot_bivariate(data, var1, var2, output_path="plot.png")
```

## 📚 Documentation

- **Full Documentation**: [https://gojiplus.github.io/statqa](https://gojiplus.github.io/statqa)
- **API Reference**: [API Docs](https://gojiplus.github.io/statqa/api/)
- **Examples**: See [examples/](examples/) directory

## 🧪 Development

### Running Tests

```bash
pytest --cov=statqa --cov-report=html
```

### Code Quality

```bash
# Linting
ruff check statqa tests

# Type checking
mypy statqa

# Formatting
black statqa tests
```

### Building Documentation

```bash
cd docs
make html
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run tests and linting
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python tools: Pydantic, pandas, statsmodels, typer
- Inspired by survey data analysis workflows (ANES, GSS, etc.)
- Statistical methods from standard social science practice

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/gojiplus/statqa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gojiplus/statqa/discussions)
- **Email**: maintainers@statqa.org

## 🗺️ Roadmap

- [ ] Support for additional codebook formats (SPSS, Stata, SAS)
- [ ] Web interface for interactive analysis
- [ ] Integration with popular survey platforms
- [ ] Advanced causal inference methods (instrumental variables, DiD)
- [ ] Automated report generation (Markdown, LaTeX, HTML)
- [ ] Cloud deployment templates

---

**Made with ❤️ for data scientists, researchers, and LLM engineers**

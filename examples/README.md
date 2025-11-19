# TableQA Examples

This directory contains examples demonstrating how to use tableqa for analyzing tabular data and generating insights.

## Quick Start

If you're new to tableqa, start here:

1. **`basic_usage.py`** - A minimal standalone script showing core functionality
2. **`simple_survey/`** - Generate synthetic survey data and run a complete analysis
3. **`iris/`** - Classic Iris dataset example (simple, well-understood data)

## Example Datasets

### `iris/`
Classic Iris flower dataset with 150 samples and 5 variables (sepal/petal measurements, species).

**Best for:** Learning the basics, understanding univariate and bivariate analysis

**Key features:**
- Small, clean dataset
- Mix of continuous and categorical variables
- Well-documented example

### `employee/`
Employee satisfaction survey data with demographics, job metrics, and attitudes.

**Best for:** Survey analysis, categorical data, group comparisons

**Key features:**
- Categorical and ordinal variables
- Multiple grouping variables (department, education)
- Real-world survey patterns

### `titanic/`
Titanic passenger survival data with demographics and ticket information.

**Best for:** Binary outcome analysis, historical data, group comparisons

**Key features:**
- Binary outcome (survival)
- Multiple predictor variables
- Missing data handling
- Real historical dataset

### `anes/`
American National Election Studies (ANES) Time Series data (1948-2020).

**Best for:** Large-scale survey analysis, political science research, advanced workflows

**Key features:**
- 70K+ rows, 1K+ variables
- PDF codebook parsing
- Comprehensive analysis pipeline
- Research-grade dataset

**Note:** Requires downloading data files (see `anes/README.md`)

### `simple_survey/`
Generate synthetic survey data and run a complete analysis pipeline.

**Best for:** Quick experimentation, learning without setup, testing workflows

**Key features:**
- No data download required
- Customizable data generation
- Complete end-to-end example
- Fast execution

## File Structure

Each example directory contains:
- `README.md` - Example-specific documentation
- `data.csv` - The dataset (except ANES, which requires download)
- `codebook.json` - Variable metadata and descriptions
- Additional outputs or scripts as needed

## Common Workflows

### 1. Load and Analyze Data

```python
import pandas as pd
from tableqa.metadata.codebook import Codebook
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.interpretation.formatter import InsightFormatter

# Load data
data = pd.read_csv('iris/data.csv')
codebook = Codebook.from_json('iris/codebook.json')

# Analyze
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

for var_name, var in codebook.variables.items():
    if var_name in data.columns:
        result = analyzer.analyze(data[var_name], var)
        insight = formatter.format_univariate(result)
        print(insight)
```

### 2. Compare Groups

```python
from tableqa.analysis.bivariate import BivariateAnalyzer

biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(
    data,
    codebook.variables['species'],  # grouping variable
    codebook.variables['sepal_length']  # outcome variable
)

if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

### 3. Generate Q/A Pairs

```python
from tableqa.qa.generator import QAGenerator

qa_gen = QAGenerator(use_llm=False)  # Template-based
qa_pairs = qa_gen.generate_qa_pairs(result, insight)

for qa in qa_pairs:
    print(f"Q: {qa['question']}")
    print(f"A: {qa['answer']}\n")
```

## Installation

```bash
# Basic installation
pip install tableqa

# With PDF support (for ANES example)
pip install tableqa[pdf]

# With LLM support (for advanced Q/A generation)
pip install tableqa[llm]

# Everything
pip install tableqa[pdf,llm]
```

## Next Steps

1. Run `basic_usage.py` to see a complete example
2. Try one of the dataset examples (iris, employee, titanic)
3. Explore the `simple_survey` for customizable synthetic data
4. Read the [full documentation](https://gojiplus.github.io/tableqa)
5. Check out the ANES example for research-grade analysis

## Support

For questions or issues:
- GitHub: https://github.com/gojiplus/tableqa/issues
- Documentation: https://gojiplus.github.io/tableqa

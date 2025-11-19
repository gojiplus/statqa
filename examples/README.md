# TableQA Examples

This directory contains examples demonstrating various features of the tableqa library.

## Quick Start

Start with `basic_usage.py` for a simple introduction to the core concepts.

## Examples Overview

### Basic Usage (`basic_usage.py`)
A standalone script showing the fundamental tableqa workflow:
- Creating codebooks from text
- Running univariate and bivariate analyses
- Generating insights and Q/A pairs

**Best for**: First-time users, understanding core concepts

### Simple Survey (`simple_survey/`)
Generate and analyze synthetic survey data.
- Quick setup (no downloads required)
- Demonstrates end-to-end pipeline
- Good for testing and experimentation

**Best for**: Learning the full pipeline, prototyping

### Iris Dataset (`iris/`)
Classic dataset with flower measurements.
- Small, well-understood dataset
- Continuous numeric variables
- Multi-class classification context

**Best for**: Testing statistical analyses, visualization

### Employee Survey (`employee/`)
Synthetic employee workplace survey.
- Mix of categorical and numeric variables
- Realistic survey structure
- Common workplace metrics

**Best for**: Understanding survey analysis, practicing with mixed data types

### Titanic Dataset (`titanic/`)
Historical passenger survival data.
- Binary outcome (survival)
- Mix of demographics and ticket information
- Well-known dataset for comparison

**Best for**: Classification analysis, survival analysis

### ANES Dataset (`anes/`)
American National Election Studies political survey (1948-2020).
- Large-scale real-world dataset
- Complex codebook with 1000+ variables
- Demonstrates advanced features

**Best for**: Production use cases, large-scale analysis, research applications

## Running Examples

### Basic Usage
```bash
python examples/basic_usage.py
```

### Simple Survey
```bash
cd examples/simple_survey
python quick_start.py
```

### Dataset Examples
```bash
# Iris
cd examples/iris
python -c "
import pandas as pd
import json
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.interpretation.formatter import InsightFormatter
from tableqa.metadata.model import Codebook

data = pd.read_csv('data.csv')
with open('codebook.json') as f:
    codebook = Codebook.from_dict(json.load(f))

analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

for var_name, variable in codebook.variables.items():
    if var_name in data.columns:
        result = analyzer.analyze(data[var_name], variable)
        print(formatter.format_univariate(result))
"
```

### ANES (Advanced)
```bash
cd examples/anes

# Step 1: Parse metadata (requires PDF files)
python parse_metadata.py \
    --codebook data/raw/anes_timeseries_cdf_codebook_var_20220916.pdf \
    --output-metadata data/anes_metadata.csv \
    --skip-questions

# Step 2: Extract insights
python extract_insights.py \
    --data-zip data/raw/anes_timeseries_cdf_csv_20220916.csv.zip \
    --metadata data/anes_metadata.csv \
    --output-dir output \
    --max-vars 50
```

## Complexity Levels

| Example | Complexity | Setup Time | Best For |
|---------|-----------|------------|----------|
| `basic_usage.py` | Beginner | < 1 min | Learning basics |
| `simple_survey/` | Beginner | < 1 min | Full pipeline |
| `iris/` | Beginner | < 1 min | Statistics |
| `employee/` | Intermediate | < 1 min | Survey analysis |
| `titanic/` | Intermediate | < 1 min | Classification |
| `anes/` | Advanced | ~10 min | Research |

## Common Workflows

### Generate Q/A Pairs
```python
from tableqa.qa.generator import QAGenerator

qa_gen = QAGenerator(use_llm=False)  # Template-based
qa_pairs = qa_gen.generate_qa_pairs(result, answer)

for qa in qa_pairs:
    print(f"Q: {qa['question']}")
    print(f"A: {qa['answer']}\n")
```

### Export Insights
```python
import json
from tableqa.utils.io import export_insights

# Save to JSON
with open('insights.json', 'w') as f:
    json.dump(insights, f, indent=2)
```

### Create Visualizations
```python
from tableqa.visualization.plots import PlotFactory

plotter = PlotFactory(style='seaborn')
plotter.plot_univariate(result, output_path='distribution.png')
plotter.plot_bivariate(result, output_path='relationship.png')
```

## File Structure

```
examples/
├── README.md              # This file
├── basic_usage.py         # Simple starting point
├── iris/                  # Iris flowers dataset
│   ├── README.md
│   ├── data.csv
│   └── codebook.json
├── employee/              # Employee survey data
│   ├── README.md
│   ├── data.csv
│   └── codebook.json
├── titanic/               # Titanic survival data
│   ├── README.md
│   ├── data.csv
│   └── codebook.json
├── anes/                  # ANES political survey (advanced)
│   ├── README.md
│   ├── parse_metadata.py
│   ├── extract_insights.py
│   ├── data/
│   └── output/
└── simple_survey/         # Synthetic survey generation
    ├── README.md
    └── quick_start.py
```

## Getting Help

- **Documentation**: https://gojiplus.github.io/tableqa
- **Issues**: https://github.com/gojiplus/tableqa/issues
- **Discussions**: https://github.com/gojiplus/tableqa/discussions

## Next Steps

1. Start with `basic_usage.py` to learn the fundamentals
2. Try `simple_survey/` for a complete workflow
3. Explore domain-specific examples (iris, employee, titanic)
4. Tackle `anes/` for advanced, real-world usage
5. Adapt examples to your own datasets

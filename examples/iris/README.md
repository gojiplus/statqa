# Iris Flowers Example

A simple example using the classic Iris flower dataset to demonstrate tableqa's core functionality.

## Dataset

The Iris dataset contains measurements of 150 iris flowers from three species:
- Sepal length and width (cm)
- Petal length and width (cm)
- Species (setosa, versicolor, virginica)

## Files

- `data.csv` - Iris flower measurements (150 rows, 5 columns)
- `codebook.json` - Variable metadata and descriptions

## Quick Start

```python
import pandas as pd
from tableqa.metadata.codebook import Codebook
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.analysis.bivariate import BivariateAnalyzer
from tableqa.interpretation.formatter import InsightFormatter

# Load data and codebook
data = pd.read_csv('data.csv')
codebook = Codebook.from_json('codebook.json')

# Analyze sepal length
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

result = analyzer.analyze(data['sepal_length'], codebook.variables['sepal_length'])
insight = formatter.format_univariate(result)
print(insight)

# Compare species by sepal length
biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(
    data,
    codebook.variables['species'],
    codebook.variables['sepal_length']
)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

## What You'll Learn

- Loading data with codebooks
- Running univariate analyses
- Running bivariate comparisons
- Formatting insights as natural language

## Next Steps

- Try the `employee` example for categorical data
- See `titanic` for a real-world survival analysis
- Check `../basic_usage.py` for a complete workflow

# Iris Flowers Dataset

A classic dataset demonstrating statqa with the famous Iris flower measurements.

## Dataset

The Iris dataset contains measurements of 150 iris flowers from three species:
- Iris setosa
- Iris versicolor
- Iris virginica

## Files

- `data.csv`: Flower measurements (sepal length, sepal width, petal length, petal width, species)
- `codebook.json`: Variable metadata and descriptions

## Usage

```python
import pandas as pd
import json
from statqa.analysis.univariate import UnivariateAnalyzer
from statqa.analysis.bivariate import BivariateAnalyzer
from statqa.interpretation.formatter import InsightFormatter
from statqa.metadata.model import Codebook

# Load data and codebook
data = pd.read_csv('data.csv')
with open('codebook.json') as f:
    codebook_dict = json.load(f)
codebook = Codebook.from_dict(codebook_dict)

# Run analyses
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

for var_name, variable in codebook.variables.items():
    if var_name in data.columns:
        result = analyzer.analyze(data[var_name], variable)
        insight = formatter.format_univariate(result)
        print(insight)
```

## Next Steps

- Run bivariate analyses to explore relationships between measurements
- Generate Q/A pairs from the insights
- Compare measurements across species

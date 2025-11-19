# Titanic Survival Dataset

The famous Titanic dataset demonstrating tableqa with historical passenger data.

## Dataset

This dataset contains information about Titanic passengers including:
- Demographics (age, gender)
- Ticket class and fare
- Family relationships (siblings, parents/children aboard)
- Survival status

## Files

- `data.csv`: Passenger records and survival outcomes
- `codebook.json`: Variable metadata and value labels

## Usage

```python
import pandas as pd
import json
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.analysis.bivariate import BivariateAnalyzer
from tableqa.interpretation.formatter import InsightFormatter
from tableqa.metadata.model import Codebook

# Load data and codebook
data = pd.read_csv('data.csv')
with open('codebook.json') as f:
    codebook_dict = json.load(f)
codebook = Codebook.from_dict(codebook_dict)

# Run bivariate analysis
biv_analyzer = BivariateAnalyzer()
formatter = InsightFormatter()

# Example: Analyze survival by passenger class
pclass_var = codebook.variables['pclass']
survived_var = codebook.variables['survived']

result = biv_analyzer.analyze(data, pclass_var, survived_var)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

## Example Analyses

- Survival rates by passenger class
- Age distribution of survivors vs non-survivors
- Impact of gender on survival
- Fare differences across classes
- Family size and survival outcomes

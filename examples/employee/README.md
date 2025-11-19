# Employee Survey Dataset

A synthetic employee survey dataset demonstrating tableqa with workplace data.

## Dataset

This dataset contains employee survey responses including:
- Demographics (age, gender, education)
- Job characteristics (department, tenure, role)
- Satisfaction and engagement metrics
- Performance indicators

## Files

- `data.csv`: Employee survey responses
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

# Example: Analyze relationship between tenure and satisfaction
tenure_var = codebook.variables['tenure']
satisfaction_var = codebook.variables['satisfaction']

result = biv_analyzer.analyze(data, tenure_var, satisfaction_var)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

## Example Analyses

- Satisfaction by department
- Performance by tenure
- Engagement trends by demographics
- Correlations between job characteristics and outcomes

# Titanic Passengers Example

An example using Titanic passenger data to demonstrate survival analysis and group comparisons.

## Dataset

Data about Titanic passengers including:
- Demographics (age, sex, class)
- Family relationships (siblings/spouses, parents/children)
- Ticket information (fare, cabin, embarked)
- Survival outcome

## Files

- `data.csv` - Titanic passenger records
- `codebook.json` - Variable metadata

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

# Analyze survival rate
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

result = analyzer.analyze(data['survived'], codebook.variables['survived'])
insight = formatter.format_univariate(result)
print(insight)

# Compare survival by passenger class
biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(
    data,
    codebook.variables['pclass'],
    codebook.variables['survived']
)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)

# Compare survival by sex
result = biv_analyzer.analyze(
    data,
    codebook.variables['sex'],
    codebook.variables['survived']
)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

## What You'll Learn

- Analyzing binary outcomes (survival)
- Group comparisons across categories
- Understanding statistical associations
- Working with real historical data

## Next Steps

- Explore age effects on survival
- Try multivariate analysis
- Generate Q/A pairs for the dataset
- See `../basic_usage.py` for complete workflows

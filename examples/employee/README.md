# Employee Survey Example

An example using employee satisfaction survey data to demonstrate tableqa's analysis of categorical and ordinal variables.

## Dataset

Employee survey data covering:
- Demographics (age, gender, department, education)
- Job metrics (tenure, salary, performance rating)
- Attitudes (satisfaction, work-life balance, career growth)
- Outcomes (turnover risk)

## Files

- `data.csv` - Employee survey responses
- `codebook.json` - Variable metadata with categorical value labels

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

# Analyze satisfaction distribution
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()

result = analyzer.analyze(data['satisfaction'], codebook.variables['satisfaction'])
insight = formatter.format_univariate(result)
print(insight)

# Compare satisfaction by department
biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(
    data,
    codebook.variables['department'],
    codebook.variables['satisfaction']
)
if result:
    insight = formatter.format_bivariate(result)
    print(insight)
```

## What You'll Learn

- Working with categorical and ordinal data
- Analyzing survey responses
- Group comparisons (e.g., by department, education)
- Correlation analysis for job metrics

## Next Steps

- Try generating Q/A pairs for training data
- Explore temporal analysis if year data is available
- See `../basic_usage.py` for more examples

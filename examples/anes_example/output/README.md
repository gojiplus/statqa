# ANES Analysis Output Directory

This directory contains generated outputs from the ANES analysis pipeline.

## Overview

All files in this directory are **generated** by running the analysis scripts and can be safely deleted and regenerated at any time.

## Generated Files

### insights.json
**Main output file** - Contains all extracted statistical insights

Structure:
```json
[
  {
    "vars": ["VCF0102"],
    "insight": "**Age of respondent** (VCF0102): mean=47.32, median=46.00, std=17.45. N=68234, dropped 2107 missing. (No weights applied.)",
    "figure": "output/univariate_VCF0102.png"
  },
  {
    "vars": ["VCF0104", "VCF0110"],
    "insight": "Correlation **Gender** ↔ **Political Interest**: r=0.12 (N=65432), p=0.001. (No weights applied.)",
    "figure": null
  }
]
```

Each insight contains:
- `vars`: List of variable names involved
- `insight`: Natural language description of the finding
- `figure`: Path to visualization (if generated), or `null`

### variable_profile.csv
**Variable profiling** - Summary statistics for all variables

Columns:
- `varname`: Variable code
- `label`: Variable label/description
- `dtype`: Data type (int64, float64, object)
- `unique`: Number of unique values
- `missing_pct`: Percentage of missing values

Example:
```csv
varname,label,dtype,unique,missing_pct
VCF0004,Year of study,int64,38,0.0
VCF0102,Age of respondent,int64,87,3.2
VCF0104,Gender,int64,2,0.1
VCF0110,Political interest,int64,4,5.3
```

### Visualization Files

#### univariate_*.png
Distribution plots for individual variables

- **Naming**: `univariate_{varname}.png` (e.g., `univariate_VCF0102.png`)
- **Content**: Histogram or bar chart showing variable distribution
- **Size**: 6×4 inches, 80-100 DPI
- **Format**: PNG

Examples:
- `univariate_VCF0102.png` - Age distribution histogram
- `univariate_VCF0104.png` - Gender distribution bar chart
- `univariate_VCF0110.png` - Political interest bar chart

#### bivariate_*.png
Relationship plots between variable pairs

- **Naming**: `bivariate_{var1}_{var2}.png` (e.g., `bivariate_VCF0104_VCF0110.png`)
- **Content**: Scatter plots, grouped bar charts, or correlation visualizations
- **Size**: 6×4 inches, 80-100 DPI
- **Format**: PNG

Examples:
- `bivariate_VCF0104_VCF0110.png` - Political interest by gender
- `bivariate_VCF0102_VCF0110.png` - Age vs political interest correlation

## File Counts

After a full analysis run, expect:
- **1** `insights.json` file
- **1** `variable_profile.csv` file
- **~100-500** `univariate_*.png` files (one per variable analyzed)
- **~100-1,000** `bivariate_*.png` files (depends on `--max-vars` setting)

Total size: ~20-50 MB

## Regenerating Outputs

To regenerate all outputs:

```bash
# Delete existing outputs
rm -f output/*.png output/*.json output/*.csv

# Run analysis again
cd ../scripts
python 02_extract_insights.py \
    --data-zip ../data/raw/anes_timeseries_cdf_csv_20220916.csv.zip \
    --metadata ../data/anes_metadata.csv \
    --output-dir ../output
```

## Using the Outputs

### Loading insights.json in Python

```python
import json

with open('insights.json', 'r') as f:
    insights = json.load(f)

# Print all insights
for insight in insights:
    print(insight['insight'])
    if insight['figure']:
        print(f"  → See figure: {insight['figure']}")
```

### Loading variable_profile.csv

```python
import pandas as pd

profile = pd.read_csv('variable_profile.csv')

# Find high-missingness variables
high_missing = profile[profile['missing_pct'] > 20]
print(f"Variables with >20% missing: {len(high_missing)}")

# Find categorical vs numeric
numeric = profile[profile['dtype'].str.contains('float|int')]
print(f"Numeric variables: {len(numeric)}")
```

### Creating a Report

```python
import json
from pathlib import Path

# Load insights
with open('insights.json', 'r') as f:
    insights = json.load(f)

# Generate markdown report
with open('report.md', 'w') as f:
    f.write("# ANES Analysis Report\n\n")

    for i, insight in enumerate(insights, 1):
        f.write(f"## Finding {i}\n\n")
        f.write(f"{insight['insight']}\n\n")

        if insight['figure']:
            rel_path = Path(insight['figure']).name
            f.write(f"![Visualization]({rel_path})\n\n")
```

## Git Ignore

These output files should **not** be committed to version control:

```gitignore
# In examples/anes_example/output/.gitignore
*.png
*.json
*.csv
!README.md
```

Rationale:
- **Large size**: Hundreds of PNG files can be 20-50 MB
- **Generated**: Can be easily recreated from data
- **Analysis-specific**: Results depend on parameters used

## Archiving Results

To archive results for later reference:

```bash
# Create dated archive
DATE=$(date +%Y%m%d)
tar -czf "anes_analysis_${DATE}.tar.gz" output/

# Or ZIP format
zip -r "anes_analysis_${DATE}.zip" output/
```

## Common Issues

### Missing Figures

**Problem**: `insights.json` references figures that don't exist
**Solution**: Re-run the analysis; ensure output directory is writable

### File Permission Errors

**Problem**: Cannot write to output directory
**Solution**: Check directory permissions; ensure it's not read-only

### Disk Space

**Problem**: Not enough disk space for all figures
**Solution**: Use `--skip-bivariate` or reduce `--max-vars`

## Output Statistics

Example statistics from a typical run:

```
Analysis Parameters:
- Variables analyzed: 120 (univariate)
- Variable pairs: 1,225 (bivariate, max-vars=50)
- Total insights: 1,345
- Figures generated: 1,165
- Total output size: 35.2 MB
- Analysis time: 8.5 minutes
```

## Cleanup

To clean up generated files while keeping the directory structure:

```bash
# Remove all generated files
rm -f output/*.png output/*.json output/*.csv

# Keep only README
ls output/
# Should show only: README.md
```

## Support

For issues with outputs:
- **tableqa package**: https://github.com/gojiplus/tableqa/issues
- **ANES example**: See `../README.md`

# Employee Survey Dataset

A synthetic workplace survey dataset demonstrating StatQA's **multimodal Q/A database generation** with employee metrics. This example generates 35 enhanced Q/A pairs with rich visual metadata and 15 publication-quality visualizations.

## Dataset

The Employee Survey dataset contains workplace measurements for 500 employees:
- Age demographics
- Education levels
- Income distribution
- Job satisfaction ratings
- Work hours patterns

## Files

- `data.csv`: Employee survey responses (age, education, income, job_satisfaction, work_hours)
- `codebook.json`: Variable metadata and descriptions
- `run_analysis.py`: Complete multimodal analysis script
- `qa_pairs.jsonl`: **35 multimodal Q/A pairs** with visual metadata
- `insights.json`: Statistical analysis results
- `plots/`: **15 publication-quality visualizations** (histograms, scatter plots, box plots, heatmaps)

## Quick Start

**Run the complete multimodal analysis:**
```bash
python run_analysis.py
```

This generates:
- Statistical insights for all 5 variables
- 15 publication-quality plots in `plots/`
- 35 enhanced Q/A pairs with visual metadata in `qa_pairs.jsonl`

## Enhanced Q/A Format

Each Q/A pair includes rich multimodal metadata:

```json
{
  "question": "What is the distribution of Annual Income?",
  "answer": "**Annual Income**: mean=65,897.15, median=64,511.00, std=23,807.36, range=[25,000.00, 133,843.00]. N=500 [non-normal distribution].",
  "type": "distributional",
  "provenance": {
    "generated_at": "2025-11-19T19:21:28+00:00",
    "tool": "statqa",
    "tool_version": "0.2.0",
    "python_commands": ["valid_data.mean()  # Result: 65897.15", "valid_data.std()  # Result: 23807.36"]
  },
  "visual": {
    "plot_type": "histogram",
    "caption": "Histogram showing income distribution with right-skewed pattern and mean=$65,897 (N=500).",
    "alt_text": "Histogram chart with income values on x-axis and frequency density on y-axis.",
    "visual_elements": {
      "chart_type": "histogram",
      "colors": ["blue bars", "red mean line"],
      "key_features": ["distribution shape", "mean line", "right skew"]
    },
    "primary_plot": "plots/univariate_income.png"
  },
  "vars": ["income"]
}
```

## Generated Visualizations

The example creates 15 plots in the `plots/` directory:

**Univariate (5 plots):**
- `univariate_age.png`: Histogram of age distribution
- `univariate_education.png`: Bar chart of education levels
- `univariate_income.png`: Histogram of income distribution (right-skewed)
- `univariate_job_satisfaction.png`: Bar chart of satisfaction ratings
- `univariate_work_hours.png`: Histogram of weekly work hours

**Bivariate (10 plots):**
- `bivariate_age_income.png`: Scatter plot showing age-income relationship
- `bivariate_education_income.png`: Box plots of income by education level
- `bivariate_age_job_satisfaction.png`: Box plots of satisfaction by age groups
- And 7 more workplace relationship visualizations...

## Use Cases

This multimodal dataset is perfect for:
- **HR analytics training** for multimodal AI systems
- **Workplace research** with comprehensive visual-text pairs
- **Survey analysis education** with reproducible examples
- **Employee satisfaction modeling** with rich metadata
- **CLIP-style training** on workplace data

## Next Steps

- Explore the enhanced Q/A pairs in `qa_pairs.jsonl`
- Use the visual metadata for multimodal AI training
- Compare workplace metrics across different employee segments
- Adapt the pipeline for your own survey datasets

# Titanic Survival Dataset

The famous Titanic dataset demonstrating StatQA's **multimodal Q/A database generation** with historical passenger data. This example generates 28 enhanced Q/A pairs with rich visual metadata and 15 publication-quality visualizations.

## Dataset

The Titanic dataset contains information about 400 passengers including:
- Survival outcomes (binary classification target)
- Passenger class (socioeconomic status)
- Demographics (gender, age)
- Ticket fare (economic indicator)

## Files

- `data.csv`: Passenger records and survival outcomes (survived, pclass, sex, age, fare)
- `codebook.json`: Variable metadata and descriptions
- `run_analysis.py`: Complete multimodal analysis script
- `qa_pairs.jsonl`: **28 multimodal Q/A pairs** with visual metadata
- `insights.json`: Statistical analysis results
- `plots/`: **15 publication-quality visualizations** (bar charts, box plots, heatmaps, scatter plots)

## Quick Start

**Run the complete multimodal analysis:**
```bash
python run_analysis.py
```

This generates:
- Statistical insights for all 5 variables
- 15 publication-quality plots in `plots/`
- 28 enhanced Q/A pairs with visual metadata in `qa_pairs.jsonl`

## Enhanced Q/A Format

Each Q/A pair includes rich multimodal metadata:

```json
{
  "question": "What is the frequency distribution of Survived?",
  "answer": "**Survived**: most common category is '0' (60.2%), N=400. Distribution: 0: 60.2%, 1: 39.8% [high diversity].",
  "type": "distributional",
  "provenance": {
    "generated_at": "2025-11-19T19:21:28+00:00",
    "tool": "statqa",
    "tool_version": "0.2.0",
    "python_commands": ["data.value_counts()  # Result: {0: 241, 1: 159}"]
  },
  "visual": {
    "plot_type": "bar_chart",
    "caption": "Bar chart showing survival frequencies across 2 categories (N=400). Most common category is 'No survival' (60.2%).",
    "alt_text": "Bar chart with survival categories on x-axis and count frequencies on y-axis.",
    "visual_elements": {
      "chart_type": "bar_chart",
      "colors": ["viridis color palette"],
      "key_features": ["frequency bars"]
    },
    "primary_plot": "plots/univariate_survived.png"
  },
  "vars": ["survived"]
}
```

## Generated Visualizations

The example creates 15 plots in the `plots/` directory:

**Univariate (5 plots):**
- `univariate_survived.png`: Bar chart of survival outcomes
- `univariate_pclass.png`: Bar chart of passenger class distribution
- `univariate_sex.png`: Bar chart of gender distribution
- `univariate_age.png`: Histogram of age distribution
- `univariate_fare.png`: Histogram of ticket fare distribution

**Bivariate (10 plots):**
- `bivariate_survived_pclass.png`: Heatmap showing survival by passenger class
- `bivariate_survived_sex.png`: Heatmap showing survival by gender
- `bivariate_survived_age.png`: Box plots comparing age by survival status
- `bivariate_pclass_fare.png`: Box plots showing fare by passenger class
- And 6 more survival analysis visualizations...

## Use Cases

This multimodal dataset is perfect for:
- **Classification model training** with CLIP-style visual-text pairs
- **Historical data analysis education** with rich metadata
- **Survival analysis research** with comprehensive visualizations
- **Binary classification benchmarking** with publication-quality plots
- **Accessibility research** with alt-text and captions for historical data

## Next Steps

- Explore the enhanced Q/A pairs in `qa_pairs.jsonl`
- Use the visual metadata for multimodal classification models
- Compare survival patterns across different passenger segments
- Adapt the pipeline for your own classification datasets with categorical outcomes

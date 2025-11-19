# Q/A Dataset Generation Pipeline

## Overview

This document describes StatQA's pipeline for generating Q/A-style datasets from tabular data with metadata. The pipeline converts raw tables into structured question-answer pairs suitable for training or fine-tuning LLMs on data analysis tasks.

## Pipeline Architecture

### Complete Flow

```
Input: Table + Metadata
         ↓
[1] Parse Codebook (Variable Metadata)
         ↓
[2] Run Statistical Analyses
    - Univariate (descriptive stats)
    - Bivariate (relationships)
    - Temporal (trends)
    - Causal (effects)
         ↓
[3] Format Insights (Natural Language)
         ↓
[4] Generate Q/A Pairs
    - Template-based questions
    - LLM paraphrasing (optional)
         ↓
[5] Export
    - JSONL format
    - OpenAI fine-tuning format
    - Anthropic format
         ↓
Output: Q/A Dataset for LLM Training
```

## Pipeline Components

### 1. Metadata/Codebook Parsing

**Purpose**: Extract variable-level metadata including:
- Variable name and label
- Type (numeric continuous/discrete, categorical nominal/ordinal, etc.)
- Value labels (for categorical variables)
- Missing value codes
- Units, range, description
- Data generating process information

**Supported Formats**:
- Text format (custom syntax)
- CSV format
- PDF codebooks (with optical parsing)

**Example**:
```python
from statqa.metadata.parsers import CSVParser

parser = CSVParser()
codebook = parser.parse('codebook.csv')
```

### 2. Statistical Analyses

**Univariate Analysis**:
- Numeric: mean, median, std, min/max, quartiles, skewness, kurtosis
- Categorical: frequencies, mode, diversity indices, entropy
- Distribution: normality tests, outlier detection
- Robust statistics: MAD, robust z-scores

**Bivariate Analysis**:
- Numeric × Numeric: Pearson/Spearman correlation, effect sizes
- Categorical × Categorical: Chi-square test, Cramér's V
- Categorical × Numeric: t-tests, ANOVA, Cohen's d, η²

**Temporal Analysis** (optional):
- Trend detection: Mann-Kendall test
- Change point detection
- Year-over-year comparisons
- Seasonal decomposition

**Causal Analysis** (optional):
- Regression with confounding control
- Treatment effect estimation
- Sensitivity analysis

**Example**:
```python
from statqa.analysis import UnivariateAnalyzer, BivariateAnalyzer

# Univariate
analyzer = UnivariateAnalyzer()
result = analyzer.analyze(data['age'], codebook.variables['age'])

# Bivariate
biv_analyzer = BivariateAnalyzer()
result = biv_analyzer.analyze(data, var1, var2)
```

### 3. Insight Formatting

**Purpose**: Convert statistical results into natural language insights that are:
- Human-readable and publication-quality
- Concise but complete
- Interpretable by domain experts and LLMs

**Formatting Rules**:
- Include variable labels (not just codes)
- Report effect sizes and statistical significance
- Add context (sample size, normality, outliers)
- Use consistent notation

**Example Output**:
```
**Annual Income**: mean=65,897.15, median=64,511.00, std=23,807.36,
range=[25,000.00, 133,843.00]. N=500 [non-normal distribution].
```

**Example**:
```python
from statqa.interpretation import InsightFormatter

formatter = InsightFormatter()
insight = formatter.format_univariate(result)
```

### 4. Q/A Pair Generation

**Template-Based Generation**:
- Uses pre-defined templates based on analysis type
- Generates 2-3 questions per insight
- Question types:
  - Descriptive: "What is the average...?"
  - Comparative: "How does X differ across Y groups?"
  - Correlational: "Are X and Y correlated?"
  - Temporal: "Has X changed over time?"
  - Distributional: "What is the distribution of X?"
  - Causal: "What is the effect of X on Y?"

**LLM-Powered Paraphrasing** (optional):
- Generates diverse phrasings of the same question
- Adds domain-specific terminology
- Varies formality and structure
- Creates 2+ paraphrases per original question

**Example**:
```python
from statqa.qa import QAGenerator

# Template-based only
qa_gen = QAGenerator(use_llm=False)
qa_pairs = qa_gen.generate_qa_pairs(insight, formatted_answer)

# With LLM paraphrasing
qa_gen = QAGenerator(use_llm=True, api_key="your-key")
qa_pairs = qa_gen.generate_qa_pairs(insight, formatted_answer)
```

**Example Q/A Pairs**:

```json
{
  "question": "What is the average Annual Income?",
  "answer": "**Annual Income**: mean=65,897.15, median=64,511.00, std=23,807.36, range=[25,000.00, 133,843.00]. N=500 [non-normal distribution].",
  "type": "descriptive",
  "dataset": "Employee Survey",
  "variables": "income"
}
```

```json
{
  "question": "How does age differ across education groups?",
  "answer": "**age** differs across **education** groups: Bachelor degree: 46.04, Graduate degree (Masters/PhD): 47.68, High school or equivalent: 45.78 (ANOVA: F=0.50, p=0.609), η²=0.00 (negligible).",
  "type": "comparative",
  "dataset": "Employee Survey",
  "variables": ["age", "education"]
}
```

### 5. Export Formats

**JSONL (Standard)**:
```json
{"question": "...", "answer": "...", "type": "...", "dataset": "...", "variables": "..."}
```

**OpenAI Fine-Tuning Format**:
```json
{
  "messages": [
    {"role": "system", "content": "You are a data analyst..."},
    {"role": "user", "content": "What is the average income?"},
    {"role": "assistant", "content": "**Annual Income**: mean=65,897..."}
  ]
}
```

**Anthropic Format**:
```json
{"prompt": "What is the average income?", "completion": "**Annual Income**: mean=65,897..."}
```

## Demo Results

We tested the pipeline on 3 public datasets:

### Dataset 1: Employee Survey (500 rows, 5 variables)

**Variables**: age, education, income, job_satisfaction, work_hours

**Results**:
- 5 univariate insights
- 5 bivariate insights
- 23 Q/A pairs generated

**Example Q/A**:
```
Q: What is the distribution of Annual Income?
A: **Annual Income**: mean=65,897.15, median=64,511.00, std=23,807.36,
   range=[25,000.00, 133,843.00]. N=500 [non-normal distribution].
```

### Dataset 2: Iris Flowers (150 rows, 5 variables)

**Variables**: sepal_length, sepal_width, petal_length, petal_width, species

**Results**:
- 5 univariate insights
- 5 bivariate insights
- 24 Q/A pairs generated

**Example Q/A**:
```
Q: Are petal_length and petal_width correlated?
A: **petal_length** and **petal_width** show a very strong positive
   correlation (r=0.96, p<0.001, N=150), effect size: very large.
```

### Dataset 3: Titanic Passengers (400 rows, 5 variables)

**Variables**: survived, pclass, sex, age, fare

**Results**:
- 5 univariate insights
- 5 bivariate insights
- 13 Q/A pairs generated

**Example Q/A**:
```
Q: What is the frequency distribution of Survived?
A: **Survived**: most common category is '0' (60.2%), N=400.
   Distribution: 0: 60.2%, 1: 39.8% [high diversity].
```

### Overall Results

- **Total Datasets**: 3
- **Total Insights**: 30 (15 univariate + 15 bivariate)
- **Total Q/A Pairs**: 60
- **Average Q/A per Insight**: 2.0

## Pipeline Validation

### ✅ Pipeline Makes Sense

**Strengths**:

1. **Comprehensive Metadata Integration**
   - Uses rich variable metadata (types, labels, descriptions)
   - Handles missing values and outliers appropriately
   - Supports multiple variable types (numeric, categorical, ordinal)

2. **Rigorous Statistical Analysis**
   - Appropriate tests for each variable type combination
   - Reports effect sizes (not just p-values)
   - Includes normality tests and distribution information
   - Handles edge cases (e.g., insufficient data, all missing)

3. **High-Quality Natural Language**
   - Insights are clear, concise, and informative
   - Uses proper statistical notation
   - Includes context (N, significance, effect size)
   - Publication-ready formatting

4. **Diverse Q/A Generation**
   - Multiple question types (descriptive, comparative, correlational, etc.)
   - Template-based ensures grammatical correctness
   - Optional LLM paraphrasing adds diversity
   - Maintains question-answer consistency

5. **Flexible Export Formats**
   - Supports major LLM training platforms
   - JSONL for custom training pipelines
   - Includes metadata for filtering/analysis

6. **Scalable Architecture**
   - Batch processing for multiple variables
   - Handles large codebooks efficiently
   - Modular components (easy to extend)

### 🔍 Potential Improvements

1. **LLM-Generated Follow-ups**
   - Add exploratory questions ("Why might this correlation exist?")
   - Generate hypothesis-generating questions
   - Create multi-hop reasoning chains

2. **Domain-Specific Templates**
   - Healthcare-specific question patterns
   - Social science terminology
   - Business/finance language

3. **Quality Filtering**
   - Skip non-significant findings (optional)
   - Prioritize large effect sizes
   - Filter out redundant Q/A pairs

4. **Multi-modal Extensions**
   - Include visualization descriptions
   - Reference plots in answers
   - Generate chart-based Q/A

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from statqa.metadata.parsers import CSVParser
from statqa.analysis import UnivariateAnalyzer, BivariateAnalyzer
from statqa.interpretation import InsightFormatter
from statqa.qa import QAGenerator

# 1. Parse codebook
parser = CSVParser()
codebook = parser.parse('codebook.csv')

# 2. Load data
import pandas as pd
data = pd.read_csv('data.csv')

# 3. Run analyses
analyzer = UnivariateAnalyzer()
formatter = InsightFormatter()
qa_gen = QAGenerator(use_llm=False)

all_qa_pairs = []

for var_name, variable in codebook.variables.items():
    # Analyze
    result = analyzer.analyze(data[var_name], variable)

    # Format insight
    insight = formatter.format_univariate(result)

    # Generate Q/A
    qa_pairs = qa_gen.generate_qa_pairs(result, insight)
    all_qa_pairs.extend(qa_pairs)

# 4. Export
with open('qa_dataset.jsonl', 'w') as f:
    for qa in all_qa_pairs:
        f.write(json.dumps(qa) + '\n')
```

### Using the CLI

```bash
# Complete pipeline
statqa pipeline data.csv codebook.csv \
    --output-dir output/ \
    --qa \
    --enrich

# Just Q/A generation from existing insights
statqa generate-qa insights.json \
    --output qa_pairs.jsonl \
    --format openai \
    --llm
```

### Running the Demo

```bash
# Run the complete demo with 3 datasets
python examples/qa_dataset_generation_demo.py

# View results
ls -lh output/qa_generation_demo/
cat output/qa_generation_demo/combined_qa_dataset.jsonl
```

## File Structure

After running the pipeline, you'll have:

```
output/qa_generation_demo/
├── employee_survey/
│   ├── data.csv                    # Original data
│   ├── codebook.json               # Variable metadata
│   ├── insights.json               # All insights
│   ├── qa_pairs.json               # Q/A pairs (JSON)
│   └── qa_pairs.jsonl              # Q/A pairs (JSONL)
├── iris_flowers/
│   └── ...
├── titanic_passengers/
│   └── ...
├── combined_qa_dataset.jsonl       # All Q/A pairs combined
└── openai_training_data.jsonl      # OpenAI fine-tuning format
```

## Best Practices

1. **Always include metadata**: The pipeline works best with rich variable descriptions
2. **Use appropriate variable types**: Correctly classifying variables improves analysis quality
3. **Start template-based**: Test with templates before adding LLM paraphrasing
4. **Filter insights**: Consider filtering non-significant or trivial findings
5. **Review samples**: Always review generated Q/A pairs for quality
6. **Domain customization**: Adapt templates for your specific domain

## Conclusion

The Q/A dataset generation pipeline successfully:

✅ Processes tabular data with metadata
✅ Runs appropriate statistical analyses
✅ Generates publication-quality insights
✅ Creates diverse, high-quality Q/A pairs
✅ Exports in multiple formats for LLM training

The pipeline is production-ready and can be customized for specific domains or use cases.

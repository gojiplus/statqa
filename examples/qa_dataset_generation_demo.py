#!/usr/bin/env python3
"""
Q/A Dataset Generation Pipeline Demo

Demonstrates the complete pipeline for generating Q/A-style datasets from tabular data:
1. Load data with metadata/codebook
2. Run statistical analyses
3. Format insights as natural language
4. Generate Q/A pairs (template-based + optional LLM)
5. Export for LLM training

This example uses 3 public datasets:
- Synthetic Survey Data (demographics)
- Iris Dataset (classification)
- Titanic Dataset (survival analysis)
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from tableqa.analysis.bivariate import BivariateAnalyzer
from tableqa.analysis.univariate import UnivariateAnalyzer
from tableqa.interpretation.formatter import InsightFormatter
from tableqa.metadata.schema import Codebook, Variable, VariableType
from tableqa.qa.generator import QAGenerator


def create_survey_dataset() -> tuple[pd.DataFrame, Codebook]:
    """Create synthetic survey dataset with metadata."""
    np.random.seed(42)
    n = 500

    # Generate correlated survey data
    data = pd.DataFrame(
        {
            "age": np.random.randint(18, 75, n),
            "education": np.random.choice(
                ["High School", "Bachelor", "Graduate"], n, p=[0.4, 0.4, 0.2]
            ),
            "income": np.random.randint(25000, 150000, n),
            "job_satisfaction": np.random.randint(1, 6, n),
            "work_hours": np.random.randint(20, 60, n),
        }
    )

    # Add correlations
    edu_income_map = {"High School": 45000, "Bachelor": 70000, "Graduate": 95000}
    base_income = data["education"].map(edu_income_map)
    data["income"] = (base_income + np.random.normal(0, 15000, n)).clip(25000, 150000).astype(int)

    # Income → satisfaction correlation
    income_norm = (data["income"] - data["income"].mean()) / data["income"].std()
    satisfaction = 3 + 0.4 * income_norm + np.random.normal(0, 0.7, n)
    data["job_satisfaction"] = satisfaction.clip(1, 5).round().astype(int)

    # Create codebook
    variables = {
        "age": Variable(
            name="age",
            label="Respondent Age",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Age of survey respondent in years",
        ),
        "education": Variable(
            name="education",
            label="Education Level",
            var_type=VariableType.CATEGORICAL_ORDINAL,
            description="Highest education level completed",
            valid_values={
                "High School": "High school or equivalent",
                "Bachelor": "Bachelor degree",
                "Graduate": "Graduate degree (Masters/PhD)",
            },
        ),
        "income": Variable(
            name="income",
            label="Annual Income",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Annual household income in USD",
        ),
        "job_satisfaction": Variable(
            name="job_satisfaction",
            label="Job Satisfaction",
            var_type=VariableType.CATEGORICAL_ORDINAL,
            description="Overall job satisfaction (1=Very Dissatisfied, 5=Very Satisfied)",
            valid_values={str(i): f"Level {i}" for i in range(1, 6)},
        ),
        "work_hours": Variable(
            name="work_hours",
            label="Weekly Work Hours",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Average hours worked per week",
        ),
    }

    codebook = Codebook(
        name="Employee Survey 2024",
        description="Survey of employee demographics and job satisfaction",
        variables=variables,
    )

    return data, codebook


def create_iris_dataset() -> tuple[pd.DataFrame, Codebook]:
    """Load Iris dataset with metadata."""
    iris = load_iris()
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data["species"] = iris.target_names[iris.target]

    # Simplify column names
    data.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

    variables = {
        "sepal_length": Variable(
            name="sepal_length",
            label="Sepal Length",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Length of sepal in centimeters",
        ),
        "sepal_width": Variable(
            name="sepal_width",
            label="Sepal Width",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Width of sepal in centimeters",
        ),
        "petal_length": Variable(
            name="petal_length",
            label="Petal Length",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Length of petal in centimeters",
        ),
        "petal_width": Variable(
            name="petal_width",
            label="Petal Width",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Width of petal in centimeters",
        ),
        "species": Variable(
            name="species",
            label="Iris Species",
            var_type=VariableType.CATEGORICAL_NOMINAL,
            description="Species of iris flower",
            valid_values={
                "setosa": "Iris setosa",
                "versicolor": "Iris versicolor",
                "virginica": "Iris virginica",
            },
        ),
    }

    codebook = Codebook(
        name="Iris Flower Dataset",
        description="Fisher's classic Iris dataset with flower measurements",
        variables=variables,
    )

    return data, codebook


def create_titanic_dataset() -> tuple[pd.DataFrame, Codebook]:
    """Create simplified Titanic dataset with metadata."""
    np.random.seed(42)
    n = 400

    # Generate realistic Titanic-like data
    pclass = np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55])
    sex = np.random.choice(["male", "female"], n, p=[0.65, 0.35])
    age = np.random.normal(30, 14, n).clip(1, 80)

    # Survival rates based on class and sex
    survival_prob = np.zeros(n)
    survival_prob[(pclass == 1) & (sex == "female")] = 0.97
    survival_prob[(pclass == 1) & (sex == "male")] = 0.37
    survival_prob[(pclass == 2) & (sex == "female")] = 0.92
    survival_prob[(pclass == 2) & (sex == "male")] = 0.16
    survival_prob[(pclass == 3) & (sex == "female")] = 0.50
    survival_prob[(pclass == 3) & (sex == "male")] = 0.14

    survived = (np.random.random(n) < survival_prob).astype(int)

    data = pd.DataFrame(
        {
            "survived": survived,
            "pclass": pclass,
            "sex": sex,
            "age": age.round(1),
            "fare": np.random.lognormal(3, 1, n).clip(5, 500).round(2),
        }
    )

    variables = {
        "survived": Variable(
            name="survived",
            label="Survived",
            var_type=VariableType.CATEGORICAL_NOMINAL,
            description="Survival status (0=No, 1=Yes)",
            valid_values={"0": "Did not survive", "1": "Survived"},
        ),
        "pclass": Variable(
            name="pclass",
            label="Passenger Class",
            var_type=VariableType.CATEGORICAL_ORDINAL,
            description="Ticket class (1=First, 2=Second, 3=Third)",
            valid_values={"1": "First class", "2": "Second class", "3": "Third class"},
        ),
        "sex": Variable(
            name="sex",
            label="Sex",
            var_type=VariableType.CATEGORICAL_NOMINAL,
            description="Passenger sex",
            valid_values={"male": "Male", "female": "Female"},
        ),
        "age": Variable(
            name="age",
            label="Age",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Passenger age in years",
        ),
        "fare": Variable(
            name="fare",
            label="Fare",
            var_type=VariableType.NUMERIC_CONTINUOUS,
            description="Ticket fare in pounds",
        ),
    }

    codebook = Codebook(
        name="Titanic Passenger Dataset",
        description="Passenger data from the Titanic disaster",
        variables=variables,
    )

    return data, codebook


def run_pipeline_on_dataset(
    dataset_name: str,
    data: pd.DataFrame,
    codebook: Codebook,
    output_dir: Path,
    max_bivariate: int = 5,
) -> dict:
    """
    Run complete Q/A generation pipeline on a dataset.

    Args:
        dataset_name: Name of dataset for labeling
        data: DataFrame with data
        codebook: Codebook with variable metadata
        output_dir: Output directory for results
        max_bivariate: Max number of bivariate analyses

    Returns:
        Dictionary with pipeline results
    """
    print(f"\n{'='*70}")
    print(f"Processing: {dataset_name}")
    print(f"{'='*70}")

    results = {
        "dataset": dataset_name,
        "n_rows": len(data),
        "n_vars": len(codebook.variables),
        "insights": [],
        "qa_pairs": [],
    }

    # Initialize analyzers
    univariate_analyzer = UnivariateAnalyzer()
    bivariate_analyzer = BivariateAnalyzer()
    formatter = InsightFormatter()
    qa_generator = QAGenerator(use_llm=False)  # Template-based for demo

    # Step 1: Univariate analysis
    print(f"\n[1/3] Running univariate analysis on {len(codebook.variables)} variables...")
    univariate_insights = []

    for var_name, variable in codebook.variables.items():
        if var_name in data.columns:
            try:
                result = univariate_analyzer.analyze(data[var_name], variable)
                insight_text = formatter.format_univariate(result)

                insight = {
                    "type": "univariate",
                    "variable": var_name,
                    "analysis": result,
                    "insight": insight_text,
                }
                univariate_insights.append(insight)

            except Exception as e:
                print(f"  Warning: Skipped {var_name}: {e}")

    print(f"  ✓ Generated {len(univariate_insights)} univariate insights")
    results["insights"].extend(univariate_insights)

    # Step 2: Bivariate analysis (limited for demo)
    print(f"\n[2/3] Running bivariate analysis (max {max_bivariate} pairs)...")
    bivariate_insights = []

    var_list = list(codebook.variables.keys())
    pairs_analyzed = 0

    for i in range(len(var_list)):
        if pairs_analyzed >= max_bivariate:
            break

        for j in range(i + 1, len(var_list)):
            if pairs_analyzed >= max_bivariate:
                break

            var1_name, var2_name = var_list[i], var_list[j]

            if var1_name in data.columns and var2_name in data.columns:
                try:
                    var1 = codebook.variables[var1_name]
                    var2 = codebook.variables[var2_name]

                    result = bivariate_analyzer.analyze(data, var1, var2)
                    insight_text = formatter.format_bivariate(result)

                    insight = {
                        "type": "bivariate",
                        "variables": [var1_name, var2_name],
                        "analysis": result,
                        "insight": insight_text,
                    }
                    bivariate_insights.append(insight)
                    pairs_analyzed += 1

                except Exception:
                    pass

    print(f"  ✓ Generated {len(bivariate_insights)} bivariate insights")
    results["insights"].extend(bivariate_insights)

    # Step 3: Generate Q/A pairs
    print(f"\n[3/3] Generating Q/A pairs from {len(results['insights'])} insights...")

    for insight in results["insights"]:
        try:
            # Add analysis_type to analysis dict for provenance tracking
            analysis = insight["analysis"].copy()
            analysis["analysis_type"] = insight["type"]

            qa_pairs = qa_generator.generate_qa_pairs(analysis, insight["insight"])

            for qa in qa_pairs:
                qa["dataset"] = dataset_name
                qa["insight_type"] = insight["type"]
                qa["variables"] = insight.get("variable") or insight.get("variables", [])

            results["qa_pairs"].extend(qa_pairs)

        except Exception as e:
            print(f"  Warning: Failed to generate Q/A: {e}")

    print(f"  ✓ Generated {len(results['qa_pairs'])} Q/A pairs")

    # Save results
    dataset_dir = output_dir / dataset_name.lower().replace(" ", "_")
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # Save data and codebook
    data.to_csv(dataset_dir / "data.csv", index=False)
    with open(dataset_dir / "codebook.json", "w") as f:
        json.dump(
            {var.name: var.model_dump() for var in codebook.variables.values()},
            f,
            indent=2,
            default=str,
        )

    # Save insights
    with open(dataset_dir / "insights.json", "w") as f:
        json.dump(results["insights"], f, indent=2, default=str)

    # Save Q/A pairs
    with open(dataset_dir / "qa_pairs.json", "w") as f:
        json.dump(results["qa_pairs"], f, indent=2, default=str)

    # Save in JSONL format (for LLM training)
    with open(dataset_dir / "qa_pairs.jsonl", "w") as f:
        for qa in results["qa_pairs"]:
            f.write(json.dumps(qa, ensure_ascii=False) + "\n")

    print(f"\n✓ Saved results to {dataset_dir}/")

    return results


def print_example_qa_pairs(results: list[dict], n_examples: int = 3):
    """Print example Q/A pairs from each dataset."""
    print(f"\n{'='*70}")
    print("EXAMPLE Q/A PAIRS")
    print(f"{'='*70}")

    for dataset_results in results:
        dataset_name = dataset_results["dataset"]
        qa_pairs = dataset_results["qa_pairs"]

        print(f"\n{dataset_name}")
        print("-" * 70)

        for i, qa in enumerate(qa_pairs[:n_examples], 1):
            print(f"\n[Example {i}]")
            print(f"Type: {qa['type']}")
            print(f"Variables: {qa.get('variables', 'N/A')}")
            print(f"\nQ: {qa['question']}")
            print(f"A: {qa['answer']}")
            print()


def main():
    """Run the complete Q/A generation pipeline demo."""
    print("=" * 70)
    print("Q/A DATASET GENERATION PIPELINE DEMO")
    print("=" * 70)
    print("\nThis demo shows how to generate Q/A-style datasets from tables with metadata.")
    print("\nPipeline steps:")
    print("  1. Load data with variable metadata (codebook)")
    print("  2. Run statistical analyses (univariate + bivariate)")
    print("  3. Format findings as natural language insights")
    print("  4. Generate question/answer pairs (template-based)")
    print("  5. Export in formats suitable for LLM training")

    # Create output directory
    output_dir = Path("output/qa_generation_demo")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Prepare datasets
    datasets = [
        ("Employee Survey", *create_survey_dataset()),
        ("Iris Flowers", *create_iris_dataset()),
        ("Titanic Passengers", *create_titanic_dataset()),
    ]

    # Run pipeline on each dataset
    all_results = []

    for dataset_name, data, codebook in datasets:
        results = run_pipeline_on_dataset(dataset_name, data, codebook, output_dir, max_bivariate=5)
        all_results.append(results)

    # Print summary
    print(f"\n{'='*70}")
    print("PIPELINE SUMMARY")
    print(f"{'='*70}")

    total_insights = sum(len(r["insights"]) for r in all_results)
    total_qa = sum(len(r["qa_pairs"]) for r in all_results)

    for r in all_results:
        print(f"\n{r['dataset']}:")
        print(f"  Rows: {r['n_rows']:,}")
        print(f"  Variables: {r['n_vars']}")
        print(f"  Insights: {len(r['insights'])}")
        print(f"  Q/A Pairs: {len(r['qa_pairs'])}")

    print("\nTOTAL:")
    print(f"  Datasets: {len(all_results)}")
    print(f"  Insights: {total_insights}")
    print(f"  Q/A Pairs: {total_qa}")

    # Print example Q/A pairs
    print_example_qa_pairs(all_results, n_examples=3)

    # Create combined dataset
    print(f"\n{'='*70}")
    print("CREATING COMBINED DATASET")
    print(f"{'='*70}")

    all_qa_pairs = []
    for r in all_results:
        all_qa_pairs.extend(r["qa_pairs"])

    # Save combined Q/A dataset
    combined_path = output_dir / "combined_qa_dataset.jsonl"
    with open(combined_path, "w") as f:
        for qa in all_qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + "\n")

    print(f"\n✓ Saved {len(all_qa_pairs)} Q/A pairs to {combined_path}")

    # Create OpenAI fine-tuning format
    openai_path = output_dir / "openai_training_data.jsonl"
    with open(openai_path, "w") as f:
        for qa in all_qa_pairs:
            entry = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a data analyst answering questions about statistical findings.",
                    },
                    {"role": "user", "content": qa["question"]},
                    {"role": "assistant", "content": qa["answer"]},
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✓ Saved OpenAI format to {openai_path}")

    print(f"\n{'='*70}")
    print("DEMO COMPLETE!")
    print(f"{'='*70}")
    print(f"\nAll results saved to: {output_dir}/")
    print("\nNext steps:")
    print("  1. Review example Q/A pairs above")
    print("  2. Explore output/qa_generation_demo/ for detailed results")
    print("  3. Use combined_qa_dataset.jsonl for LLM training")
    print("  4. Customize the pipeline for your own datasets")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()

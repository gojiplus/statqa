"""
Plotting utilities for statistical visualizations.

Creates publication-quality plots for insights.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from statqa.metadata.schema import Variable


class PlotFactory:
    """Factory for creating statistical visualizations."""

    def __init__(
        self,
        style: str = "whitegrid",
        context: str = "notebook",
        figsize: tuple[int, int] = (8, 6),
        dpi: int = 100,
    ) -> None:
        """
        Initialize plot factory.

        Args:
            style: Seaborn style ('whitegrid', 'darkgrid', 'white', 'dark', 'ticks')
            context: Seaborn context ('paper', 'notebook', 'talk', 'poster')
            figsize: Default figure size (width, height)
            dpi: DPI for rasterized output
        """
        self.figsize = figsize
        self.dpi = dpi
        sns.set_style(style)
        sns.set_context(context)

    def plot_univariate(
        self,
        data: pd.Series,
        variable: Variable,
        output_path: str | Path | None = None,
    ) -> plt.Figure:
        """
        Create univariate plot (histogram or bar chart).

        Args:
            data: Data series
            variable: Variable metadata
            output_path: Optional path to save plot

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Clean data
        clean_data = self._clean_data(data, variable)

        if variable.is_numeric():
            self._plot_numeric_distribution(clean_data, variable, ax)
        elif variable.is_categorical():
            self._plot_categorical_distribution(clean_data, variable, ax)

        ax.set_title(f"Distribution of {variable.label}")

        if output_path:
            fig.savefig(output_path, bbox_inches="tight", dpi=self.dpi)

        return fig

    def plot_bivariate(
        self,
        data: pd.DataFrame,
        var1: Variable,
        var2: Variable,
        output_path: str | Path | None = None,
    ) -> plt.Figure:
        """
        Create bivariate plot (scatter, box, or heatmap).

        Args:
            data: DataFrame with both variables
            var1: First variable
            var2: Second variable
            output_path: Optional path to save plot

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Clean data
        subset = data[[var1.name, var2.name]].copy()
        subset = self._clean_dataframe(subset, [var1, var2])
        subset = subset.dropna()

        if var1.is_numeric() and var2.is_numeric():
            self._plot_scatter(subset, var1, var2, ax)
        elif var1.is_categorical() and var2.is_numeric():
            self._plot_boxplot(subset, var1, var2, ax)
        elif var1.is_categorical() and var2.is_categorical():
            self._plot_heatmap(subset, var1, var2, ax)

        if output_path:
            fig.savefig(output_path, bbox_inches="tight", dpi=self.dpi)

        return fig

    def plot_temporal(
        self,
        data: pd.DataFrame,
        time_var: Variable,
        value_var: Variable,
        group_var: Variable | None = None,
        output_path: str | Path | None = None,
    ) -> plt.Figure:
        """
        Create temporal trend plot.

        Args:
            data: DataFrame with time and value
            time_var: Time variable
            value_var: Value variable
            group_var: Optional grouping variable
            output_path: Optional path to save plot

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Clean and sort
        cols = [time_var.name, value_var.name]
        if group_var:
            cols.append(group_var.name)

        subset = data[cols].copy()
        subset = self._clean_dataframe(
            subset, [time_var, value_var] + ([group_var] if group_var else [])
        )
        subset = subset.dropna().sort_values(time_var.name)

        if group_var:
            # Grouped line plot
            for group_name, group_data in subset.groupby(group_var.name):
                label = (
                    group_var.valid_values.get(group_name, str(group_name))
                    if group_var.valid_values
                    else str(group_name)
                )
                ax.plot(
                    group_data[time_var.name],
                    group_data[value_var.name],
                    marker="o",
                    label=label,
                )
            ax.legend()
        else:
            # Simple line plot
            ax.plot(subset[time_var.name], subset[value_var.name], marker="o", linewidth=2)

        ax.set_xlabel(time_var.label)
        ax.set_ylabel(value_var.label)
        ax.set_title(f"{value_var.label} over {time_var.label}")
        ax.grid(True, alpha=0.3)

        if output_path:
            fig.savefig(output_path, bbox_inches="tight", dpi=self.dpi)

        return fig

    def _clean_data(self, data: pd.Series, variable: Variable) -> pd.Series:
        """Clean missing values from series."""
        clean = data.copy()
        if variable.missing_values:
            clean = clean.replace(dict.fromkeys(variable.missing_values, np.nan))
        return clean.dropna()

    def _clean_dataframe(self, data: pd.DataFrame, variables: list[Variable]) -> pd.DataFrame:
        """Clean missing values from dataframe."""
        clean = data.copy()
        for var in variables:
            if var.missing_values:
                clean[var.name] = clean[var.name].replace(dict.fromkeys(var.missing_values, np.nan))
        return clean

    def _plot_numeric_distribution(self, data: pd.Series, variable: Variable, ax: plt.Axes) -> None:
        """Plot histogram/KDE for numeric variable."""
        n_unique = data.nunique()

        if n_unique > 50:
            # Use KDE for continuous data
            sns.histplot(data, kde=True, ax=ax, stat="density")
            ax.set_ylabel("Density")
        else:
            # Use count histogram for discrete data
            sns.histplot(data, kde=False, ax=ax, bins=min(n_unique, 30))
            ax.set_ylabel("Count")

        ax.set_xlabel(variable.label)

        # Add mean line
        mean = data.mean()
        ax.axvline(mean, color="red", linestyle="--", label=f"Mean: {mean:.2f}", alpha=0.7)
        ax.legend()

    def _plot_categorical_distribution(
        self, data: pd.Series, variable: Variable, ax: plt.Axes
    ) -> None:
        """Plot bar chart for categorical variable."""
        counts = data.value_counts()

        # Map to labels if available
        if variable.valid_values:
            counts.index = counts.index.map(lambda x: variable.valid_values.get(x, str(x)))

        sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="viridis")
        ax.set_xlabel(variable.label)
        ax.set_ylabel("Count")

        # Rotate labels if many categories
        if len(counts) > 5:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    def _plot_scatter(
        self, data: pd.DataFrame, var1: Variable, var2: Variable, ax: plt.Axes
    ) -> None:
        """Plot scatter plot with regression line."""
        sns.regplot(
            x=var1.name,
            y=var2.name,
            data=data,
            ax=ax,
            scatter_kws={"alpha": 0.5},
            line_kws={"color": "red"},
        )
        ax.set_xlabel(var1.label)
        ax.set_ylabel(var2.label)
        ax.set_title(f"{var1.label} vs {var2.label}")

    def _plot_boxplot(
        self, data: pd.DataFrame, var_cat: Variable, var_num: Variable, ax: plt.Axes
    ) -> None:
        """Plot box plot for categorical vs numeric."""
        # Map categories to labels
        plot_data = data.copy()
        if var_cat.valid_values:
            plot_data[var_cat.name] = plot_data[var_cat.name].map(
                lambda x: var_cat.valid_values.get(x, str(x))
            )

        sns.boxplot(x=var_cat.name, y=var_num.name, data=plot_data, ax=ax, palette="Set2")
        ax.set_xlabel(var_cat.label)
        ax.set_ylabel(var_num.label)
        ax.set_title(f"{var_num.label} by {var_cat.label}")

        if len(plot_data[var_cat.name].unique()) > 5:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    def _plot_heatmap(
        self, data: pd.DataFrame, var1: Variable, var2: Variable, ax: plt.Axes
    ) -> None:
        """Plot heatmap for categorical vs categorical."""
        # Create contingency table
        contingency = pd.crosstab(data[var1.name], data[var2.name])

        # Map to labels
        if var1.valid_values:
            contingency.index = contingency.index.map(lambda x: var1.valid_values.get(x, str(x)))
        if var2.valid_values:
            contingency.columns = contingency.columns.map(
                lambda x: var2.valid_values.get(x, str(x))
            )

        sns.heatmap(contingency, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
        ax.set_xlabel(var2.label)
        ax.set_ylabel(var1.label)
        ax.set_title(f"{var1.label} vs {var2.label}")

    def close_all(self) -> None:
        """Close all open figures."""
        plt.close("all")

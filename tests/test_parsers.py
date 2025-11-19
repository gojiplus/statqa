"""Tests for codebook parsers."""

from statqa.metadata.parsers.text import TextParser


def test_text_parser():
    """Test text codebook parser."""
    text_codebook = """
# Codebook: Test

# Variable: age
Label: Age in years
Type: numeric_continuous
Units: years
Range: 18-99
Missing: -1, 999

# Variable: gender
Label: Gender
Type: categorical_nominal
Values:
  1: Male
  2: Female
Missing: 0
"""

    parser = TextParser()
    assert parser.validate(text_codebook)

    codebook = parser.parse(text_codebook)
    assert len(codebook.variables) == 2
    assert "age" in codebook.variables
    assert "gender" in codebook.variables

    age_var = codebook.variables["age"]
    assert age_var.units == "years"
    assert age_var.range_min == 18
    assert age_var.range_max == 99
    assert -1 in age_var.missing_values

    gender_var = codebook.variables["gender"]
    assert 1 in gender_var.valid_values
    assert gender_var.valid_values[1] == "Male"

# ANES Data Directory

This directory contains the ANES Time Series Cumulative Data File and associated metadata.

## Directory Structure

```
data/
├── README.md                    # This file
├── anes_metadata.csv           # Parsed variable metadata (generated)
└── raw/                        # Raw ANES files (download required)
    ├── anes_timeseries_cdf_codebook_app_20220916.pdf
    ├── anes_timeseries_cdf_codebook_var_20220916.pdf
    └── anes_timeseries_cdf_csv_20220916.csv.zip
```

## Files

### anes_metadata.csv
**Generated file** - Created by running `01_parse_metadata.py`

Contains parsed metadata for all ANES variables:
- `varname`: Variable code (e.g., VCF0001)
- `label`: Variable description/question text
- `valid_values`: Valid value ranges and codes
- `missing_values`: Missing data codes
- `notes`: Additional descriptive information

### raw/anes_timeseries_cdf_csv_20220916.csv.zip
**Main data file** - Contains the complete ANES dataset (1948-2020)

- Format: ZIP archive containing CSV file
- Size: ~18 MB (zipped), ~300+ MB (unzipped)
- Rows: 70,000+ survey responses
- Columns: 1,000+ variables

### raw/anes_timeseries_cdf_codebook_var_20220916.pdf
**Variable codebook** - Detailed documentation for each variable

- Format: PDF
- Size: ~4.4 MB
- Content: Variable descriptions, value coding, question wording

### raw/anes_timeseries_cdf_codebook_app_20220916.pdf
**Appendix codebook** - Supplementary documentation

- Format: PDF
- Size: ~1.1 MB
- Content: Study design, sampling, weighting, methodological notes

## Downloading the Data

The ANES data files are **not included in this repository** due to their size and licensing terms.

### Option 1: Download from ANES Website (Recommended)

1. Visit the ANES Data Center:
   https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/

2. Register for an account (free)

3. Download the following files:
   - **ANES Time Series Cumulative Data File (CSV)** → save as `raw/anes_timeseries_cdf_csv_20220916.csv.zip`
   - **Variable Codebook (PDF)** → save as `raw/anes_timeseries_cdf_codebook_var_20220916.pdf`
   - **Appendix Codebook (PDF)** → save as `raw/anes_timeseries_cdf_codebook_app_20220916.pdf`

4. Place files in the `raw/` directory

### Option 2: Download via Command Line

```bash
cd raw/

# Note: Direct download links require authentication
# Manual download from the website is recommended

# After downloading manually, verify files
ls -lh
```

### Verification

After downloading, verify the files:

```bash
cd raw/

# Check file sizes (approximate)
du -h *
# Expected output:
# 1.1M    anes_timeseries_cdf_codebook_app_20220916.pdf
# 4.4M    anes_timeseries_cdf_codebook_var_20220916.pdf
#  18M    anes_timeseries_cdf_csv_20220916.csv.zip

# Verify ZIP archive
unzip -t anes_timeseries_cdf_csv_20220916.csv.zip
# Should show: "No errors detected"
```

## Data Usage Terms

The ANES data is provided for research and educational purposes. Please:

1. **Cite the data**: Include proper citation in publications (see main README.md)
2. **Register usage**: Complete the ANES registration to track data usage
3. **Do not redistribute**: Do not share the data files directly; instead, refer users to the ANES website
4. **Review terms**: See the full terms at https://electionstudies.org/data-center/

## File Formats

### CSV Data Format

The main data file is a standard CSV with:
- **Header row**: Variable names (e.g., VCF0001, VCF0002, ...)
- **Data rows**: One row per survey respondent
- **Encoding**: UTF-8
- **Separator**: Comma (,)
- **Missing values**: Coded as specific integers (varies by variable)

Example:
```csv
VCF0001,VCF0004,VCF0006,VCF0102,VCF0104,...
1,1948,1,42,1,...
2,1948,2,35,2,...
```

### Metadata CSV Format

The parsed metadata file has the following structure:

```csv
varname,label,valid_values,missing_values,notes
VCF0001,Case ID,,,Unique identifier for each respondent
VCF0004,Year of study,Valid: 1948-2020,Missing: 0,Study year
VCF0102,Age of respondent,Valid: 18-99,Missing: 0 99,Age in years at time of interview
```

## Common Issues

### File Not Found Errors

**Problem**: `FileNotFoundError: No CSV matched pattern`
**Solution**: Ensure the ZIP file is in the `raw/` directory with the exact filename

### Large File Warnings

**Problem**: Dataset is too large to load into memory
**Solution**: The scripts use `low_memory=False` and process in chunks where possible

### Encoding Issues

**Problem**: Special characters display incorrectly
**Solution**: The data uses UTF-8 encoding; ensure your system supports it

## Alternative Datasets

If you want to test the pipeline with a smaller dataset:

1. **Subset the data**: Extract a subset of variables or years
2. **Use synthetic data**: See `../simple_survey/` example
3. **Use other surveys**: General Social Survey (GSS), Pew Research, etc.

## Support

For data-related questions:
- **ANES support**: https://electionstudies.org/contact/
- **tableqa issues**: https://github.com/gojiplus/tableqa/issues

## File Checksums

To verify file integrity, compare checksums (update these after downloading):

```bash
# Generate checksums
md5sum raw/* > checksums.md5

# Verify later
md5sum -c checksums.md5
```

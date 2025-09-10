# Spreadsheet Consolidator

A powerful tool to consolidate multiple spreadsheets with different header structures into a unified master sheet with standardized headers.

## Features

- **Multi-format Support**: Upload CSV, Excel (.xlsx, .xls) files
- **Smart Header Mapping**: Automatically maps similar headers using fuzzy matching
- **Data Consolidation**: Merges all data into a single master sheet
- **Interactive Filtering**: Filter data by any column with multiple criteria
- **Flexible Sorting**: Sort by any column in ascending or descending order
- **Export Options**: Download consolidated data as Excel or CSV
- **Analytics Dashboard**: View data quality metrics and distribution charts
- **Source Tracking**: Keeps track of which file and sheet each row came from

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:

```bash
streamlit run app.py
```

2. Open your browser and navigate to the displayed URL (typically `http://localhost:8501`)

3. Follow these steps in the web interface:

### Step 1: Upload & Process
- Upload your spreadsheet files (supports multiple files at once)
- Click "Process Files" to analyze the data structure
- Review the processing summary

### Step 2: Header Mapping
- Review the automatically suggested header mappings
- Adjust mappings as needed using the dropdown menus
- Apply the mapping configuration

### Step 3: Master Sheet
- Click "Consolidate Data" to merge all data
- Use filters to narrow down your data view
- Sort by any column
- Export your consolidated data

### Step 4: Analytics
- View data quality metrics
- See source distribution charts
- Analyze individual column statistics

## File Structure

```
spreadsheet-consolidator/
├── app.py                    # Main Streamlit application
├── data_consolidator.py      # Core data consolidation logic
├── header_mapper.py          # Header standardization engine
├── spreadsheet_processor.py  # File processing utilities
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Key Components

### HeaderMapper
- Uses fuzzy string matching to identify similar headers
- Maintains a dictionary of common header variations
- Supports custom mappings for domain-specific headers

### SpreadsheetProcessor
- Handles multiple file formats (CSV, Excel)
- Extracts data from multiple sheets within Excel files
- Preserves source information for traceability

### DataConsolidator
- Orchestrates the entire consolidation process
- Applies header mappings across all datasets
- Provides filtering, sorting, and export functionality

## Supported Header Standards

The tool recognizes common variations of these standard headers:

- **name**: name, full_name, customer_name, client_name, etc.
- **email**: email, email_address, e_mail, contact_email, etc.
- **phone**: phone, phone_number, telephone, mobile, cell, etc.
- **address**: address, street_address, location, full_address, etc.
- **date**: date, created_date, modified_date, timestamp, etc.
- **amount**: amount, price, cost, value, total, sum, etc.
- **id**: id, identifier, unique_id, record_id, customer_id, etc.

And many more categories...

## Customization

You can extend the header mapping by:

1. Modifying the `standard_headers` dictionary in `header_mapper.py`
2. Adding custom mappings through the web interface
3. Extending the fuzzy matching logic for domain-specific terms

## Export Formats

- **Excel (.xlsx)**: Full-featured spreadsheet with formatting
- **CSV**: Comma-separated values for maximum compatibility

## Tips for Best Results

1. **Consistent Data Types**: Ensure similar columns across files contain similar data types
2. **Header Clarity**: Use descriptive column headers in your source files
3. **Data Validation**: Review the header mappings before consolidation
4. **Large Datasets**: For very large datasets, use filtering to focus on specific data subsets

## Troubleshooting

- **Memory Issues**: For very large files, consider processing in smaller batches
- **Encoding Errors**: Ensure your CSV files use UTF-8 encoding
- **Date Formats**: Dates may need manual review if formats vary significantly across files

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- OpenPyXL
- FuzzyWuzzy
- Plotly

## License

This project is open source and available under the MIT License.
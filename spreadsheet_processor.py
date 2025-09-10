import pandas as pd
import os
from typing import Dict, List, Tuple, Any
import logging
from pathlib import Path

class SpreadsheetProcessor:
    def __init__(self):
        self.supported_formats = {'.xlsx', '.xls', '.csv'}
        self.processed_sheets = {}
        self.master_data = pd.DataFrame()
        
    def read_file(self, file_path: str) -> List[pd.DataFrame]:
        """Read a spreadsheet file and return list of DataFrames (one per sheet)"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
            
        try:
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
                return [df]
            elif file_ext in ['.xlsx', '.xls']:
                excel_file = pd.ExcelFile(file_path)
                sheets = []
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name)
                    df.attrs['sheet_name'] = sheet_name
                    df.attrs['file_name'] = Path(file_path).name
                    sheets.append(df)
                return sheets
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {str(e)}")
            raise
            
    def process_uploaded_files(self, uploaded_files: List[Any]) -> Dict[str, List[pd.DataFrame]]:
        """Process multiple uploaded files and return organized data"""
        processed_data = {}
        
        for uploaded_file in uploaded_files:
            try:
                file_name = uploaded_file.name
                file_ext = Path(file_name).suffix.lower()
                
                if file_ext == '.csv':
                    df = pd.read_csv(uploaded_file)
                    df.attrs['sheet_name'] = 'Sheet1'
                    df.attrs['file_name'] = file_name
                    processed_data[file_name] = [df]
                    
                elif file_ext in ['.xlsx', '.xls']:
                    excel_file = pd.ExcelFile(uploaded_file)
                    sheets = []
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                        df.attrs['sheet_name'] = sheet_name
                        df.attrs['file_name'] = file_name
                        sheets.append(df)
                    processed_data[file_name] = sheets
                    
            except Exception as e:
                logging.error(f"Error processing file {uploaded_file.name}: {str(e)}")
                continue
                
        return processed_data
        
    def get_all_headers(self, processed_data: Dict[str, List[pd.DataFrame]]) -> List[str]:
        """Extract all unique headers from processed data"""
        all_headers = set()
        
        for file_name, sheets in processed_data.items():
            for sheet in sheets:
                all_headers.update(sheet.columns.tolist())
                
        return sorted(list(all_headers))
        
    def apply_header_mapping(self, df: pd.DataFrame, header_mapping: Dict[str, str]) -> pd.DataFrame:
        """Apply header mapping to a DataFrame"""
        df_copy = df.copy()
        
        # Rename columns based on mapping
        df_copy = df_copy.rename(columns=header_mapping)
        
        return df_copy
        
    def consolidate_data(self, processed_data: Dict[str, List[pd.DataFrame]], 
                        header_mapping: Dict[str, str]) -> pd.DataFrame:
        """Consolidate all data into a single master DataFrame"""
        consolidated_frames = []
        
        for file_name, sheets in processed_data.items():
            for sheet in sheets:
                try:
                    # Make a copy to avoid modifying original data
                    sheet_copy = sheet.copy()
                    
                    # Reset index to avoid duplicate index issues
                    sheet_copy.reset_index(drop=True, inplace=True)
                    
                    # Handle duplicate column names by making them unique
                    if sheet_copy.columns.duplicated().any():
                        # Create unique column names
                        new_columns = []
                        col_counts = {}
                        for col in sheet_copy.columns:
                            if col in col_counts:
                                col_counts[col] += 1
                                new_columns.append(f"{col}_{col_counts[col]}")
                            else:
                                col_counts[col] = 0
                                new_columns.append(col)
                        sheet_copy.columns = new_columns
                    
                    # Apply header mapping
                    mapped_sheet = self.apply_header_mapping(sheet_copy, header_mapping)
                    
                    # Add metadata columns
                    mapped_sheet['source_file'] = sheet.attrs.get('file_name', file_name)
                    mapped_sheet['source_sheet'] = sheet.attrs.get('sheet_name', 'Sheet1')
                    
                    consolidated_frames.append(mapped_sheet)
                    
                except Exception as e:
                    # Log the error but continue with other sheets
                    logging.error(f"Error processing sheet {sheet.attrs.get('sheet_name', 'unknown')} from {file_name}: {str(e)}")
                    continue
                
        if consolidated_frames:
            try:
                # Ensure all frames have unique indices
                for i, frame in enumerate(consolidated_frames):
                    frame.reset_index(drop=True, inplace=True)
                
                # Import header mapper to get required headers
                from header_mapper import HeaderMapper
                header_mapper = HeaderMapper()
                required_headers = header_mapper.get_required_headers()
                
                # Add metadata columns to required headers
                final_headers = required_headers + ['source_file', 'source_sheet']
                
                # Reindex all frames to have exactly the required headers
                aligned_frames = []
                for frame in consolidated_frames:
                    # Ensure frame has unique column names before reindexing
                    if frame.columns.duplicated().any():
                        # Fix duplicates in this frame too
                        new_columns = []
                        col_counts = {}
                        for col in frame.columns:
                            if col in col_counts:
                                col_counts[col] += 1
                                new_columns.append(f"{col}_{col_counts[col]}")
                            else:
                                col_counts[col] = 0
                                new_columns.append(col)
                        frame.columns = new_columns
                    
                    # Reindex to only include required headers
                    aligned_frame = frame.reindex(columns=final_headers, fill_value='')
                    aligned_frames.append(aligned_frame)
                
                # Concatenate all frames
                master_df = pd.concat(aligned_frames, ignore_index=True, sort=False)
                
                # Fill NaN values with empty strings for better display
                master_df = master_df.fillna('')
                
                return master_df
                
            except Exception as e:
                logging.error(f"Error during concatenation: {str(e)}")
                # Fallback: create empty DataFrame with error info
                return pd.DataFrame({'error': [f"Consolidation failed: {str(e)}"]})
        else:
            return pd.DataFrame()
            
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics for the consolidated data"""
        if df.empty:
            return {}
            
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'source_files': df['source_file'].nunique() if 'source_file' in df.columns else 0,
            'source_sheets': df['source_sheet'].nunique() if 'source_sheet' in df.columns else 0,
            'column_info': {}
        }
        
        for col in df.columns:
            if col not in ['source_file', 'source_sheet']:
                try:
                    # Ensure we're working with a Series, not DataFrame
                    col_series = df[col] if isinstance(df[col], pd.Series) else df[col].iloc[:, 0]
                    non_empty = col_series.astype(str).str.strip().ne('').sum()
                    summary['column_info'][col] = {
                        'non_empty_values': non_empty,
                        'empty_values': len(df) - non_empty,
                        'data_type': str(col_series.dtype)
                    }
                except Exception as e:
                    # Fallback for problematic columns
                    summary['column_info'][col] = {
                        'non_empty_values': 0,
                        'empty_values': len(df),
                        'data_type': 'unknown',
                        'error': str(e)
                    }
                
        return summary
import pandas as pd
from typing import Dict, List, Any, Optional
from header_mapper import HeaderMapper
from spreadsheet_processor import SpreadsheetProcessor
import streamlit as st

class DataConsolidator:
    def __init__(self):
        self.header_mapper = HeaderMapper()
        self.processor = SpreadsheetProcessor()
        self.master_data = pd.DataFrame()
        self.processed_data = {}
        self.current_mapping = {}
        
    def process_files(self, uploaded_files: List[Any]) -> Dict[str, Any]:
        """Process uploaded files and return processing results"""
        try:
            # Process all uploaded files
            self.processed_data = self.processor.process_uploaded_files(uploaded_files)
            
            # Get all unique headers
            all_headers = self.processor.get_all_headers(self.processed_data)
            
            # Generate automatic mappings
            auto_mappings = self.header_mapper.map_headers(all_headers)
            
            # Get mapping suggestions for user review
            mapping_suggestions = self.header_mapper.get_mapping_suggestions(all_headers)
            
            return {
                'success': True,
                'headers': all_headers,
                'auto_mappings': auto_mappings,
                'mapping_suggestions': mapping_suggestions,
                'file_count': len(self.processed_data),
                'total_sheets': sum(len(sheets) for sheets in self.processed_data.values())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def update_header_mapping(self, header_mapping: Dict[str, str]):
        """Update the header mapping configuration"""
        self.current_mapping = header_mapping
        
        # Add custom mappings to the header mapper
        for original, standard in header_mapping.items():
            if standard != original:
                self.header_mapper.add_custom_mapping(original, standard)
                
    def consolidate_data(self) -> Dict[str, Any]:
        """Consolidate all processed data using current header mapping"""
        try:
            if not self.processed_data or not self.current_mapping:
                return {
                    'success': False,
                    'error': 'No data processed or mapping configured'
                }
                
            # Consolidate data
            self.master_data = self.processor.consolidate_data(
                self.processed_data, 
                self.current_mapping
            )
            
            # Get summary statistics
            summary = self.processor.get_data_summary(self.master_data)
            
            return {
                'success': True,
                'data': self.master_data,
                'summary': summary
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def filter_data(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the master data"""
        if self.master_data.empty:
            return pd.DataFrame()
            
        filtered_data = self.master_data.copy()
        
        for column, filter_value in filters.items():
            if filter_value and column in filtered_data.columns:
                if isinstance(filter_value, str):
                    # Text filter - case insensitive contains
                    try:
                        col_series = filtered_data[column]
                        if isinstance(col_series, pd.DataFrame):
                            col_series = col_series.iloc[:, 0]
                        filtered_data = filtered_data[
                            col_series.astype(str).str.contains(
                                filter_value, case=False, na=False
                            )
                        ]
                    except Exception:
                        # Skip filter if it fails
                        continue
                elif isinstance(filter_value, list):
                    # Multi-select filter
                    filtered_data = filtered_data[
                        filtered_data[column].isin(filter_value)
                    ]
                    
        return filtered_data
        
    def sort_data(self, data: pd.DataFrame, sort_column: str, 
                  ascending: bool = True) -> pd.DataFrame:
        """Sort data by specified column"""
        if data.empty or sort_column not in data.columns:
            return data
            
        try:
            # Try to sort numerically first
            numeric_data = pd.to_numeric(data[sort_column], errors='coerce')
            if not numeric_data.isna().all():
                return data.sort_values(sort_column, ascending=ascending, 
                                      key=lambda x: pd.to_numeric(x, errors='coerce'))
            else:
                # Sort as strings
                return data.sort_values(sort_column, ascending=ascending)
        except:
            return data.sort_values(sort_column, ascending=ascending)
            
    def export_data(self, data: pd.DataFrame, format: str = 'xlsx') -> bytes:
        """Export data in specified format"""
        if format == 'xlsx':
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                data.to_excel(writer, index=False, sheet_name='Master_Sheet')
            return output.getvalue()
        elif format == 'csv':
            return data.to_csv(index=False).encode('utf-8')
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
    def get_column_stats(self, column: str) -> Dict[str, Any]:
        """Get statistics for a specific column"""
        if self.master_data.empty or column not in self.master_data.columns:
            return {}
            
        col_data = self.master_data[column]
        
        try:
            # Ensure we're working with a Series
            if isinstance(col_data, pd.DataFrame):
                col_data = col_data.iloc[:, 0]
            
            stats = {
                'total_values': len(col_data),
                'non_empty_values': col_data.astype(str).str.strip().ne('').sum(),
                'unique_values': col_data.nunique(),
                'most_common': col_data.value_counts().head(5).to_dict()
            }
        except Exception as e:
            stats = {
                'total_values': len(col_data) if hasattr(col_data, '__len__') else 0,
                'non_empty_values': 0,
                'unique_values': 0,
                'most_common': {},
                'error': str(e)
            }
        
        # Try to get numeric stats
        try:
            numeric_data = pd.to_numeric(col_data, errors='coerce')
            if not numeric_data.isna().all():
                stats['numeric_stats'] = {
                    'mean': numeric_data.mean(),
                    'median': numeric_data.median(),
                    'min': numeric_data.min(),
                    'max': numeric_data.max(),
                    'std': numeric_data.std()
                }
        except:
            pass
            
        return stats
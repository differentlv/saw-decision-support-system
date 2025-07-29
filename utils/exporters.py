import pandas as pd
from datetime import datetime
from typing import List, Tuple
from config.settings import AppConfig
from utils.validators import DataValidator


class ResultExporter:
    """Export calculation results"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def export_to_csv(self, results: List[Tuple[str, float]], 
                     custom_filename: str = None) -> str:
        """Export results to CSV file"""
        if not results:
            raise ValueError("No results to export")
        
        # Create DataFrame
        df = pd.DataFrame(results, columns=['Alternatif', 'Skor SAW'])
        df['Peringkat'] = range(1, len(df) + 1)
        df = df[['Peringkat', 'Alternatif', 'Skor SAW']]
        
        # Generate filename
        if custom_filename:
            filename = self.validator.sanitize_filename(custom_filename)
            if not filename.endswith('.csv'):
                filename += '.csv'
        else:
            timestamp = datetime.now().strftime(AppConfig.EXPORT_DATE_FORMAT)
            filename = f"{AppConfig.EXPORT_FILENAME_PREFIX}{timestamp}.csv"
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        return filename
    
    def export_to_excel(self, results: List[Tuple[str, float]], 
                       calculation_steps: dict = None,
                       custom_filename: str = None) -> str:
        """Export results to Excel file with multiple sheets"""
        if not results:
            raise ValueError("No results to export")
        
        # Generate filename
        if custom_filename:
            filename = self.validator.sanitize_filename(custom_filename)
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
        else:
            timestamp = datetime.now().strftime(AppConfig.EXPORT_DATE_FORMAT)
            filename = f"{AppConfig.EXPORT_FILENAME_PREFIX}{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Results sheet
            df_results = pd.DataFrame(results, columns=['Alternatif', 'Skor SAW'])
            df_results['Peringkat'] = range(1, len(df_results) + 1)
            df_results = df_results[['Peringkat', 'Alternatif', 'Skor SAW']]
            df_results.to_excel(writer, sheet_name='Hasil', index=False)
            
            # Calculation steps if provided
            if calculation_steps:
                # Original matrix
                df_original = pd.DataFrame(
                    calculation_steps['original_matrix'],
                    columns=calculation_steps['criteria'],
                    index=calculation_steps['alternatives']
                )
                df_original.to_excel(writer, sheet_name='Matriks Asli')
                
                # Normalized matrix
                df_normalized = pd.DataFrame(
                    calculation_steps['normalized_matrix'],
                    columns=calculation_steps['criteria'],
                    index=calculation_steps['alternatives']
                )
                df_normalized.to_excel(writer, sheet_name='Matriks Ternormalisasi')
                
                # Criteria info
                df_criteria = pd.DataFrame({
                    'Kriteria': calculation_steps['criteria'],
                    'Bobot': calculation_steps['weights'],
                    'Tipe': calculation_steps['criteria_types']
                })
                df_criteria.to_excel(writer, sheet_name='Kriteria', index=False)
        
        return filename


class SensitivityExporter:
    """Export sensitivity analysis results"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def export_sensitivity_to_csv(self, sensitivity_results: List[dict], 
                                 criteria_name: str,
                                 stability_info: dict,
                                 custom_filename: str = None) -> str:
        """Export sensitivity analysis to CSV"""
        if not sensitivity_results:
            raise ValueError("No sensitivity results to export")
        
        # Create DataFrame
        data = []
        for result in sensitivity_results:
            data.append({
                'Perubahan_Bobot': result['change'],
                'Bobot_Baru': result['new_weight'],
                'Alternatif_Terbaik': result['winner'],
                'Skor_Terbaik': result['score']
            })
        
        df = pd.DataFrame(data)
        
        # Add stability info as header comments
        header_info = [
            f"# Analisis Sensitivitas - Kriteria: {criteria_name}",
            f"# Stabilitas: {stability_info['stability']:.1f}% ({stability_info['level']})",
            f"# Alternatif Terbaik Asli: {stability_info['original_winner']}"
        ]
        
        # Generate filename
        if custom_filename:
            filename = self.validator.sanitize_filename(custom_filename)
            if not filename.endswith('.csv'):
                filename += '.csv'
        else:
            timestamp = datetime.now().strftime(AppConfig.EXPORT_DATE_FORMAT)
            criteria_safe = self.validator.sanitize_filename(criteria_name)
            filename = f"sensitivitas_{criteria_safe}_{timestamp}.csv"
        
        # Write file with headers
        with open(filename, 'w', encoding='utf-8') as f:
            for header in header_info:
                f.write(header + '\n')
            f.write('\n')
        
        # Append DataFrame
        df.to_csv(filename, mode='a', index=False, encoding='utf-8')
        return filename
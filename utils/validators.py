from typing import List, Tuple, Optional
import re


class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_alternative_name(name: str) -> Tuple[bool, str]:
        """Validate alternative name"""
        if not name or not name.strip():
            return False, "Nama alternatif tidak boleh kosong"
        
        if len(name.strip()) < 2:
            return False, "Nama alternatif minimal 2 karakter"
        
        if len(name.strip()) > 50:
            return False, "Nama alternatif maksimal 50 karakter"
        
        return True, ""
    
    @staticmethod
    def validate_criteria_name(name: str) -> Tuple[bool, str]:
        """Validate criteria name"""
        if not name or not name.strip():
            return False, "Nama kriteria tidak boleh kosong"
        
        if len(name.strip()) < 2:
            return False, "Nama kriteria minimal 2 karakter"
        
        if len(name.strip()) > 30:
            return False, "Nama kriteria maksimal 30 karakter"
        
        return True, ""
    
    @staticmethod
    def validate_weight(weight_str: str) -> Tuple[bool, float, str]:
        """Validate weight value"""
        try:
            weight = float(weight_str)
            if weight <= 0:
                return False, 0, "Bobot harus lebih besar dari 0"
            if weight > 1:
                return False, 0, "Bobot tidak boleh lebih dari 1"
            return True, weight, ""
        except ValueError:
            return False, 0, "Bobot harus berupa angka"
    
    @staticmethod
    def validate_matrix_value(value_str: str) -> Tuple[bool, float, str]:
        """Validate matrix value"""
        try:
            value = float(value_str)
            if value < 0:
                return False, 0, "Nilai tidak boleh negatif"
            return True, value, ""
        except ValueError:
            return False, 0, "Nilai harus berupa angka"
    
    @staticmethod
    def validate_criteria_type(criteria_type: str) -> Tuple[bool, str]:
        """Validate criteria type"""
        valid_types = ['benefit', 'cost']
        if criteria_type not in valid_types:
            return False, f"Tipe kriteria harus salah satu dari: {', '.join(valid_types)}"
        return True, ""
    
    @staticmethod
    def validate_sensitivity_range(range_str: str) -> Tuple[bool, float, str]:
        """Validate sensitivity analysis range"""
        try:
            range_val = float(range_str)
            if range_val <= 0:
                return False, 0, "Range harus lebih besar dari 0"
            if range_val > 1:
                return False, 0, "Range tidak boleh lebih dari 1"
            return True, range_val, ""
        except ValueError:
            return False, 0, "Range harus berupa angka"
    
    @staticmethod
    def check_duplicate_names(names: List[str], new_name: str) -> bool:
        """Check if name already exists in list"""
        return new_name.strip() in [name.strip() for name in names]
    
    @staticmethod
    def validate_complete_data(alternatives: List[str], criteria: List[str], 
                             weights: List[float], decision_matrix: List[List[float]]) -> Tuple[bool, str]:
        """Validate complete dataset for SAW calculation"""
        if not alternatives:
            return False, "Tidak ada alternatif yang didefinisikan"
        
        if not criteria:
            return False, "Tidak ada kriteria yang didefinisikan"
        
        if len(weights) != len(criteria):
            return False, "Jumlah bobot tidak sesuai dengan jumlah kriteria"
        
        if not decision_matrix:
            return False, "Matriks keputusan kosong"
        
        if len(decision_matrix) != len(alternatives):
            return False, "Jumlah baris matriks tidak sesuai dengan jumlah alternatif"
        
        for i, row in enumerate(decision_matrix):
            if len(row) != len(criteria):
                return False, f"Baris {i+1} matriks tidak sesuai dengan jumlah kriteria"
        
        # Check for empty values
        for i, row in enumerate(decision_matrix):
            for j, value in enumerate(row):
                if value is None or (isinstance(value, str) and not value.strip()):
                    return False, f"Nilai pada baris {i+1}, kolom {j+1} kosong"
        
        return True, ""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for export"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Remove multiple underscores
        filename = re.sub(r'_+', '_', filename)
        return filename.strip('_')
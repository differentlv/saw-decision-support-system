import tkinter as tk
from tkinter import ttk
from models.saw_model import SAWModel
from views.input_tab import InputTabView
from views.calculation_tab import CalculationTabView
from views.results_tab import ResultsTabView
from views.sensitivity_tab import SensitivityTabView
from views.group_tab import GroupTabView
from utils.validators import DataValidator
from config.settings import AppConfig


class SPKSAWController:
    """Main application controller"""
    
    def __init__(self, root):
        self.root = root
        self.model = SAWModel()
        self.validator = DataValidator()
        
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Initialize views
        self._create_views()
        
        # Create title
        title_label = ttk.Label(self.root, 
        text=AppConfig.WINDOW_TITLE, 
        style='Title.TLabel')
        title_label.pack(pady=10, before=self.notebook)
    
    def _create_views(self):
        """Create all tab views"""
        self.input_view = InputTabView(self.notebook, self)
        self.calculation_view = CalculationTabView(self.notebook, self)
        self.results_view = ResultsTabView(self.notebook, self)
        self.sensitivity_view = SensitivityTabView(self.notebook, self)
        self.group_view = GroupTabView(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.input_view.frame, text="Input Data")
        self.notebook.add(self.calculation_view.frame, text="Perhitungan")
        self.notebook.add(self.results_view.frame, text="Hasil & Visualisasi")
        self.notebook.add(self.sensitivity_view.frame, text="Analisis Sensitivitas")
        self.notebook.add(self.group_view.frame, text="Pembuat")
    
    def get_model(self):
        """Get the SAW model"""
        return self.model
    
    def get_validator(self):
        """Get the data validator"""
        return self.validator
    
    def update_sensitivity_criteria(self):
        """Update criteria options in sensitivity tab"""
        self.sensitivity_view.update_criteria_options(self.model.criteria)
    
    def refresh_all_views(self):
        """Refresh all views after data changes"""
        self.calculation_view.clear_results()
        self.results_view.clear_results()
        self.sensitivity_view.clear_results()
        self.update_sensitivity_criteria()